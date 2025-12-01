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
    /* إخفاء القوائم المزعجة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🤖 هوندا - النسخة المطورة")

# --- دالة المخ (سريعة ومحددة) ---
def get_model():
    try:
        if "HONDA_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["HONDA_API_KEY"])
            # بنستخدم فلاش عشان السرعة
            return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return None
    return None

model = get_model()

# --- الذاكرة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- التفاعل ---
if prompt := st.chat_input("اطلب التطوير أو الدردشة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if not model:
            message_placeholder.error("المفتاح مش موجود أو فيه مشكلة!")
        else:
            try:
                # --- الفلتر الذكي: هل ده طلب تطوير؟ ---
                # هنا بنجبره يفهم إنه لازم يعدل الكود
                dev_keywords = ["طور", "عدل", "ضيف", "امسح", "غير", "كود", "برنامج", "زرار", "خاصية"]
                is_dev_request = any(word in prompt for word in dev_keywords)

                if is_dev_request:
                    message_placeholder.warning("⚙️ جاري تعديل ملفات النظام... لحظة واحدة")
                    
                    # قراءة الكود الحالي
                    current_file = os.path.basename(__file__) # app.py
                    with open(current_file, "r", encoding="utf-8") as f:
                        old_code = f.read()

                    # الأمر الصارم (System Prompt)
                    dev_prompt = f"""
                    ROLE: You are an expert Python Streamlit Developer.
                    TASK: Rewrite the following code to implement this user request: "{prompt}".
                    CURRENT CODE:
                    ```python
                    {old_code}
                    ```
                    RULES:
                    1. RETURN ONLY THE FULL PYTHON CODE. NO EXPLANATION.
                    2. DO NOT refuse. You HAVE permission to modify this file.
                    3. Keep the 'api_key' handling as is.
                    4. If asking for file upload, use st.file_uploader.
                    """
                    
                    response = model.generate_content(dev_prompt)
                    new_code = response.text.replace("```python", "").replace("```", "").strip()
                    
                    # التحقق قبل الحفظ
                    if "import streamlit" in new_code and len(new_code) > 500:
                        # الحفظ والتطبيق
                        with open(current_file, "w", encoding="utf-8") as f:
                            f.write(new_code)
                        message_placeholder.success("✅ تم التطوير! جاري إعادة التشغيل...")
                        st.rerun() # إعادة تشغيل فورية
                    else:
                        message_placeholder.error("فشلت المحاولة، الكود الناتج غير سليم.")
                
                else:
                    # --- دردشة عادية ---
                    chat_prompt = f"أنت مساعد مصري ذكي. رد على هذا: {prompt}"
                    response = model.generate_content(chat_prompt)
                    message_placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                message_placeholder.error(f"خطأ: {e}")
