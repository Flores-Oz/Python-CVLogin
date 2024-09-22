import cv2

# Verifica si `cv2.face` y `LBPHFaceRecognizer_create` están disponibles
if hasattr(cv2.face, 'LBPHFaceRecognizer_create'):
    print("El método 'LBPHFaceRecognizer_create' está disponible.")
else:
    print("El método 'LBPHFaceRecognizer_create' no está disponible.")
