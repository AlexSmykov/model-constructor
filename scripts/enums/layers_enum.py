from typing import Type

from scripts.model_layers.abstract_layer import AbstractLayer
from scripts.model_layers.batch_normalization import BatchNormalization
from scripts.model_layers.convolution import Convolution
from scripts.model_layers.dense import Dense
from scripts.model_layers.dropout import Dropout
from scripts.model_layers.elu import Elu
from scripts.model_layers.flatten import Flatten
from scripts.model_layers.max_pooling import MaxPooling
from scripts.model_layers.relu import Relu
from scripts.model_layers.selu import Selu
from scripts.model_layers.sigmoid import Sigmoid
from scripts.model_layers.softmax import Softmax
from scripts.model_layers.tanh import Tanh
from scripts.model_layers.up_sampling import UpSampling


def layer_values(text: str, class_item: Type[AbstractLayer]) -> dict[str, str]:
    return {'text': text, 'class': class_item}


ELayers = {
    'BATCH': layer_values('Batch', BatchNormalization),
    'CONVOLUTION': layer_values('Convolution', Convolution),
    'MAX_POOLING': layer_values('Max pooling', MaxPooling),
    'UP_SAMPLING': layer_values('Up sampling', UpSampling),
    'DENSE': layer_values('Dense', Dense),
    'DROPOUT': layer_values('Dropout', Dropout),
    'FLATTEN': layer_values('Flatten', Flatten),
    'ELU': layer_values('Elu', Elu),
    'RELU': layer_values('Relu', Relu),
    'SELU': layer_values('Selu', Selu),
    'SIGMOID': layer_values('Sigmoid', Sigmoid),
    'SOFTMAX': layer_values('Softmax', Softmax),
    'TANH': layer_values('Tanh', Tanh)
}
