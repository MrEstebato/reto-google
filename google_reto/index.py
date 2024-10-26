from tkinter import *
from PIL import Image, ImageTk
import funciones as func

# Crear la ventana principal
v_main = Tk()
v_main.iconbitmap("google.ico")
v_main.title("Llamada entrante")
v_main.resizable(False, False)
v_main.geometry("300x600")

# Cargar la imagen de fondo y adaptarla al tamaño de la ventana
image = Image.open("blurred.jpg")
image = image.resize((300, 600), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(image)

# Crear un Canvas y colocar la imagen de fondo en él
canvas = Canvas(v_main, width=300, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Añadir el número de teléfono en la parte superior
canvas.create_text(150, 50, text="555 121 702", fill="white", font=("Arial", 24, "bold"))

# Añadir el nombre o descripción debajo del número
canvas.create_text(150, 90, text="Desconocido", fill="white", font=("Arial", 12))

# Cargar imágenes redondeadas para los botones
accept_img = Image.open("accept.png").resize((64, 64), Image.LANCZOS)
accept_photo = ImageTk.PhotoImage(accept_img)

reject_img = Image.open("reject.png").resize((64, 64), Image.LANCZOS)
reject_photo = ImageTk.PhotoImage(reject_img)

# Agregar las imágenes como botones en el canvas
accept_button = canvas.create_image(220, 500, image=accept_photo)
reject_button = canvas.create_image(80, 500, image=reject_photo)

# Función para manejar el clic en los botones
def on_button_click(event):
    x, y = event.x, event.y
    # Verificar si el clic fue dentro de algún botón
    if accept_button in canvas.find_overlapping(x-32, y-32, x+32, y+32):
        func.aceptar_llamada(v_main)  # Pasar la ventana
    elif reject_button in canvas.find_overlapping(x-32, y-32, x+32, y+32):
        func.rechazar_llamada(v_main)  # Pasar la ventana

# Vincular la función al evento de clic en el canvas
canvas.bind("<Button-1>", on_button_click)

v_main.mainloop()
