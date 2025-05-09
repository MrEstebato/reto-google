from tkinter import *
from PIL import Image, ImageTk
import funciones as func
import os
import threading
import callia

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

# Define the function to start the external script
def start_call_script():
    #os.system("python callia.py")
    chat_session = callia.model.start_chat(history=[])
    # chat_session.send_message(pre_text)
    callia.generateSTT("ESTE_BANQUITO", chat_session)
    v_main.quit()  # Close the main Tkinter window once the thread ends

# Function to handle button clicks
def on_button_click(event):
    x, y = event.x, event.y
    if accept_button in canvas.find_overlapping(x-32, y-32, x+32, y+32):
        func.aceptar_llamada(v_main)
        threading.Thread(target=start_call_script).start()  # Start in a separate thread
    elif reject_button in canvas.find_overlapping(x-32, y-32, x+32, y+32):
        func.rechazar_llamada(v_main)

# Bind the click event to the canvas
canvas.bind("<Button-1>", on_button_click)

v_main.mainloop()
