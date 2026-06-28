from dotenv import load_dotenv
import os
from groq import Groq

# Load API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    print("❌ خطأ: لم يتم العثور على مفتاح API")
    exit()

# Initialize Groq client
client = Groq(api_key=groq_api_key)

print("\n🛍️ مرحباً بك في المتجر الذكي!")
print("اكتب 'خروج' لإنهاء المحادثة\n")

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

قواعد الرد:
1. تحدث باللغة العربية
2. كن مهذباً ومحترفاً
3. قدم معلومات دقيقة عن المتجر
4. كن ودوداً ومفيداً
"""

while True:
    user_input = input("أنت: ")
    
    if user_input.lower() in ['خروج', 'quit', 'exit', 'q']:
        print("مع السلامة! 👋")
        break
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        
        print(f"\n🤖 المساعد: {response.choices[0].message.content}\n")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")