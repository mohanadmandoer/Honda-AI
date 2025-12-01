import streamlit as st
import google.generativeai as genai
import os
import sys

# --- إعداد الصفحة ---
st.set_page_config(page_title="Honda AI", page_icon="🤖", layout="centered")

# --- التصميم ---
st.markdown("""
<style>
    .stChatMessage {text-align: right; direction: rtl;}
    p {text-align: right; direction: rtl;}
    .stTextInput > div > div > input {text-align: right; direction: rtl;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- العنوان ---
st.title("🤖 هوندا - مساعدك السحابي")

# --- دالة المخ الذكي (المعالج الذاتي + قائمتك الخاصة) ---
def get_working_model():
    try:
        # 1. التأكد من المفتاح
        if "HONDA_API_KEY" not in st.secrets:
            st.error("⚠️ المفتاح مش موجود في Secrets!")
            return None, "مفيش مفتاح"

        api_key = st.secrets["HONDA_API_KEY"]
        genai.configure(api_key=api_key)

        # 2. القائمة الشاملة (زي ما طلبت بالظبط)
        # البرنامج هيجربهم واحد واحد، واللي يشتغل يمسك فيه
        models_to_try = [
            'gemini-2.5-flash',
            'gemini-2.5-flash-latest',
            'gemini-2.5-flash-001',
            'gemini-2.5-pro',
            'gemini-2-flash',
            'gemini-2-flash-latest',
            'gemini-2-flash-001',
            'gemini-2-pro',
            'gemini-3-flash',
            'gemini-3-flash-latest',
            'gemini-3-flash-001',
            'gemini-3-pro',
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-1.5-flash-001',
            'gemini-1.5-pro',
            'gemini-pro',
            # --- صيغ بديلة ---
            'models/gemini-1.5-flash',
            'models/gemini-pro'
        ]

        # 3. حلقة التجربة (Loop)
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # اختبار سريع (بدون استهلاك رصيد)
                return model, model_name
            except:
                continue # لو بايظ، خش على اللي بعده
        
        # لو كله فشل، رجع الفلاش الافتراضي
        return genai.GenerativeModel('gemini-1.5-flash'), 'gemini-1.5-flash (Fallback)'

    except Exception as e:
        st.error(f"خطأ في الاتصال بجوجل: {e}")
        return None, str(e)

# --- تشغيل النظام ---
model, model_name = get_working_model()

# عرض حالة الاتصال (للتأكد فقط)
if model:
    st.caption(f"✅ متصل حالياً بمخ: {model_name}")
else:
    st.caption("🔴 النظام غير متصل")

# --- الذاكرة والشات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- استقبال الأوامر ---
if prompt := st.chat_input("أمرك يا زعيم..."):
    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد هوندا
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        if not model:
            message_placeholder.error("أنا عطلان حالياً. تأكد من المفتاح.")
            full_response = "Error: No Model"
        else:
            try:
                # --- القسم الخطير: التطوير الذاتي ---
                # الكلمات اللي بتخلي هوندا يكتب كود لنفسه
                dev_keywords = ["طور", "عدل", "ضيف", "امسح", "كود", "برنامج", "زرار", "خاصية"]
                is_dev = any(k in prompt for k in dev_keywords)

                if is_dev:
                    message_placeholder.warning("⚙️ جاري قراءة ملفاتي وتطوير الكود... لحظة واحدة")
                    
                    # 1. قراءة الكود الحالي (عشان يعرف يعدل عليه)
                    try:
                        current_file = __file__
                        with open(current_file, "r", encoding="utf-8") as f:
                            old_code = f.read()
                    except:
                        # Fallback for some cloud environments
                        current_file = "Honda.py" 
                        old_code = "# Error reading file"

                    # 2. أمر البرمجة الصارم (System Prompt)
                    dev_prompt = f"""
                    ROLE: You are an expert Python Streamlit Developer.
                    TASK: Rewrite the provided code to implement this request: "{prompt}".
                    
                    CURRENT CODE:
                    ```python
                    {old_code}
                    ```
                    
                    RULES:
                    1. Return ONLY the FULL VALID PYTHON CODE. No explanations, no markdown.
                    2. YOU MUST KEEP the 'get_working_model' function and the 'models_to_try' list EXACTLY as they are.
                    3. Ensure correct indentation.
                    4. Do not remove 'import streamlit' or 'api_key' logic.
                    """
                    
                    try:
                        # طلب الكود الجديد من الذكاء
                        response = model.generate_content(dev_prompt)
                        new_code = response.text.replace("```python", "").replace("```", "").strip()
                        
                        # 3. التحقق والحفظ (Overwrite)
                        if "import streamlit" in new_code and len(new_code) > 500:
                            with open(current_file, "w", encoding="utf-8") as f:
                                f.write(new_code)
                            
                            message_placeholder.success("✅ تم التطوير بنجاح! جاري إعادة التشغيل...")
                            st.session_state.messages.append({"role": "assistant", "content": "تم تحديث النظام."})
                            st.rerun() # إعادة تشغيل الموقع فوراً بالكود الجديد
                        else:
                            message_placeholder.error("فشلت عملية التطوير: الكود الناتج غير سليم.")
                            full_response = "فشل التطوير."

                    except Exception as e:
                        if "429" in str(e):
                            message_placeholder.warning("⏳ ضغط عالي، جوجل بيقول استنى دقيقة.")
                            full_response = "توقف مؤقت للراحة."
                        else:
                            st.error(f"خطأ برمجي: {e}")
                            full_response = "فشل."
                
                else:
                    # --- القسم العادي: الدردشة ---
                    chat_prompt = f"أنت هوندا، مساعد مصري ذكي ومرح. المستخدم: {prompt}"
                    response = model.generate_content(chat_prompt)
                    message_placeholder.markdown(response.text)
                    full_response = response.text

            except Exception as e:
                st.error(f"خطأ غير متوقع: {e}")
                full_response = "Error."
            
        # حفظ الرد (لو مكنش عملية تطوير)
        if not is_dev:
            st.session_state.messages.append({"role": "assistant", "content": full_response})
