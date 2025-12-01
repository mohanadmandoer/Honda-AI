def clean_code_block(text):
    pattern = r"```python(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

# --- دالة المخ الذكي ---
def get_working_model():
    try:
        if "HONDA_API_KEY" not in st.secrets:
            st.error("⚠️ المفتاح مش موجود في Secrets!")
            return None, "No Key"

        api_key = st.secrets["HONDA_API_KEY"]
        genai.configure(api_key=api_key)

        # القائمة الشاملة (زي ما طلبت بالظبط)
        models_to_try = [
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
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-1.5-flash-001',
            'gemini-1.5-pro',
            'gemini-pro',
        ]

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                return model, model_name
            except:
                continue 
        
        return genai.GenerativeModel('gemini-1.5-flash'), 'gemini-1.5-flash (Fallback)'

    except Exception as e:
        return None, str(e)

# --- تشغيل النظام ---
model, model_name = get_working_model()

if model:
    st.caption(f"✅ متصل بمخ: {model_name}")
else:
    st.caption("🔴 النظام غير متصل")

# --- الذاكرة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- التفاعل ---
if prompt := st.chat_input("أمرك يا زعيم..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        if not model:
            message_placeholder.error("أنا عطلان حالياً.")
            full_response = "Error."
        else:
            try:
                # --- نظام التطوير الذاتي ---
                dev_keywords = ["طور", "عدل", "ضيف", "امسح", "كود", "برنامج", "زرار", "خاصية"]
                is_dev = any(k in prompt for k in dev_keywords)

                if is_dev:
                    message_placeholder.warning("⚙️ جاري التطوير الذاتي... (لحظة واحدة)")
                    
                    try:
                        current_file = __file__
                        with open(current_file, "r", encoding="utf-8") as f:
                            old_code = f.read()
                    except:
                        old_code = ""

                    dev_prompt = f"""
                    Act as an expert Python Streamlit Developer.
                    TASK: Rewrite the ENTIRE current code to implement this request: "{prompt}".
                    
                    CURRENT CODE:
                    ```python
                    {old_code}
                    ```
                    
                    CRITICAL RULES:
                    1. Return the FULL VALID PYTHON CODE only.
                    2. KEEP 'get_working_model' and 'models_to_try' list EXACTLY as is.
                    3. KEEP 'clean_code_block' function.
                    4. Ensure correct indentation (4 spaces).
                    """
                    
                    try:
                        response = model.generate_content(dev_prompt)
                        new_code = clean_code_block(response.text)
                        
                        if "import streamlit" in new_code and len(new_code) > 500:
                            with open(current_file, "w", encoding="utf-8") as f:
                                f.write(new_code)
                            
                            message_placeholder.success("✅ تم التطوير! جاري إعادة التشغيل...")
                            st.rerun()
                        else:
                            message_placeholder.error("فشل التطوير: الكود الناتج غير سليم.")
                            full_response = "فشل."

                    except Exception as e:
                        st.error(f"خطأ برمجي: {e}")
                        full_response = "فشل."
                
                else:
                    # --- الشات العادي ---
                    chat_prompt = f"أنت هوندا، مساعد مصري ذكي. المستخدم: {prompt}"
                    response = model.generate_content(chat_prompt)
                    message_placeholder.markdown(response.text)
                    full_response = response.text

            except Exception as e:
                st.error(f"خطأ غير متوقع: {e}")
                full_response = "Error."
            
        if not is_dev:
            st.session_state.messages.append({"role": "assistant", "content": full_response})
