import streamlit as st
import google.generativeai as genai
import os

# --- إعداد الصفحة ---
st.set_page_config(page_title="Honda AI", page_icon="🤖", layout="centered")

# --- التصميم ---
st.markdown("""
<style>
    .stChatMessage {text-align: right; direction: rtl;}
    p {text-align: right; direction: rtl;}
    .stTextInput > div > div > input {text-align: right; direction: rtl;}
</style>
""", unsafe_allow_html=True)

# --- العنوان ---
st.title("🤖 هوندا - مساعدك السحابي")
st.caption("موجود معاك على كل الأجهزة، مربوط بذكاء Gemini")

# --- إعداد المفاتيح ---
try:
    # محاولة جلب المفتاح من أسرار الموقع
    if "HONDA_API_KEY" in st.secrets:
        api_key = st.secrets["HONDA_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("⚠️ لم يتم العثور على المفتاح في Secrets. تأكد من إضافته باسم HONDA_API_KEY")
except Exception as e:
    st.error(f"مشكلة في إعداد المفتاح: {e}")

# --- ذاكرة الشات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- عرض الشات القديم ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- التفاعل ---
if prompt := st.chat_input("اطلب مني أي حاجة يا زعيم..."):
    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # تفكير هوندا
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # الأوامر الخاصة (التطوير الذاتي)
        if "طور نفسك" in prompt or "اكتب كود" in prompt:
            full_response = "جاري كتابة الكود الجديد لتطوير الموقع...\n"
            ai_prompt = f"أنت خبير Streamlit. المستخدم يريد: {prompt}. اكتب كود python كامل لملف app.py يحقق هذا."
            try:
                response = model.generate_content(ai_prompt)
                ai_text = response.text
                full_response += ai_text
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"خطأ في التطوير: {e}")
                message_placeholder.markdown("عقلي مشغول دلوقتي.")
        else:
            # دردشة عادية
            try:
                chat_prompt = f"أنت هوندا، مساعد شخصي مصري. المستخدم: {prompt}"
                response = model.generate_content(chat_prompt)
                full_response = response.text
                message_placeholder.markdown(full_response)
            except Exception as e:
                # كشف الخطأ الحقيقي هنا
                st.error(f"⚠️ تفاصيل الخطأ: {e}")
                full_response = "عندي مشكلة تقنية، بص على الرسالة الحمراء فوق."
                message_placeholder.markdown(full_response)
                
    st.session_state.messages.append({"role": "assistant", "content": full_response})
