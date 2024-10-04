import face_recognition
import cv2

# Cargar la imagen de referencia del usuario
reference_image = face_recognition.load_image_file("path/to/registered_image.png")
reference_encoding = face_recognition.face_encodings(reference_image)[0]

# Capturar la imagen de la cámara
capture = cv2.VideoCapture(0)
ret, frame = capture.read()
capture.release()

# Procesar la imagen capturada
unknown_face_encodings = face_recognition.face_encodings(frame)

# Comparar la imagen capturada con la imagen de referencia
results = face_recognition.compare_faces([reference_encoding], unknown_face_encodings[0])

if results[0]:
    print("¡Cara reconocida!")
else:
    print("No se reconoció la cara.")
