# استخدام نسخة بايثون نحيفة ومستقرة
FROM python:3.10-slim

# منع التوقف لطلبات الإدخال وتحديد المنطقة الزمنية
ENV DEBIAN_FRONTEND=noninteractive

# تغيير مصادر الحزم إلى مرايا أكثر استقراراً وإضافة محاولات إعادة الاتصال
RUN sed -i 's/deb.debian.org/ftp.us.debian.org/g' /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# تحديث pip وتثبيت المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]

