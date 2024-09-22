import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Directorio para almacenar imágenes y modelos
dataPath = 'C:\\Users\\Oscar\\OneDrive\\Documentos\\Python Face\\Data'
namesFilePath = 'names.txt'  # Archivo para guardar los nombres asociados con las etiquetas

# Inicializar la variable global cap
cap = None

def open_camera():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        messagebox.showerror("Error", "No se puede acceder a la cámara.")
        return

def capture_face():
    global cap
    if cap is None:
        open_camera()
    
    person_name = entry_name.get()
    if person_name:
        person_path = os.path.join(dataPath, person_name)
        if not os.path.exists(person_path):
            os.makedirs(person_path)
        
        count = 0
        while count < 40:  # Captura 30 fotos
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "No se puede leer el frame del video.")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = faceClassif.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (100, 100), interpolation=cv2.INTER_CUBIC)  # Reducción del tamaño de la imagen
                img_path = os.path.join(person_path, f'face_{count}.jpg')
                cv2.imwrite(img_path, face)
                count += 1
            
            cv2.putText(frame, f'Capturando foto {count}/40', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Capturando rostros', frame)

            if cv2.waitKey(1) & 0xFF == 27:  # Permitir salir con la tecla 'Esc'
                break

        cv2.destroyWindow('Capturando rostros')
        messagebox.showinfo("Info", f"Captura completada. Se guardaron {count} fotos.")
    else:
        messagebox.showwarning("Warning", "Por favor, ingrese un nombre.")

def delete_person():
    person_name = entry_name.get()
    if person_name:
        person_path = os.path.join(dataPath, person_name)
        if os.path.exists(person_path):
            for file_name in os.listdir(person_path):
                os.remove(os.path.join(person_path, file_name))
            os.rmdir(person_path)
            update_names_file()
            messagebox.showinfo("Info", "Datos de la persona eliminados.")
        else:
            messagebox.showwarning("Warning", "La persona no existe.")
    else:
        messagebox.showwarning("Warning", "Por favor, ingrese un nombre.")

def identify_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    peopleList = os.listdir(dataPath)
    labels = []
    facesData = []
    label = 0
    
    # Guardar los nombres asociados con cada etiqueta
    names = {}
    
    for nameDir in peopleList:
        personPath = os.path.join(dataPath, nameDir)
        # Asegúrate de que personPath es un directorio
        if os.path.isdir(personPath):
            for fileName in os.listdir(personPath):
                img_path = os.path.join(personPath, fileName)
                # Asegúrate de que img_path es un archivo
                if os.path.isfile(img_path):
                    img = cv2.imread(img_path, 0)
                    if img is not None:
                        img = cv2.resize(img, (100, 100))  # Reducción del tamaño de la imagen
                        facesData.append(img)
                        labels.append(label)
            names[label] = nameDir  # Guardar el nombre de la persona con la etiqueta
            label += 1
    
    recognizer.train(facesData, np.array(labels))
    recognizer.write('modeloLBPHFace.xml')
    
    # Guardar los nombres en un archivo
    with open(namesFilePath, 'w') as f:
        for lbl, name in names.items():
            f.write(f'{lbl}:{name}\n')
    
    messagebox.showinfo("Info", "Modelo entrenado y guardado.")

def update_names_file():
    # Actualizar el archivo de nombres al eliminar una persona
    names = {}
    peopleList = os.listdir(dataPath)
    label = 0
    for nameDir in peopleList:
        personPath = os.path.join(dataPath, nameDir)
        if os.path.isdir(personPath):
            names[label] = nameDir
            label += 1
    with open(namesFilePath, 'w') as f:
        for lbl, name in names.items():
            f.write(f'{lbl}:{name}\n')

def show_frame():
    global cap
    if cap is None:
        open_camera()
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = faceClassif.detectMultiScale(gray, 1.3, 5)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('modeloLBPHFace.xml')
        
        # Cargar los nombres asociados con las etiquetas
        names = {}
        if os.path.exists(namesFilePath):
            with open(namesFilePath, 'r') as f:
                for line in f:
                    lbl, name = line.strip().split(':')
                    names[int(lbl)] = name
        
        for (x, y, w, h) in faces:
            rostro = gray[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (100, 100), interpolation=cv2.INTER_CUBIC)  # Reducción del tamaño de la imagen
            result = recognizer.predict(rostro)
            label, confidence = result
            
            if confidence < 70:  # Ajusta este umbral según el método y el modelo utilizado
                name = names.get(label, "Desconocido")
                cv2.putText(frame, name, (x, y-25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Desconocido', (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
    
    lbl_video.after(10, show_frame)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Reconocimiento Facial")

lbl_name = tk.Label(root, text="Nombre:")
lbl_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

btn_capture = tk.Button(root, text="Capturar Cara", command=capture_face)
btn_capture.pack()

btn_delete = tk.Button(root, text="Eliminar Persona", command=delete_person)
btn_delete.pack()

btn_identify = tk.Button(root, text="Entrenar Modelo", command=identify_faces)
btn_identify.pack()

lbl_video = tk.Label(root)
lbl_video.pack()

show_frame()

root.mainloop()

if cap is not None:
    cap.release()
cv2.destroyAllWindows()
