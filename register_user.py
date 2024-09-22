# register_user.py

import tkinter as tk
from tkinter import messagebox
import hashlib
import os

passwordsFilePath = 'passwords.txt'  # Archivo para guardar las contraseñas

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if username and password:
        with open(passwordsFilePath, 'a') as f:
            f.write(f'{username}:{hash_password(password)}\n')
        messagebox.showinfo("Info", "Usuario registrado exitosamente.")
        root.destroy()
        import login  # Vuelve a la pantalla de login
    else:
        messagebox.showwarning("Warning", "Por favor, ingrese un nombre de usuario y una contraseña.")

def setup_register_interface():
    global entry_username, entry_password, root
    root = tk.Tk()
    root.title("Registro de Usuario")

    lbl_username = tk.Label(root, text="Nombre de Usuario:")
    lbl_username.pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    lbl_password = tk.Label(root, text="Contraseña:")
    lbl_password.pack()
    entry_password = tk.Entry(root, show='*')
    entry_password.pack()

    btn_register = tk.Button(root, text="Registrar", command=register_user)
    btn_register.pack()

    btn_back_to_login = tk.Button(root, text="Volver al Login", command=lambda: (root.destroy(), __import__('login').setup_login_interface()))
    btn_back_to_login.pack()

    root.mainloop()

if __name__ == "__main__":
    setup_register_interface()
