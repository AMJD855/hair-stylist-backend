FACE_STYLES = {
    "round": {
        "recommended_styles": ["Fade عالي", "Quiff", "Faux Hawk", "Undercut"],
        "avoid_styles": ["قصات قصيرة جدًا", "غرة مستقيمة تغطي الجبهة"],
        "notes": "وجهك دائري، هدفنا هو إضافة طول للوجه وتقليل العرض. الجوانب القصيرة والارتفاع من الأعلى هو الأفضل."
    },
    "oval": {
        "recommended_styles": ["Buzz Cut", "Pompadour", "Side Part", "Slicked Back"],
        "avoid_styles": ["غرة كثيفة تغطي الوجه"],
        "notes": "وجهك بيضاوي، وهو الشكل المثالي تقريبًا. معظم القصات تليق بك، فقط حافظ على توازن الملامح."
    },
    "square": {
        "recommended_styles": ["Crew Cut", "Classic Side Part", "Messy Crop"],
        "avoid_styles": ["تسريحات مسطحة جدًا", "الجوانب الطويلة"],
        "notes": "وجهك مربع بفك قوي. القصات القصيرة تبرز رجولة الفك، والقصات الطويلة قليلًا تنعم الحواف."
    },
    "rectangular": {
        "recommended_styles": ["Side Part", "Slicked Back", "Layered Cuts"],
        "avoid_styles": ["جوانب قصيرة جدًا (تزيد الطول)", "ارتفاع مبالغ فيه من الأعلى"],
        "notes": "وجهك مستطيل. تجنب الجوانب القصيرة جدًا للحفاظ على عرض الوجه وتقليل حدة الطول."
    }
}

def get_recommendation(shape: str):
    return FACE_STYLES.get(shape, {
        "recommended_styles": [],
        "avoid_styles": [],
        "notes": "شكل غير محدد بدقة، ننصح باستشارة الحلاق."
    })

