import cv2
import os
import numpy as np

dataPath = 'C:\\Users\\Oscar\\OneDrive\\Documentos\\Python Face\\Data'
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)

labels = []
facesData = []
label = 0

for nameDir in peopleList:
    personPath = os.path.join(dataPath, nameDir)
    print('Leyendo las imágenes de:', personPath)

    for fileName in os.listdir(personPath):
        img_path = os.path.join(personPath, fileName)
        print('Rostro:', img_path)
        img = cv2.imread(img_path, 0)
        if img is not None:
            img = cv2.resize(img, (200, 200))  # Ajusta el tamaño si es necesario
            facesData.append(img)
            labels.append(label)
    label += 1

# Crear el reconocedor de rostros LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Entrenar el modelo con los datos de las caras
recognizer.train(facesData, np.array(labels))

# Guardar el modelo entrenado
recognizer.write('modeloLBPHFace.xml')

print('Modelo entrenado y guardado como modeloLBPHFace.xml')
