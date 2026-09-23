from datetime import datetime

EDUCATION_HIERARCHY = {
    "10th Standard": 1,
    "12th Standard": 2,
    "Diploma": 3,
    "Undergraduate": 4,
    "Postgraduate": 5,
    "Doctorate": 6
}

def get_age(dob_str):
    if not dob_str:
        return None
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except Exception:
        return None

def evaluate_scheme_eligibility(student_profile, scheme):
    """
    Evaluates student profile against government scheme criteria.
    Returns dict with status ('Eligible', 'Possibly Eligible', 'Not Eligible') and rationale list.
    """
    reasons = []
    missing_info = []
    failed_criteria = []
    
    # Extract student metrics
    edu_level = student_profile.get('education_level')
    dob = student_profile.get('dob')
    location = student_profile.get('location')
    gender = student_profile.get('gender')
    age = get_age(dob)
    
    # 1. Education Criteria
    scheme_min_edu = scheme.get('min_education', 'Undergraduate')
    if not edu_level:
        missing_info.append("Education level not updated in profile.")
    else:
        student_edu_rank = EDUCATION_HIERARCHY.get(edu_level, 3)
        scheme_edu_rank = EDUCATION_HIERARCHY.get(scheme_min_edu, 3)
        if student_edu_rank >= scheme_edu_rank:
            reasons.append(f"Education requirement met ({edu_level} >= {scheme_min_edu}).")
        else:
            failed_criteria.append(f"Requires minimum education level of {scheme_min_edu} (Current: {edu_level}).")
            
    # 2. Age Criteria
    age_min = scheme.get('age_min', 0)
    age_max = scheme.get('age_max', 100)
    if age_min > 0 or age_max < 100:
        if age is None:
            missing_info.append("Date of Birth / Age required for age eligibility check.")
        else:
            if age_min <= age <= age_max:
                reasons.append(f"Age criterion satisfied ({age} years old; eligible range: {age_min}-{age_max}).")
            else:
                failed_criteria.append(f"Age must be between {age_min} and {age_max} years (Current age: {age}).")

    # 3. Target Audience / Gender Criteria
    target_audience = scheme.get('target_audience', 'All Students')
    if "Girls" in target_audience or "Female" in target_audience or "Women" in target_audience:
        if not gender:
            missing_info.append("Gender status not specified in profile.")
        elif gender.lower() in ["female", "girl", "woman"]:
            reasons.append("Target demographic criteria (Female students) satisfied.")
        else:
            failed_criteria.append("Scheme is reserved exclusively for female applicants.")

    # 4. Region / State Criteria
    scheme_region = scheme.get('region', 'All India')
    if scheme_region not in ["All India", "National", "All"]:
        if not location:
            missing_info.append("Location / State domicile not specified in profile.")
        elif scheme_region.lower() in location.lower() or location.lower() in scheme_region.lower():
            reasons.append(f"Domicile/State location verified ({location}).")
        else:
            # Not strict fail for demo unless distinctly specified
            reasons.append(f"Regional domicile applicability subject to verification for {scheme_region}.")

    # Status Determination
    if failed_criteria:
        status = "Not Eligible"
        all_reasons = failed_criteria + reasons
    elif missing_info:
        status = "Possibly Eligible / Needs Verification"
        all_reasons = [f"Missing Info: {m}" for m in missing_info] + reasons
    else:
        status = "Eligible"
        all_reasons = reasons if reasons else ["All standard profile criteria met."]
        
    return {
        "scheme_id": scheme['id'],
        "scheme_name": scheme['scheme_name'],
        "department": scheme['department'],
        "status": status,
        "reasons": all_reasons,
        "official_url": scheme['official_url'],
        "is_demo": bool(scheme.get('is_demo', 0))
    }
