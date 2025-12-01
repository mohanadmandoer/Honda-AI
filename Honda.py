import streamlit as st
import google.generativeai as genai
import os

def get_working_model():
    """يتصل بأفضل موديل متاح (نظام المناعة ضد التوقف)"""
    try:
        if "HONDA_API_KEY" not in st.secrets:
            st.error("⚠️ مفتاح التشغيل غير موجود في Secrets!")
            return None, "No Key"

        api_key = st.secrets["HONDA_API_KEY"]
        genai.configure(api_key=api_key)

        # قائمة الموديلات الشاملة (الحاضر والمستقبل)
        models_to_try = [
            'gemini-2.5-flash',
            'gemini-2.5-flash-latest',
            'gemini-2.5-pro',
            'gemini-2.0-flash',
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-1.5-pro',
            'gemini-3-flash',
            'gemini-3-flash-latest',
            'gemini-3-pro',
            'gemini-pro',
            'models/gemini-1.5-flash', 'models/gemini-pro'
        ]

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                return model, model_name
            except:
                continue 
        
        return genai.GenerativeModel('gemini-1.5-flash'), 'Fallback'

    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return None, str(e)

# ================= واجهة المستخدم =================

st.title("🤖 هوندا - الذكاء الاصطناعي المتطور")
st.caption("أنا أطور نفسي، أصنع الملفات، وأتحكم في مظهري.")

# --- الشريط الجانبي (للأدوات) ---
with st.sidebar:
    st.header("📂 إدارة الملفات")
    uploaded_file = st.file_uploader("اعطني ملفاً لأفحصه (صور، نصوص، كود)")
    
    if st.button("🗑️ مسح الذاكرة"):
        st.session_state.messages = []
        st.rerun()

# --- تشغيل المخ ---
model, model_name = get_working_model()
if not model:
    st.error("❌ النظام متوقف. تأكد من المفتاح.")
    st.stop()

# --- عرض الشات ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # لو فيه ملفات تم إنشاؤها، نعرضها هنا (مستقبلاً)

# ================= معالجة الأوامر (قلب هوندا) =================

if prompt := st.chat_input("اطلب المستحيل..."):
    # 1. عرض طلب المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. تفكير هوندا وتنفيذ الأوامر
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # --- أ) فحص هل يوجد ملف مرفق؟ ---
            file_context = ""
            if uploaded_file:
                try:
                    # قراءة محتوى الملف (نصي)
                    stringio = uploaded_file.getvalue().decode("utf-8")
                    file_context = f"\n\n[USER UPLOADED FILE CONTENT]:\n{stringio}\n"
                    st.toast("تم قراءة الملف بنجاح! 📂")
                except:
                    file_context = "\n[USER UPLOADED A BINARY FILE - I CAN SEE IT BUT NOT READ TEXT DIRECTLY YET]\n"

            # --- ب) هل هذا طلب تطوير ذاتي؟ (Evolve) ---
            dev_keywords = ["طور نفسك", "عدل الكود", "غير لون", "غير الخلفية", "ضيف خاصية"]
            is_dev = any(k in prompt for k in dev_keywords)

            # --- ج) هل هذا طلب إنشاء ملفات؟ (Generate) ---
            gen_keywords = ["اعمل ملف", "اكتب ملف", "انشيء", "اصنع", "pdf", "صورة", "كود"]
            is_gen = any(k in prompt for k in gen_keywords)

            if is_dev:
                message_placeholder.warning("⚙️ جاري الدخول لوضع المطور... سأقوم بتعديل الكود وإعادة التشغيل.")
                
                # قراءة الكود الحالي
                current_file = __file__
                with open(current_file, "r", encoding="utf-8") as f:
                    old_code = f.read()

                dev_prompt = f"""
                Act as an expert Streamlit Python Developer (Honda).
                User Request: "{prompt}"
                
                Current Code:
                ```python
                {old_code}
                ```
                
                MISSION: Rewrite the FULL code to implement the request.
                RULES:
                1. If user asks to change color, modify 'st.session_state.ui_color' or CSS.
                2. If user asks to add features, add standard Streamlit widgets.
                3. KEEP 'get_working_model' and 'clean_code_block' functions intact.
                4. Return ONLY valid Python code.
                """
                
                response = model.generate_content(dev_prompt)
                new_code = clean_code_block(response.text)
                
                # الحفظ والتطبيق
                if "import streamlit" in new_code and len(new_code) > 500:
                    with open(current_file, "w", encoding="utf-8") as f:
                        f.write(new_code)
                    message_placeholder.success("✅ تم التحديث! إعادة تشغيل النظام...")
                    time.sleep(1)
                    st.rerun()
                else:
                    message_placeholder.error("فشل التطوير: الكود الناتج غير مكتمل.")

            elif is_gen:
                message_placeholder.info("🔨 جاري العمل على إنشاء الملفات المطلوبة...")
                
                # هنا نطلب من هوندا كتابة كود بايثون يصنع الملف (PDF, Image, etc)
                gen_prompt = f"""
                Act as a Python Coding Assistant.
                User wants to create a file/program based on: "{prompt}"
                
                Write a COMPLETE Python script that uses standard libraries (like fpdf for pdf, matplotlib for images, etc.) to generate this file.
                The script should save the result to a file (e.g., output.txt, output.png).
                Use Streamlit to display/download the result if possible.
                
                Output ONLY the Python code to generate this.
                """
                
                response = model.generate_content(gen_prompt)
                code_to_run = clean_code_block(response.text)
                
                # عرض الكود للمستخدم (لأننا على السحابة، التشغيل المباشر للملفات الثقيلة مقيد، فالأفضل نعرض الكود)
                message_placeholder.markdown("لقد قمت بكتابة البرنامج الذي يصنع هذا الملف. يمكنك نسخه وتشغيله، أو سأحاول تنفيذه الآن:")
                st.code(code_to_run, language='python')
                
                # محاولة تنفيذ الكود (Sandbox execution - dangerous but requested)
                # ملاحظة: في بيئة Streamlit Cloud، الكتابة على الديسك محدودة
                # سنقوم بمحاولة بسيطة للتنفيذ
                try:
                    exec(code_to_run)
                    st.success("تم تنفيذ الكود! (تحقق من النتيجة إذا كانت واجهة)")
                except Exception as e:
                    st.warning(f"كتبت الكود لكن لم أستطع تشغيله بالكامل هنا: {e}")
                
                full_response = "تمت المعالجة."

            else:
                # --- د) دردشة عادية وتحليل ملفات ---
                chat_prompt = f"""
                أنت 'هوندا'، مساعد ذكي ومحترف ومبرمج.
                تتحدث باللهجة المصرية الودودة.
                سياق الملف المرفق (إن وجد): {file_context}
                
                سؤال المستخدم: {prompt}
                """
                response = model.generate_content(chat_prompt)
                full_response = response.text
                message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"حدث خطأ غير متوقع: {e}")
            full_response = "حدث خطأ."

    # حفظ في الذاكرة
    if not is_dev:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
```

4.  اضغط **Commit changes**.
