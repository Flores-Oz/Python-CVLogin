# main_app.py
import tkinter as tk

def setup_main_app_interface():
    root = tk.Tk()
    root.title("Aplicación Principal")

    lbl_welcome = tk.Label(root, text="¡Bienvenido a la Aplicación Principal!", font=('Helvetica', 16))
    lbl_welcome.pack()

    root.mainloop()

if __name__ == "__main__":
    setup_main_app_interface()
