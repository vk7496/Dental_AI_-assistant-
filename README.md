# Dental_AI_-assistant-
# 🦷 Dental AI Diagnostic Assistant
### دستیار تشخیص دندانپزشکی | مساعد طب الأسنان بالذكاء الاصطناعي

A trilingual (Persian 🇮🇷 / English 🇬🇧 / Arabic 🇸🇦) AI-powered dental radiograph analysis tool built with Streamlit + Claude API.

---

## Features
- Upload dental X-rays (Periapical, Bitewing, Panoramic, CBCT)
- AI analysis via Claude claude-opus-4-5 vision
- Full clinical reports in Persian, English, or Arabic
- RTL/LTR layout switching
- Patient info input (age, chief complaint)
- Copy report to clipboard

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Usage
1. Enter your Anthropic API key in the sidebar (get one at console.anthropic.com)
2. Select language
3. Upload a radiograph image
4. Fill in patient details
5. Click "Analyze with AI"
6. Review and copy the clinical report

## Stack
- **Frontend**: Streamlit
- **AI**: Anthropic Claude claude-opus-4-5 (vision)
- **Languages**: Python 3.10+
- **Fonts**: Vazirmatn (RTL support)

## Disclaimer
This tool is for clinical decision support only. It does not replace examination by a licensed dental professional.
