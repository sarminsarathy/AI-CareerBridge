import http.server
import socketserver
import json
import urllib.parse
import os
import re

from src.database import get_db, init_db
from src.auth import hash_password, verify_password, generate_token, verify_token
from src.ai_engine import calculate_skill_breakdown, calculate_skill_gaps, calculate_career_recommendations
from src.eligibility_engine import evaluate_scheme_eligibility
from src.opportunity_engine import match_all_opportunities
from src.roadmap_engine import generate_personalized_roadmap

PORT = 5000
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')

class CareerBridgeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def end_headers(self):
        origin = self.headers.get('Origin', '') if self.headers else ''
        if origin:
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Access-Control-Allow-Credentials', 'true')
        else:
            self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Content-Length', '0')
        self.end_headers()

    def send_json(self, data, status_code=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message, status_code=400):
        self.send_json({"error": message}, status_code=status_code)

    def parse_json_body(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                return {}
            raw_body = self.rfile.read(content_length).decode('utf-8')
            return json.loads(raw_body)
        except Exception:
            return {}

    def get_authenticated_user(self):
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        if not payload:
            return None
        return payload.get('sub') # returns user_id

    # --- MAIN ROUTER ---
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path.startswith('/api/'):
            return self.handle_api_get(path, query)

        # Handle static file serving from public/ directory
        rel_path = path[7:] if path.startswith('/public/') else path.lstrip('/')
        target_file = os.path.join(PUBLIC_DIR, rel_path)

        if path in ('/', '/public', '/public/') or not os.path.exists(target_file) or os.path.isdir(target_file):
            self.path = '/index.html'
        elif path.startswith('/public/'):
            self.path = '/' + rel_path

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith('/api/'):
            return self.handle_api_post(path)
        self.send_error_json("Not Found", 404)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith('/api/'):
            return self.handle_api_put(path)
        self.send_error_json("Not Found", 404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith('/api/'):
            return self.handle_api_delete(path)
        self.send_error_json("Not Found", 404)

    # --- GET HANDLERS ---
    def handle_api_get(self, path, query):
        conn = get_db()
        cursor = conn.cursor()

        # Public master skills list
        if path == '/api/master/skills':
            cursor.execute("SELECT name, category FROM skills_master ORDER BY category, name;")
            skills = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json({"skills": skills})

        # Protected endpoints require auth token
        user_id = self.get_authenticated_user()
        if not user_id:
            conn.close()
            return self.send_error_json("Unauthorized access. Please login.", 401)

        if path == '/api/auth/me':
            cursor.execute("SELECT id, full_name, email FROM users WHERE id = ?;", (user_id,))
            user = cursor.fetchone()
            if not user:
                conn.close()
                return self.send_error_json("User not found.", 404)
            
            cursor.execute("SELECT * FROM student_profiles WHERE user_id = ?;", (user_id,))
            profile = cursor.fetchone()
            profile_dict = dict(profile) if profile else {}
            if profile_dict.get('career_interests'):
                try:
                    profile_dict['career_interests'] = json.loads(profile_dict['career_interests'])
                except Exception:
                    profile_dict['career_interests'] = []
            
            conn.close()
            return self.send_json({
                "user": dict(user),
                "profile": profile_dict
            })

        elif path == '/api/profile':
            cursor.execute("SELECT u.full_name, u.email, sp.* FROM users u JOIN student_profiles sp ON u.id = sp.user_id WHERE u.id = ?;", (user_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return self.send_error_json("Profile not found.", 404)
            p = dict(row)
            if p.get('career_interests'):
                try:
                    p['career_interests'] = json.loads(p['career_interests'])
                except Exception:
                    p['career_interests'] = []
            conn.close()
            return self.send_json({"profile": p})

        elif path == '/api/profile/skills':
            cursor.execute("SELECT id, skill_name, category, proficiency FROM student_skills WHERE user_id = ? ORDER BY id DESC;", (user_id,))
            skills = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json({"skills": skills})

        elif path == '/api/analysis/skills':
            cursor.execute("SELECT skill_name, category, proficiency FROM student_skills WHERE user_id = ?;", (user_id,))
            skills = [dict(r) for r in cursor.fetchall()]
            breakdown = calculate_skill_breakdown(skills)
            conn.close()
            return self.send_json(breakdown)

        elif path == '/api/analysis/gaps':
            role_id = query.get('role_id', [None])[0]
            cursor.execute("SELECT skill_name, category, proficiency FROM student_skills WHERE user_id = ?;", (user_id,))
            student_skills = [dict(r) for r in cursor.fetchall()]

            if role_id:
                cursor.execute("SELECT * FROM career_required_skills WHERE role_id = ?;", (role_id,))
            else:
                cursor.execute("SELECT * FROM career_required_skills WHERE role_id = 1;")
                
            req_skills = [dict(r) for r in cursor.fetchall()]
            gaps = calculate_skill_gaps(student_skills, req_skills)
            conn.close()
            return self.send_json({"gaps": gaps})

        elif path == '/api/analysis/recommendations':
            cursor.execute("SELECT skill_name, category, proficiency FROM student_skills WHERE user_id = ?;", (user_id,))
            student_skills = [dict(r) for r in cursor.fetchall()]

            cursor.execute("SELECT career_interests FROM student_profiles WHERE user_id = ?;", (user_id,))
            prof_row = cursor.fetchone()
            career_interests = json.loads(prof_row['career_interests']) if prof_row and prof_row['career_interests'] else []

            cursor.execute("SELECT * FROM career_roles;")
            roles = [dict(r) for r in cursor.fetchall()]

            roles_with_skills = []
            for r in roles:
                cursor.execute("SELECT skill_name, required_proficiency, importance FROM career_required_skills WHERE role_id = ?;", (r['id'],))
                r_skills = [dict(s) for s in cursor.fetchall()]
                roles_with_skills.append({
                    "role": r,
                    "required_skills": r_skills
                })

            recommendations = calculate_career_recommendations(student_skills, career_interests, roles_with_skills)
            conn.close()
            return self.send_json({"recommendations": recommendations})

        elif path == '/api/opportunities/internships':
            cursor.execute("SELECT skill_name, category, proficiency FROM student_skills WHERE user_id = ?;", (user_id,))
            student_skills = [dict(r) for r in cursor.fetchall()]

            cursor.execute("SELECT * FROM internships;")
            internships = [dict(r) for r in cursor.fetchall()]
            matched = match_all_opportunities(student_skills, internships)
            conn.close()
            return self.send_json({"internships": matched})

        elif path == '/api/opportunities/jobs':
            cursor.execute("SELECT skill_name, category, proficiency FROM student_skills WHERE user_id = ?;", (user_id,))
            student_skills = [dict(r) for r in cursor.fetchall()]

            cursor.execute("SELECT * FROM jobs;")
            jobs = [dict(r) for r in cursor.fetchall()]
            matched = match_all_opportunities(student_skills, jobs)
            conn.close()
            return self.send_json({"jobs": matched})

        elif path == '/api/schemes/eligibility':
            cursor.execute("SELECT * FROM student_profiles WHERE user_id = ?;", (user_id,))
            profile = dict(cursor.fetchone())

            cursor.execute("SELECT * FROM government_schemes;")
            schemes = [dict(r) for r in cursor.fetchall()]

            evaluations = []
            for s in schemes:
                eval_res = evaluate_scheme_eligibility(profile, s)
                # Fetch required documents
                cursor.execute("SELECT document_name, reason FROM scheme_documents WHERE scheme_id = ?;", (s['id'],))
                docs = [dict(d) for d in cursor.fetchall()]
                eval_res['documents'] = docs
                evaluations.append(eval_res)

            conn.close()
            return self.send_json({"evaluations": evaluations})

        elif path == '/api/schemes/documents':
            cursor.execute("SELECT document_name, status FROM student_documents WHERE user_id = ?;", (user_id,))
            docs = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json({"documents": docs})

        elif path == '/api/roadmap':
            # Gather profile, skills, top recommendation, gaps, internships, jobs, schemes
            cursor.execute("SELECT * FROM student_profiles WHERE user_id = ?;", (user_id,))
            profile = dict(cursor.fetchone())

            cursor.execute("SELECT skill_name, category, proficiency FROM student_skills WHERE user_id = ?;", (user_id,))
            student_skills = [dict(r) for r in cursor.fetchall()]

            career_interests = json.loads(profile['career_interests']) if profile.get('career_interests') else []

            cursor.execute("SELECT * FROM career_roles;")
            roles = [dict(r) for r in cursor.fetchall()]
            roles_with_skills = []
            for r in roles:
                cursor.execute("SELECT skill_name, required_proficiency, importance FROM career_required_skills WHERE role_id = ?;", (r['id'],))
                r_skills = [dict(s) for s in cursor.fetchall()]
                roles_with_skills.append({"role": r, "required_skills": r_skills})

            recommendations = calculate_career_recommendations(student_skills, career_interests, roles_with_skills)
            top_rec = recommendations[0] if recommendations else None

            # Calculate gaps for top recommendation
            if top_rec:
                cursor.execute("SELECT * FROM career_required_skills WHERE role_id = ?;", (top_rec['role_id'],))
                req_skills = [dict(r) for r in cursor.fetchall()]
                gaps = calculate_skill_gaps(student_skills, req_skills)
            else:
                gaps = []

            cursor.execute("SELECT * FROM internships;")
            internships = match_all_opportunities(student_skills, [dict(r) for r in cursor.fetchall()])

            cursor.execute("SELECT * FROM jobs;")
            jobs = match_all_opportunities(student_skills, [dict(r) for r in cursor.fetchall()])

            cursor.execute("SELECT * FROM government_schemes;")
            schemes = [dict(r) for r in cursor.fetchall()]
            eligible_schemes = [s for s in schemes if evaluate_scheme_eligibility(profile, s)['status'] == 'Eligible']

            roadmap = generate_personalized_roadmap(profile, student_skills, top_rec, gaps, internships, jobs, eligible_schemes)
            conn.close()
            return self.send_json(roadmap)

        conn.close()
        return self.send_error_json("API Route Not Found", 404)

    # --- POST HANDLERS ---
    def handle_api_post(self, path):
        data = self.parse_json_body()
        conn = get_db()
        cursor = conn.cursor()

        if path == '/api/auth/register':
            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()
            full_name = data.get('full_name', '').strip()

            if not email or not password or not full_name:
                conn.close()
                return self.send_error_json("Name, Email and Password are required.")

            cursor.execute("SELECT id FROM users WHERE email = ?;", (email,))
            if cursor.fetchone():
                conn.close()
                return self.send_error_json("User with this email already exists.")

            pass_hash = hash_password(password)
            cursor.execute("INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?);", (full_name, email, pass_hash))
            user_id = cursor.lastrowid

            career_interests = json.dumps(data.get('career_interests', ["Software Developer"]))
            cursor.execute("""
            INSERT INTO student_profiles 
            (user_id, phone, dob, gender, location, education_level, institution, course, graduation_year, career_interests, profile_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1);
            """, (
                user_id,
                data.get('phone', ''),
                data.get('dob', ''),
                data.get('gender', 'Select'),
                data.get('location', ''),
                data.get('education_level', 'Undergraduate'),
                data.get('institution', ''),
                data.get('course', ''),
                int(data.get('graduation_year', 2026)),
                career_interests
            ))

            conn.commit()
            token = generate_token(user_id, email)
            conn.close()

            return self.send_json({
                "message": "Registration successful",
                "token": token,
                "user": {"id": user_id, "full_name": full_name, "email": email}
            }, status_code=201)

        elif path == '/api/auth/login':
            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()

            if not email or not password:
                conn.close()
                return self.send_error_json("Email and Password are required.")

            cursor.execute("SELECT id, full_name, password_hash FROM users WHERE email = ?;", (email,))
            user = cursor.fetchone()

            if not user or not verify_password(password, user['password_hash']):
                conn.close()
                return self.send_error_json("Invalid email or password.", 401)

            token = generate_token(user['id'], email)
            conn.close()
            return self.send_json({
                "message": "Login successful",
                "token": token,
                "user": {"id": user['id'], "full_name": user['full_name'], "email": email}
            })

        elif path == '/api/auth/logout':
            conn.close()
            return self.send_json({"message": "Logged out successfully"})

        # Authenticated POST endpoints
        user_id = self.get_authenticated_user()
        if not user_id:
            conn.close()
            return self.send_error_json("Unauthorized access.", 401)

        if path == '/api/profile/skills':
            skill_name = data.get('skill_name', '').strip()
            category = data.get('category', 'Other').strip()
            proficiency = data.get('proficiency', 'Beginner').strip()

            if not skill_name:
                conn.close()
                return self.send_error_json("Skill name is required.")

            cursor.execute("""
            INSERT INTO student_skills (user_id, skill_name, category, proficiency)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, skill_name) DO UPDATE SET proficiency = excluded.proficiency, category = excluded.category;
            """, (user_id, skill_name, category, proficiency))
            
            conn.commit()
            conn.close()
            return self.send_json({"message": "Skill saved successfully."})

        conn.close()
        return self.send_error_json("POST Endpoint Not Found", 404)

    # --- PUT HANDLERS ---
    def handle_api_put(self, path):
        data = self.parse_json_body()
        conn = get_db()
        cursor = conn.cursor()

        user_id = self.get_authenticated_user()
        if not user_id:
            conn.close()
            return self.send_error_json("Unauthorized access.", 401)

        if path == '/api/profile':
            career_interests = json.dumps(data.get('career_interests', []))
            cursor.execute("""
            UPDATE student_profiles SET
                phone = ?, dob = ?, gender = ?, location = ?,
                education_level = ?, institution = ?, course = ?, graduation_year = ?,
                career_interests = ?, profile_completed = 1
            WHERE user_id = ?;
            """, (
                data.get('phone', ''),
                data.get('dob', ''),
                data.get('gender', ''),
                data.get('location', ''),
                data.get('education_level', ''),
                data.get('institution', ''),
                data.get('course', ''),
                int(data.get('graduation_year', 2026)),
                career_interests,
                user_id
            ))
            conn.commit()
            conn.close()
            return self.send_json({"message": "Profile updated successfully."})

        elif path == '/api/schemes/documents/status':
            doc_name = data.get('document_name')
            status = data.get('status', 'Not Available')

            if not doc_name:
                conn.close()
                return self.send_error_json("Document name is required.")

            cursor.execute("""
            INSERT INTO student_documents (user_id, document_name, status)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, document_name) DO UPDATE SET status = excluded.status;
            """, (user_id, doc_name, status))
            conn.commit()
            conn.close()
            return self.send_json({"message": "Document status updated."})

        conn.close()
        return self.send_error_json("PUT Endpoint Not Found", 404)

    # --- DELETE HANDLERS ---
    def handle_api_delete(self, path):
        conn = get_db()
        cursor = conn.cursor()

        user_id = self.get_authenticated_user()
        if not user_id:
            conn.close()
            return self.send_error_json("Unauthorized access.", 401)

        if path.startswith('/api/profile/skills/'):
            skill_name = urllib.parse.unquote(path.replace('/api/profile/skills/', ''))
            cursor.execute("DELETE FROM student_skills WHERE user_id = ? AND skill_name = ?;", (user_id, skill_name))
            conn.commit()
            conn.close()
            return self.send_json({"message": "Skill removed successfully."})

        conn.close()
        return self.send_error_json("DELETE Endpoint Not Found", 404)

def run_server():
    init_db()
    with socketserver.TCPServer(("", PORT), CareerBridgeRequestHandler) as httpd:
        print(f"==================================================")
        print(f" AI CareerBridge Unified Student Platform Server ")
        print(f" URL: http://localhost:{PORT}")
        print(f" Demo Credentials: demo@student.local / Demo@12345")
        print(f"==================================================")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
