pyinstaller --noconfirm --onedir --console --name "Classificator idle" --add-data "C:/Users/User/Desktop/Studies/NN/5/dataset_all;dataset_all/" --add-data "C:/Users/User/Desktop/Studies/NN/5/resources;resources/"  "C:/Users/User/Desktop/Studies/NN/5/main.py"
powershell Compress-Archive "build/Classificator idle" "Classificator idle.zip"