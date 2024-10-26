from google.cloud import speech
import pyaudio
import keyboard
import threading
import time
import os
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
import google.generativeai as genai
import json

# Ensure pydub finds FFmpeg
AudioSegment.converter = "C:/Program Files/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"  # Update path if necessary

# API SETUP ==============================================================
# GEMINI API
genai.configure(api_key="AIzaSyDapeWfBoIaJHEU5ElASDhUnuJaafaEGRc")  # Esteban
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # Especificar aqui las instrucciones
    system_instruction='You will receive a conversation in phrases, determine whether the conersation conversation is a scam. Use this schema to return a scam value between 0 and 100 and a reason why you think the user is being scammed in spanish: {"scamValue": int, "reason" : str}',
)


def generateAudioSample(filename):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1  # Changed from 2 to 1
    rate = 44100

    p = pyaudio.PyAudio()

    # Find the index of the default input device
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

    print(f"Starting Recording {filename}")
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
    print(f"Audio saved as {mp3_filename}")


def compareAudiotoTxt(file_name):

    client = speech.SpeechClient.from_service_account_file("key.json")

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


def generateSTT(filename):
    count = 1
    transcripts = []

    print("Press SPACE to start recordings")
    keyboard.wait("space")
    print("Recording... Press SPACE again to stop.")
    time.sleep(0.2)

    def process_audio(audio_filename):
        text = compareAudiotoTxt(audio_filename)
        transcripts.append(text)
        print(f"Transcript for {audio_filename}: {text}")

    while True:
        try:
            current_filename = f"{filename}{count}.mp3"
            generateAudioSample(f"{filename}{count}")

            # Start processing the previous audio file (if any) in a separate thread
            if count > 1:
                previous_filename = f"{filename}{count-1}.mp3"
                thread = threading.Thread(
                    target=process_audio,
                    args=(previous_filename,),
                )
                thread.start()

            count += 1
            time.sleep(0.2)

            if keyboard.is_pressed("space"):
                print("STOPPING ALL RECORDINGS")
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
    generateSTT("ESTE_BANQUITO")


if __name__ == "__main__":
    main()
