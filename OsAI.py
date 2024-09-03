import os
import google.generativeai as genai
import speech_recognition as sr
import tempfile
import pygame
import edge_tts

# Konfigurasi Gemini API
os.environ["API_KEY"] = "AIzaSyDdkDzW35qgr3uEK7wDZ1dks1-epOvvcyI"
genai.configure(api_key=os.environ["API_KEY"])
model_name = "ogi"
model_role = "Asisten Virtual Berbasis AI untuk Menjawab Pertanyaan dalam Bahasa Indonesia"
model = genai.GenerativeModel('gemini-1.5-flash')

# Fungsi untuk text-to-speech menggunakan Edge TTS
async def text_to_speech(text, lang='id'):
    communicate = edge_tts.Communicate(text, voice="id-ID-ArdiNeural")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        await communicate.save(fp.name)
    return fp.name

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()


    if os.path.exists(file_path):
        os.remove(file_path)

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Silakan bicara...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="id-ID")
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition tidak dapat memahami audio")
        return None
    except sr.RequestError as e:
        print(f"Tidak dapat meminta hasil dari layanan Google Speech Recognition; {e}")
        return None

def generate_content(prompt):
    full_prompt = (
        f"{model_name}, {model_role}. "
        f"{prompt}"
    )
    response = model.generate_content(full_prompt)
    return response.text

async def main():
    print(f"Selamat datang!")
    while True:
        input_text = speech_to_text()
        if input_text:
            print(f"👨User: {input_text}")

            if input_text.lower() in ["keluar", "stop"]:
                print("Terima kasih telah menggunakan asisten suara. Sampai jumpa!")
                break

            prompt = f"Berikan respons dengan singkat dan jelas, jangan gunakan emoticon: {input_text}"
            response = generate_content(prompt)
            print(f"🕵️OsAI: {response}")

            audio_file = await text_to_speech(response)
            play_audio(audio_file)
            
        else:
            print("Maaf, saya tidak mendengar apa-apa. Silakan coba lagi.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
