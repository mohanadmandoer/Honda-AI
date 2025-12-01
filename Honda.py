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

# --- دالة الاستكشاف الذكي (الحل السحري) ---
def get_auto_model():
    try:
        if "HONDA_API_KEY" not in st.secrets:
            st.error("⚠️ المفتاح مش موجود في Secrets!")
            return None, "No Key"

        api_key = st.secrets["HONDA_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 1. نسأل جوجل: إيه الموديلات اللي شغالة؟
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if not available_models:
            st.error("❌ المفتاح سليم بس مفيش موديلات متاحة للحساب ده!")
            return None, "No Models"

     # 2. نختار الأفضل بالترتيب (تعديل هام: بنجبره يختار الفلاش عشان الكوتا)
        # القائمة دي مرتبة من الأسرع والأوفر للأثقل
        preferences = [
            'models/gemini-2.5-flash',
            'models/gemini-2.5-flash-latest',
            'models/gemini-2.5-flash-001',
            'models/gemini-2.5-pro',
            'models/gemini-2-flash',
            'models/gemini-2-flash-latest',
            'models/gemini-2-flash-001',
            'models/gemini-2-pro',
            'models/gemini-3-flash',
            'models/gemini-3-flash-latest',
            'models/gemini-3-flash-001',
            'models/gemini-3-pro',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash-001',
            'models/gemini-1.5-pro',
            'models/gemini-pro'
        ]
        
        selected_name = None
        
        # البحث عن الفلاش أولاً
        for pref in preferences:
            if pref in available_models:
                selected_name = pref
                break
        
        # لو ملقاش ولا واحد من اللي فوق، خد أي واحد متاح وخلاص
        if not selected_name:
            selected_name = available_models[0]
        
        return genai.GenerativeModel(selected_name), selected_name

    except Exception as e:
        st.error(f"خطأ في الاتصال بجوجل: {e}")
        return None, str(e)

# --- تشغيل المخ ---
model, model_name = get_auto_model()

if model:
    st.caption(f"✅ تم الاتصال بنجاح بالموديل: {model_name}")
else:
    st.caption("🔴 النظام غير متصل")

# --- الذاكرة والشات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اطلب مني أي حاجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if not model:
            message_placeholder.markdown("أنا عطلان حالياً.")
        else:
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
                    chat_prompt = f"أنت هوندا، مساعد مصري ذكي. المستخدم: {prompt}"
                    response = model.generate_content(chat_prompt)
                    message_placeholder.markdown(response.text)
                    full_response = response.text
            except Exception as e:
                st.error(f"⚠️ خطأ أثناء الرد: {e}")
                full_response = "حصلت مشكلة."
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
