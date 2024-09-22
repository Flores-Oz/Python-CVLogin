import cv2
import os

# Crear el objeto de reconocimiento facial LBPH
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Leer el modelo entrenado
face_recognizer.read('modeloLBPHFace.xml')

# Inicializar el capturador de video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Usa 'Video.mp4' si tienes un archivo de video

# Cargar el clasificador de rostros
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()

    # Detectar rostros en la imagen
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (200, 200), interpolation=cv2.INTER_CUBIC)  # Ajusta el tamaño si es necesario
        result = face_recognizer.predict(rostro)

        # Mostrar el resultado del reconocimiento facial
        if result[1] < 70:  # Ajusta este umbral según el método y el modelo utilizado
            cv2.putText(frame, 'Persona {}'.format(result[0]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Desconocido', (x, y-20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == 27:  # Esc para salir
        break

cap.release()
cv2.destroyAllWindows()
