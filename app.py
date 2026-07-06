import streamlit as st
import anthropic
import base64
from PIL import Image
import io

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dental AI | دستیار دندانپزشکی | مساعد طب الأسنان",
    page_icon="🦷",
    layout="centered"
)

# ─── Translations ────────────────────────────────────────────────────────────────
T = {
    "fa": {
        "dir": "rtl",
        "app_title": "دستیار تشخیص دندانپزشکی هوشمند",
        "app_sub": "تحلیل رادیوگرافی با هوش مصنوعی",
        "upload_label": "رادیوگرافی را بارگذاری کنید",
        "upload_help": "فرمت‌های JPG، PNG، WEBP پشتیبانی می‌شوند",
        "xray_type": "نوع رادیوگرافی",
        "xray_options": ["پری‌اپیکال", "بایت‌وینگ", "پانورامیک", "CBCT"],
        "patient_age": "سن بیمار",
        "age_placeholder": "مثال: ۳۵",
        "chief_complaint": "شکایت اصلی بیمار",
        "complaint_placeholder": "درد، حساسیت، تورم...",
        "analyze_btn": "🔍 تحلیل با هوش مصنوعی",
        "analyzing": "در حال تحلیل تصویر...",
        "result_title": "گزارش تشخیص",
        "copy_btn": "📋 کپی گزارش",
        "new_btn": "🔄 رادیوگرافی جدید",
        "error_upload": "لطفاً ابتدا یک تصویر بارگذاری کنید.",
        "api_error": "خطا در ارتباط با API. کلید API را بررسی کنید.",
        "api_key_label": "کلید API آنتروپیک",
        "api_key_help": "از console.anthropic.com دریافت کنید",
        "lang_label": "زبان / Language / اللغة",
        "system_prompt": """شما یک دندانپزشک متخصص رادیولوژی دهان و دندان هستید. 
رادیوگرافی دندانی ارائه‌شده را به دقت بررسی کنید و یک گزارش بالینی کامل به زبان فارسی ارائه دهید.

گزارش شما باید شامل موارد زیر باشد:
١. **یافته‌های اصلی**: ضایعات پوسیدگی، بیماری پریودنتال، تغییرات استخوانی
٢. **دندان‌های درگیر**: شماره و موقعیت دندان‌های مبتلا
٣. **شدت**: خفیف / متوسط / شدید
٤. **تشخیص احتمالی**: افتراقی در صورت لزوم
٥. **توصیه درمانی**: اقدامات پیشنهادی اولویت‌بندی شده
٦. **پیگیری**: زمان‌بندی کنترل بعدی

در صورت وجود محدودیت در تفسیر تصویر، آن را صادقانه ذکر کنید.
این گزارش صرفاً جنبه کمک تشخیصی دارد و جایگزین معاینه بالینی نمی‌شود."""
    },
    "en": {
        "dir": "ltr",
        "app_title": "Dental AI Diagnostic Assistant",
        "app_sub": "AI-powered radiograph analysis for clinicians",
        "upload_label": "Upload radiograph",
        "upload_help": "JPG, PNG, WEBP formats supported",
        "xray_type": "Radiograph type",
        "xray_options": ["Periapical", "Bitewing", "Panoramic", "CBCT"],
        "patient_age": "Patient age",
        "age_placeholder": "e.g. 35",
        "chief_complaint": "Chief complaint",
        "complaint_placeholder": "Pain, sensitivity, swelling...",
        "analyze_btn": "🔍 Analyze with AI",
        "analyzing": "Analyzing radiograph...",
        "result_title": "Diagnostic Report",
        "copy_btn": "📋 Copy report",
        "new_btn": "🔄 New radiograph",
        "error_upload": "Please upload a radiograph first.",
        "api_error": "API connection error. Please check your API key.",
        "api_key_label": "Anthropic API Key",
        "api_key_help": "Get it from console.anthropic.com",
        "lang_label": "Language / زبان / اللغة",
        "system_prompt": """You are an expert oral and maxillofacial radiologist. 
Carefully analyze the provided dental radiograph and produce a structured clinical report in English.

Your report must include:
1. **Key Findings**: Carious lesions, periodontal disease, bone changes, pathologies
2. **Teeth Involved**: FDI/Universal notation of affected teeth
3. **Severity**: Mild / Moderate / Severe
4. **Differential Diagnosis**: If applicable
5. **Treatment Recommendations**: Prioritized list of suggested interventions
6. **Follow-up**: Recommended recall interval

If image quality limits your interpretation, note this honestly.
This report is a clinical decision support tool and does not replace clinical examination."""
    },
    "ar": {
        "dir": "rtl",
        "app_title": "مساعد تشخيص طب الأسنان بالذكاء الاصطناعي",
        "app_sub": "تحليل الأشعة السينية للأسنان بالذكاء الاصطناعي",
        "upload_label": "رفع الصورة الشعاعية",
        "upload_help": "تنسيقات JPG و PNG و WEBP مدعومة",
        "xray_type": "نوع الصورة الشعاعية",
        "xray_options": ["البيري أبيكال", "عض الجناح", "البانورامية", "CBCT"],
        "patient_age": "عمر المريض",
        "age_placeholder": "مثال: ٣٥",
        "chief_complaint": "الشكوى الرئيسية",
        "complaint_placeholder": "ألم، حساسية، تورم...",
        "analyze_btn": "🔍 تحليل بالذكاء الاصطناعي",
        "analyzing": "جارٍ تحليل الصورة الشعاعية...",
        "result_title": "تقرير التشخيص",
        "copy_btn": "📋 نسخ التقرير",
        "new_btn": "🔄 صورة شعاعية جديدة",
        "error_upload": "يرجى رفع صورة شعاعية أولاً.",
        "api_error": "خطأ في الاتصال بـ API. تحقق من مفتاح API.",
        "api_key_label": "مفتاح Anthropic API",
        "api_key_help": "احصل عليه من console.anthropic.com",
        "lang_label": "اللغة / Language / زبان",
        "system_prompt": """أنت طبيب أسنان متخصص في أشعة الفم والفكين.
قم بتحليل الصورة الشعاعية للأسنان المقدمة بعناية وأنتج تقريرًا سريريًا منظمًا باللغة العربية.

يجب أن يتضمن تقريرك:
١. **النتائج الرئيسية**: آفات التسوس، أمراض اللثة، تغيرات العظام
٢. **الأسنان المصابة**: ترميز FDI للأسنان المتضررة
٣. **الخطورة**: خفيفة / متوسطة / شديدة
٤. **التشخيص التفريقي**: عند الاقتضاء
٥. **توصيات العلاج**: قائمة العلاجات المقترحة حسب الأولوية
٦. **المتابعة**: الفاصل الزمني الموصى به للمراجعة

إذا كانت جودة الصورة تحد من التفسير، أشر إلى ذلك بصدق.
هذا التقرير أداة دعم للقرار السريري ولا يحل محل الفحص السريري."""
    }
}

# ─── CSS Styling ─────────────────────────────────────────────────────────────────
def get_css(direction):
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700&display=swap');

    * {{ direction: {direction}; }}

    html, body, [class*="css"] {{
        font-family: 'Vazirmatn', 'Segoe UI', sans-serif !important;
    }}

    .main-header {{
        text-align: center;
        padding: 2rem 0 1rem;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }}

    .main-header h1 {{
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a2e;
        margin: 0;
    }}

    .main-header p {{
        color: #6b7280;
        font-size: 0.95rem;
        margin-top: 0.4rem;
    }}

    .report-box {{
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        direction: {direction};
    }}

    .report-box h3 {{
        color: #0369a1;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #bae6fd;
        padding-bottom: 0.5rem;
    }}

    .report-content {{
        color: #1e3a5f;
        line-height: 1.9;
        font-size: 0.95rem;
        white-space: pre-wrap;
    }}

    .stButton > button {{
        width: 100%;
        background: #0ea5e9;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 500;
        padding: 0.65rem 1rem;
        transition: background 0.2s;
    }}

    .stButton > button:hover {{
        background: #0284c7;
    }}

    .disclaimer {{
        font-size: 0.78rem;
        color: #9ca3af;
        text-align: center;
        margin-top: 1.5rem;
        border-top: 1px solid #f3f4f6;
        padding-top: 0.75rem;
    }}
</style>
"""

# ─── Helpers ─────────────────────────────────────────────────────────────────────
def image_to_base64(img_bytes):
    return base64.standard_b64encode(img_bytes).decode("utf-8")

def get_media_type(uploaded_file):
    ext = uploaded_file.name.lower().split(".")[-1]
    mapping = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    return mapping.get(ext, "image/jpeg")

def analyze_xray(api_key, img_b64, media_type, xray_type, patient_age, complaint, system_prompt, lang):
    client = anthropic.Anthropic(api_key=api_key)

    user_content = [
        {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": img_b64}
        },
        {
            "type": "text",
            "text": f"نوع رادیوگرافی / Radiograph type / نوع الصورة: {xray_type}\n"
                    f"سن بیمار / Patient age / عمر المريض: {patient_age or 'نامشخص / Unknown / غير معروف'}\n"
                    f"شکایت / Complaint / الشكوى: {complaint or '-'}\n\n"
                    "لطفاً گزارش کامل بالینی ارائه دهید. / Please provide a complete clinical report. / يرجى تقديم تقرير سريري كامل."
        }
    ]

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}]
    )
    return message.content[0].text

# ─── UI ──────────────────────────────────────────────────────────────────────────
def main():
    # Language selector (top, sidebar)
    lang_map = {"فارسی 🇮🇷": "fa", "English 🇬🇧": "en", "العربية 🇸🇦": "ar"}
    with st.sidebar:
        st.markdown("### 🌐 Language / زبان / اللغة")
        lang_choice = st.radio("", list(lang_map.keys()), index=0, label_visibility="collapsed")
        lang = lang_map[lang_choice]
        t = T[lang]

        st.divider()
        st.markdown(f"### 🔑 {t['api_key_label']}")
        api_key = st.text_input(
            t["api_key_label"],
            type="password",
            placeholder="sk-ant-...",
            help=t["api_key_help"],
            label_visibility="collapsed"
        )

    t = T[lang]
    direction = t["dir"]

    # Inject CSS
    st.markdown(get_css(direction), unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🦷 {t['app_title']}</h1>
        <p>{t['app_sub']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Upload
    uploaded = st.file_uploader(
        t["upload_label"],
        type=["jpg", "jpeg", "png", "webp"],
        help=t["upload_help"]
    )

    if uploaded:
        col1, col2 = st.columns([1, 1])
        with col1:
            img = Image.open(uploaded)
            st.image(img, use_container_width=True, caption=uploaded.name)

        with col2:
            xray_type = st.selectbox(t["xray_type"], t["xray_options"])
            patient_age = st.text_input(t["patient_age"], placeholder=t["age_placeholder"])
            complaint = st.text_area(t["chief_complaint"], placeholder=t["complaint_placeholder"], height=80)

            analyze_clicked = st.button(t["analyze_btn"], use_container_width=True)

        if analyze_clicked:
            if not api_key:
                st.error("⚠️ " + t["api_key_label"])
                return

            with st.spinner(t["analyzing"]):
                try:
                    uploaded.seek(0)
                    img_bytes = uploaded.read()
                    img_b64 = image_to_base64(img_bytes)
                    media_type = get_media_type(uploaded)

                    report = analyze_xray(
                        api_key, img_b64, media_type,
                        xray_type, patient_age, complaint,
                        t["system_prompt"], lang
                    )

                    st.session_state["report"] = report
                    st.session_state["report_lang"] = lang

                except anthropic.AuthenticationError:
                    st.error("❌ " + t["api_error"])
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    # Show report
    if "report" in st.session_state:
        report_text = st.session_state["report"]
        rep_lang = st.session_state.get("report_lang", "fa")
        rep_dir = T[rep_lang]["dir"]

        st.markdown(f"""
        <div class="report-box">
            <h3>🔬 {T[rep_lang]['result_title']}</h3>
            <div class="report-content">{report_text}</div>
        </div>
        """, unsafe_allow_html=True)

        col_c, col_r = st.columns(2)
        with col_c:
            if st.button(T[rep_lang]["copy_btn"]):
                st.code(report_text, language=None)
        with col_r:
            if st.button(T[rep_lang]["new_btn"]):
                del st.session_state["report"]
                st.rerun()

    # Disclaimer
    disc = {
        "fa": "⚠️ این گزارش صرفاً جنبه کمک تشخیصی دارد و جایگزین معاینه بالینی توسط دندانپزشک نمی‌شود.",
        "en": "⚠️ This report is a clinical decision-support tool and does not replace examination by a licensed dentist.",
        "ar": "⚠️ هذا التقرير أداة دعم سريري ولا يُعدّ بديلاً عن الفحص من قِبل طبيب أسنان مرخّص."
    }
    st.markdown(f'<div class="disclaimer">{disc.get(lang, disc["en"])}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
