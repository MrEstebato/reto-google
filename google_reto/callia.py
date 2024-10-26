from google.cloud import speech
import pyaudio
import keyboard
import threading
import time
from pydub import AudioSegment
from io import BytesIO
import google.generativeai as genai
from load_creds import load_creds
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Variables and configurations
pre_text = "This is an instruction message. You will receive a conversation only reading the possible scammer's side. Use it to determine whether it is a scam call or a normal call. Return a value from 0 to 100. 0 if not a scam, 100 if it is totally a scam"
AudioSegment.converter = "C:/Program Files/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"  # Ensure pydub finds FFmpeg
creds = load_creds()  # Load credentials
genai.configure(credentials=creds)  # Configure credentials
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="tunedModels/scamstuned-ski2920q7evd",
    generation_config=generation_config,
)  # Use fine-tuned model


def generateAudioSample(filename):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1  # Changed from 2 to 1
    rate = 44100

    p = pyaudio.PyAudio()

    default_input_device_index = p.get_default_input_device_info()["index"]

    stream = p.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        input_device_index=default_input_device_index,
        frames_per_buffer=chunk,
    )

    frames = []

    # print(f"Starting Recording {filename}")
    starting_time = time.time()

    # Record audio until 10 seconds or SPACE is pressed again
    while time.time() - starting_time <= 10:
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print(f"Stopping recording {filename}")

    # Convert the frames to an MP3 in memory
    audio_data = BytesIO(b"".join(frames))
    audio_segment = AudioSegment(
        audio_data.read(),
        sample_width=p.get_sample_size(format),
        frame_rate=rate,
        channels=channels,
    )

    # Export to MP3
    mp3_filename = f"{filename}.mp3"
    audio_segment.export(mp3_filename, format="mp3")
    # print(f"Audio saved as {mp3_filename}")


def transcribeAudioToText(file_name):
    # Autenticación OAuth
    creds = load_creds()
    client = speech.SpeechClient(credentials=creds)

    with open(file_name, "rb") as file:
        mp3_data = file.read()

    audio_file = speech.RecognitionAudio(content=mp3_data)

    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        enable_automatic_punctuation=True,
        language_code="es-MX",
    )

    response = client.recognize(config=config, audio=audio_file)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return " ".join(transcripts)


def generateSTT(filename, chat_session):
    scam_value_counter = 0
    count = 1
    transcripts = []

    print("Recording... Press SPACE again to stop.")
    time.sleep(0.2)

    def process_audio(audio_filename, chat_session):
        nonlocal scam_value_counter
        text = transcribeAudioToText(audio_filename)  # Transcribe audio to text
        print(f"Transcript for {audio_filename}: {text}")

        with open("call_log.txt", "r") as f:
            call_log = f.read()
            text = (call_log + " " + text) if call_log is not None else text

        # Send prompt to model
        response = chat_session.send_message(
            text,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
        )
        scam_value = int(response.text) if int(response.text) <= 100 else 100

        with open("scam_values.txt", "w") as scam_file:
            scam_file.write(f"{scam_value} {scam_value_counter}\n")

        print(f"Scam Value: {scam_value}")
        if scam_value >= 80:  # scam value threshhold
            scam_value_counter += 1
        else:
            scam_value_counter = 0
        # print(chat_session.history)
        # reason = "Some Reason"

        # Guardar la respuesta en un archivo o imprimirla
        with open("call_log.txt", "w") as f:
            f.write(f"{text}. ")

    while True:
        try:
            current_filename = f"{filename}{count}.mp3"
            generateAudioSample(f"{filename}{count}")

            # Start processing the previous audio file (if any) in a separate thread
            if count > 1:
                previous_filename = f"{filename}{count-1}.mp3"
                thread = threading.Thread(
                    target=process_audio,
                    args=(previous_filename, chat_session),
                )
                thread.start()

            count += 1
            time.sleep(0.2)

            if keyboard.is_pressed("space"):
                print("STOPPING ALL RECORDINGS")
                break

            if scam_value_counter == 3:
                print("Scam detected. Stopping recordings.")
                break

        except KeyboardInterrupt:
            break

    # Process the last recorded audio
    last_filename = f"{filename}{count-1}.mp3"
    process_audio(last_filename)

    # Wait for all threads to complete
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

    return transcripts


def main():
    chat_session = model.start_chat(history=[])
    chat_session.send_message(pre_text)
    generateSTT("ESTE_BANQUITO", chat_session)


if __name__ == "__main__":
    main()
