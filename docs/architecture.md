# VoiceFlow AI Architecture

## System Overview
VoiceFlow AI is architected as a modular, state-driven speech-to-speech pipeline managed via Streamlit. The application decouples UI logic from external AI services, allowing seamless integration and interchangeable models. Audio input is captured asynchronously, routed through a sequence of modular pipelines (STT -> LLM -> TTS), and played back, while maintaining local conversation history.

## 1. High-Level Component Diagram
```mermaid
graph LR
    subgraph Frontend
        UI[app.py - Streamlit]
        Utils[utils.py - Formatting & Export]
    end

    subgraph Modular Services
        STT[services/deepgram_service.py]
        LLM[services/llm_service.py]
        TTS[services/tts_service.py]
    end

    subgraph External Engines
        DG[Deepgram API / Whisper fallback]
        OL[Ollama Local LLM Daemon]
        PT[Piper TTS Models / pyttsx3 fallback]
    end

    UI --> Utils
    UI --> STT
    UI --> LLM
    UI --> TTS
    
    STT --> DG
    LLM --> OL
    TTS --> PT
```

## 2. Sequence Diagram
```mermaid
sequenceDiagram
    actor User
    participant UI as app.py (Frontend)
    participant STT as STT Service
    participant LLM as LLM Service
    participant TTS as TTS Service

    User->>UI: Speaks (Audio Bytes)
    UI->>STT: Transcribe Audio Bytes
    STT-->>UI: Return Transcript (Text) + Latency Metrics
    UI->>LLM: Pass Transcript + Chat History + Personality Profile
    LLM-->>UI: Return Contextual Response (Text) + Latency Metrics
    UI->>TTS: Synthesize Audio from Response
    TTS-->>UI: Return Generated Audio (.wav) + Latency Metrics
    UI->>User: Play Response Audio
    UI->>UI: Append Response to Session State
```

## 3. Data Flow Diagram
```mermaid
flowchart TD
    A1(Raw Audio Bytes) --> STT{STT Service}
    STT --> |Extracts via Deepgram/Whisper| S1(String Transcript)
    S1 --> MEM[Conversation Session State]
    MEM --> PROMPT(System Prompt + History + User Message)
    PROMPT --> LLM[Local Ollama Inference]
    LLM --> |Generates via qwen/llama| S2(AI Response String)
    S2 --> TTS{TTS Service}
    TTS --> |Synthesizes via Piper/pyttsx3| A2(Generated Audio .wav)
```
