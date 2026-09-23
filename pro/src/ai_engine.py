PROFICIENCY_SCORES = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3,
    "Expert": 4
}

def get_proficiency_score(level_str):
    return PROFICIENCY_SCORES.get(level_str, 1)

def calculate_skill_breakdown(student_skills):
    """Categorizes student skills into levels and categories."""
    breakdown = {
        "strong": [],       # Advanced / Expert
        "moderate": [],     # Intermediate
        "beginner": [],     # Beginner
        "by_category": {},
        "total_skills": len(student_skills)
    }
    
    for s in student_skills:
        name = s['skill_name']
        cat = s['category']
        prof = s['proficiency']
        
        item = {"skill_name": name, "category": cat, "proficiency": prof}
        
        if prof in ["Advanced", "Expert"]:
            breakdown["strong"].append(item)
        elif prof == "Intermediate":
            breakdown["moderate"].append(item)
        else:
            breakdown["beginner"].append(item)
            
        if cat not in breakdown["by_category"]:
            breakdown["by_category"][cat] = []
        breakdown["by_category"][cat].append(item)
        
    return breakdown

def calculate_skill_gaps(student_skills, career_required_skills):
    """
    Calculates numerical skill gaps between student's skills and a target career's requirements.
    Returns gaps with priority (High, Medium, Low).
    """
    student_map = {s['skill_name'].lower(): s['proficiency'] for s in student_skills}
    gaps = []
    
    for req in career_required_skills:
        req_name = req['skill_name']
        req_prof = req['required_proficiency']
        importance = req.get('importance', 'Medium')
        
        req_score = get_proficiency_score(req_prof)
        curr_prof = student_map.get(req_name.lower(), None)
        
        if curr_prof is None:
            curr_score = 0
            curr_prof_str = "Missing"
        else:
            curr_score = get_proficiency_score(curr_prof)
            curr_prof_str = curr_prof
            
        gap_score = max(0, req_score - curr_score)
        
        if curr_score == 0:
            priority = "High" if importance in ["High", "Medium"] else "Medium"
        elif gap_score >= 2:
            priority = "High"
        elif gap_score == 1:
            priority = "Medium" if importance == "High" else "Low"
        else:
            priority = "Low"
            
        gaps.append({
            "skill_name": req_name,
            "current_level": curr_prof_str,
            "required_level": req_prof,
            "gap_score": gap_score,
            "importance": importance,
            "priority": priority,
            "is_met": gap_score == 0
        })
        
    # Sort by priority (High -> Medium -> Low)
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    gaps.sort(key=lambda x: priority_order.get(x['priority'], 4))
    return gaps

def calculate_career_recommendations(student_skills, career_interests, career_roles_with_skills):
    """
    Evaluates career roles against student skills and interests.
    Generates explainable "Why this recommendation?" rationale dynamically.
    """
    student_map = {s['skill_name'].lower(): s['proficiency'] for s in student_skills}
    recommendations = []
    
    for role_data in career_roles_with_skills:
        role = role_data['role']
        req_skills = role_data['required_skills']
        
        if not req_skills:
            continue
            
        total_req_points = 0
        earned_points = 0
        matching_skills = []
        missing_skills = []
        
        for req in req_skills:
            req_name = req['skill_name']
            req_prof = req['required_proficiency']
            weight = 2.0 if req.get('importance') == 'High' else 1.0
            
            req_score = get_proficiency_score(req_prof)
            total_req_points += (req_score * weight)
            
            student_prof = student_map.get(req_name.lower())
            if student_prof:
                s_score = get_proficiency_score(student_prof)
                # Earn capped points
                earned_points += (min(s_score, req_score) * weight)
                matching_skills.append({
                    "skill_name": req_name,
                    "student_proficiency": student_prof,
                    "required_proficiency": req_prof
                })
            else:
                missing_skills.append({
                    "skill_name": req_name,
                    "required_proficiency": req_prof,
                    "importance": req.get('importance', 'Medium')
                })
                
        raw_match_pct = (earned_points / total_req_points * 100) if total_req_points > 0 else 0
        
        # Boost score slightly if user explicitly selected this career interest
        is_interested = any(
            interest.lower() in role['title'].lower() or role['title'].lower() in interest.lower()
            for interest in career_interests
        )
        if is_interested:
            match_pct = min(100.0, raw_match_pct + 15.0)
        else:
            match_pct = raw_match_pct
            
        match_pct = round(match_pct, 1)
        
        # Build explainable text dynamically
        reasons = []
        if is_interested:
            reasons.append(f"Directly matches your stated career interest in '{role['title']}'.")
            
        if matching_skills:
            matched_names = [m['skill_name'] for m in matching_skills[:3]]
            reasons.append(f"You demonstrate solid proficiency in core required skills: {', '.join(matched_names)}.")
        else:
            reasons.append("Presents a foundational growth opportunity in a new technical domain.")
            
        if missing_skills:
            high_pri_missing = [m['skill_name'] for m in missing_skills if m.get('importance') == 'High']
            if high_pri_missing:
                reasons.append(f"Key skills to focus on next include: {', '.join(high_pri_missing[:2])}.")
                
        why_text = " ".join(reasons)
        
        recommendations.append({
            "role_id": role['id'],
            "role_title": role['title'],
            "category": role['category'],
            "description": role['description'],
            "avg_salary": role['avg_salary'],
            "match_percentage": match_pct,
            "is_interested": is_interested,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "why_recommended": why_text,
            "next_skills_to_learn": [m['skill_name'] for m in missing_skills[:3]]
        })
        
    # Sort recommendations by match percentage descending
    recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
    return recommendations
