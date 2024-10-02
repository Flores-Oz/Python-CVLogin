import tkinter as tk
from tkinter import messagebox  # Importar messagebox correctamente
import os
import shutil
from app2  import FaceRecognitionApp  # Asegúrate de que la ruta sea correcta

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Usuarios")

        # Inicializa la interfaz de gestión de usuarios
        self.setup_user_management_interface()

    def setup_user_management_interface(self):
        # Limpiar widgets existentes
        for widget in self.root.winfo_children():
            widget.destroy()

        self.lbl_title = tk.Label(self.root, text="Gestión de Usuarios", font=("Arial", 24))
        self.lbl_title.pack(pady=20)

        self.user_listbox = tk.Listbox(self.root, width=50)
        self.user_listbox.pack(pady=10)

        self.load_users()

        self.btn_delete = tk.Button(self.root, text="Eliminar Usuario", command=self.delete_user)
        self.btn_delete.pack(pady=5)

        self.btn_back = tk.Button(self.root, text="Volver", command=self.go_back)
        self.btn_back.pack(pady=5)

    def load_users(self):
        self.user_listbox.delete(0, tk.END)  # Limpiar el listbox
        user_dirs = os.listdir("dataset")
        for user in user_dirs:
            self.user_listbox.insert(tk.END, user)

    def delete_user(self):
        selected_user = self.user_listbox.curselection()
        if not selected_user:
            messagebox.showerror("Error", "Por favor, seleccione un usuario para eliminar.")
            return

        username = self.user_listbox.get(selected_user)
        user_dir = f"dataset/{username}"

        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar a {username}?"):
            shutil.rmtree(user_dir)  # Elimina el directorio del usuario
            messagebox.showinfo("Éxito", "Usuario eliminado con éxito.")
            self.load_users()  # Recargar la lista de usuarios

    def go_back(self):
        self.root.destroy()  # Cerrar la ventana actual
        # Regresar a la ventana de inicio de sesión
        root = tk.Tk()
        app = FaceRecognitionApp(root)  # Ahora debería estar definida
        root.mainloop()

# Crear la ventana de Tkinter y ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()
