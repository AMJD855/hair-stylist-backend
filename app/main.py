from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.face.analyzer import analyze_face_mesh
from app.face.recommendations import get_recommendation
from app.database import engine, Base, get_db
from app.models import FaceAnalysisLog
import json

# إنشاء الجداول في قاعدة البيانات عند البدء
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FaceShape AI Stylist",
    description="API لتحليل شكل الوجه واقتراح قصات شعر مناسبة دون حفظ الصور.",
    version="1.0.0"
)

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
        # 3. تحليل الوجه
        analysis_result = analyze_face_mesh(image_bytes)
        
        if not analysis_result:
            raise HTTPException(status_code=400, detail="No face detected in the image")

        shape = analysis_result["shape"]
        measurements = analysis_result["measurements"]

        # 4. الحصول على التوصيات
        recommendations = get_recommendation(shape)

        # 5. حفظ السجلات (Metadata فقط) في قاعدة البيانات
        # ملاحظة: لا نحفظ الصورة الخام (image_bytes) التزاماً بمبدأ الأمان
        db_log = FaceAnalysisLog(
            face_shape=shape,
            measurements=measurements
        )
        db.add(db_log)
        db.commit()

        # 6. إرجاع النتيجة JSON
        return {
            "face_shape": shape,
            "measurements": {k: round(v, 2) for k, v in measurements.items()},
            "recommendations": recommendations
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # طباعة الخطأ في الكونسول للمطور
        print(f"Error: {e}") 
        raise HTTPException(status_code=500, detail="Internal Server Error during processing")

