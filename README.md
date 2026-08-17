# Local Voice-to-Voice AI Assistant

A privacy-focused, 100% offline voice assistant that integrates a Large Language Model (LLM), Speech-to-Text (STT), and Text-to-Speech (TTS) into a seamless, real-time execution loop.

---

Choose language / Wybierz język:

* [English Version](#english-version)
* [Wersja Polska](#wersja-polska)

---

## English Version

### Video Demonstration

https://github.com/user-attachments/assets/4a68d230-8b4e-470f-939e-20fa91a97646

### Features
* Privacy First: All data processing occurs strictly on your local machine.
* Low Latency STT: Powered by Vosk for real-time speech recognition.
* Open Source LLM Integration: Powered by llama-cpp-python supporting GGUF models.
* High-Quality TTS: Powered by Piper TTS (ONNX format) for natural voice generation.
* Fail-Fast Validation: Smart environment check aggregates any missing models into a single, clean error message upon startup.

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Wilchelm/offline-speech-to-speech-ai.git
   cd offline-speech-to-speech-ai
   ```

2. **Run the installation script**
   This script handles system dependencies and sets up an isolated Python environment inside the `env/` directory.
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Download Required AI Models**
   Due to file size restrictions, models are excluded from Git tracking. You must place them in the `models/` folder:
   * **STT (Vosk):** Download and extract the [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models) model into `models/`.
   * **TTS (Piper):** Download `en_US-amy-medium.onnx` and its `.json` config from [Piper Voices](https://huggingface.co/rhasspy/piper-voices) and place in `models/`.
   * **LLM (Llama):** Download any `.gguf` model from Hugging Face and name it `llm_model.gguf` inside the `models/` folder.

4. **Run the application**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

### License & Third-Party Components

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. The full legal text is available in the LICENSE file in this repository.


### Third-Party Components

This project orchestrates third-party open-source components. The NonCommercial restriction applies strictly to this orchestration code.

* **Vosk API & Models:** Apache 2.0 License
* **llama-cpp-python:** MIT License
* **Piper TTS (Amy Voice):** MIT License
* **PyAudio:** MIT License

---

## Wersja Polska

### Demonstracja Wideo

> ***Uwaga:** Prezentacja wideo jest w języku angielskim.*

https://github.com/user-attachments/assets/4a68d230-8b4e-470f-939e-20fa91a97646

### Funkcje
* Prywatność: Wszystkie dane przetwarzane są lokalnie.
* Niskie opóźnienia STT: Wykorzystanie Vosk do rozpoznawania mowy w czasie rzeczywistym.
* Integracja LLM: Wsparcie dla modeli GGUF przez llama-cpp-python.
* Wysoka jakość TTS: Piper TTS (format ONNX) dla naturalnej syntezy mowy.
* Walidacja środowiska: Automatyczne sprawdzanie obecności modeli przy starcie.

### Instalacja i Konfiguracja

1. **Sklonuj repozytorium**
   ```bash
   git clone https://github.com/Wilchelm/offline-speech-to-speech-ai.git
   cd offline-speech-to-speech-ai
   ```

2. **Uruchom skrypt instalacyjny**
   Skrypt instaluje zależności systemowe i tworzy izolowane środowisko Python w folderze `env/`.
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Pobierz wymagane modele**
   Ze względu na rozmiar, modele nie są dołączone do repozytorium. Musisz je umieścić w folderze `models/`:
   * **STT (Vosk):** Pobierz i wypakuj model [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models) do folderu `models/`.
   * **TTS (Piper):** Pobierz plik `en_US-amy-medium.onnx` oraz plik `.json` z [Piper Voices](https://huggingface.co/rhasspy/piper-voices) i umieść w `models/`.
   * **LLM (Llama):** Pobierz dowolny model `.gguf` z Hugging Face i nazwij go `llm_model.gguf` w folderze `models/`.

4. **Uruchom aplikację**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

### Licencja i Komponenty Zewnętrzne

Ten projekt jest objęty licencją **GNU Affero General Public License v3.0 (AGPL-3.0)**. Pełny tekst prawny znajduje się w pliku LICENSE w tym repozytorium.

### Komponenty osób trzecich

Projekt integruje komponenty open-source. Ograniczenie "Non-Commercial" dotyczy wyłącznie kodu sterującego tym projektem.

* **Vosk API & Models:** Licencja Apache 2.0
* **llama-cpp-python:** Licencja MIT
* **Piper TTS (Amy Voice):** Licencja MIT
* **PyAudio:** Licencja MIT
