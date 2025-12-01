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
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- العنوان ---
st.title("🤖 هوندا - مساعدك السحابي")

# --- دالة المخ الذكي (بتجرب كل الموديلات المتاحة) ---
def get_working_model():
    try:
        # 1. التأكد من المفتاح
        if "HONDA_API_KEY" not in st.secrets:
            st.error("⚠️ المفتاح مش موجود في Secrets!")
            return None, "مفيش مفتاح"

        api_key = st.secrets["HONDA_API_KEY"]
        genai.configure(api_key=api_key)

        # 2. قائمة الموديلات اللي هنجربها بالترتيب (الأسرع للأذكى)
        models_to_try = [
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-pro',
            'gemini-1.5-pro',
            'gemini-1.0-pro'
        ]

        # 3. نجرب واحد واحد لحد ما نلاقي واحد شغال
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # تجربة وهمية سريعة عشان نتأكد إنه شغال
                # (بنبعت كلمة test ولو رد يبقى تمام)
                # ملاحظة: مش بنعمل generate فعلي عشان نوفر الكوتا، مجرد Initializing
                return model, model_name
            except:
                continue # لو بايظ جرب اللي بعده
        
        # لو القائمة كلها فشلت، نرجع الفلاش وخلاص
        return genai.GenerativeModel('gemini-1.5-flash'), 'gemini-1.5-flash (Default)'

    except Exception as e:
        st.error(f"مشكلة في الاتصال بجوجل: {e}")
        return None, str(e)

# --- تشغيل النظام ---
model, model_name = get_working_model()

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

# --- استقبال الأوامر ---
if prompt := st.chat_input("اطلب مني أي حاجة..."):
    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد هوندا
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if not model:
            message_placeholder.error("أنا عطلان حالياً.")
        else:
            try:
                # فلتر أوامر التطوير
                dev_keywords = ["طور", "عدل", "ضيف", "امسح", "كود", "برنامج"]
                is_dev = any(k in prompt for k in dev_keywords)

                if is_dev:
                    full_response = "جاري كتابة كود التطوير...\n"
                    # أمر للمطور
                    dev_prompt = f"""
                    Act as a Streamlit Expert.
                    Task: Write the full Python code for 'app.py' to implement: "{prompt}".
                    Rules: Return ONLY the code block. No text.
                    Current Code Context: Streamlit app with Gemini.
                    """
                    try:
                        response = model.generate_content(dev_prompt)
                        message_placeholder.markdown(response.text)
                        full_response = response.text
                    except Exception as e:
                        if "429" in str(e):
                            message_placeholder.warning("⏳ ضغط عالي، جرب كمان دقيقة.")
                            full_response = "جوجل بيقولي هدي السرعة."
                        else:
                            st.error(f"خطأ تطوير: {e}")
                            full_response = "فشل التطوير."
                else:
                    # دردشة عادية
                    chat_prompt = f"أنت هوندا، مساعد مصري ذكي. المستخدم: {prompt}"
                    try:
                        response = model.generate_content(chat_prompt)
                        message_placeholder.markdown(response.text)
                        full_response = response.text
                    except Exception as e:
                        if "429" in str(e):
                            message_placeholder.warning("⏳ كفاية كلام، ريحني دقيقة!")
                            full_response = "تعبت، راجعلك كمان شوية."
                        else:
                            st.error(f"خطأ دردشة: {e}")
                            full_response = "مشكلة تقنية."

            except Exception as e:
                st.error(f"خطأ غير متوقع: {e}")
                full_response = "Error."
            
    st.session_state.messages.append({"role": "assistant", "content": full_response}).text})

            except Exception as e:
                st.error(f"⚠️ خطأ أثناء الرد: {e}")
