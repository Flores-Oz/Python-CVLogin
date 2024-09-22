# login.py

import tkinter as tk
from tkinter import messagebox
import hashlib
import os

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

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if verify_password(username, password):
        messagebox.showinfo("Info", "Acceso concedido.")
        root.destroy()
        import main_app  # Importa y ejecuta la aplicación principal
    else:
        messagebox.showwarning("Warning", "Nombre de usuario o contraseña incorrectos.")

def switch_to_register():
    root.destroy()
    import register_user  # Importa y ejecuta el registro de usuario

def setup_login_interface():
    global entry_username, entry_password, root
    root = tk.Tk()
    root.title("Iniciar Sesión")

    lbl_username = tk.Label(root, text="Nombre de Usuario:")
    lbl_username.pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    lbl_password = tk.Label(root, text="Contraseña:")
    lbl_password.pack()
    entry_password = tk.Entry(root, show='*')
    entry_password.pack()

    btn_login = tk.Button(root, text="Iniciar Sesión", command=login)
    btn_login.pack()

    btn_register = tk.Button(root, text="Registrarse", command=switch_to_register)
    btn_register.pack()

    root.mainloop()

if __name__ == "__main__":
    setup_login_interface()
