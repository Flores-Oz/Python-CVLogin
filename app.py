import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import os
import subprocess

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
        
        self.lbl_pass = tk.Label(self.root, text="Contraseña:")
        self.lbl_pass.pack()
        self.entry_pass = tk.Entry(self.root, show="*")
        self.entry_pass.pack()
        
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
    
    def username_exists(self, username):
        # Check if username already exists in the dataset folder
        return os.path.exists(f"dataset/{username}")

    def start_face_registration(self, username):
        # Create a directory for the user if it doesn't exist
        user_dir = f"dataset/{username}"
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        # Start the camera and capture images for face registration
        capture = cv2.VideoCapture(0)
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

    def face_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        # Placeholder for password check
        if not self.password_is_correct(username, password):
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
            return
        
        # Start face recognition for login
        self.start_face_recognition(username)
    
    def password_is_correct(self, username, password):
        # Placeholder for password check
        # You should implement actual password verification here
        return True
    
    def start_face_recognition(self, username):
        # Start the camera and attempt to recognize the face
        capture = cv2.VideoCapture(0)
        recognized = False
        while not recognized:
            ret, frame = capture.read()
            if ret:
                cv2.imshow("Face Recognition", frame)
                # Perform face recognition
                recognized = self.recognize_face(frame, username)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        capture.release()
        cv2.destroyAllWindows()
        if recognized:
            messagebox.showinfo("Acceso Concedido", "Ingreso exitoso.")
        else:
            messagebox.showerror("Acceso Denegado", "No se reconoció la cara.")

    def recognize_face(self, frame, username):
        # Placeholder for face recognition logic
        # Implement your face recognition logic here
        return True

# Create the Tkinter window and start the application
root = tk.Tk()
app = FaceRecognitionApp(root)
root.mainloop()
