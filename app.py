import tkinter as tk
from tkinter import messagebox
import hashlib
import os
import subprocess

passwordsFilePath = 'passwords.txt'  # Archivo para guardar las contraseñas

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(username, password):
    hashed_password = hash_password(password)
    if os.path.exists(passwordsFilePath):
        with open(passwordsFilePath, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split(':')
                if stored_username == username and stored_password == hashed_password:
                    return True
    return False

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if username and password:
        with open(passwordsFilePath, 'a') as f:
            f.write(f'{username}:{hash_password(password)}\n')
        messagebox.showinfo("Info", "Usuario registrado exitosamente.")
        switch_to_login()  # Volver a la pantalla de login
    else:
        messagebox.showwarning("Warning", "Por favor, ingrese un nombre de usuario y una contraseña.")

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if verify_password(username, password):
        messagebox.showinfo("Info", "Acceso concedido.")
        root.destroy()
        try:
            print("Intentando ejecutar main_app...")
            process = subprocess.Popen(["python", "main_app.py"])
            print("main_app ejecutado exitosamente.")
            process.wait()  # Esperar a que main_app.py termine de ejecutarse
        except Exception as e:
            print(f"Error al ejecutar main_app: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al iniciar la aplicación principal: {e}")
    else:
        messagebox.showwarning("Warning", "Nombre de usuario o contraseña incorrectos.")

def switch_to_register():
    clear_frame()
    lbl_title = tk.Label(root, text="Registro de Usuario", font=('Helvetica', 16))
    lbl_title.pack()

    lbl_username = tk.Label(root, text="Nombre de Usuario:")
    lbl_username.pack()
    global entry_username
    entry_username = tk.Entry(root)
    entry_username.pack()

    lbl_password = tk.Label(root, text="Contraseña:")
    lbl_password.pack()
    global entry_password
    entry_password = tk.Entry(root, show='*')
    entry_password.pack()

    btn_register = tk.Button(root, text="Registrar", command=register_user)
    btn_register.pack()

    btn_back_to_login = tk.Button(root, text="Volver al Login", command=switch_to_login)
    btn_back_to_login.pack()

def switch_to_login():
    clear_frame()
    lbl_title = tk.Label(root, text="Iniciar Sesión", font=('Helvetica', 16))
    lbl_title.pack()

    lbl_username = tk.Label(root, text="Nombre de Usuario:")
    lbl_username.pack()
    global entry_username
    entry_username = tk.Entry(root)
    entry_username.pack()

    lbl_password = tk.Label(root, text="Contraseña:")
    lbl_password.pack()
    global entry_password
    entry_password = tk.Entry(root, show='*')
    entry_password.pack()

    btn_login = tk.Button(root, text="Iniciar Sesión", command=login)
    btn_login.pack()

    btn_register = tk.Button(root, text="Registrarse", command=switch_to_register)
    btn_register.pack()

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def setup_app_interface():
    global root
    root = tk.Tk()
    root.title("Aplicación de Login y Registro")

    # Inicializar la pantalla de login
    switch_to_login()

    root.mainloop()

if __name__ == "__main__":
    setup_app_interface()
