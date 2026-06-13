import streamlit as st
import time
import os
from utils.utils import inject_custom_css, export_conversation_txt, export_conversation_pdf
from services.deepgram_service import STTService
from services.llm_service import LLMService
from services.tts_service import TTSService

st.set_page_config(page_title="VoiceFlow AI", page_icon="🎙️", layout="wide")

# Initialize state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "stats" not in st.session_state:
    st.session_state.stats = {"conversations": 0, "messages": 0, "audio_processed": 0, "response_times": []}
if "stt_service" not in st.session_state:
    st.session_state.stt_service = STTService()
if "llm_service" not in st.session_state:
    st.session_state.llm_service = LLMService()
if "tts_service" not in st.session_state:
    st.session_state.tts_service = TTSService()

inject_custom_css()

# Header & Hero
st.markdown("""
<div class="hero-container">
    <div class="hero-title">VoiceFlow <span class="accent-text">AI</span></div>
    <div class="hero-subtitle">Real-Time Speech Recognition, Local LLM Reasoning, Natural Voice Responses.</div>
</div>
""", unsafe_allow_html=True)

# Controls
st.sidebar.header("⚙️ Configuration")

selected_model = st.sidebar.selectbox("LLM Model", st.session_state.llm_service.available_models)
personality = st.sidebar.selectbox("AI Personality", [
    "General Assistant", "Technical Expert", "Interview Coach", "Career Mentor", "Teacher", "Research Assistant"
])
explanation = st.sidebar.selectbox("Explanation Mode", ["Simple", "Detailed", "Technical", "Interview Style"])
voice_selection = st.sidebar.selectbox("Voice Selection", ["Female Voice", "Male Voice", "Fast Voice", "Natural Voice"])
language = st.sidebar.selectbox("Language Support", ["English", "Hindi", "Telugu"])

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🎤 Voice Interaction")
    audio_bytes = st.audio_input("Record your message")

    if audio_bytes is not None:
        st.session_state.stats["audio_processed"] += 1
        st.session_state.stats["conversations"] += 1
        
        with st.spinner("Transcribing..."):
            transcript, stt_latency, conf, stt_engine = st.session_state.stt_service.transcribe_audio_bytes(audio_bytes.getvalue(), language)
            
        if transcript:
            st.markdown(f"**You:** {transcript}")
            st.session_state.messages.append({"role": "user", "content": transcript})
            st.session_state.stats["messages"] += 1
            
            with st.spinner("AI is thinking..."):
                ai_response, llm_latency = st.session_state.llm_service.generate_response(
                    transcript, st.session_state.messages[:-1], selected_model, personality, explanation
                )
                
            if ai_response:
                st.markdown(f"**VoiceFlow AI:** {ai_response}")
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.stats["messages"] += 1
                
                with st.spinner("Generating voice..."):
                    audio_path, tts_latency, tts_engine = st.session_state.tts_service.generate_audio(ai_response, voice_selection)
                
                if audio_path:
                    st.audio(audio_path, format="audio/wav", autoplay=True)
                    with open(audio_path, "rb") as f:
                        st.download_button("Download Audio Response", f, file_name="response.wav", mime="audio/wav")
                    
                # Update Analytics
                total_latency = stt_latency + llm_latency + tts_latency
                st.session_state.stats["response_times"].append(total_latency)
                st.session_state.current_analytics = {
                    "STT": stt_latency, "LLM": llm_latency, "TTS": tts_latency, "Total": total_latency,
                    "STT_Engine": stt_engine, "TTS_Engine": tts_engine
                }
            else:
                st.warning("Failed to generate AI response.")
        else:
            st.warning("Could not transcribe audio. Please try again.")
            
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📝 History & Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["History", "Health & Analytics", "Statistics"])
    
    with tab1:
        if st.session_state.messages:
            for msg in st.session_state.messages:
                rc = "chat-user" if msg["role"] == "user" else "chat-assistant"
                name = "You" if msg["role"] == "user" else "VoiceFlow AI"
                st.markdown(f'<div class="chat-message {rc}"><strong>{name}:</strong><br/>{msg["content"]}</div>', unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                txt_export = export_conversation_txt(st.session_state.messages)
                st.download_button("Export TXT", txt_export, file_name="conversation.txt")
            with col_b:
                pdf_path = export_conversation_pdf(st.session_state.messages)
                with open(pdf_path, "rb") as f:
                    st.download_button("Export PDF", f.read(), file_name="conversation.pdf", mime="application/pdf")
            
            if st.button("Clear Conversation"):
                st.session_state.messages = []
                st.rerun()
        else:
            st.info("Start speaking to see history here.")

    with tab2:
        st.write("### System Health")
        stt = st.session_state.stt_service
        st.write(f"- Deepgram: {'✅' if stt.deepgram_available else '❌'}")
        st.write(f"- Faster-Whisper: {'✅' if stt.whisper_available else '❌'}")
        st.write(f"- Ollama: {'✅' if len(st.session_state.llm_service.available_models)>0 else '❌'}")
        tts = st.session_state.tts_service
        st.write(f"- Piper TTS: {'✅' if tts.piper_available else '❌'}")
        st.write(f"- Pyttsx3: {'✅' if tts.pyttsx3_available else '❌'}")
        st.write("- Microphone: ✅")
        
        st.write("### Last Response Analytics")
        if hasattr(st.session_state, "current_analytics"):
            a = st.session_state.current_analytics
            st.write(f"STT Latency ({a.get('STT_Engine', 'Unknown')}): {a['STT']:.2f}s")
            st.write(f"LLM Latency: {a['LLM']:.2f}s")
            st.write(f"TTS Latency ({a.get('TTS_Engine', 'Unknown')}): {a['TTS']:.2f}s")
            st.write(f"**Total Time: {a['Total']:.2f}s**")
        else:
            st.write("No responses yet.")

    with tab3:
        st.write("### Session Statistics")
        st.write(f"Total Conversations: {st.session_state.stats['conversations']}")
        st.write(f"Total Messages: {st.session_state.stats['messages']}")
        st.write(f"Total Audio Processed: {st.session_state.stats['audio_processed']}")
        rts = st.session_state.stats["response_times"]
        avg_rt = sum(rts)/len(rts) if rts else 0.0
        st.write(f"Average Response Time: {avg_rt:.2f}s")
        
    st.markdown('</div>', unsafe_allow_html=True)
