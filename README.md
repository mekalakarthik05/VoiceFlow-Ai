# 🎙️ VoiceFlow AI
<div align="center">

# Real-Time Conversational AI Voice Assistant

### Speech-to-Text • Local LLMs • Text-to-Speech • Conversation Memory

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge)
![Deepgram](https://img.shields.io/badge/Deepgram-FF6B35?style=for-the-badge)
![Piper](https://img.shields.io/badge/Piper_TTS-2E8B57?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

### 🧠 Speech → Intelligence → Voice

*A production-grade AI voice assistant combining Deepgram STT, Ollama LLMs, and Piper TTS for natural real-time conversations.*

</div>

---

# 🌟 Overview

VoiceFlow AI is an end-to-end Conversational AI system that enables users to interact with AI entirely through voice.

The application captures speech, transcribes it using Deepgram, processes it through local Large Language Models running on Ollama, and generates natural voice responses using Piper Text-to-Speech.

Unlike traditional cloud-only assistants, VoiceFlow AI combines local AI inference, privacy-first design, modular architecture, fallback mechanisms, and a modern SaaS-style interface.

---

# 🎯 Key Highlights

- 🎤 Real-Time Speech Recognition
- 🧠 Local LLM Inference using Ollama
- 🔊 Natural Voice Responses using Piper TTS
- 💾 Multi-Turn Conversation Memory
- ⚡ Low-Latency AI Pipeline
- 🛡 Robust Error Handling & Fallbacks
- 📊 System Health Monitoring
- 🧪 Automated Validation Pipeline
- 🏗 Modular Service-Oriented Architecture
- 🎨 Modern Streamlit SaaS Interface

---

# 🎥 Demo

[Open Post](https://www.linkedin.com/posts/karthik-mekala-k05_artificialintelligence-ai-generativeai-ugcPost-7471949627089616896-_ZeX/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEVTF0wB3qXhefPbOttnaqoVeYZck53kUCQ)

# 📸 Screenshots

| Main Dashboard | Language Support |
|----------------|------------------|
| ![](assets/screenshots/main-dashboard.png) | ![](assets/screenshots/language-support.png) |

| Conversation Memory | Health Monitoring |
|---------------------|-------------------|
| ![](assets/screenshots/history.png) | ![](assets/screenshots/health-dashboard.png) |

| Analytics Dashboard | Multi-Model Configuration | Personality Engine | 
|---------------------|---------------------------|--------------------|
| ![](assets/screenshots/analytics.png) | ![](assets/screenshots/configuration.png) | ![](assets/screenshots/personality.png) |


| Voice Interaction Pipeline | 
|----------------------------|
| ![](assets/screenshots/voice-interaction.png) | 

---

# 🚀 Features

| Category | Features |
|-----------|-----------|
| Speech Recognition | Deepgram STT, Faster-Whisper Fallback |
| AI Reasoning | Ollama Integration, Qwen3, Llama Models |
| Text-to-Speech | Piper TTS, pyttsx3 Fallback |
| Memory | Multi-Turn Context Retention |
| UI | Streamlit SaaS Dashboard |
| Monitoring | Health Dashboard, Validation Pipeline |
| Reliability | Automatic Fallback Architecture |
| Export | Conversation Export |
| Testing | Unit Testing + Pipeline Validation |

---

# 📊 System Capabilities

| Capability | Supported |
|------------|------------|
| Speech Recognition | ✅ |
| Multi-Turn Conversations | ✅ |
| Local AI Inference | ✅ |
| Text-to-Speech | ✅ |
| Voice Download | ✅ |
| PDF Export | ✅ |
| TXT Export | ✅ |
| Multi-Model Support | ✅ |
| Personality Switching | ✅ |
| Multi-Language Support | ✅ |
| Health Monitoring | ✅ |
| Analytics Dashboard | ✅ |
| Session Statistics | ✅ |

---

```mermaid
flowchart LR

A[User Voice]

--> B[Deepgram STT]

--> C[Conversation Memory]

--> D[LLM Router]

D --> E[Llama 3.2]
D --> F[Qwen3]

E --> G[Response Generator]
F --> G

G --> H[Personality Engine]

H --> I[Explanation Mode]

I --> J[Piper TTS]

J --> K[Audio Response]

K --> L[Analytics Dashboard]

L --> M[Export Services]
```

---


# 🏗 High-Level Architecture

```mermaid
flowchart LR

User[🎤 User Voice]
--> STT[Deepgram STT]

STT
--> Memory[Conversation Memory]

Memory
--> LLM[Ollama Local LLM]

LLM
--> TTS[Piper TTS]

TTS
--> Output[🔊 Voice Response]
```

---

# 🧩 Component Architecture

```mermaid
flowchart TB

UI[Streamlit Frontend]

STT[Deepgram Service]
LLM[LLM Service]
TTS[TTS Service]

UI --> STT
STT --> LLM
LLM --> TTS
TTS --> UI
```

---

# 🔄 Sequence Diagram

```mermaid
sequenceDiagram

participant User
participant STT
participant LLM
participant TTS

User->>STT: Voice Input
STT->>LLM: Transcript
LLM->>TTS: AI Response
TTS->>User: Audio Output
```

---

# ⚙ End-to-End Pipeline

```mermaid
flowchart TD

A[Voice Input]
--> B[Deepgram STT]

B
--> C[Conversation Memory]

C
--> D[Ollama LLM]

D
--> E[Piper TTS]

E
--> F[Voice Response]
```

---

# 📂 Repository Structure

```text
voiceflow-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
│
├── services/
│   ├── deepgram_service.py
│   ├── llm_service.py
│   └── tts_service.py
│
├── utils/
│   └── utils.py
│
├── scripts/
│   └── validate_pipeline.py
│
├── tests/
│   ├── test_deepgram.py
│   ├── test_llm.py
│   └── test_tts.py
│
├── docs/
│
└── assets/
```

---

# 🛠 Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | Streamlit |
| Language | Python |
| Speech-to-Text | Deepgram |
| Fallback STT | Faster Whisper |
| LLM Runtime | Ollama |
| Models | Qwen3:4B, Llama3.2 |
| Text-to-Speech | Piper |
| Fallback TTS | pyttsx3 |
| Testing | unittest |
| Documentation | Markdown + Mermaid |

---

# 📊 System Metrics

| Metric | Capability |
|----------|------------|
| Real-Time Voice Input | ✅ |
| Multi-Turn Conversations | ✅ |
| Local AI Inference | ✅ |
| Offline Voice Generation | ✅ |
| Service Health Monitoring | ✅ |
| Automated Validation | ✅ |
| Fallback Recovery | ✅ |

---

# 🔒 Reliability Architecture

```mermaid
flowchart TD

Deepgram
--> Success

Deepgram
--> WhisperFallback

Piper
--> VoiceOutput

Piper
--> pyttsx3Fallback
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/mekalakarthik05/VoiceFlow-Ai.git
cd VoiceFlow-Ai
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Configuration

Create:

```env
DEEPGRAM_API_KEY=your_api_key_here
```

---

# 🤖 Ollama Setup

Install Ollama and pull a model:

```bash
ollama pull qwen3:4b
```

or

```bash
ollama pull llama3.2:3b
```

---

# ▶ Running the Application

```bash
streamlit run app.py
```

---

# 🧪 Testing

Run Unit Tests

```bash
python -m unittest discover tests/
```

Validate Full Pipeline

```bash
python scripts/validate_pipeline.py
```

---

# 💡 Technical Challenges Solved

### Deepgram SDK Migration

Resolved compatibility issues introduced by newer Deepgram SDK versions.

### Audio Pipeline Engineering

Implemented proper WAV generation and audio channel configuration for Piper TTS.

### Event Loop Management

Resolved Streamlit and asynchronous service integration issues.

### Fallback Architecture

Implemented recovery mechanisms:

- Deepgram → Faster Whisper
- Piper → pyttsx3

---

# 📈 Engineering Achievements

- Built complete Speech-to-Speech AI pipeline
- Integrated 3 independent AI systems
- Implemented modular architecture
- Added automated validation framework
- Developed production-ready error handling
- Designed recruiter-grade portfolio project

---

# Author
Karthik Mekala
---

If you found this project useful:

⭐ Star the Repository

🍴 Fork the Repository

📢 Share Feedback

---

# 📄 License

This project is licensed under the MIT License.
