def generate_personalized_roadmap(profile, skills, top_recommendation, skill_gaps, matching_internships, matching_jobs, eligible_schemes):
    """
    Generates a personalized, step-by-step career progression roadmap based on live student data.
    """
    top_role_title = top_recommendation['role_title'] if top_recommendation else "Software Developer"
    
    # High priority missing skills
    high_priority_gaps = [g['skill_name'] for g in skill_gaps if g['priority'] == 'High']
    med_priority_gaps = [g['skill_name'] for g in skill_gaps if g['priority'] == 'Medium']
    
    skill_focus_1 = high_priority_gaps[0] if high_priority_gaps else "Advanced Problem Solving"
    skill_focus_2 = high_priority_gaps[1] if len(high_priority_gaps) > 1 else (med_priority_gaps[0] if med_priority_gaps else "System Architecture")
    
    top_internship = matching_internships[0] if matching_internships else None
    top_job = matching_jobs[0] if matching_jobs else None
    top_scheme = eligible_schemes[0] if eligible_schemes else None
    
    steps = [
        {
            "step": 1,
            "title": f"Master Core Skill: {skill_focus_1}",
            "category": "Skill Enhancement",
            "description": f"Focus on building proficiency in {skill_focus_1}, which is a high-priority requirement for your target role of {top_role_title}.",
            "action_label": "View Skill Gap Analysis",
            "target_route": "gaps"
        },
        {
            "step": 2,
            "title": f"Expand Domain Competency: {skill_focus_2}",
            "category": "Project Building",
            "description": f"Develop 2 practical portfolio projects demonstrating {skill_focus_2} and integration with real API services.",
            "action_label": "Update Skills Profile",
            "target_route": "skills"
        },
        {
            "step": 3,
            "title": "Build Practical Industry Projects",
            "category": "Portfolio Development",
            "description": f"Create an open-source GitHub repository showcasing full-stack applications tailored to {top_role_title} requirements.",
            "action_label": "Edit Profile & Projects",
            "target_route": "profile"
        },
        {
            "step": 4,
            "title": f"Apply for Industry Internships" + (f" ({top_internship['company']})" if top_internship else ""),
            "category": "Experiential Learning",
            "description": f"Gain hands-on work experience by applying to matching internships like '{top_internship['role'] if top_internship else 'Software Development Intern'}'.",
            "action_label": "Explore Internships",
            "target_route": "internships"
        },
        {
            "step": 5,
            "title": f"Unlock Government Student Support" + (f" ({top_scheme['scheme_name']})" if top_scheme else ""),
            "category": "Financial & Skill Support",
            "description": f"Avail eligible government support programs like '{top_scheme['scheme_name'] if top_scheme else 'Higher Education Skill Grant'}' to fund certifications and training.",
            "action_label": "Check Schemes & Documents",
            "target_route": "schemes"
        },
        {
            "step": 6,
            "title": "Target Career Placement Roles",
            "category": "Career Transition",
            "description": f"Apply for full-time opportunities matching your skill profile, such as '{top_job['title'] if top_job else top_role_title}'.",
            "action_label": "View Job Opportunities",
            "target_route": "jobs"
        },
        {
            "step": 7,
            "title": f"Achieve Target Goal: {top_role_title}",
            "category": "Milestone Achievement",
            "description": f"Complete final technical interview preparation, refine your resume, and secure a full-time role in {top_role_title}.",
            "action_label": "View Final Dashboard",
            "target_route": "dashboard"
        }
    ]
    
    return {
        "target_career": top_role_title,
        "total_steps": len(steps),
        "steps": steps
    }
