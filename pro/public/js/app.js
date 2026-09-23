const App = {
    state: {
        user: null,
        profile: null,
        skills: [],
        currentView: 'landing',
        masterSkills: []
    },

    async init() {
        console.log("Initializing AI CareerBridge Client App...");
        this.bindEvents();
        I18N.applyLanguage();
        await this.loadMasterSkills();
        await this.checkAuthStatus();
    },

    bindEvents() {
        // Navigation link clicks
        document.querySelectorAll('[data-view]').forEach(elem => {
            elem.addEventListener('click', (e) => {
                e.preventDefault();
                const view = elem.getAttribute('data-view');
                this.navigateTo(view);
            });
        });

        // Language toggle
        document.getElementById('lang-btn-en')?.addEventListener('click', () => {
            I18N.setLanguage('en');
            this.reRenderCurrentView();
        });
        document.getElementById('lang-btn-ta')?.addEventListener('click', () => {
            I18N.setLanguage('ta');
            this.reRenderCurrentView();
        });

        // Auth forms
        document.getElementById('login-form')?.addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('register-form')?.addEventListener('submit', (e) => this.handleRegister(e));
        document.getElementById('btn-demo-login')?.addEventListener('click', () => this.handleDemoLogin());
        document.getElementById('btn-logout')?.addEventListener('click', () => this.handleLogout());

        // Profile form
        document.getElementById('profile-form')?.addEventListener('submit', (e) => this.handleSaveProfile(e));

        // Skill form
        document.getElementById('add-skill-form')?.addEventListener('submit', (e) => this.handleAddSkill(e));

        // Unauthorized event listener
        window.addEventListener('auth:unauthorized', () => {
            this.state.user = null;
            this.state.profile = null;
            this.updateNavUI();
            this.showToast("Session expired. Please log in again.", "danger");
            this.navigateTo('login');
        });
    },

    async checkAuthStatus() {
        const token = API.getToken();
        if (!token) {
            this.updateNavUI();
            this.navigateTo('landing');
            return;
        }

        try {
            const res = await API.get('/api/auth/me');
            this.state.user = res.user;
            this.state.profile = res.profile;
            this.updateNavUI();
            this.navigateTo('dashboard');
        } catch (err) {
            API.setToken(null);
            this.updateNavUI();
            this.navigateTo('landing');
        }
    },

    updateNavUI() {
        const isLoggedIn = !!this.state.user;
        document.querySelectorAll('.guest-only').forEach(el => el.style.display = isLoggedIn ? 'none' : 'inline-block');
        document.querySelectorAll('.auth-only').forEach(el => el.style.display = isLoggedIn ? 'inline-block' : 'none');
        
        if (isLoggedIn && this.state.user) {
            const userNameElem = document.getElementById('nav-user-name');
            if (userNameElem) userNameElem.textContent = this.state.user.full_name;
        }
    },

    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 3500);
    },

    async loadMasterSkills() {
        try {
            const res = await API.get('/api/master/skills');
            this.state.masterSkills = res.skills || [];
            this.populateSkillDropdown();
        } catch (err) {
            console.error("Failed to load master skills list.");
        }
    },

    populateSkillDropdown() {
        const datalist = document.getElementById('master-skills-list');
        if (!datalist) return;
        datalist.innerHTML = '';
        this.state.masterSkills.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s.name;
            opt.label = `${s.name} (${s.category})`;
            datalist.appendChild(opt);
        });
    },

    async navigateTo(viewName) {
        const protectedViews = ['dashboard', 'profile', 'skills', 'analysis', 'recommendations', 'internships', 'jobs', 'schemes', 'roadmap'];
        if (protectedViews.includes(viewName) && !this.state.user) {
            this.showToast("Please log in to access your dashboard.", "warning");
            viewName = 'login';
        }

        this.state.currentView = viewName;

        // Switch active view container
        document.querySelectorAll('.view-page').forEach(el => el.classList.remove('active'));
        const targetView = document.getElementById(`view-${viewName}`);
        if (targetView) targetView.classList.add('active');

        // Update active navbar link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.getAttribute('data-view') === viewName);
        });

        // Trigger view rendering logic
        await this.renderView(viewName);
        window.scrollTo(0, 0);
    },

    async reRenderCurrentView() {
        I18N.applyLanguage();
        await this.renderView(this.state.currentView);
    },

    async renderView(viewName) {
        switch (viewName) {
            case 'dashboard':
                await this.renderDashboard();
                break;
            case 'profile':
                await this.renderProfile();
                break;
            case 'skills':
                await this.renderSkills();
                break;
            case 'analysis':
                await this.renderAnalysis();
                break;
            case 'recommendations':
                await this.renderRecommendations();
                break;
            case 'internships':
                await this.renderInternships();
                break;
            case 'jobs':
                await this.renderJobs();
                break;
            case 'schemes':
                await this.renderSchemes();
                break;
            case 'roadmap':
                await this.renderRoadmap();
                break;
        }
    },

    // --- AUTH HANDLERS ---
    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        try {
            const res = await API.post('/api/auth/login', { email, password });
            API.setToken(res.token);
            this.state.user = res.user;
            this.showToast(I18N.t('loginSuccess') || "Login successful!", "success");
            await this.checkAuthStatus();
        } catch (err) {
            this.showToast(err.message, "danger");
        }
    },

    async handleDemoLogin() {
        document.getElementById('login-email').value = "demo@student.local";
        document.getElementById('login-password').value = "Demo@12345";
        const form = document.getElementById('login-form');
        if (form) form.dispatchEvent(new Event('submit'));
    },

    async handleRegister(e) {
        e.preventDefault();
        const full_name = document.getElementById('reg-fullname').value;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;
        const phone = document.getElementById('reg-phone').value;
        const dob = document.getElementById('reg-dob').value;
        const gender = document.getElementById('reg-gender').value;
        const location = document.getElementById('reg-location').value;
        const education_level = document.getElementById('reg-education').value;
        const institution = document.getElementById('reg-institution').value;
        const course = document.getElementById('reg-course').value;
        const graduation_year = document.getElementById('reg-gradyear').value;

        try {
            const res = await API.post('/api/auth/register', {
                full_name, email, password, phone, dob, gender, location,
                education_level, institution, course, graduation_year
            });
            API.setToken(res.token);
            this.state.user = res.user;
            this.showToast("Account created successfully!", "success");
            await this.checkAuthStatus();
        } catch (err) {
            this.showToast(err.message, "danger");
        }
    },

    handleLogout() {
        API.setToken(null);
        this.state.user = null;
        this.state.profile = null;
        this.updateNavUI();
        this.showToast("Logged out successfully.", "info");
        this.navigateTo('landing');
    },

    // --- VIEW RENDERERS ---
    async renderDashboard() {
        if (!this.state.user) return;
        
        try {
            const [profileRes, recRes, skillsRes, schemesRes, roadmapRes] = await Promise.all([
                API.get('/api/profile'),
                API.get('/api/analysis/recommendations'),
                API.get('/api/profile/skills'),
                API.get('/api/schemes/eligibility'),
                API.get('/api/roadmap')
            ]);

            const p = profileRes.profile;
            const topRec = recRes.recommendations[0];
            const skills = skillsRes.skills;
            const eligibleSchemes = schemesRes.evaluations.filter(e => e.status === 'Eligible');
            const roadmap = roadmapRes;

            // Welcome name
            document.getElementById('dash-user-name').textContent = p.full_name;
            document.getElementById('dash-user-course').textContent = `${p.course} | ${p.institution}`;

            // Profile completion calculation
            const fields = [p.phone, p.dob, p.gender, p.location, p.education_level, p.institution, p.course, p.graduation_year];
            const filled = fields.filter(f => f && f !== '').length;
            const compPct = Math.round((filled / fields.length) * 100);
            document.getElementById('dash-profile-pct').textContent = `${compPct}%`;
            document.getElementById('dash-profile-progress').style.width = `${compPct}%`;

            // Top recommendation card
            if (topRec) {
                document.getElementById('dash-top-career').textContent = topRec.role_title;
                document.getElementById('dash-top-match').textContent = `${topRec.match_percentage}% Match`;
                document.getElementById('dash-top-why').textContent = topRec.why_recommended;
            }

            // Skill overview counters
            document.getElementById('dash-total-skills').textContent = skills.length;
            
            // Eligible schemes counter
            document.getElementById('dash-eligible-schemes-count').textContent = eligibleSchemes.length;

            // Roadmap preview step
            if (roadmap && roadmap.steps && roadmap.steps.length > 0) {
                const nextStep = roadmap.steps[0];
                document.getElementById('dash-next-step-title').textContent = nextStep.title;
                document.getElementById('dash-next-step-desc').textContent = nextStep.description;
            }
        } catch (err) {
            console.error("Dashboard render error:", err);
        }
    },

    async renderProfile() {
        try {
            const res = await API.get('/api/profile');
            const p = res.profile;

            document.getElementById('prof-fullname').value = p.full_name || '';
            document.getElementById('prof-email').value = p.email || '';
            document.getElementById('prof-phone').value = p.phone || '';
            document.getElementById('prof-dob').value = p.dob || '';
            document.getElementById('prof-gender').value = p.gender || 'Female';
            document.getElementById('prof-location').value = p.location || '';
            document.getElementById('prof-education').value = p.education_level || 'Undergraduate';
            document.getElementById('prof-institution').value = p.institution || '';
            document.getElementById('prof-course').value = p.course || '';
            document.getElementById('prof-gradyear').value = p.graduation_year || 2026;

            const interests = p.career_interests || [];
            document.querySelectorAll('.interest-checkbox').forEach(cb => {
                cb.checked = interests.includes(cb.value);
            });
        } catch (err) {
            this.showToast("Failed to load profile data.", "danger");
        }
    },

    async handleSaveProfile(e) {
        e.preventDefault();
        const selectedInterests = Array.from(document.querySelectorAll('.interest-checkbox:checked')).map(cb => cb.value);

        const payload = {
            phone: document.getElementById('prof-phone').value,
            dob: document.getElementById('prof-dob').value,
            gender: document.getElementById('prof-gender').value,
            location: document.getElementById('prof-location').value,
            education_level: document.getElementById('prof-education').value,
            institution: document.getElementById('prof-institution').value,
            course: document.getElementById('prof-course').value,
            graduation_year: document.getElementById('prof-gradyear').value,
            career_interests: selectedInterests
        };

        try {
            await API.put('/api/profile', payload);
            this.showToast("Profile updated successfully!", "success");
        } catch (err) {
            this.showToast(err.message, "danger");
        }
    },

    async renderSkills() {
        try {
            const res = await API.get('/api/profile/skills');
            this.state.skills = res.skills;

            const container = document.getElementById('skills-card-grid');
            if (!container) return;

            if (this.state.skills.length === 0) {
                container.innerHTML = `<div class="card" style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 3rem;">
                    ${I18N.t('noSkillsAdded')}
                </div>`;
                return;
            }

            container.innerHTML = this.state.skills.map(s => `
                <div class="card" style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="font-size: 1.1rem; font-weight: 700;">${s.skill_name}</h4>
                        <div style="margin-top: 0.25rem;">
                            <span class="badge badge-primary">${s.category}</span>
                            <span class="badge badge-info">${s.proficiency}</span>
                        </div>
                    </div>
                    <button class="btn btn-danger" style="padding: 0.35rem 0.65rem; font-size: 0.8rem;" onclick="App.handleDeleteSkill('${s.skill_name}')">Delete</button>
                </div>
            `).join('');
        } catch (err) {
            this.showToast("Failed to load skills.", "danger");
        }
    },

    async handleAddSkill(e) {
        e.preventDefault();
        const skill_name = document.getElementById('skill-input-name').value.trim();
        const category = document.getElementById('skill-input-cat').value;
        const proficiency = document.getElementById('skill-input-prof').value;

        if (!skill_name) return;

        try {
            await API.post('/api/profile/skills', { skill_name, category, proficiency });
            document.getElementById('skill-input-name').value = '';
            this.showToast("Skill added successfully!", "success");
            await this.renderSkills();
        } catch (err) {
            this.showToast(err.message, "danger");
        }
    },

    async handleDeleteSkill(skillName) {
        try {
            await API.delete(`/api/profile/skills/${encodeURIComponent(skillName)}`);
            this.showToast("Skill removed.", "info");
            await this.renderSkills();
        } catch (err) {
            this.showToast(err.message, "danger");
        }
    },

    async renderAnalysis() {
        try {
            const [breakdown, gapsRes] = await Promise.all([
                API.get('/api/analysis/skills'),
                API.get('/api/analysis/gaps')
            ]);

            // Skill Breakdown Lists
            const renderSkillBadges = (list) => list.length ? list.map(item => `<span class="badge badge-primary" style="margin: 0.25rem;">${item.skill_name} (${item.proficiency})</span>`).join('') : '<em style="color: var(--text-muted);">None listed</em>';
            
            document.getElementById('analysis-strong-list').innerHTML = renderSkillBadges(breakdown.strong);
            document.getElementById('analysis-moderate-list').innerHTML = renderSkillBadges(breakdown.moderate);
            document.getElementById('analysis-beginner-list').innerHTML = renderSkillBadges(breakdown.beginner);

            // Skill Gap Table
            const tbody = document.getElementById('gaps-table-body');
            if (tbody) {
                tbody.innerHTML = gapsRes.gaps.map(g => `
                    <tr>
                        <td style="padding: 0.85rem; border-bottom: 1px solid var(--border); font-weight: 600;">${g.skill_name}</td>
                        <td style="padding: 0.85rem; border-bottom: 1px solid var(--border);">${g.current_level}</td>
                        <td style="padding: 0.85rem; border-bottom: 1px solid var(--border); font-weight: 600;">${g.required_level}</td>
                        <td style="padding: 0.85rem; border-bottom: 1px solid var(--border);">
                            <span class="badge badge-${g.priority === 'High' ? 'danger' : (g.priority === 'Medium' ? 'warning' : 'info')}">${g.priority} Priority</span>
                        </td>
                        <td style="padding: 0.85rem; border-bottom: 1px solid var(--border);">
                            ${g.is_met ? '<span class="badge badge-success">Target Met ✓</span>' : '<span class="badge badge-warning">Gap to Fill</span>'}
                        </td>
                    </tr>
                `).join('');
            }
        } catch (err) {
            this.showToast("Failed to load skill analysis.", "danger");
        }
    },

    async renderRecommendations() {
        try {
            const res = await API.get('/api/analysis/recommendations');
            const container = document.getElementById('recommendations-grid');
            if (!container) return;

            container.innerHTML = res.recommendations.map(r => `
                <div class="card" style="margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <h3 style="font-size: 1.35rem; font-weight: 700; color: var(--primary);">${r.role_title}</h3>
                            <span class="badge badge-primary" style="margin-top: 0.25rem;">${r.category}</span>
                        </div>
                        <div style="text-align: right;">
                            <span class="badge badge-success" style="font-size: 1.1rem; padding: 0.4rem 0.85rem;">${r.match_percentage}% Match</span>
                            <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">Avg: ${r.avg_salary}</div>
                        </div>
                    </div>
                    <p style="margin: 1rem 0; color: var(--text-muted); font-size: 0.95rem;">${r.description}</p>

                    <div style="background: var(--surface-alt); padding: 1rem; border-radius: var(--radius-sm); border-left: 4px solid var(--primary); margin-bottom: 1rem;">
                        <strong style="font-size: 0.85rem; text-transform: uppercase; color: var(--primary); display: block; margin-bottom: 0.25rem;">${I18N.t('whyRecommended')}</strong>
                        <span style="font-size: 0.9rem; color: var(--text-main);">${r.why_recommended}</span>
                    </div>

                    <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
                        <div>
                            <strong style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.35rem;">Matching Skills:</strong>
                            ${r.matching_skills.length ? r.matching_skills.map(m => `<span class="badge badge-success" style="margin-right: 0.35rem;">${m.skill_name} (${m.student_proficiency})</span>`).join('') : '<em>None yet</em>'}
                        </div>
                        <div>
                            <strong style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.35rem;">Next Skills to Learn:</strong>
                            ${r.next_skills_to_learn.length ? r.next_skills_to_learn.map(s => `<span class="badge badge-warning" style="margin-right: 0.35rem;">${s}</span>`).join('') : '<em>Target criteria fulfilled!</em>'}
                        </div>
                    </div>
                </div>
            `).join('');
        } catch (err) {
            this.showToast("Failed to load recommendations.", "danger");
        }
    },

    async renderInternships() {
        try {
            const res = await API.get('/api/opportunities/internships');
            const container = document.getElementById('internships-grid');
            if (!container) return;

            container.innerHTML = res.internships.map(i => `
                <div class="card" style="margin-bottom: 1.25rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <h3 style="font-size: 1.2rem; font-weight: 700;">${i.role}</h3>
                            <div style="font-weight: 600; color: var(--text-muted);">${i.company} &bull; ${i.location}</div>
                        </div>
                        <span class="badge badge-${i.match_percentage >= 80 ? 'success' : (i.match_percentage >= 50 ? 'primary' : 'warning')}" style="font-size: 0.95rem;">
                            ${i.match_percentage}% Skill Match
                        </span>
                    </div>

                    <div style="display: flex; gap: 1.5rem; margin: 0.85rem 0; font-size: 0.85rem; color: var(--text-muted);">
                        <div><strong>Duration:</strong> ${i.duration}</div>
                        <div><strong>Stipend:</strong> ${i.stipend}</div>
                        <div><strong>Type:</strong> ${i.work_type}</div>
                    </div>

                    <p style="font-size: 0.9rem; margin-bottom: 1rem;">${i.description}</p>

                    <div style="margin-bottom: 1rem;">
                        <span style="font-size: 0.85rem; font-weight: 600; margin-right: 0.5rem;">Matching Skills:</span>
                        ${i.matching_skills.length ? i.matching_skills.map(m => `<span class="badge badge-success" style="margin-right: 0.25rem;">${m.skill_name}</span>`).join('') : '<em>None</em>'}
                        ${i.missing_skills.length ? `<span style="font-size: 0.85rem; font-weight: 600; margin: 0 0.5rem 0 1rem;">Missing:</span>` + i.missing_skills.map(m => `<span class="badge badge-warning" style="margin-right: 0.25rem;">${m}</span>`).join('') : ''}
                    </div>

                    <a href="${i.apply_url}" target="_blank" class="btn btn-outline" style="font-size: 0.85rem;">
                        Apply Now ↗
                    </a>
                </div>
            `).join('');
        } catch (err) {
            this.showToast("Failed to load internships.", "danger");
        }
    },

    async renderJobs() {
        try {
            const res = await API.get('/api/opportunities/jobs');
            const container = document.getElementById('jobs-grid');
            if (!container) return;

            container.innerHTML = res.jobs.map(j => `
                <div class="card" style="margin-bottom: 1.25rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <h3 style="font-size: 1.2rem; font-weight: 700;">${j.title}</h3>
                            <div style="font-weight: 600; color: var(--text-muted);">${j.company} &bull; ${j.location}</div>
                        </div>
                        <span class="badge badge-${j.match_percentage >= 80 ? 'success' : (j.match_percentage >= 50 ? 'primary' : 'warning')}" style="font-size: 0.95rem;">
                            ${j.match_percentage}% Skill Match
                        </span>
                    </div>

                    <div style="display: flex; gap: 1.5rem; margin: 0.85rem 0; font-size: 0.85rem; color: var(--text-muted);">
                        <div><strong>Employment Type:</strong> ${j.employment_type}</div>
                        <div><strong>Min Experience:</strong> ${j.min_experience}</div>
                    </div>

                    <p style="font-size: 0.9rem; margin-bottom: 1rem;">${j.description}</p>

                    <div style="margin-bottom: 1rem;">
                        <span style="font-size: 0.85rem; font-weight: 600; margin-right: 0.5rem;">Matching Skills:</span>
                        ${j.matching_skills.length ? j.matching_skills.map(m => `<span class="badge badge-success" style="margin-right: 0.25rem;">${m.skill_name}</span>`).join('') : '<em>None</em>'}
                    </div>

                    <a href="${j.apply_url}" target="_blank" class="btn btn-outline" style="font-size: 0.85rem;">
                        Apply Now ↗
                    </a>
                </div>
            `).join('');
        } catch (err) {
            this.showToast("Failed to load job listings.", "danger");
        }
    },

    async renderSchemes() {
        try {
            const [evalRes, docRes] = await Promise.all([
                API.get('/api/schemes/eligibility'),
                API.get('/api/schemes/documents')
            ]);

            const docStatusMap = {};
            (docRes.documents || []).forEach(d => docStatusMap[d.document_name] = d.status);

            const container = document.getElementById('schemes-grid');
            if (!container) return;

            container.innerHTML = evalRes.evaluations.map(s => `
                <div class="card" style="margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <h3 style="font-size: 1.25rem; font-weight: 700; color: var(--primary);">${s.scheme_name}</h3>
                            <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">${s.department}</div>
                        </div>
                        <span class="badge badge-${s.status === 'Eligible' ? 'success' : (s.status.includes('Possibly') ? 'warning' : 'danger')}" style="font-size: 0.95rem; padding: 0.4rem 0.75rem;">
                            ${s.status}
                        </span>
                    </div>

                    <div style="background: var(--surface-alt); padding: 0.85rem; border-radius: var(--radius-sm); margin: 1rem 0;">
                        <strong style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.35rem;">Rule Evaluation Rationale:</strong>
                        <ul style="padding-left: 1.2rem; font-size: 0.85rem; color: var(--text-main);">
                            ${s.reasons.map(r => `<li>${r}</li>`).join('')}
                        </ul>
                    </div>

                    <div style="margin-bottom: 1rem;">
                        <strong style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.5rem;">Required Documents Checklist:</strong>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            ${s.documents.map(d => {
                                const currentStatus = docStatusMap[d.document_name] || 'Not Available';
                                return `
                                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; background: var(--surface); padding: 0.5rem 0.75rem; border: 1px solid var(--border); border-radius: var(--radius-sm);">
                                        <div>
                                            <strong>${d.document_name}</strong> - <span style="color: var(--text-muted);">${d.reason}</span>
                                        </div>
                                        <select class="form-select" style="width: auto; padding: 0.25rem 0.5rem; font-size: 0.8rem;" onchange="App.handleUpdateDocStatus('${d.document_name}', this.value)">
                                            <option value="Available" ${currentStatus === 'Available' ? 'selected' : ''}>Available ✓</option>
                                            <option value="Not Available" ${currentStatus === 'Not Available' ? 'selected' : ''}>Not Available ✗</option>
                                            <option value="Need to Obtain" ${currentStatus === 'Need to Obtain' ? 'selected' : ''}>Need to Obtain ⏳</option>
                                        </select>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <a href="${s.official_url}" target="_blank" class="btn btn-primary" style="font-size: 0.85rem;">
                            Official Scheme Portal ↗
                        </a>
                        ${s.is_demo ? '<span class="badge badge-info">Sample / Demo Record</span>' : ''}
                    </div>
                </div>
            `).join('');
        } catch (err) {
            this.showToast("Failed to load government schemes.", "danger");
        }
    },

    async handleUpdateDocStatus(docName, newStatus) {
        try {
            await API.put('/api/schemes/documents/status', { document_name: docName, status: newStatus });
            this.showToast("Document status saved.", "success");
        } catch (err) {
            this.showToast("Failed to update status.", "danger");
        }
    },

    async renderRoadmap() {
        try {
            const roadmap = await API.get('/api/roadmap');
            document.getElementById('roadmap-target-career').textContent = roadmap.target_career;

            const container = document.getElementById('roadmap-steps-container');
            if (!container) return;

            container.innerHTML = roadmap.steps.map(s => `
                <div class="roadmap-step-card">
                    <div class="step-number">${s.step}</div>
                    <div style="flex-grow: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="font-size: 1.15rem; font-weight: 700;">${s.title}</h3>
                            <span class="badge badge-primary">${s.category}</span>
                        </div>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin: 0.5rem 0 1rem 0;">${s.description}</p>
                        <button class="btn btn-outline" style="font-size: 0.8rem; padding: 0.4rem 0.85rem;" onclick="App.navigateTo('${s.target_route}')">
                            ${s.action_label} →
                        </button>
                    </div>
                </div>
            `).join('');
        } catch (err) {
            this.showToast("Failed to load roadmap.", "danger");
        }
    }
};

window.App = App;
document.addEventListener('DOMContentLoaded', () => App.init());
