import cv2
import mediapipe as mp
import numpy as np
from .rules import determine_face_shape

mp_face_mesh = mp.solutions.face_mesh

def analyze_face_mesh(image_bytes):
    # تحويل الصورة من Bytes إلى تنسيق يفهمه OpenCV
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Could not decode image")

    img_h, img_w, _ = img.shape

    # تهيئة MediaPipe
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as face_mesh:
        
        results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if not results.multi_face_landmarks:
            return None # لم يتم العثور على وجه

        landmarks = results.multi_face_landmarks[0].landmark

        # دالة مساعدة لتحويل الإحداثيات النسبية إلى بكسل
        def get_coords(index):
            return np.array([landmarks[index].x * img_w, landmarks[index].y * img_h])

        # النقاط المرجعية (Landmarks indices)
        # العرض (Cheekbones): 454 (يسار), 234 (يمين)
        # الطول: 10 (أعلى الجبهة), 152 (الذقن)
        # الفك: 132 (يسار), 361 (يمين) - تقريبي
        # الجبهة: 103 (يسار), 333 (يمين)

        left_cheek = get_coords(234)
        right_cheek = get_coords(454)
        
        top_head = get_coords(10)
        chin = get_coords(152)
        
        left_jaw = get_coords(132)
        right_jaw = get_coords(361)
        
        left_forehead = get_coords(103)
        right_forehead = get_coords(333)

        # حساب المسافات الإقليدية (Euclidean Distance)
        measurements = {
            "face_width": float(np.linalg.norm(left_cheek - right_cheek)),
            "face_height": float(np.linalg.norm(top_head - chin)),
            "jaw_width": float(np.linalg.norm(left_jaw - right_jaw)),
            "forehead_width": float(np.linalg.norm(left_forehead - right_forehead))
        }

        # تحديد الشكل
        shape = determine_face_shape(measurements)

        return {
            "shape": shape,
            "measurements": measurements
        }

