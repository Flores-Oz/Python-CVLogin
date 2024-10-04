import cv2

# El índice de la cámara puede variar, generalmente es 0 o 1
cap = cv2.VideoCapture(1)  # Cambia el número si no ves el video

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Muestra el video en una ventana
    cv2.imshow('Video desde DroidCam', frame)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
