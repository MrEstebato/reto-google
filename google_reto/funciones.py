from tkinter import *
from PIL import Image, ImageTk

# Función que muestra el mensaje de llamada aceptada en la misma ventana
def aceptar_llamada(v_main):
    v_main.title("Llamada en curso")
    # Limpiar la ventana
    for widget in v_main.winfo_children():
        widget.destroy()

    # Cargar la imagen de fondo y adaptarla al tamaño de la ventana
    image = Image.open("blurred.jpg")
    image = image.resize((300, 600), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)

    # Crear un Canvas y colocar la imagen de fondo en él
    canvas = Canvas(v_main, width=300, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # Mantener una referencia a la imagen de fondo
    canvas.bg_image = bg_image  # Esto mantiene la referencia

    # Añadir el número de teléfono en la parte superior
    canvas.create_text(150, 50, text="555 121 702", fill="white", font=("Arial", 24, "bold"))

    # Cambiar el nombre o descripción si es necesario, por ejemplo, "En llamada"
    canvas.create_text(150, 90, text="En llamada", fill="white", font=("Arial", 12))

    # Agregar el contador de llamada
    canvas.call_counter = 0  # Inicializar el contador
    call_counter_text = canvas.create_text(150, 130, text="00:00", fill="white", font=("Arial", 12))
    
    # Función para actualizar el contador
    def update_counter():
        canvas.call_counter += 1
        minutes = canvas.call_counter // 60
        seconds = canvas.call_counter % 60
        # Formatear el tiempo en formato 00:00
        time_formatted = f"{minutes:02}:{seconds:02}"
        canvas.itemconfig(call_counter_text, text=f"{time_formatted}")
        # Llamar a esta función cada segundo
        canvas.after(1000, update_counter)

    # Iniciar el contador
    update_counter()

    # Agregar el botón de rechazar
    reject_img = Image.open("reject.png").resize((64, 64), Image.LANCZOS)
    reject_photo = ImageTk.PhotoImage(reject_img)
    reject_button = canvas.create_image(150, 500, image=reject_photo)

    # Mantener la referencia a la imagen del botón de rechazar
    canvas.reject_photo = reject_photo  # Esto mantiene la referencia

    # Vincular el botón de rechazar a su función
    canvas.tag_bind(reject_button, "<Button-1>", lambda event: rechazar_llamada(v_main))

# Función que muestra el mensaje de llamada rechazada en la misma ventana
def rechazar_llamada(v_main):
    v_main.destroy()  # Elimina la ventana original
