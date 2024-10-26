from tkinter import *
from PIL import Image, ImageTk
import whatsapp_handling

def read_last_line(file_path):
    with open(file_path, 'r') as file:
        # Move the cursor to the end of the file
        file.seek(0, 2)
        # Get the current position
        position = file.tell()
        # Read lines backwards until we find the last line
        while position > 0:
            file.seek(position - 1)
            if file.read(1) == '\n' and position != 1:  # Check for newline character
                break
            position -= 1
        last_line = file.readline().strip()  # Read the last line
    return last_line


def leerScamValues():
    try:
        with open("scam_values.txt", "r") as file:
            line = file.readline().strip()  # Leer la primera línea y quitar espacios en blanco
            values = line.split()  # Separar la línea en una lista por espacios
            
            # Asegurarse de que se han leído exactamente dos valores
            if len(values) == 2:
                return int(values[0]), int(values[1])  # Convertir a enteros y devolver
            else:
                print("El archivo no contiene exactamente dos valores.")
                return None, None
    except FileNotFoundError:
        print("El archivo 'scam_values.txt' no fue encontrado.")
        return None, None
    except ValueError:
        print("Error al convertir los valores a enteros.")
        return None, None

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
    def actualizar_probabilidad(v_main):
        scamVal, scamCount = leerScamValues()
        probabilidad = scamVal # Obtener la probabilidad

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

        
        try:
            if(scamCount > 2):
                rechazar_llamada(v_main)
                last_message = read_last_line("call_log.txt")
                print(f"last_message: {last_message}")
                whatsapp_handling.sendWhatsappMessage("7223892688", f"La llamada ha sido colgada debido a distintos mensajes misteriosos El ultimo fue: {last_message}")
        except:
            pass

        # Llamar a esta función cada 15 segundos
        canvas.after(5000,  lambda: actualizar_probabilidad(v_main))

    # Llamar a la función de actualización de probabilidad al inicio
    actualizar_probabilidad(v_main)

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
    with open("scam_values.txt", "w") as scam_file:
            scam_file.write(f"")
    v_main.destroy()  # Elimina la ventana original
    
