import streamlit as st
import tempfile
from fpdf import FPDF

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #FAFAFA;
            color: #111827;
        }

        .hero-container {
            text-align: center;
            padding: 4rem 2rem;
            margin-bottom: 2rem;
            background: #FFFFFF;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #F3F4F6;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            color: #111827;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }
        .hero-subtitle {
            font-size: 1.125rem;
            font-weight: 400;
            color: #4B5563;
            max-width: 600px;
            margin: 0 auto;
        }
        .accent-text {
            color: #FF6B35;
        }

        .feature-card {
            background: #FFFFFF;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            border: 1px solid #E5E7EB;
        }
        
        .chat-message {
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            line-height: 1.5;
            font-size: 1rem;
        }
        .chat-user {
            background-color: #F3F4F6;
            color: #1F2937;
            border: 1px solid #E5E7EB;
        }
        .chat-assistant {
            background-color: #FFF6F3;
            color: #1F2937;
            border: 1px solid #FFEDe6;
        }
        
        .stButton>button {
            background-color: #FF6B35 !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button:hover {
            background-color: #e55a2b !important;
        }
        
        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #FF6B35;
        }
        .metric-label {
            font-size: 0.875rem;
            color: #6B7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Custom inputs */
        [data-testid="stAudioInput"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #E5E7EB;
            padding: 1rem;
            background: #FFFFFF;
        }
        </style>
    """, unsafe_allow_html=True)

def export_conversation_txt(messages):
    content = "VoiceFlow AI Conversation Export\n\n"
    for msg in messages:
        sender = "You" if msg["role"] == "user" else "VoiceFlow AI"
        content += f"{sender}:\n{msg['content']}\n\n"
    return content

def export_conversation_pdf(messages):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, txt="VoiceFlow AI Conversation Export", ln=True, align="C")
    pdf.ln(10)
    for msg in messages:
        sender = "You" if msg["role"] == "user" else "VoiceFlow AI"
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(0, 10, txt=f"{sender}:", ln=True)
        pdf.set_font("Helvetica", size=11)
        # Using multi_cell for text wrapping
        pdf.multi_cell(0, 10, txt=msg['content'])
        pdf.ln(5)
    
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp.close()
    pdf.output(temp.name)
    return temp.name
