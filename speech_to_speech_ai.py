import os
import sys
import json
import wave
import pyaudio
import threading
import subprocess
import ctypes
import shlex  # Essential for handling spaces in file paths
from vosk import Model, KaldiRecognizer, SetLogLevel
from llama_cpp import Llama

# Define ANSI escape codes for terminal text coloring (native to Ubuntu)
C_CYAN = "\033[1;96m"
C_GREEN = "\033[1;92m"
C_RESET = "\033[0m"

# Function to silence ALSA/JACK errors on startup
def silence_system_errors():
    try:
        # Redirecting stderr to null to prevent clutter in terminal
        libc = ctypes.CDLL('libc.so.6')
        stderr = libc.fdopen(2, 'w')
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 2)
        os.close(devnull)
    except Exception:
        pass

silence_system_errors()
SetLogLevel(-1)

# Configuration
MODEL_NAME = "llm_model.gguf"
MODEL_PATH = f"./models/{MODEL_NAME}"
VOSK_MODEL_PATH = "./models/vosk-model-small-en-us-0.15"
PIPER_MODEL_FILE = "./models/en_US-amy-medium.onnx"

num_threads = max(1, os.cpu_count() - 2)
num_context = 4096

BASE_RATE = 18700
LENGTH_SCALE = 0.7
NOISE_W = 0.72

def verify_required_models():
    """Verifies all required models and exits with a single concise error if any are missing."""
    missing = []
    
    # 1. Individual checks that feed into a single missing list
    if not os.path.exists(MODEL_PATH):
        missing.append("LLM")
        
    if not os.path.exists(VOSK_MODEL_PATH):
        missing.append("Vosk STT")
        
    if not os.path.exists(PIPER_MODEL_FILE):
        missing.append("Piper TTS")

    # 2. If the list is not empty, print one consolidated message and exit
    if missing:
        # Joins the missing models with commas (e.g., "LLM, Vosk STT")
        models_str = ", ".join(missing)
        print(f"Error: Models ({models_str}) not found. Please check your setup or refer to README.md.")
        sys.exit(1)
        
verify_required_models()
    
print("Loading AI model, please wait...")
global_llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=0, 
    n_ctx=num_context,
    n_threads=num_threads,
    verbose=False  
)
print("Model loaded successfully!")

recording = False

# Function to monitor recording stop (running in a separate thread)
def isRecording():
    global recording
    print("[Recording started - Type 'q' and press Enter to STOP]")
    while True:
        if input().strip().lower() == 'q':
            recording = False
            break

# TTS (Text-to-Speech) using Piper
def run_piper(text):
    python_exe = sys.executable
    
    # shlex.quote handles spaces in the path and special characters in the text
    safe_text = shlex.quote(text)
    
    # The command uses 2>/dev/null at the end to silence aplay/jack errors
    command = f'echo {safe_text} | "{python_exe}" -m piper --model "{PIPER_MODEL_FILE}" --length_scale {LENGTH_SCALE} --noise_w {NOISE_W} --output_raw | aplay -D plug:default -c 1 -r {BASE_RATE} -f S16_LE -t raw 2>/dev/null'
    
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        
        if error and error.strip():
            print(f"Piper Error: {error.decode()}")
        else:
            print("AI Response played successfully.")
    except Exception as e:
        print(f"Failed to run Piper: {e}")

# Audio recording function
def record_sound():
    global recording
    mic = pyaudio.PyAudio() 
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    
    thread = threading.Thread(target=isRecording)
    thread.start()

    frames = []
    recording = True
    print("[Recording in progress...]")
    
    try:
        while recording:
            data = stream.read(8192, exception_on_overflow=False)
            frames.append(data)
    except Exception as e:
        print(f"Recording error: {e}")
        recording = False

    thread.join()
    print("[Recording finished]")

    stream.stop_stream()
    stream.close()
    mic.terminate()

    with wave.open("temp_recorded_sound.wav", 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(mic.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))

# STT (Speech-to-Text) using Vosk
def get_text_from_voice():
    if not os.path.exists("temp_recorded_sound.wav"):
        return ""

    wf = wave.open("temp_recorded_sound.wav", "rb")
    
    if not os.path.exists(VOSK_MODEL_PATH):
        print(f"Error: Vosk model not found at {VOSK_MODEL_PATH}")
        wf.close()
        return ""

    model = Model(VOSK_MODEL_PATH)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
 
    text_lst = []
    p_text_lst = []

    while True:
        data = wf.readframes(8196)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            text_lst.append(rec.Result())
        else:
            p_text_lst.append(rec.PartialResult())
      
    text_lst.append(rec.FinalResult())
    wf.close()

    final_phrases = []
    for item in text_lst:
        try:
            jd = json.loads(item)
            if "text" in jd and jd["text"].strip():
                final_phrases.append(jd["text"].strip())
        except Exception:
            continue

    if final_phrases:
        txt_str = " ".join(final_phrases)
    elif len(p_text_lst) != 0: 
        p_str = [json.loads(item).get('partial', '') for item in p_text_lst]
        txt_str = max(p_str, key=len) if p_str else ''
    else:
        txt_str = ''
    
    return txt_str


# LLM Interaction
def my_gpt(question):
    messages = [
        {
            "role": "system", 
            "content": (
                "You are a helpful, conversational AI assistant. Always reply in English. "
                "Keep your answers extremely brief, concise, and friendly (maximum 2 sentences). "
                "Optimize text for Text-to-Speech: do not use bullet points, markdown bolding, or special characters."
            )
        },
        {"role": "user", "content": question}
    ]
    response = global_llm.create_chat_completion(
        messages=messages,
        temperature=0.7,
        max_tokens=60
    )
    
    return response["choices"][0]["message"]["content"].strip()

# Main Loop
if __name__ == "__main__":
    try:
        while True:
            print("Options: (s) Start Recording | (quit) Exit: ")
            cmd = input().lower()
              
            if cmd == 'quit':
                if os.path.exists("temp_recorded_sound.wav"):
                    os.remove("temp_recorded_sound.wav")
                print("Exiting...")
                break
                
            elif cmd == 's':
                record_sound()
                text_from_voice = get_text_from_voice()
                print(f"{C_CYAN}You said: {text_from_voice}{C_RESET}")
                
                if text_from_voice.strip():
                    gpt_text = my_gpt(text_from_voice)
                    print(f"{C_GREEN}AI: {gpt_text}{C_RESET}")
                    run_piper(gpt_text)
                else:
                    print("No speech detected.")
            else:
                print("Invalid command. Use 's' or 'quit'.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")

