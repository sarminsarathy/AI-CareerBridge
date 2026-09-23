import json
import os
from src.database import get_db, init_db
from src.auth import hash_password

def seed_data():
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    
    print("Clearing existing data...")
    cursor.execute("DELETE FROM student_documents;")
    cursor.execute("DELETE FROM scheme_documents;")
    cursor.execute("DELETE FROM government_schemes;")
    cursor.execute("DELETE FROM jobs;")
    cursor.execute("DELETE FROM internships;")
    cursor.execute("DELETE FROM career_required_skills;")
    cursor.execute("DELETE FROM career_roles;")
    cursor.execute("DELETE FROM student_skills;")
    cursor.execute("DELETE FROM skills_master;")
    cursor.execute("DELETE FROM student_profiles;")
    cursor.execute("DELETE FROM users;")
    
    # 1. Master Skills
    skills_data = [
        # Programming & Web
        ("Python", "Programming"),
        ("JavaScript", "Web Development"),
        ("HTML", "Web Development"),
        ("CSS", "Web Development"),
        ("Git", "Programming"),
        ("REST APIs", "Web Development"),
        ("Node.js", "Web Development"),
        ("React.js", "Web Development"),
        
        # Data & AI
        ("SQL", "Data"),
        ("Excel", "Data"),
        ("Statistics", "Data"),
        ("Data Visualization", "Data"),
        ("Machine Learning", "AI/ML"),
        ("Deep Learning", "AI/ML"),
        ("Mathematics", "AI/ML"),
        ("Pandas & NumPy", "Data"),
        
        # Cloud & Security
        ("Linux", "Cybersecurity"),
        ("Networking", "Cybersecurity"),
        ("Security Fundamentals", "Cybersecurity"),
        ("Threat Analysis", "Cybersecurity"),
        ("AWS / Cloud Basics", "Cloud"),
        ("Docker", "Cloud"),
        
        # Soft Skills & Design
        ("Problem Solving", "Other"),
        ("Communication", "Communication"),
        ("Leadership", "Leadership"),
        ("Figma / UI Design", "Design"),
        ("User Research", "Design")
    ]
    cursor.executemany("INSERT INTO skills_master (name, category) VALUES (?, ?);", skills_data)
    
    # 2. Career Roles & Required Skills
    roles_data = [
        {
            "role_key": "software_developer",
            "title": "Software Developer",
            "category": "Software Engineering",
            "description": "Designs, develops, tests, and maintains web applications and software systems.",
            "avg_salary": "₹6,00,000 - ₹12,00,000 / year",
            "skills": [
                ("HTML", "Advanced", "High"),
                ("CSS", "Intermediate", "Medium"),
                ("JavaScript", "Advanced", "High"),
                ("Git", "Intermediate", "High"),
                ("SQL", "Intermediate", "High"),
                ("REST APIs", "Advanced", "High"),
                ("Problem Solving", "Advanced", "High")
            ]
        },
        {
            "role_key": "data_analyst",
            "title": "Data Analyst",
            "category": "Data Science & Analytics",
            "description": "Interprets complex datasets, builds analytical dashboards, and delivers business insights.",
            "avg_salary": "₹5,00,000 - ₹9,50,000 / year",
            "skills": [
                ("Excel", "Advanced", "High"),
                ("SQL", "Advanced", "High"),
                ("Python", "Intermediate", "High"),
                ("Statistics", "Intermediate", "Medium"),
                ("Data Visualization", "Advanced", "High"),
                ("Pandas & NumPy", "Intermediate", "Medium")
            ]
        },
        {
            "role_key": "aiml_engineer",
            "title": "AI/ML Engineer",
            "category": "Artificial Intelligence",
            "description": "Builds predictive machine learning models, neural networks, and scalable AI solutions.",
            "avg_salary": "₹8,00,000 - ₹18,00,000 / year",
            "skills": [
                ("Python", "Expert", "High"),
                ("Mathematics", "Advanced", "High"),
                ("Statistics", "Advanced", "High"),
                ("Machine Learning", "Advanced", "High"),
                ("SQL", "Intermediate", "Medium"),
                ("Deep Learning", "Intermediate", "Medium")
            ]
        },
        {
            "role_key": "cybersecurity_analyst",
            "title": "Cybersecurity Analyst",
            "category": "Information Security",
            "description": "Monitors network infrastructure, performs threat analysis, and prevents cyber attacks.",
            "avg_salary": "₹6,50,000 - ₹14,00,000 / year",
            "skills": [
                ("Networking", "Advanced", "High"),
                ("Linux", "Advanced", "High"),
                ("Security Fundamentals", "Advanced", "High"),
                ("Python", "Intermediate", "Medium"),
                ("Threat Analysis", "Advanced", "High")
            ]
        },
        {
            "role_key": "cloud_engineer",
            "title": "Cloud Engineer",
            "category": "Infrastructure & Operations",
            "description": "Deploys, manages, and optimizes cloud server architectures and DevOps pipelines.",
            "avg_salary": "₹7,00,000 - ₹15,00,000 / year",
            "skills": [
                ("AWS / Cloud Basics", "Advanced", "High"),
                ("Linux", "Advanced", "High"),
                ("Docker", "Intermediate", "High"),
                ("Networking", "Intermediate", "Medium"),
                ("Python", "Intermediate", "Medium")
            ]
        },
        {
            "role_key": "uiux_designer",
            "title": "UI/UX Designer",
            "category": "Design & User Experience",
            "description": "Conducts user research, creates wireframes, and crafts intuitive user interfaces.",
            "avg_salary": "₹4,50,000 - ₹10,00,000 / year",
            "skills": [
                ("Figma / UI Design", "Advanced", "High"),
                ("User Research", "Advanced", "High"),
                ("HTML", "Intermediate", "Low"),
                ("CSS", "Intermediate", "Low"),
                ("Communication", "Advanced", "High")
            ]
        }
    ]
    
    for r in roles_data:
        cursor.execute("""
        INSERT INTO career_roles (role_key, title, category, description, avg_salary)
        VALUES (?, ?, ?, ?, ?);
        """, (r['role_key'], r['title'], r['category'], r['description'], r['avg_salary']))
        role_id = cursor.lastrowid
        
        for sk_name, req_prof, imp in r['skills']:
            cursor.execute("""
            INSERT INTO career_required_skills (role_id, skill_name, required_proficiency, importance)
            VALUES (?, ?, ?, ?);
            """, (role_id, sk_name, req_prof, imp))
            
    # 3. Internships
    internships_data = [
        (
            "Frontend Web Development Intern",
            "TechInnovate Solutions",
            "Chennai / Hybrid",
            "Hybrid",
            "6 Months",
            "₹15,00,00 / month",
            json.dumps(["HTML", "CSS", "JavaScript", "Git"]),
            "Work with our core frontend engineering team building responsive educational web portals.",
            "https://internshala.com"
        ),
        (
            "Data Analytics Intern",
            "Analytics Edge",
            "Bengaluru / Remote",
            "Remote",
            "3 Months",
            "₹18,000 / month",
            json.dumps(["SQL", "Excel", "Python", "Data Visualization"]),
            "Analyze raw customer dataset trends and build real-time executive reporting dashboards.",
            "https://unstop.com"
        ),
        (
            "Machine Learning Engineer Intern",
            "AI Vision Labs",
            "Hyderabad / On-site",
            "On-site",
            "6 Months",
            "₹22,000 / month",
            json.dumps(["Python", "Machine Learning", "Mathematics", "SQL"]),
            "Assist research scientists in training natural language processing and computer vision models.",
            "https://linkedin.com"
        ),
        (
            "Cybersecurity Junior Intern",
            "SecureNet Systems",
            "Coimbatore / Hybrid",
            "Hybrid",
            "4 Months",
            "₹12,000 / month",
            json.dumps(["Linux", "Networking", "Security Fundamentals"]),
            "Perform vulnerability assessments and assist in monitoring internal network security logs.",
            "https://naukri.com"
        ),
        (
            "Cloud DevOps Apprentice",
            "CloudScale Infra",
            "Remote",
            "Remote",
            "6 Months",
            "₹20,000 / month",
            json.dumps(["AWS / Cloud Basics", "Linux", "Docker", "Python"]),
            "Learn automated deployment pipelines, container orchestration, and cloud infrastructure monitoring.",
            "https://internships.gov.in"
        )
    ]
    cursor.executemany("""
    INSERT INTO internships (role, company, location, work_type, duration, stipend, required_skills, description, apply_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, internships_data)

    # 4. Jobs
    jobs_data = [
        (
            "Junior Full Stack Developer",
            "Cognitive Tech India",
            "Chennai, Tamil Nadu",
            "Full-time",
            "0-2 Years",
            json.dumps(["HTML", "CSS", "JavaScript", "SQL", "REST APIs", "Git"]),
            "Looking for energetic computer science graduates to build scalable SaaS web solutions.",
            "https://careers.google.com"
        ),
        (
            "Associate Data Analyst",
            "DataCorp International",
            "Bengaluru, Karnataka",
            "Full-time",
            "0-1 Years",
            json.dumps(["SQL", "Excel", "Python", "Statistics", "Data Visualization"]),
            "Transform complex data into actionable operational insights for global enterprise clients.",
            "https://naukri.com"
        ),
        (
            "Junior AI & Data Scientist",
            "Neural Mind Systems",
            "Hyderabad, Telangana",
            "Full-time",
            "1-2 Years",
            json.dumps(["Python", "Machine Learning", "Statistics", "Deep Learning", "SQL"]),
            "Develop state-of-the-art predictive algorithms for automotive and industrial IoT clients.",
            "https://linkedin.com"
        ),
        (
            "Cybersecurity Associate",
            "CyberArmor Global",
            "Chennai, Tamil Nadu",
            "Full-time",
            "0-2 Years",
            json.dumps(["Networking", "Linux", "Security Fundamentals", "Threat Analysis"]),
            "Join our 24/7 Security Operations Center to protect enterprise endpoints from zero-day threats.",
            "https://indeed.com"
        )
    ]
    cursor.executemany("""
    INSERT INTO jobs (title, company, location, employment_type, min_experience, required_skills, description, apply_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, jobs_data)

    # 5. Government Schemes & Required Documents
    schemes_data = [
        {
            "scheme_name": "Naan Mudhalvan Skill Enhancement Scheme",
            "department": "Tamil Nadu Skill Development Corporation (TNSDC)",
            "target_audience": "College Students in Tamil Nadu",
            "region": "Tamil Nadu",
            "min_education": "Undergraduate",
            "age_min": 17,
            "age_max": 28,
            "max_family_income": 0,
            "category_criteria": "All",
            "description": "Flagship scheme offering free industry-aligned technical skill training, certification vouchers, and placement assistance for students across Tamil Nadu colleges.",
            "official_url": "https://www.naanmudhalvan.tn.gov.in",
            "is_demo": 0,
            "documents": [
                ("Aadhaar Card", "Mandatory identity and biometric state domicile verification."),
                ("College ID Card", "Proof of current active enrollment in a recognized institution."),
                ("Semester Marksheets", "Verification of academic standing and ongoing course degree.")
            ]
        },
        {
            "scheme_name": "PM Vidya Lakshmi Higher Education Loan Portal",
            "department": "Ministry of Education & Finance, Govt. of India",
            "target_audience": "All Students pursuing Higher Education",
            "region": "All India",
            "min_education": "Undergraduate",
            "age_min": 17,
            "age_max": 35,
            "max_family_income": 800000,
            "category_criteria": "All",
            "description": "Single-window portal providing transparent access to government-subsidized education loans and interest subsidies for higher technical studies.",
            "official_url": "https://www.vidyalakshmi.co.in",
            "is_demo": 0,
            "documents": [
                ("Aadhaar Card", "Applicant national identity verification."),
                ("Income Certificate", "Verification of annual household income for interest subsidy."),
                ("Admission Letter", "Official college admission confirmation letter.")
            ]
        },
        {
            "scheme_name": "AICTE Pragati Scholarship for Girl Students",
            "department": "All India Council for Technical Education (AICTE)",
            "target_audience": "Female Students in Technical Courses",
            "region": "All India",
            "min_education": "Undergraduate",
            "age_min": 16,
            "age_max": 30,
            "max_family_income": 800000,
            "category_criteria": "Female",
            "description": "Financial assistance of ₹50,000 per year for eligible female students pursuing technical degree or diploma courses in AICTE-approved colleges.",
            "official_url": "https://www.aicte-india.org/schemes/students-development-schemes/Pragathi",
            "is_demo": 0,
            "documents": [
                ("Aadhaar Card", "Identity proof."),
                ("Income Certificate", "Annual family income certificate issued by competent authority."),
                ("12th / Diploma Marksheet", "Proof of qualifying exam academic score.")
            ]
        },
        {
            "scheme_name": "Central Sector Scheme of Scholarships for College Students",
            "department": "Department of Higher Education, MHRD",
            "target_audience": "Meritorious Underprivileged Students",
            "region": "All India",
            "min_education": "Undergraduate",
            "age_min": 17,
            "age_max": 25,
            "max_family_income": 450000,
            "category_criteria": "All",
            "description": "Scholarship awarded to meritorious students who scored above 80th percentile in 12th standard exams pursuing full-time graduate courses.",
            "official_url": "https://scholarships.gov.in",
            "is_demo": 0,
            "documents": [
                ("Aadhaar Card", "Identity & bank account seeding verification."),
                ("Income Certificate", "Family income proof under ₹4.5 Lakhs."),
                ("12th Standard Marksheet", "Proof of scoring above 80th percentile.")
            ]
        },
        {
            "scheme_name": "Post Matric Scholarship for SC / ST / BC / MBC",
            "department": "State Adi Dravidar & Backward Classes Welfare Dept.",
            "target_audience": "SC / ST / BC / MBC Students",
            "region": "Tamil Nadu",
            "min_education": "Undergraduate",
            "age_min": 17,
            "age_max": 30,
            "max_family_income": 250000,
            "category_criteria": "BC/MBC/SC/ST",
            "description": "Full tuition fee reimbursement and maintenance allowance for post-matriculate students belonging to reserved communities.",
            "official_url": "https://tnadwdev.tn.gov.in",
            "is_demo": 0,
            "documents": [
                ("Community Certificate", "Valid community certificate issued by Revenue Authority."),
                ("Income Certificate", "Family income certificate under prescribed ceiling."),
                ("Bank Passbook Copy", "Aadhaar-linked bank account details for direct benefit transfer.")
            ]
        }
    ]
    
    for s in schemes_data:
        cursor.execute("""
        INSERT INTO government_schemes 
        (scheme_name, department, target_audience, region, min_education, age_min, age_max, max_family_income, category_criteria, description, official_url, is_demo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            s['scheme_name'], s['department'], s['target_audience'], s['region'],
            s['min_education'], s['age_min'], s['age_max'], s['max_family_income'],
            s['category_criteria'], s['description'], s['official_url'], s['is_demo']
        ))
        scheme_id = cursor.lastrowid
        
        for doc_name, reason in s['documents']:
            cursor.execute("""
            INSERT INTO scheme_documents (scheme_id, document_name, reason)
            VALUES (?, ?, ?);
            """, (scheme_id, doc_name, reason))

    # 6. Seed Demo Student Account
    demo_email = "demo@student.local"
    demo_pass_hash = hash_password("Demo@12345")
    
    cursor.execute("""
    INSERT INTO users (full_name, email, password_hash)
    VALUES (?, ?, ?);
    """, ("Priyadarshini Sundaram", demo_email, demo_pass_hash))
    user_id = cursor.lastrowid
    
    cursor.execute("""
    INSERT INTO student_profiles 
    (user_id, phone, dob, gender, location, education_level, institution, course, graduation_year, career_interests, profile_completed)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        user_id,
        "+91 98765 43210",
        "2003-05-15",
        "Female",
        "Chennai, Tamil Nadu",
        "Undergraduate",
        "Anna University",
        "B.E. Computer Science and Engineering",
        2026,
        json.dumps(["Software Developer", "AI/ML Engineer", "Data Analyst"]),
        1
    ))
    
    demo_skills = [
        ("Python", "Programming", "Advanced"),
        ("SQL", "Data", "Intermediate"),
        ("HTML", "Web Development", "Advanced"),
        ("CSS", "Web Development", "Intermediate"),
        ("JavaScript", "Web Development", "Intermediate"),
        ("Git", "Programming", "Beginner"),
        ("Data Visualization", "Data", "Intermediate")
    ]
    for sk, cat, prof in demo_skills:
        cursor.execute("""
        INSERT INTO student_skills (user_id, skill_name, category, proficiency)
        VALUES (?, ?, ?, ?);
        """, (user_id, sk, cat, prof))
        
    demo_docs = [
        ("Aadhaar Card", "Available"),
        ("College ID Card", "Available"),
        ("Semester Marksheets", "Available"),
        ("Income Certificate", "Need to Obtain"),
        ("12th Standard Marksheet", "Available"),
        ("Community Certificate", "Available"),
        ("Bank Passbook Copy", "Available")
    ]
    for doc_name, status in demo_docs:
        cursor.execute("""
        INSERT INTO student_documents (user_id, document_name, status)
        VALUES (?, ?, ?);
        """, (user_id, doc_name, status))

    conn.commit()
    conn.close()
    print("Database seeding completed successfully.")

if __name__ == '__main__':
    seed_data()
