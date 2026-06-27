import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Page configuration
st.set_page_config(
    page_title="مساعد المتجر الذكي",
    page_icon="🛍️",
    layout="wide"
)

# Custom CSS for better Arabic styling
st.markdown("""
    <style>
        .stChatMessage {
            direction: rtl !important;
            text-align: right !important;
        }
        .st-chat-message {
            direction: rtl !important;
        }
        .st-emotion-cache-1rsy6r8 {
            direction: rtl !important;
        }
        h1, h2, h3, p, div {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar with shop info
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3105/3105538.png", width=80)
    st.title("🛍️ المتجر الذكي")
    st.markdown("---")
    st.markdown("### 📋 معلومات المتجر")
    st.info("""
    **🏪 اسم المتجر:** الذكاء للتسوق  
    **📞 رقم الهاتف:** 800-1234  
    **📍 العنوان:** دبي، الإمارات العربية المتحدة  
    **🕐 ساعات العمل:** 9:00 صباحاً - 10:00 مساءً
    """)

    st.markdown("---")
    st.markdown("### 📦 سياسات المتجر")
    st.success("""
    ✅ شحن مجاني للطلبات فوق 200 درهم  
    ✅ استرجاع خلال 14 يوماً  
    ✅ دفع عند الاستلام  
    ✅ ضمان على جميع المنتجات
    """)

    st.markdown("---")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

    st.caption("🤖 مدعوم من Groq AI")

# Main title
st.title("🛍️ مرحباً بك في المتجر الذكي!")
st.subheader("كيف يمكنني مساعدتك اليوم؟")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            try:
                system_prompt = """
                أنت مساعد خدمة عملاء ذكي لمتجر إلكتروني في الإمارات العربية المتحدة.
                
                معلومات مهمة عن المتجر:
                - اسم المتجر: الذكاء للتسوق
                - الهاتف: 800-1234
                - العنوان: دبي
                - ساعات العمل: 9 صباحاً - 10 مساءً
                - سياسة الاسترجاع: 14 يوماً
                - الشحن: مجاني للطلبات فوق 200 درهم
                - الدفع: عند الاستلام
                - جميع المنتجات عليها ضمان
                
                قواعد الرد:
                1. تحدث باللغة العربية الفصحى أو العامية الخليجية
                2. كن مهذباً ومحترفاً
                3. قدم معلومات دقيقة عن المتجر
                4. إذا لم تعرف الإجابة، قل: "سأحولك إلى أحد المندوبين للمساعدة"
                5. كن ودوداً ومفيداً
                6. استخدم الإيموجي المناسب في الردود
                """

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    temperature=0.7,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ]
                )

                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply})

            except Exception as e:
                st.error(f"حدث خطأ: {e}")
