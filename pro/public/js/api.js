const API_CONFIG = {
    development: 'http://localhost:5000',
    // Replace 'YOUR_DEPLOYED_BACKEND_URL' with your actual deployed backend URL (e.g. 'https://your-backend.onrender.com') when deploying
    production: 'YOUR_DEPLOYED_BACKEND_URL'
};

const isLocalEnvironment = 
    window.location.hostname === 'localhost' || 
    window.location.hostname === '127.0.0.1' || 
    window.location.hostname === '[::1]' ||
    window.location.hostname === '';

const API_BASE_URL = isLocalEnvironment ? API_CONFIG.development : API_CONFIG.production;


const API = {
    baseUrl: API_BASE_URL,

    getToken() {
        return localStorage.getItem('careerbridge_token');
    },

    setToken(token) {
        if (token) {
            localStorage.setItem('careerbridge_token', token);
        } else {
            localStorage.removeItem('careerbridge_token');
        }
    },

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },

    async request(method, endpoint, body = null) {
        const options = {
            method,
            headers: this.getHeaders()
        };
        if (body) {
            options.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, options);
            const data = await response.json();

            if (!response.ok) {
                if (response.status === 401 && endpoint !== '/api/auth/login') {
                    this.setToken(null);
                    window.dispatchEvent(new Event('auth:unauthorized'));
                }
                throw new Error(data.error || 'Server error occurred.');
            }
            return data;
        } catch (err) {
            if (err.name === 'TypeError' || err.message.includes('fetch') || err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
                const customErr = new Error('Backend server is not running. Please start the CareerBridge backend.');
                customErr.isBackendDown = true;
                console.warn(`[API Network Error] Unreachable backend at: ${this.baseUrl}${endpoint}`);
                throw customErr;
            }
            console.error(`[API Error] (${method} ${endpoint}):`, err.message);
            throw err;
        }
    },

    get(endpoint) {
        return this.request('GET', endpoint);
    },

    post(endpoint, body) {
        return this.request('POST', endpoint, body);
    },

    put(endpoint, body) {
        return this.request('PUT', endpoint, body);
    },

    delete(endpoint) {
        return this.request('DELETE', endpoint);
    }
};

window.API_CONFIG = API_CONFIG;
window.API_BASE_URL = API_BASE_URL;
window.API = API;
