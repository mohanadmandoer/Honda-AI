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
st.caption("شغال بموديل gemini-pro المستقر ✅")

# --- إعداد المفاتيح ---
try:
    if "HONDA_API_KEY" in st.secrets:
        api_key = st.secrets["HONDA_API_KEY"]
        genai.configure(api_key=api_key)
        # هنا استخدمنا الموديل المضمون عشان نمنع الأخطاء
        model = genai.GenerativeModel('gemini-pro')
    else:
        st.error("⚠️ المفتاح مش موجود في Secrets!")
except Exception as e:
    st.error(f"مشكلة في المفتاح: {e}")

# --- ذاكرة الشات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- عرض الشات ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- التفاعل ---
if prompt := st.chat_input("اطلب مني أي حاجة يا زعيم..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # أوامر التطوير
            if "طور نفسك" in prompt or "اكتب كود" in prompt:
                full_response = "جاري كتابة الكود الجديد...\n"
                ai_prompt = f"أنت خبير Streamlit. المستخدم يريد: {prompt}. اكتب كود python كامل لملف app.py."
                response = model.generate_content(ai_prompt)
                message_placeholder.markdown(response.text)
                full_response = response.text
            else:
                # دردشة عادية
                chat_prompt = f"أنت هوندا، مساعد مصري ذكي ومرح. المستخدم: {prompt}"
                response = model.generate_content(chat_prompt)
                message_placeholder.markdown(response.text)
                full_response = response.text
        except Exception as e:
            st.error(f"⚠️ خطأ: {e}")
            full_response = "حصلت مشكلة، جرب تاني."
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
