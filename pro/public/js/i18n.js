const I18N = {
    currentLanguage: localStorage.getItem('careerbridge_lang') || 'en',
    
    translations: {
        en: {
            brandName: "AI CareerBridge",
            navHome: "Home",
            navDashboard: "Dashboard",
            navProfile: "Profile",
            navSkills: "Skills",
            navAnalysis: "Skill Analysis",
            navRecommendations: "Career AI",
            navInternships: "Internships",
            navJobs: "Jobs",
            navSchemes: "Govt Schemes",
            navRoadmap: "Roadmap",
            navLogin: "Login",
            navRegister: "Register",
            navLogout: "Logout",
            
            heroTitle: "Unified Student Career & Skill Gap Platform",
            heroSubtitle: "Bridge your skills to industry requirements, discover eligible government schemes, and navigate your personalized AI career roadmap.",
            getStartedBtn: "Get Started Now",
            tryDemoBtn: "Try Live Demo",
            
            dashboardTitle: "Student Control Dashboard",
            profileCompletion: "Profile Completion",
            topCareerRecommendation: "Top Career Recommendation",
            skillOverview: "Skill Overview",
            skillGapSummary: "Skill Gap Summary",
            matchingInternships: "Matching Internships",
            matchingJobs: "Matching Placement Jobs",
            eligibleGovtSchemes: "Eligible Govt Schemes",
            careerRoadmap: "Personalized Career Roadmap",
            nextRecommendedAction: "Next Recommended Action",
            
            profileTitle: "Student Profile & Education",
            fullName: "Full Name",
            emailAddress: "Email Address",
            phoneNumber: "Phone Number",
            dateOfBirth: "Date of Birth",
            gender: "Gender",
            location: "State / Location",
            educationLevel: "Education Level",
            institution: "College / Institution",
            courseDegree: "Course / Degree",
            graduationYear: "Graduation Year",
            careerInterests: "Career Interests",
            saveProfileBtn: "Save Profile Changes",
            
            skillsTitle: "Skill Management System",
            addSkillHeader: "Add / Update Skill",
            skillName: "Skill Name",
            category: "Category",
            proficiencyLevel: "Proficiency Level",
            addSkillBtn: "Add Skill to Profile",
            yourSkills: "Your Skills Profile",
            noSkillsAdded: "No skills added yet. Add your skills to generate your skill analysis.",
            
            analysisTitle: "Skill & Gap Analysis",
            strongSkills: "Strong Skills (Advanced/Expert)",
            moderateSkills: "Moderate Skills (Intermediate)",
            beginnerSkills: "Beginner Skills",
            missingSkills: "Missing Required Skills",
            priorityHigh: "High Priority",
            priorityMed: "Medium Priority",
            priorityLow: "Low Priority",
            
            recommendationsTitle: "Explainable AI Career Recommendations",
            whyRecommended: "Why This Recommendation?",
            matchScore: "Match Score",
            nextSkillsToLearn: "Next Skills to Learn",
            
            internshipsTitle: "Industry Internship Opportunities",
            filterBySkill: "Filter by Skill",
            allSkills: "All Skills",
            stipend: "Stipend",
            duration: "Duration",
            applyNow: "Apply Now",
            matchingSkills: "Matching Skills",
            missingOpportunitySkills: "Missing Skills",
            
            jobsTitle: "Placement Job Opportunities",
            employmentType: "Employment Type",
            minExperience: "Experience Required",
            
            schemesTitle: "Government Student Schemes & Support",
            schemeDepartment: "Department",
            eligibilityStatus: "Eligibility Status",
            statusEligible: "Eligible",
            statusNeedsVerification: "Needs Verification",
            statusNotEligible: "Not Eligible",
            requiredDocuments: "Required Documents",
            officialLink: "Official Application",
            demoDataNotice: "Sample / Demo Record",
            docAvailable: "Available",
            docNotAvailable: "Not Available",
            docNeedToObtain: "Need to Obtain",
            
            roadmapTitle: "Your Personalized 7-Step Career Roadmap",
            stepLabel: "Step",
            actionLabel: "Take Action",
            
            demoLoginText: "Click below to auto-fill sample student credentials:",
            useDemoAccBtn: "Use Demo Account (demo@student.local)"
        },
        ta: {
            brandName: "AI கேரியர்பிரிட்ஜ்",
            navHome: "முகப்பு",
            navDashboard: "டாஷ்போர்டு",
            navProfile: "சுயவிவரம்",
            navSkills: "திறன்கள்",
            navAnalysis: "திறன் பகுப்பாய்வு",
            navRecommendations: "தொழில் AI",
            navInternships: "பயிற்சிகள்",
            navJobs: "வேலைவாய்ப்புகள்",
            navSchemes: "அரசு திட்டங்கள்",
            navRoadmap: "வழிகாட்டி வரைபடம்",
            navLogin: "உள்நுழை",
            navRegister: "பதிவுசெய்",
            navLogout: "வெளியேறு",
            
            heroTitle: "ஒருங்கிணைந்த மாணவர் தொழில் மற்றும் திறன் வழிகாட்டி",
            heroSubtitle: "உங்கள் திறன்களை தொழில்துறை தேவைகளுடன் இணைக்கவும், தகுதியான அரசு திட்டங்களைக் கண்டறியவும், தனிப்பயனாக்கப்பட்ட தொழில் பாதையைப் பின்பற்றவும்.",
            getStartedBtn: "இப்போதே தொடங்குங்கள்",
            tryDemoBtn: "டெமோ கணக்கு முயற்சி செய்",
            
            dashboardTitle: "மாணவர் கட்டுப்பாட்டு பலகை",
            profileCompletion: "சுயவிவர நிறைவு",
            topCareerRecommendation: "முதன்மை தொழில் பரிந்துரை",
            skillOverview: "திறன் மேலோட்டம்",
            skillGapSummary: "திறன் இடைவெளி சுருக்கம்",
            matchingInternships: "பொருந்தும் பயிற்சிகள் (Internships)",
            matchingJobs: "பொருந்தும் வேலைவாய்ப்புகள்",
            eligibleGovtSchemes: "தகுதியான அரசு திட்டங்கள்",
            careerRoadmap: "தனிப்பயனாக்கப்பட்ட தொழில் வரைபடம்",
            nextRecommendedAction: "அடுத்த பரிந்துரைக்கப்பட்ட நடவடிக்கை",
            
            profileTitle: "மாணவர் சுயவிவரம் மற்றும் கல்வி",
            fullName: "முழு பெயர்",
            emailAddress: "மின்னஞ்சல் முகவரி",
            phoneNumber: "தொலைபேசி எண்",
            dateOfBirth: "பிறந்த தேதி",
            gender: "பாலினம்",
            location: "மாநிலம் / இருப்பிடம்",
            educationLevel: "கல்வி நிலை",
            institution: "கல்லூரி / நிறுவனம்",
            courseDegree: "படிப்பு / பட்டம்",
            graduationYear: "முடிக்கும் ஆண்டு",
            careerInterests: "தொழில் விருப்பங்கள்",
            saveProfileBtn: "சுயவிவரத்தை சேமிக்கவும்",
            
            skillsTitle: "திறன் மேலாண்மை அமைப்பு",
            addSkillHeader: "திறனைச் சேர்க்கவும் / புதுப்பிக்கவும்",
            skillName: "திறன் பெயர்",
            category: "பிரிவு",
            proficiencyLevel: "திறன் நிலை",
            addSkillBtn: "திறனை சேர்",
            yourSkills: "உங்கள் திறன்கள் சுயவிவரம்",
            noSkillsAdded: "இன்னும் திறன்கள் சேர்க்கப்படவில்லை. பகுப்பாய்வை உருவாக்க திறன்களைச் சேர்க்கவும்.",
            
            analysisTitle: "திறன் மற்றும் இடைவெளி பகுப்பாய்வு",
            strongSkills: "சிறந்த திறன்கள் (Advanced/Expert)",
            moderateSkills: "மிதமான திறன்கள் (Intermediate)",
            beginnerSkills: "தொடக்க நிலை திறன்கள்",
            missingSkills: "தேவையான விடுபட்ட திறன்கள்",
            priorityHigh: "அதிக முன்னுரிமை",
            priorityMed: "நடுத்தர முன்னுரிமை",
            priorityLow: "குறைந்த முன்னுரிமை",
            
            recommendationsTitle: "விளக்கமான AI தொழில் பரிந்துரைகள்",
            whyRecommended: "ஏன் இந்த பரிந்துரை?",
            matchScore: "பொருத்தம் மதிப்பெண்",
            nextSkillsToLearn: "அடுத்து கற்க வேண்டிய திறன்கள்",
            
            internshipsTitle: "தொழில்துறை பயிற்சி வாய்ப்புகள்",
            filterBySkill: "திறன் மூலம் வடிகட்டவும்",
            allSkills: "அனைத்து திறன்களும்",
            stipend: "உதவித்தொகை",
            duration: "காலஅளவு",
            applyNow: "இப்போதே விண்ணப்பிக்கவும்",
            matchingSkills: "பொருந்தும் திறன்கள்",
            missingOpportunitySkills: "விடுபட்ட திறன்கள்",
            
            jobsTitle: "வேலை வாய்ப்புகள்",
            employmentType: "வேலை வகை",
            minExperience: "தேவையான அனுபவம்",
            
            schemesTitle: "அரசு மாணவர் திட்டங்கள் மற்றும் உதவிகள்",
            schemeDepartment: "துறை",
            eligibilityStatus: "தகுதி நிலை",
            statusEligible: "தகுதியுடையவர்",
            statusNeedsVerification: "சரிபார்ப்பு தேவை",
            statusNotEligible: "தகுதியற்றவர்",
            requiredDocuments: "தேவையான ஆவணங்கள்",
            officialLink: "அதிகாரப்பூர்வ விண்ணப்பம்",
            demoDataNotice: "மாதிரி தரவு",
            docAvailable: "கைவசம் உள்ளது",
            docNotAvailable: "இல்லை",
            docNeedToObtain: "பெறப்பட வேண்டும்",
            
            roadmapTitle: "உங்கள் 7-படி தொழில் வளர்ச்சி வரைபடம்",
            stepLabel: "படி",
            actionLabel: "நடவடிக்கை எடுக்கவும்",
            
            demoLoginText: "டெமோ மாணவர் கணக்கைப் பயன்படுத்த கீழே கிளிக் செய்யவும்:",
            useDemoAccBtn: "டெமோ கணக்கை பயன்படுத்து (demo@student.local)"
        }
    },
    
    setLanguage(lang) {
        if (lang === 'en' || lang === 'ta') {
            this.currentLanguage = lang;
            localStorage.setItem('careerbridge_lang', lang);
            this.applyLanguage();
        }
    },
    
    t(key) {
        return this.translations[this.currentLanguage][key] || this.translations['en'][key] || key;
    },
    
    applyLanguage() {
        document.querySelectorAll('[data-i18n]').forEach(elem => {
            const key = elem.getAttribute('data-i18n');
            if (this.translations[this.currentLanguage][key]) {
                if (elem.tagName === 'INPUT' && elem.getAttribute('placeholder')) {
                    elem.placeholder = this.t(key);
                } else {
                    elem.textContent = this.t(key);
                }
            }
        });
        
        // Update active class on language switcher buttons
        const btnEn = document.getElementById('lang-btn-en');
        const btnTa = document.getElementById('lang-btn-ta');
        if (btnEn && btnTa) {
            btnEn.classList.toggle('active', this.currentLanguage === 'en');
            btnTa.classList.toggle('active', this.currentLanguage === 'ta');
        }
    }
};

window.I18N = I18N;
