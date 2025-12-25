import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

# استيراد المكونات المحلية
from app.face.analyzer import analyze_face_mesh
from app.face.recommendations import get_recommendation
from app.database import engine, Base, get_db
from app.models import FaceAnalysisLog

# إنشاء الجداول في قاعدة البيانات عند البدء
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FaceShape AI Stylist",
    description="API لتحليل شكل الوجه واقتراح قصات شعر مناسبة دون حفظ الصور.",
    version="1.0.0"
)

# مسار أساسي للتحقق من عمل السيرفر (Health Check)
@app.get("/")
async def root():
    return {"message": "Face Shape Analyzer API is running!"}

@app.post("/api/face/analyze")
async def analyze_face(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. التحقق من نوع الملف
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # 2. قراءة الملف (في الذاكرة فقط)
    image_bytes = await image.read()

    try:
        # 3. تحليل الوجه باستخدام MediaPipe
        analysis_result = analyze_face_mesh(image_bytes)

        if not analysis_result:
            raise HTTPException(status_code=400, detail="لم يتم اكتشاف وجه في الصورة. يرجى محاولة صورة أخرى واضحة.")

        shape = analysis_result["shape"]
        measurements = analysis_result["measurements"]

        # 4. الحصول على التوصيات بناءً على الشكل
        recommendations = get_recommendation(shape)

        # 5. حفظ السجلات (Metadata فقط) في قاعدة البيانات للخصوصية
        db_log = FaceAnalysisLog(
            face_shape=shape,
            measurements=measurements
        )
        db.add(db_log)
        db.commit()

        # 6. إرجاع النتيجة النهائية
        return {
            "face_shape": shape,
            "measurements": {k: round(v, 2) for k, v in measurements.items()},
            "recommendations": recommendations
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # طباعة الخطأ في السجلات لمساعدتك في تتبعه على Render
        print(f"Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail="حدث خطأ داخلي أثناء معالجة الصورة.")

# هذا الجزء ضروري لـ Render للتعرف على المنفذ (Port)
if __name__ == "__main__":
    # جلب المنفذ من بيئة Render أو استخدام 10000 كافتراضي
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)

