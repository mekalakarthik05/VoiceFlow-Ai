# VoiceFlow AI — Career Package

## 1. ATS Resume Description
**Software Engineer | AI & Voice Technologies**
Architected and developed VoiceFlow AI, a real-time conversational voice assistant utilizing a modern Python stack. Integrated Deepgram's Speech-to-Text (STT) and OpenAI's GPT and Text-to-Speech (TTS) APIs to deliver seamless, natural voice interactions. Designed a responsive, premium SaaS-style interface using Streamlit, featuring custom CSS and stateful conversation memory. Engineered modular service components ensuring high maintainability, robust error handling, and scalable AI service integrations.

## 2. Resume Bullet Points
- **Architected a real-time voice assistant** using Streamlit, Python, Deepgram STT, and OpenAI GPT/TTS, enabling zero-latency conversational workflows.
- **Engineered modular AI service integrations**, wrapping external APIs into isolated, test-driven Python services for improved maintainability.
- **Designed a custom state-management system** using Streamlit's session state to maintain conversation history and provide context-aware LLM responses.
- **Implemented a premium UI/UX** with custom injected CSS, featuring modern typography, responsive layouts, and cross-browser audio playback support.

## 3. Interview Explanation
"In my recent project, VoiceFlow AI, I wanted to build a ChatGPT Voice Mode-like experience. The core challenge was orchestrating three distinct AI services seamlessly: capturing user audio, transcribing it with Deepgram for speed, generating a contextual response with OpenAI, and synthesizing the voice back to the user. I structured the project into modular Python services—this allowed me to independently unit test the Deepgram, LLM, and TTS modules. For the frontend, I used Streamlit with custom CSS to create a polished, SaaS-style interface while managing the complex asynchronous state of the conversation."

## 4. Architecture Explanation
"The architecture follows a strict decoupled service pattern. The frontend is built with Streamlit, handling UI rendering and browser audio capture. When audio is received, it passes through three sequential service layers:
1. **DeepgramService**: Processes the raw audio bytes into a transcript.
2. **LLMService**: Takes the transcript and the session's conversation history to generate a text response via GPT-3.5.
3. **TTSService**: Converts the AI's text response into an MP3 file using OpenAI's TTS API.
This modularity ensures that if we want to swap out the LLM or STT provider in the future, we only need to modify a single service class without touching the core application logic."

## 5. Technical Story for Recruiters
"I recently built a real-time voice AI assistant from scratch. I noticed that many AI apps struggle with latency and messy codebases when chaining multiple APIs. To solve this, I designed a pipeline that streams user audio directly to Deepgram, which is incredibly fast for transcription, and then routes the text to OpenAI for processing and voice synthesis. I enforced strict separation of concerns by building independent modules for each API and wrote unit tests for all of them. The result was a highly responsive, production-ready application with a beautiful, custom-styled interface that users can interact with naturally using their voice."
