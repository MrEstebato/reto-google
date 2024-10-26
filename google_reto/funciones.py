from tkinter import *
from PIL import Image, ImageTk

def obtener_probabilidad():
    return 50  # Simulación de una probabilidad de estafa

def aceptar_llamada(v_main):
    v_main.title("Llamada en curso")
    for widget in v_main.winfo_children():
        widget.destroy()

    image = Image.open("blurred.jpg").resize((300, 600), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)
    canvas = Canvas(v_main, width=300, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    canvas.bg_image = bg_image

    canvas.create_text(150, 50, text="555 121 702", fill="white", font=("Arial", 24, "bold"))
    canvas.create_text(150, 90, text="En llamada", fill="white", font=("Arial", 12))

    # Inicializar el rectángulo y el texto de probabilidad
    rect_height = 40
    rect_top = 160
    probabilidad_text_id = canvas.create_text(150, 200 + rect_height // 2, text="", fill="white", font=("Arial", 12))
    rect_id = canvas.create_rectangle(0, rect_top, 300, rect_top + rect_height, fill="red", outline="")  # Color inicial

    # Función para actualizar la probabilidad
    def actualizar_probabilidad():
        probabilidad = obtener_probabilidad()  # Obtener la probabilidad

        # Solo actualizar si hay una probabilidad válida
        if probabilidad is not None:
            probabilidad_text = f"Probabilidad de estafa: {probabilidad}%"
            canvas.itemconfig(probabilidad_text_id, text=probabilidad_text)

            # Cambiar el color del fondo según la probabilidad
            if probabilidad < 30:
                canvas.itemconfig(rect_id, fill="green")  # Bajo riesgo
            elif probabilidad < 70:
                canvas.itemconfig(rect_id, fill="yellow")  # Riesgo moderado
            else:
                canvas.itemconfig(rect_id, fill="red")  # Alto riesgo
        else:
            canvas.itemconfig(probabilidad_text_id, text="Probabilidad de estafa: No disponible")
            canvas.itemconfig(rect_id, fill="gray")  # Color por defecto si no hay datos

        # Llamar a esta función cada 15 segundos
        canvas.after(15000, actualizar_probabilidad)

    # Llamar a la función de actualización de probabilidad al inicio
    actualizar_probabilidad()

    canvas.call_counter = 0
    call_counter_text = canvas.create_text(150, 130, text="00:00", fill="white", font=("Arial", 12))

    def update_counter():
        canvas.call_counter += 1
        minutes = canvas.call_counter // 60
        seconds = canvas.call_counter % 60
        time_formatted = f"{minutes:02}:{seconds:02}"
        canvas.itemconfig(call_counter_text, text=time_formatted)
        canvas.after(1000, update_counter)

    update_counter()

    reject_img = Image.open("reject.png").resize((64, 64), Image.LANCZOS)
    reject_photo = ImageTk.PhotoImage(reject_img)
    reject_button = canvas.create_image(150, 500, image=reject_photo)
    canvas.reject_photo = reject_photo
    canvas.tag_bind(reject_button, "<Button-1>", lambda event: rechazar_llamada(v_main))


# Función que muestra el mensaje de llamada rechazada en la misma ventana
def rechazar_llamada(v_main):
    v_main.destroy()  # Elimina la ventana original
