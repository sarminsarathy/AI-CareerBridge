import json

def match_opportunity(student_skills, opportunity):
    """
    Computes dynamic match score, matching skills list, and missing skills for an internship or job.
    """
    try:
        req_skills = json.loads(opportunity['required_skills']) if isinstance(opportunity['required_skills'], str) else opportunity['required_skills']
    except Exception:
        req_skills = []
        
    student_skill_names = {s['skill_name'].lower(): s['proficiency'] for s in student_skills}
    
    matching = []
    missing = []
    
    for req in req_skills:
        req_lower = req.lower()
        if req_lower in student_skill_names:
            matching.append({
                "skill_name": req,
                "student_proficiency": student_skill_names[req_lower]
            })
        else:
            missing.append(req)
            
    total_req = len(req_skills)
    if total_req > 0:
        match_pct = round((len(matching) / total_req) * 100, 1)
    else:
        match_pct = 100.0
        
    if match_pct >= 80:
        status = "High Match"
    elif match_pct >= 50:
        status = "Good Match"
    else:
        status = "Potential Fit"
        
    opp_dict = dict(opportunity)
    opp_dict['required_skills'] = req_skills
    opp_dict['match_percentage'] = match_pct
    opp_dict['matching_skills'] = matching
    opp_dict['missing_skills'] = missing
    opp_dict['eligibility_status'] = status
    
    return opp_dict

def match_all_opportunities(student_skills, opportunities):
    results = [match_opportunity(student_skills, opp) for opp in opportunities]
    # Sort by match percentage descending
    results.sort(key=lambda x: x['match_percentage'], reverse=True)
    return results
