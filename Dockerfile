# 1. استخدام نسخة بايثون مستقرة متوافقة مع MediaPipe
FROM python:3.10-slim

# 2. منع بايثون من إنشاء ملفات .pyc وتقليل حجم الحاوية
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

# 3. تحديث المستودعات وتثبيت مكتبات النظام اللازمة لـ OpenCV و MediaPipe
# تم إضافة --fix-missing وتكرار محاولة التحديث لتجنب خطأ 100
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# 5. نسخ ملف المتطلبات أولاً (للاستفادة من Cache في Render)
COPY requirements.txt .

# 6. تحديث pip وتثبيت المكتبات البرمجية
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. نسخ كافة ملفات المشروع إلى الحاوية
COPY . .

# 8. فتح المنفذ الذي يستخدمه Render تلقائياً
EXPOSE 10000

# 9. أمر تشغيل السيرفر باستخدام uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]

