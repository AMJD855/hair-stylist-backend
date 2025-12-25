# 1. اختيار نسخة بايثون متوافقة تماماً مع MediaPipe
FROM python:3.10-slim

# 2. تثبيت المكتبات البرمجية التي يحتاجها OpenCV للعمل في بيئة Linux
# هذه الخطوة ضرورية لتجنب أخطاء "libGL.so.1" المشهورة
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# 4. نسخ ملف المتطلبات أولاً لتسريع عملية البناء (Caching)
COPY requirements.txt .

# 5. تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# 6. نسخ باقي ملفات المشروع إلى داخل الحاوية
COPY . .

# 7. تشغيل السيرفر
# نستخدم البورت 10000 لأنه الافتراضي في Render
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]

