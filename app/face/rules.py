def determine_face_shape(measurements: dict) -> str:
    """
    تحديد شكل الوجه بناءً على النسب بين الطول والعرض والفك والجبهة.
    """
    width = measurements['face_width']
    height = measurements['face_height']
    jaw = measurements['jaw_width']
    forehead = measurements['forehead_width']

    # حساب النسب
    ratio_height_width = height / width
    ratio_jaw_forehead = jaw / forehead

    # القواعد (Rules-Based Logic)
    
    # 1. الوجه المستطيل أو البيضاوي (الطول أكبر بوضوح من العرض)
    if ratio_height_width > 1.4:
        # إذا كان الفك عريضًا مقاربًا للجبهة -> مستطيل
        if ratio_jaw_forehead > 0.9:
            return "rectangular"
        else:
            return "oval"
    
    # 2. الوجه المربع أو الدائري (الطول مقارب للعرض)
    else:
        # إذا كان الفك حادًا وعريضًا -> مربع
        if ratio_jaw_forehead > 0.9: # الفك مقارب لعرض الجبهة
            return "square"
        else:
            return "round"

