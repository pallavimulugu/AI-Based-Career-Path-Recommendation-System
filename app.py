from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'pathforge_secret_key_2025'

# ============================================================
# COMPREHENSIVE CAREER DATABASE - 10+ Careers per Branch
# ============================================================

CAREER_DATA = {
    "CSE": {
        "Software Engineer": {
            "description": "Design, develop, and maintain software applications and systems. Work on backend, frontend, or full-stack development.",
            "skills_needed": ["Python", "Java", "JavaScript", "React", "Node.js", "HTML", "CSS", "SQL", "Git", "Data Structures", "Algorithms"],
            "salary_range": "₹4L - ₹40L",
            "growth": "Very High",
            "icon": "💻",
            "jobs": [
                {"company": "Google India", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://careers.google.com/jobs", "role": "SDE", "salary": "₹20-35 LPA"},
                {"company": "Microsoft", "location": "Hyderabad", "lat": 17.4401, "lng": 78.3489, "link": "https://careers.microsoft.com", "role": "Software Engineer", "salary": "₹18-30 LPA"},
                {"company": "Amazon", "location": "Bangalore", "lat": 12.9915, "lng": 77.6968, "link": "https://amazon.jobs", "role": "SDE-1", "salary": "₹15-28 LPA"}
            ]
        },
        "Frontend Developer": {
            "description": "Build responsive and interactive user interfaces using modern web technologies.",
            "skills_needed": ["HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "Tailwind", "Bootstrap", "UI/UX"],
            "salary_range": "₹3L - ₹25L",
            "growth": "High",
            "icon": "🎨",
            "jobs": [
                {"company": "Flipkart", "location": "Bangalore", "lat": 12.9260, "lng": 77.6720, "link": "https://www.flipkartcareers.com", "role": "Frontend Engineer", "salary": "₹12-22 LPA"},
                {"company": "Swiggy", "location": "Bangalore", "lat": 12.9352, "lng": 77.6245, "link": "https://careers.swiggy.com", "role": "UI Developer", "salary": "₹10-18 LPA"}
            ]
        },
        "Backend Developer": {
            "description": "Build server-side logic, APIs, and database integrations for web applications.",
            "skills_needed": ["Python", "Java", "Node.js", "SQL", "MongoDB", "REST APIs", "Express.js", "Spring Boot", "Django"],
            "salary_range": "₹4L - ₹35L",
            "growth": "Very High",
            "icon": "⚙️",
            "jobs": [
                {"company": "Razorpay", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://razorpay.com/careers", "role": "Backend Engineer", "salary": "₹14-25 LPA"},
                {"company": "Zomato", "location": "Gurgaon", "lat": 28.4595, "lng": 77.0266, "link": "https://www.zomato.com/careers", "role": "Backend Developer", "salary": "₹12-22 LPA"}
            ]
        },
        "Full Stack Developer": {
            "description": "Build complete web applications from frontend to backend with database integration.",
            "skills_needed": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Python", "SQL", "MongoDB", "Git", "REST APIs"],
            "salary_range": "₹5L - ₹45L",
            "growth": "Very High",
            "icon": "🌐",
            "jobs": [
                {"company": "Netflix", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://jobs.netflix.com", "role": "Full Stack Engineer", "salary": "₹25-50 LPA"},
                {"company": "Uber", "location": "Bangalore", "lat": 12.9716, "lng": 77.5946, "link": "https://www.uber.com/careers", "role": "Software Engineer", "salary": "₹20-35 LPA"}
            ]
        },
        "Data Scientist": {
            "description": "Extract insights from data using statistical methods and machine learning algorithms.",
            "skills_needed": ["Python", "SQL", "Statistics", "Machine Learning", "Pandas", "NumPy", "TensorFlow", "Data Visualization"],
            "salary_range": "₹6L - ₹50L",
            "growth": "Very High",
            "icon": "📊",
            "jobs": [
                {"company": "IBM", "location": "Bangalore", "lat": 13.0222, "lng": 77.5679, "link": "https://ibm.com/careers", "role": "Data Scientist", "salary": "₹12-25 LPA"},
                {"company": "Accenture", "location": "Pune", "lat": 18.5912, "lng": 73.7381, "link": "https://accenture.com/careers", "role": "Analytics Lead", "salary": "₹10-22 LPA"}
            ]
        },
        "Machine Learning Engineer": {
            "description": "Build and deploy machine learning models at scale for production systems.",
            "skills_needed": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "SQL", "Docker", "MLOps", "Statistics"],
            "salary_range": "₹8L - ₹60L",
            "growth": "Explosive",
            "icon": "🧠",
            "jobs": [
                {"company": "NVIDIA", "location": "Bangalore", "lat": 12.9260, "lng": 77.6720, "link": "https://nvidia.com/careers", "role": "ML Engineer", "salary": "₹20-40 LPA"},
                {"company": "Intel", "location": "Bangalore", "lat": 12.8774, "lng": 77.6380, "link": "https://jobs.intel.com", "role": "AI Engineer", "salary": "₹18-35 LPA"}
            ]
        },
        "Cybersecurity Analyst": {
            "description": "Protect systems and networks from cyber threats and unauthorized access.",
            "skills_needed": ["Networking", "Linux", "Python", "Cryptography", "Penetration Testing", "SIEM", "Firewalls"],
            "salary_range": "₹5L - ₹35L",
            "growth": "High",
            "icon": "🛡️",
            "jobs": [
                {"company": "Palo Alto Networks", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://jobs.paloaltonetworks.com", "role": "Security Engineer", "salary": "₹15-30 LPA"},
                {"company": "CrowdStrike", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://crowdstrike.com/careers", "role": "Threat Analyst", "salary": "₹12-25 LPA"}
            ]
        },
        "Cloud Architect": {
            "description": "Design and manage scalable cloud infrastructure on AWS, Azure, or GCP.",
            "skills_needed": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Linux", "CI/CD"],
            "salary_range": "₹8L - ₹50L",
            "growth": "Very High",
            "icon": "☁️",
            "jobs": [
                {"company": "AWS", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://aws.amazon.com/careers", "role": "Cloud Architect", "salary": "₹25-45 LPA"},
                {"company": "Google Cloud", "location": "Hyderabad", "lat": 17.4401, "lng": 78.3489, "link": "https://cloud.google.com/careers", "role": "Cloud Engineer", "salary": "₹20-40 LPA"}
            ]
        },
        "DevOps Engineer": {
            "description": "Automate deployment, monitoring, and infrastructure management.",
            "skills_needed": ["Docker", "Kubernetes", "Jenkins", "AWS", "Linux", "Terraform", "CI/CD", "Python"],
            "salary_range": "₹6L - ₹45L",
            "growth": "Very High",
            "icon": "🔄",
            "jobs": [
                {"company": "Salesforce", "location": "Hyderabad", "lat": 17.4401, "lng": 78.3489, "link": "https://salesforce.com/careers", "role": "DevOps Engineer", "salary": "₹15-30 LPA"},
                {"company": "Adobe", "location": "Noida", "lat": 28.5355, "lng": 77.3910, "link": "https://adobe.com/careers", "role": "Site Reliability Engineer", "salary": "₹18-35 LPA"}
            ]
        },
        "Database Administrator": {
            "description": "Manage, optimize, and secure database systems for organizations.",
            "skills_needed": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "Database Design", "Performance Tuning", "Backup/Recovery"],
            "salary_range": "₹3L - ₹25L",
            "growth": "Medium",
            "icon": "🗄️",
            "jobs": [
                {"company": "Oracle", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://oracle.com/careers", "role": "DBA", "salary": "₹10-20 LPA"},
                {"company": "TCS", "location": "Multiple", "lat": 0, "lng": 0, "link": "https://www.tcs.com/careers", "role": "Database Administrator", "salary": "₹6-12 LPA"}
            ]
        }
    },
    "ECE": {
        "Embedded Systems Engineer": {
            "description": "Design and program hardware-integrated systems for IoT and automotive applications.",
            "skills_needed": ["C", "C++", "Microcontrollers", "RTOS", "PCB Design", "Communication Protocols", "ARM"],
            "salary_range": "₹4L - ₹25L",
            "growth": "High",
            "icon": "🔧",
            "jobs": [
                {"company": "Texas Instruments", "location": "Bangalore", "lat": 12.9915, "lng": 77.6968, "link": "https://careers.ti.com", "role": "Embedded Engineer", "salary": "₹8-18 LPA"},
                {"company": "Bosch", "location": "Bangalore", "lat": 12.9340, "lng": 77.6190, "link": "https://bosch.careers", "role": "Firmware Engineer", "salary": "₹7-15 LPA"}
            ]
        },
        "VLSI Design Engineer": {
            "description": "Design integrated circuits and semiconductor chips for modern electronics.",
            "skills_needed": ["Verilog", "VHDL", "FPGA", "ASIC", "Timing Analysis", "Cadence", "Synopsys"],
            "salary_range": "₹5L - ₹35L",
            "growth": "High",
            "icon": "⚡",
            "jobs": [
                {"company": "Intel", "location": "Bangalore", "lat": 12.8774, "lng": 77.6380, "link": "https://jobs.intel.com", "role": "VLSI Engineer", "salary": "₹12-25 LPA"},
                {"company": "Qualcomm", "location": "Hyderabad", "lat": 17.4435, "lng": 78.3773, "link": "https://qualcomm.com/careers", "role": "ASIC Design", "salary": "₹15-28 LPA"}
            ]
        }
    },
    "AIML": {
        "Machine Learning Engineer": {
            "description": "Build and deploy ML models at scale for production systems.",
            "skills_needed": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "SQL", "Docker", "MLOps", "Statistics"],
            "salary_range": "₹8L - ₹60L",
            "growth": "Explosive",
            "icon": "🧠",
            "jobs": [
                {"company": "NVIDIA", "location": "Bangalore", "lat": 12.9260, "lng": 77.6720, "link": "https://nvidia.com/careers", "role": "ML Engineer", "salary": "₹20-40 LPA"},
                {"company": "OpenAI", "location": "Remote", "lat": 0, "lng": 0, "link": "https://openai.com/careers", "role": "AI Engineer", "salary": "₹40-80 LPA"}
            ]
        },
        "AI Research Scientist": {
            "description": "Conduct cutting-edge research to advance artificial intelligence capabilities.",
            "skills_needed": ["Python", "Deep Learning", "Transformers", "NLP", "Computer Vision", "PyTorch", "Research Papers"],
            "salary_range": "₹12L - ₹1Cr",
            "growth": "Explosive",
            "icon": "🔬",
            "jobs": [
                {"company": "Google DeepMind", "location": "Remote", "lat": 0, "lng": 0, "link": "https://deepmind.com/careers", "role": "Research Scientist", "salary": "₹50-1Cr"},
                {"company": "Meta AI", "location": "Remote", "lat": 0, "lng": 0, "link": "https://meta.com/careers", "role": "AI Researcher", "salary": "₹45-80 LPA"}
            ]
        },
        "Computer Vision Engineer": {
            "description": "Build systems that enable machines to interpret visual information.",
            "skills_needed": ["Python", "OpenCV", "PyTorch", "CNN", "Image Processing", "YOLO", "TensorFlow"],
            "salary_range": "₹7L - ₹45L",
            "growth": "Very High",
            "icon": "👁️",
            "jobs": [
                {"company": "Tesla", "location": "Remote", "lat": 0, "lng": 0, "link": "https://tesla.com/careers", "role": "CV Engineer", "salary": "₹30-60 LPA"},
                {"company": "NVIDIA", "location": "Bangalore", "lat": 12.9260, "lng": 77.6720, "link": "https://nvidia.com/careers", "role": "Vision Engineer", "salary": "₹20-40 LPA"}
            ]
        },
        "NLP Engineer": {
            "description": "Build natural language processing systems for text analysis and generation.",
            "skills_needed": ["Python", "NLP", "Transformers", "BERT", "GPT", "PyTorch", "NLTK", "SpaCy"],
            "salary_range": "₹8L - ₹50L",
            "growth": "Very High",
            "icon": "📝",
            "jobs": [
                {"company": "Google", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://careers.google.com", "role": "NLP Engineer", "salary": "₹25-45 LPA"},
                {"company": "Microsoft", "location": "Hyderabad", "lat": 17.4401, "lng": 78.3489, "link": "https://careers.microsoft.com", "role": "NLP Scientist", "salary": "₹22-40 LPA"}
            ]
        },
        "Data Engineer": {
            "description": "Build and maintain data pipelines for large-scale data processing.",
            "skills_needed": ["Python", "SQL", "Spark", "Kafka", "Airflow", "AWS", "Hadoop"],
            "salary_range": "₹6L - ₹40L",
            "growth": "High",
            "icon": "🔄",
            "jobs": [
                {"company": "Amazon", "location": "Bangalore", "lat": 12.9915, "lng": 77.6968, "link": "https://amazon.jobs", "role": "Data Engineer", "salary": "₹15-30 LPA"},
                {"company": "Uber", "location": "Bangalore", "lat": 12.9716, "lng": 77.5946, "link": "https://uber.com/careers", "role": "Big Data Engineer", "salary": "₹18-35 LPA"}
            ]
        },
        "Prompt Engineer": {
            "description": "Design and optimize prompts for large language models and generative AI.",
            "skills_needed": ["Python", "LLMs", "GPT", "Claude", "LangChain", "API Integration", "Prompt Design"],
            "salary_range": "₹6L - ₹35L",
            "growth": "High",
            "icon": "✨",
            "jobs": [
                {"company": "Anthropic", "location": "Remote", "lat": 0, "lng": 0, "link": "https://anthropic.com/careers", "role": "Prompt Engineer", "salary": "₹20-40 LPA"},
                {"company": "OpenAI", "location": "Remote", "lat": 0, "lng": 0, "link": "https://openai.com/careers", "role": "AI Prompt Specialist", "salary": "₹25-50 LPA"}
            ]
        }
    },
    "Pharmaceutical Chemistry": {
        "Medicinal Chemist": {
            "description": "Design and synthesize new drug molecules for pharmaceutical applications.",
            "skills_needed": ["Organic Chemistry", "Spectroscopy", "HPLC", "Molecular Modeling", "Drug Design", "Synthesis"],
            "salary_range": "₹4L - ₹30L",
            "growth": "High",
            "icon": "🧪",
            "jobs": [
                {"company": "Novartis", "location": "Hyderabad", "lat": 17.4065, "lng": 78.3170, "link": "https://novartis.com/careers", "role": "Medicinal Chemist", "salary": "₹8-15 LPA"},
                {"company": "Dr. Reddy's", "location": "Hyderabad", "lat": 17.5379, "lng": 78.3744, "link": "https://drreddys.com/careers", "role": "Research Scientist", "salary": "₹6-12 LPA"}
            ]
        },
        "Analytical Chemist": {
            "description": "Analyze pharmaceutical compounds using advanced analytical techniques.",
            "skills_needed": ["HPLC", "GC-MS", "Spectroscopy", "Method Validation", "GMP", "Quality Control"],
            "salary_range": "₹3L - ₹18L",
            "growth": "Medium",
            "icon": "🔬",
            "jobs": [
                {"company": "Cipla", "location": "Mumbai", "lat": 19.0760, "lng": 72.8777, "link": "https://cipla.com/careers", "role": "Analytical Chemist", "salary": "₹5-10 LPA"},
                {"company": "Sun Pharma", "location": "Mumbai", "lat": 19.0760, "lng": 72.8777, "link": "https://sunpharma.com/careers", "role": "QC Chemist", "salary": "₹4-8 LPA"}
            ]
        }
    },
    "Pharmacology": {
        "Clinical Research Associate": {
            "description": "Manage and monitor clinical trials for drug development and safety.",
            "skills_needed": ["Clinical Trials", "GCP", "ICH Guidelines", "Medical Terminology", "Data Management", "Pharmacovigilance"],
            "salary_range": "₹4L - ₹20L",
            "growth": "High",
            "icon": "🏥",
            "jobs": [
                {"company": "IQVIA", "location": "Mumbai", "lat": 19.1136, "lng": 72.8697, "link": "https://iqvia.com/careers", "role": "CRA", "salary": "₹5-10 LPA"},
                {"company": "Syneos Health", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://syneoshealth.com/careers", "role": "Clinical Research Associate", "salary": "₹5-9 LPA"}
            ]
        },
        "Pharmacovigilance Specialist": {
            "description": "Monitor drug safety and manage adverse event reporting.",
            "skills_needed": ["MedDRA", "Drug Safety", "Adverse Events", "Regulatory Reporting", "Signal Detection"],
            "salary_range": "₹3.5L - ₹18L",
            "growth": "High",
            "icon": "💊",
            "jobs": [
                {"company": "Wipro Life Sciences", "location": "Bangalore", "lat": 12.9698, "lng": 77.7500, "link": "https://wipro.com/careers", "role": "PV Specialist", "salary": "₹4-9 LPA"},
                {"company": "Cognizant", "location": "Chennai", "lat": 13.0827, "lng": 80.2707, "link": "https://cognizant.com/careers", "role": "Drug Safety Associate", "salary": "₹4-8 LPA"}
            ]
        }
    }
}

# ============================================================
# DYNAMIC INTERVIEW QUESTIONS - Changes based on skills
# ============================================================

def get_interview_questions(career, skills):
    """Generate interview questions based on career and user's skills"""
    skills_lower = [s.lower() for s in skills]
    
    # Technology-specific questions
    tech_questions = []
    if any(s in skills_lower for s in ['java', 'javascript', 'react', 'nodejs', 'html', 'css']):
        if 'javascript' in str(skills_lower):
            tech_questions.append({"q": "Explain closures in JavaScript and how they work.", "tip": "Closures allow functions to access variables from outer scope even after the outer function has returned."})
        if 'react' in str(skills_lower):
            tech_questions.append({"q": "What is the Virtual DOM and how does React use it?", "tip": "Virtual DOM is a lightweight copy of the real DOM that React uses to optimize updates."})
        if 'nodejs' in str(skills_lower):
            tech_questions.append({"q": "Explain the event-driven architecture of Node.js.", "tip": "Node.js uses an event loop to handle asynchronous operations non-blocking."})
        if 'java' in str(skills_lower):
            tech_questions.append({"q": "What are the principles of OOP in Java?", "tip": "Encapsulation, Inheritance, Polymorphism, and Abstraction."})
        if 'html' in str(skills_lower) or 'css' in str(skills_lower):
            tech_questions.append({"q": "Explain CSS Box Model and Flexbox.", "tip": "Box model: margin, border, padding, content. Flexbox for 1D layouts."})
    
    # Base questions for the career
    base_questions = {
        "Software Engineer": [
            {"q": "Explain the difference between TCP and UDP.", "tip": "TCP is connection-oriented, reliable; UDP is connectionless, faster."},
            {"q": "What is the time complexity of binary search?", "tip": "O(log n) - divides search space in half each time."},
            {"q": "Explain REST API design principles.", "tip": "Stateless, client-server, cacheable, uniform interface."}
        ],
        "Frontend Developer": [
            {"q": "What is the difference between localStorage and sessionStorage?", "tip": "localStorage persists until deleted, sessionStorage clears on tab close."},
            {"q": "Explain the event loop in JavaScript.", "tip": "Event loop handles async operations, callback queue, and call stack."},
            {"q": "What are React hooks? Give examples.", "tip": "useState, useEffect, useContext allow functional components to have state."}
        ],
        "Backend Developer": [
            {"q": "What is the difference between SQL and NoSQL databases?", "tip": "SQL is relational, structured; NoSQL is flexible, document-based."},
            {"q": "Explain middleware in Express.js.", "tip": "Functions that execute during request-response cycle."},
            {"q": "What is JWT and how is it used?", "tip": "JSON Web Token for authentication and information exchange."}
        ],
        "Full Stack Developer": [
            {"q": "Explain the MVC architecture.", "tip": "Model-View-Controller separates data, UI, and business logic."},
            {"q": "What is CORS and how do you handle it?", "tip": "Cross-Origin Resource Sharing - configure server headers."},
            {"q": "Explain the difference between PUT and PATCH.", "tip": "PUT replaces entire resource, PATCH partially updates."}
        ]
    }
    
    # Get career-specific questions
    career_questions = base_questions.get(career, [
        {"q": f"What interests you about a career in {career}?", "tip": "Connect your passion and skills to the role."},
        {"q": "Tell us about a challenging project you worked on.", "tip": "Use STAR method: Situation, Task, Action, Result."},
        {"q": "Where do you see yourself in 5 years?", "tip": "Show ambition aligned with company growth."}
    ])
    
    # Combine and return (max 6 questions)
    all_questions = career_questions[:3] + tech_questions[:3]
    return all_questions[:6]

# ============================================================
# CAREER MATCHING ENGINE
# ============================================================

def calculate_match_percentage(user_skills, user_interests, career_skills):
    """Calculate skill match percentage for a career"""
    user_skills_lower = [s.lower().strip() for s in user_skills]
    career_skills_lower = [s.lower() for s in career_skills]
    
    # Calculate skill overlap
    matched = 0
    for us in user_skills_lower:
        for cs in career_skills_lower:
            if us in cs or cs in us:
                matched += 1
                break
    
    match_percent = min(98, int((matched / max(len(career_skills_lower), 1)) * 100)) if len(career_skills_lower) > 0 else 50
    return max(20, match_percent)

def recommend_careers(branch, domain, skills, interests):
    """Recommend careers based on rule-based scoring"""
    branch_data = CAREER_DATA.get(branch, {})
    if not branch_data:
        return []
    
    results = []
    for career_name, career_info in branch_data.items():
        # Calculate skill match
        skill_match = calculate_match_percentage(skills, interests, career_info.get("skills_needed", []))
        
        # Calculate interest match
        interest_match = 0
        career_text = (career_name + " " + career_info.get("description", "")).lower()
        for interest in interests:
            if interest.lower() in career_text:
                interest_match += 15
        interest_match = min(40, interest_match)
        
        # Domain match bonus
        domain_match = 20 if domain and domain.lower() in career_text else 0
        
        # Final score
        total_match = min(98, skill_match + interest_match + domain_match)
        
        results.append({
            "career": career_name,
            "match_percent": total_match,
            "skill_match": skill_match,
            "description": career_info.get("description", ""),
            "skills_needed": career_info.get("skills_needed", [])[:10],
            "salary_range": career_info.get("salary_range", ""),
            "growth": career_info.get("growth", ""),
            "icon": career_info.get("icon", "🎯"),
            "jobs": career_info.get("jobs", [])
        })
    
    # Sort by match percentage
    results.sort(key=lambda x: x["match_percent"], reverse=True)
    return results[:12]  # Return top 12 careers

# ============================================================
# FLASK ROUTES
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    branch = data.get('branch', '')
    domain = data.get('domain', '')
    skills = data.get('skills', [])
    interests = data.get('interests', [])
    name = data.get('name', 'Student')
    
    results = recommend_careers(branch, domain, skills, interests)
    
    session['last_results'] = {
        'name': name,
        'branch': branch,
        'skills': skills,
        'interests': interests,
        'results': results,
        'timestamp': datetime.now().strftime("%d %B %Y, %I:%M %p")
    }
    
    return jsonify({'success': True, 'results': results, 'name': name})

@app.route('/api/jobs', methods=['POST'])
def get_jobs():
    data = request.get_json()
    career_name = data.get('career', '')
    branch = data.get('branch', '')
    
    branch_data = CAREER_DATA.get(branch, {})
    for career, info in branch_data.items():
        if career == career_name:
            return jsonify({'success': True, 'jobs': info.get('jobs', []), 'career': career})
    
    return jsonify({'success': False, 'jobs': []})

@app.route('/api/interview-questions', methods=['POST'])
def interview_questions():
    data = request.get_json()
    career = data.get('career', '')
    skills = data.get('skills', [])
    
    questions = get_interview_questions(career, skills)
    return jsonify({'success': True, 'questions': questions, 'career': career})

@app.route('/api/trending')
def trending_careers():
    trending = [
        {"career": "Full Stack Developer", "branch": "CSE", "demand": 96, "icon": "🌐", "growth": "+45%"},
        {"career": "Machine Learning Engineer", "branch": "AIML/CSE", "demand": 95, "icon": "🧠", "growth": "+50%"},
        {"career": "Frontend Developer", "branch": "CSE", "demand": 92, "icon": "🎨", "growth": "+38%"},
        {"career": "Backend Developer", "branch": "CSE", "demand": 91, "icon": "⚙️", "growth": "+40%"},
        {"career": "Data Scientist", "branch": "CSE/AIML", "demand": 90, "icon": "📊", "growth": "+42%"},
        {"career": "Cloud Architect", "branch": "CSE", "demand": 88, "icon": "☁️", "growth": "+35%"},
        {"career": "Cybersecurity Analyst", "branch": "CSE", "demand": 85, "icon": "🛡️", "growth": "+32%"},
        {"career": "Embedded Engineer", "branch": "ECE", "demand": 82, "icon": "🔧", "growth": "+25%"},
        {"career": "NLP Engineer", "branch": "AIML", "demand": 84, "icon": "📝", "growth": "+48%"},
        {"career": "DevOps Engineer", "branch": "CSE", "demand": 86, "icon": "🔄", "growth": "+36%"}
    ]
    return jsonify({'trending': trending})

@app.route('/api/skills-quiz', methods=['POST'])
def skills_quiz():
    data = request.get_json()
    branch = data.get('branch', 'CSE')
    
    quiz_bank = {
        "CSE": [
            {"q": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "None"], "ans": 0},
            {"q": "Which of the following is a JavaScript framework?", "options": ["Django", "React", "Flask", "Spring"], "ans": 1},
            {"q": "What does CSS stand for?", "options": ["Creative Style Sheets", "Cascading Style Sheets", "Computer Style Sheets", "None"], "ans": 1},
            {"q": "Which company developed Java?", "options": ["Microsoft", "Apple", "Sun Microsystems", "Google"], "ans": 2},
            {"q": "What is Node.js used for?", "options": ["Frontend only", "Backend JavaScript", "Database", "Styling"], "ans": 1}
        ]
    }
    
    questions = quiz_bank.get(branch, quiz_bank["CSE"])
    return jsonify({'questions': questions})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)