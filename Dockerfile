# 1. استخدام نسخة كاملة مبنية على Ubuntu (أكثر استقراراً في التحميل)
FROM python:3.10

# 2. تعيين متغيرات البيئة الأساسية
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# 3. تثبيت المكتبات بأبسط صورة ممكنة (أضفنا محاولات إعادة الاتصال)
RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# 4. إعداد المجلد والملفات
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. نسخ المشروع
COPY . .

# 6. تشغيل التطبيق
# استبدل السطر الأخير بهذا
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000", "--proxy-headers"]

