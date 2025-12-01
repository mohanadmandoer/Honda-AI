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

st.title("🤖 هوندا - مساعدك السحابي")

# --- دالة الاستكشاف الذكي (المصححة) ---
def get_auto_model():
    try:
        if "HONDA_API_KEY" not in st.secrets:
            st.error("⚠️ المفتاح مش موجود في Secrets!")
            return None, "No Key"

        api_key = st.secrets["HONDA_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 1. نسأل جوجل: إيه الموديلات اللي شغالة؟
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except Exception as e:
            st.warning(f"مش عارف أجيب القائمة، هجرب الموديلات الأساسية. الخطأ: {e}")
        
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
            if not selected_name:
                selected_name = available_models[0]
        else:
            # لو فشل في جلب القائمة، جرب الفلاش وخلاص
            selected_name = 'models/gemini-1.5-flash'
        
        return genai.GenerativeModel(selected_name), selected_name

    except Exception as e:
        st.error(f"خطأ في الاتصال بجوجل: {e}")
        return None, str(e)

# --- تشغيل المخ ---
model, model_name = get_auto_model()

if model:
    st.caption(f"✅ متصل بمخ: {model_name}")
else:
    st.caption("🔴 النظام غير متصل")

# --- الذاكرة والشات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- التفاعل ---
if prompt := st.chat_input("اطلب مني أي حاجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if not model:
            message_placeholder.error("أنا عطلان حالياً بسبب مشكلة في الاتصال.")
        else:
            try:
                # --- الفلتر الذكي: هل ده طلب تطوير؟ ---
                dev_keywords = ["طور", "عدل", "ضيف", "امسح", "غير", "كود", "برنامج", "زرار", "خاصية"]
                is_dev_request = any(word in prompt for word in dev_keywords)

                if is_dev_request:
                    message_placeholder.warning("⚙️ جاري كتابة كود التطوير...")
                    
                    # قراءة الكود الحالي (عشان يعدل عليه)
                    try:
                        current_file = os.path.basename(__file__)
                        with open(current_file, "r", encoding="utf-8") as f:
                            old_code = f.read()
                    except:
                        old_code = "# Code file read error"

                    # الأمر الصارم (عشان يكتب كود بجد)
                    dev_prompt = f"""
                    ROLE: You are an expert Python Streamlit Developer.
                    TASK: Rewrite the following code to implement this user request: "{prompt}".
                    CURRENT CODE:
                    ```python
                    {old_code}
                    ```
                    RULES:
                    1. RETURN ONLY THE FULL PYTHON CODE. NO EXPLANATION.
                    2. Keep the 'api_key' handling and 'get_auto_model' logic safe.
                    3. If adding a feature (like file upload), use st.file_uploader.
                    """
                    
                    response = model.generate_content(dev_prompt)
                    new_code = response.text.replace("```python", "").replace("```", "").strip()
                    
                    # عرض الكود الجديد للمستخدم
                    message_placeholder.code(new_code, language='python')
                    st.session_state.messages.append({"role": "assistant", "content": "تم توليد الكود الجديد! انسخه وحطه في GitHub عشان يتطبق."})
                
                else:
                    # --- دردشة عادية ---
                    chat_prompt = f"أنت هوندا، مساعد مصري ذكي. المستخدم: {prompt}"
                    response = model.generate_content(chat_prompt)
                    message_placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                st.error(f"⚠️ خطأ أثناء الرد: {e}")
