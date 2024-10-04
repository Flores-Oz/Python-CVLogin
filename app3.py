import tkinter as tk
from tkinter import messagebox
import cv2
import os
import time
import subprocess
import numpy as np  # Necesario para manejar etiquetas en el entrenamiento

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")
        
        # Initialize widgets for the login and registration interface
        self.setup_login_interface()

    def setup_login_interface(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.lbl_title = tk.Label(self.root, text="Iniciar Sesión", font=("Arial", 24))
        self.lbl_title.pack(pady=20)
        
        self.lbl_user = tk.Label(self.root, text="Nombre de usuario:")
        self.lbl_user.pack()
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack()
        
        self.btn_login = tk.Button(self.root, text="Iniciar Sesión", command=self.face_login)
        self.btn_login.pack(pady=10)
        
        self.btn_register = tk.Button(self.root, text="Registrar", command=self.switch_to_register)
        self.btn_register.pack(pady=10)

    def switch_to_register(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.lbl_title = tk.Label(self.root, text="Registro Facial", font=("Arial", 24))
        self.lbl_title.pack(pady=20)
        
        self.lbl_user = tk.Label(self.root, text="Nombre de usuario:")
        self.lbl_user.pack()
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack()
        
        self.btn_register = tk.Button(self.root, text="Registrar", command=self.face_register)
        self.btn_register.pack(pady=10)
        
        self.btn_back = tk.Button(self.root, text="Volver", command=self.setup_login_interface)
        self.btn_back.pack(pady=10)
    
    def face_register(self):
        username = self.entry_user.get()
        if not username:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario.")
            return
        
        if self.username_exists(username):
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
            return

        self.start_face_registration(username)
        self.train_model(username)  # Llamar a la función de entrenamiento después de capturar las imágenes
    
    def username_exists(self, username):
        return os.path.exists(f"dataset/{username}")

    def start_face_registration(self, username):
        user_dir = f"dataset/{username}"
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        capture = cv2.VideoCapture(1)
        num_images = 0
        while num_images < 100:
            ret, frame = capture.read()
            if ret:
                cv2.imshow("Face Registration", frame)
                cv2.imwrite(f"{user_dir}/{num_images}.png", frame)
                num_images += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        capture.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Registro Completo", "Registro facial completado exitosamente.")
    
    def train_model(self, username):
        user_dir = f"dataset/{username}"
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        faces = []
        labels = []
        
        for img_name in os.listdir(user_dir):
            img_path = os.path.join(user_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(0)  # Etiqueta correspondiente al usuario (0 ya que es un solo usuario)
        
        recognizer.train(faces, np.array(labels))
        recognizer.save(f'{user_dir}/model.yml')
        print(f"Modelo guardado en {user_dir}/model.yml")

    def face_login(self):
        username = self.entry_user.get()
        
        if not username:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario.")
            return
        
        if not self.username_exists(username):
            messagebox.showerror("Error", "El nombre de usuario no existe.")
            return
        
        self.start_face_recognition(username)

    def start_face_recognition(self, username):
        capture = cv2.VideoCapture(1)
        recognized = False
        wait_time = 10
        start_time = time.time()
        
        while not recognized and (time.time() - start_time < wait_time):
            ret, frame = capture.read()
            if ret:
                cv2.imshow("Face Recognition", frame)
                recognized = self.recognize_face(frame, username)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        capture.release()
        cv2.destroyAllWindows()
        
        if recognized:
            messagebox.showinfo("Acceso Concedido", "Ingreso exitoso.")
            subprocess.Popen(["python", "user_management.py"])
            self.root.withdraw()
        else:
            messagebox.showerror("Acceso Denegado", "No se reconoció la cara.")

    def recognize_face(self, frame, username):
        user_dir = f"dataset/{username}"
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        try:
            recognizer.read(f'{user_dir}/model.yml')
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo del modelo no se encontró. Asegúrate de haber registrado la cara correctamente.")
            return False
        except cv2.error as e:
            messagebox.showerror("Error", f"No se pudo cargar el modelo facial: {e}")
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face_roi)
            if confidence < 200:  # Ajusta el umbral de confianza si es necesario
                return True
        
        return False

# Crear la ventana de Tkinter y ejecutar la aplicación
root = tk.Tk()
app = FaceRecognitionApp(root)
root.mainloop()
