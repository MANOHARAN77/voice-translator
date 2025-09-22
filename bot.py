import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import tempfile

# Page Config
st.set_page_config(page_title="🌐 Voice Translator Bot", page_icon="🎤", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
    }
    .title {
        font-size: 36px !important;
        color: #2c3e50;
        text-align: center;
        font-weight: bold;
    }
    .subtitle {
        font-size: 18px !important;
        color: #34495e;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 8px 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title'>🌐 Voice Translator Bot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Translate your text or speech into another language with real-time voice output!</p>", unsafe_allow_html=True)

# Languages with flags and full names
languages = {
    "🇬🇧 English": "en",
    "🇫🇷 French": "fr",
    "🇮🇳 Hindi": "hi",
    "🇮🇳 Tamil": "ta",
    "🇮🇳 Telugu": "te",
    "🇮🇳 Kannada": "kn",
    "🇮🇳 Malayalam": "ml",
    "🇮🇳 Marathi": "mr",
    "🇧🇩 Bengali": "bn",
    "🇪🇸 Spanish": "es",
    "🇩🇪 German": "de",
    "🇨🇳 Chinese (Simplified)": "zh-CN",
    "🇯🇵 Japanese": "ja"
}

# Sidebar Settings
st.sidebar.header("⚙️ Settings")
source_lang_name = st.sidebar.selectbox("Select Source Language", list(languages.keys()))
target_lang_name = st.sidebar.selectbox("Select Target Language", list(languages.keys()))
source_lang = languages[source_lang_name]
target_lang = languages[target_lang_name]

# Layout: Two columns
col1, col2 = st.columns(2)

# ---- Column 1: Text Translator ----
with col1:
    st.subheader("✍️ Text Translator")
    text_input = st.text_area("Enter text to translate:")

    if st.button("🔄 Translate Text"):
        if text_input.strip() != "":
            translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text_input)
            st.success(f"✅ Translated Text: {translated}")

            # Convert to speech
            tts = gTTS(translated, lang=target_lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                st.audio(tmp.name, format="audio/mp3")

# ---- Column 2: Speech Translator ----
with col2:
    st.subheader("🎤 Speech Translator")
    if st.button("🎙️ Record & Translate"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Listening... please speak now.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            spoken_text = recognizer.recognize_google(audio, language=source_lang)
            st.success(f"🗣️ You said: {spoken_text}")

            # Translate speech
            translated = GoogleTranslator(source=source_lang, target=target_lang).translate(spoken_text)
            st.success(f"🌍 Translated: {translated}")

            # Speak translated text
            tts = gTTS(translated, lang=target_lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                st.audio(tmp.name, format="audio/mp3")

        except sr.UnknownValueError:
            st.error("❌ Sorry, I could not understand audio.")
        except sr.RequestError:
            st.error("❌ Could not connect to Google Speech Recognition service.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:grey;'>🚀 Built with Streamlit | GoogleTranslator | gTTS | SpeechRecognition</p>", unsafe_allow_html=True)
