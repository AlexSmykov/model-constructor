import os
import random
import shutil

import cv2
import tensorflow as tf

from scripts.enums.layers_enum import ELayers


def image_process(path, names, shape):
    for name in names:
        image = cv2.imread(f'dataset_all/{path}/{name}')
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_resized = cv2.resize(image_gray, shape)
        cv2.imwrite(f'dataset/{path}/{name}', image_resized)


def prepare_dataset(image_count, shape):
    try:
        shutil.rmtree('../dataset')
    except:
        pass

    try:
        os.mkdir('dataset')
        os.mkdir('dataset/train')
        os.mkdir('dataset/test')
        os.mkdir('dataset/train/cat')
        os.mkdir('dataset/train/not_cat')
        os.mkdir('dataset/test/cat')
        os.mkdir('dataset/test/not_cat')
    except:
        pass

    train_cats_images_names = random.sample(os.listdir('dataset_all/train/cat'), k=image_count)
    train_not_cats_images_names = random.sample(os.listdir('dataset_all/train/not_cat'), k=image_count)

    test_cats_images_names = os.listdir('dataset_all/test/cat')
    test_not_cats_images_names = os.listdir('dataset_all/test/not_cat')

    test_cats_images_names = random.sample(test_cats_images_names, k=min(image_count, len(test_cats_images_names)))
    test_not_cats_images_names = random.sample(test_not_cats_images_names,
                                               k=min(image_count, len(test_not_cats_images_names)))

    print('Preprocess images for train...')
    image_process('train/cat', train_cats_images_names, shape)
    image_process('train/not_cat', train_not_cats_images_names, shape)
    print('Train done!')

    print('Preprocess images for test...')
    image_process('test/cat', test_cats_images_names, shape)
    image_process('test/not_cat', test_not_cats_images_names, shape)
    print('Test done!')


def fit(model, optimizer, epochs, layers: dict[dict[float]], dataset_size, images_shape):
    if model is None:
        flatten_detected = False
        for layer_name, layer_parameters in layers.items():
            if layer_name == ELayers['FLATTEN']['text']:
                flatten_detected = True

            if layer_name == ELayers['DENSE']['text'] and not flatten_detected:
                print("No flatten layer before dense")
                return ()

            if layer_name == ELayers['CONVOLUTION']['text'] and flatten_detected:
                print("Convolution layer after flatten")
                return ()

            if layer_name == ELayers['MAX_POOLING']['text'] and flatten_detected:
                print("Max pooling layer after flatten")
                return ()

        if not flatten_detected:
            print("No flatten layer")
            return ()

        image_size = images_shape[0]
        for layer_name, layer_parameters in layers.items():
            if layer_name == ELayers['CONVOLUTION']['text']:
                image_size -= (layer_parameters['kernel_size'] - 1)

                if image_size <= 0:
                    print("Convolution size greater than calculated image size")

                    return ()

            if layer_name == ELayers['MAX_POOLING']['text']:
                image_size /= layer_parameters['pool_size']

                if image_size <= 1:
                    print("Max pooling size greater than calculated image size")

                    return ()

            if layer_name == ELayers['UP_SAMPLING']['text']:
                image_size *= layer_parameters['pool_size']

        prepare_dataset(dataset_size, images_shape)

        converted_layers = []
        converted_layers.append(
            tf.keras.layers.Rescaling(scale=1. / 255.))
        for layer_name, layer_parameters in layers.items():
            if layer_name == ELayers['DENSE']['text']:
                converted_layers.append(
                    tf.keras.layers.Dense(units=layer_parameters.count.neuron_count))

            elif layer_name == ELayers['BATCH']['text']:
                converted_layers.append(
                    tf.keras.layers.BatchNormalization(momentum=layer_parameters['Momentum'],
                                                       epsilon=layer_parameters['Epsilon']))

            elif layer_name == ELayers['CONVOLUTION']['text']:
                converted_layers.append(
                    tf.keras.layers.Convolution2D(filters=layer_parameters['Filters count'],
                                                  kernel_size=(
                                                      layer_parameters['Kernel size'],
                                                      layer_parameters['Kernel size'])))

            elif layer_name == ELayers['MAX_POOLING']['text']:
                converted_layers.append(
                    tf.keras.layers.MaxPooling2D(
                        pool_size=(layer_parameters['Pool size'], layer_parameters['Pool size'])))

            elif layer_name == ELayers['UP_SAMPLING']['text']:
                converted_layers.append(
                    tf.keras.layers.UpSampling2D(size=(layer_parameters['Pool size'], layer_parameters['Pool size'])))

            elif layer_name == ELayers['DROPOUT']['text']:
                converted_layers.append(
                    tf.keras.layers.Dropout(rate=layer_parameters['Coefficient']))

            elif layer_name == ELayers['FLATTEN']['text']:
                converted_layers.append(tf.keras.layers.Flatten())

            elif layer_name == ELayers['ELU']['text']:
                converted_layers.append(tf.keras.layers.ELU())

            elif layer_name == ELayers['RELU']['text']:
                converted_layers.append(tf.keras.layers.ReLU())

            elif layer_name == ELayers['SELU']['text']:
                converted_layers.append(tf.keras.layers.Activation("selu"))

            elif layer_name == ELayers['SIGMOID']['text']:
                converted_layers.append(tf.keras.layers.Activation("sigmoid"))

            elif layer_name == ELayers['TANH']['text']:
                converted_layers.append(tf.keras.layers.Activation("tanh"))

        converted_layers.append(tf.keras.layers.Dense(units=2,
                                                      activation='softmax'))
        model = tf.keras.Sequential(converted_layers)
        model.compile(optimizer, "sparse_categorical_crossentropy", ['accuracy'])

        print("Fitting new model...")

    else:
        print("Fitting existence model...")

    ds = tf.keras.utils.image_dataset_from_directory(
        'dataset/test',
        shuffle=True,
        seed=69,
        image_size=images_shape,
        color_mode="grayscale",
        batch_size=8)

    ds_size = len(ds)
    train_ds = ds.take(int(ds_size * 0.8))
    validation_ds = ds.skip(int(ds_size * 0.8))

    fit_result = model.fit(train_ds.cache(), validation_data=validation_ds.cache(), epochs=epochs, verbose=2)
    print("Model fitted!")

    return model, fit_result


def predict(model: tf.keras.Model, batch_size, images_shape):
    try:
        shutil.rmtree('to_predict')
    except:
        pass

    try:
        os.mkdir('to_predict')
        os.mkdir('to_predict/cat')
        os.mkdir('to_predict/not_cat')
    except:
        pass

    test_cats_images_names = [f'cat/{name}' for name in os.listdir('dataset/test/cat')]
    test_not_cats_images_names = [f'not_cat/{name}' for name in os.listdir('dataset/test/not_cat')]

    test_images_names = test_cats_images_names + test_not_cats_images_names
    test_images_names = random.sample(test_images_names, k=min(batch_size, len(test_images_names)))

    for i in range(len(test_images_names)):
        image = cv2.imread(f'dataset/test/{test_images_names[i]}')
        cv2.imwrite(f'to_predict/{test_images_names[i]}', image)

    image_id = random.randint(0, len(test_images_names) - 1)
    predicted_image_name = test_images_names[image_id]

    image = cv2.imread(f'dataset_all/test/{predicted_image_name}')
    image_resized = cv2.resize(image, images_shape)
    cv2.imwrite(f'image_to_show_on_predict.jpg', image_resized)

    predict_ds = tf.keras.utils.image_dataset_from_directory(
        'to_predict',
        shuffle=False,
        image_size=images_shape,
        color_mode="grayscale",
        batch_size=batch_size)

    predicted_image_labels = []
    for image, label in predict_ds.take(1):
        predicted_image_labels = label.numpy()
        break

    results = model.predict(predict_ds, verbose=2)

    return results, predicted_image_name, predicted_image_labels, image_id


def clear():
    tf.keras.backend.clear_session()
