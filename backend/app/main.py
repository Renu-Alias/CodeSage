import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from dotenv import load_dotenv
from app.analyzer import analyze_code
from app.gemini_service import analyze_with_gemini

load_dotenv()

# In-memory storage for submission logs so the user's dashboard updates dynamically!
SUBMISSION_HISTORY = [
    {
        "id": "1",
        "filename": "calculate_average.py",
        "language": "Python",
        "timestamp": "2 hours ago",
        "errors_count": 2,
        "suggestions_count": 2,
        "code": "def calculate_average(numbers):\n    total = sum(numbers)\n    # Bug: division without zero check\n    return total / len(numbers)"
    },
    {
        "id": "2",
        "filename": "auth_handler.js",
        "language": "JavaScript",
        "timestamp": "5 hours ago",
        "errors_count": 4,
        "suggestions_count": 3,
        "code": "function verifyUser(user) {\n  const token = user.token;\n  if(!token) return null\n  return jwt.decode(token)\n}"
    },
    {
        "id": "3",
        "filename": "data_processor.py",
        "language": "Python",
        "timestamp": "Yesterday",
        "errors_count": 1,
        "suggestions_count": 1,
        "code": "def process_data(data):\n    # Potential TypeError\n    return [d * 2.5 for d in data]"
    },
    {
        "id": "4",
        "filename": "api_endpoints.py",
        "language": "Python",
        "timestamp": "2 days ago",
        "errors_count": 7,
        "suggestions_count": 5,
        "code": "def get_items(req):\n    res = db.fetch_all()\n    return res"
    },
    {
        "id": "5",
        "filename": "utils_test.js",
        "language": "JavaScript",
        "timestamp": "3 days ago",
        "errors_count": 2,
        "suggestions_count": 1,
        "code": "test('math', () => {\n  expect(sum(1, 2)).toBe(3)\n})"
    }
]

class CodeSageHTTPHandler(BaseHTTPRequestHandler):
    def _safe_write(self, data: bytes):
        """Write response data, ignoring client disconnects."""
        try:
            self.wfile.write(data)
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass

    def end_headers(self):
        # Handle CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"app": "CodeSage AI API", "status": "online"}
            self._safe_write(json.dumps(response).encode('utf-8'))
            
        elif path == "/api/dashboard":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Calculate metrics
            total_uploads = len(SUBMISSION_HISTORY) + 42
            total_errors_found = sum(sub["errors_count"] for sub in SUBMISSION_HISTORY) + 112
            
            # Top language
            lang_counts = {}
            for sub in SUBMISSION_HISTORY:
                lang_counts[sub["language"]] = lang_counts.get(sub["language"], 0) + 1
            top_lang = max(lang_counts, key=lang_counts.get) if lang_counts else "Python"
            
            dashboard_data = {
                "metrics": {
                    "totalUploads": total_uploads,
                    "errorsFound": total_errors_found,
                    "errorsThisWeek": 12,
                    "errorsThisWeekChange": "-8%",
                    "topLanguage": top_lang
                },
                "recentUploads": SUBMISSION_HISTORY,
                "weaknessReport": [
                    { "topic": "Loop logic", "count": 23, "badge": "PRACTICE THIS" },
                    { "topic": "Null / zero handling", "count": 14, "badge": "PRACTICE THIS" },
                    { "topic": "Variable scoping", "count": 8, "badge": "PRACTICE THIS" }
                ],
                "badges": [
                    {"id": "first_upload", "name": "First upload", "icon": "rocket", "unlocked": True},
                    {"id": "uploads_10", "name": "10 uploads", "icon": "award", "unlocked": True},
                    {"id": "week_streak", "name": "Week streak", "icon": "flame", "unlocked": True},
                    {"id": "bug_hunter", "name": "Bug hunter", "icon": "bug", "unlocked": False}
                ],
                "errorsOverTime": [
                    {"week": "Week 1", "errors": 50},
                    {"week": "Week 2", "errors": 45},
                    {"week": "Week 3", "errors": 35},
                    {"week": "Week 4", "errors": 25},
                    {"week": "Week 5", "errors": 20},
                    {"week": "Week 6", "errors": 18},
                    {"week": "Week 7", "errors": 15},
                    {"week": "Week 8", "errors": 12}
                ]
            }
            self._safe_write(json.dumps(dashboard_data).encode('utf-8'))
            
        elif path.startswith("/api/submission/"):
            sub_id = path.split("/")[-1]
            found_sub = None
            for sub in SUBMISSION_HISTORY:
                if sub["id"] == sub_id:
                    found_sub = sub
                    break
            
            if found_sub:
                if "analysis" not in found_sub:
                    found_sub["analysis"] = analyze_code(found_sub["code"], found_sub["language"], "Beginner")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self._safe_write(json.dumps(found_sub).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self._safe_write(json.dumps({"detail": "Submission not found"}).encode('utf-8'))
                
        elif path == "/api/pricing":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            pricing_data = {
                "plans": [
                    {
                        "id": "free",
                        "name": "Free",
                        "descriptor": "Perfect for getting started",
                        "priceMonthly": 0,
                        "priceYearly": 0,
                        "features": ["10 analyses", "3 languages", "Basic detection", "30-day history"],
                        "cta": "Get started"
                    },
                    {
                        "id": "pro",
                        "name": "Pro",
                        "descriptor": "For serious learners",
                        "priceMonthly": 299,
                        "priceYearly": 239,
                        "features": ["Unlimited analyses", "All languages", "Weakness report", "Full history", "Priority AI", "Beginner/Intermediate modes"],
                        "cta": "Upgrade to Pro",
                        "popular": True
                    },
                    {
                        "id": "classroom",
                        "name": "Classroom",
                        "descriptor": "For teachers and institutions",
                        "priceMonthly": 999,
                        "priceYearly": 799,
                        "features": ["30 students included", "Teacher dashboard", "Class-wide reports", "Assignment mode", "Everything in Pro"],
                        "cta": "Contact us"
                    }
                ],
                "faqs": [
                    {
                        "question": "Can I switch plans anytime?",
                        "answer": "Yes, you can upgrade, downgrade, or cancel your subscription at any time. When you change plans, your access will be adjusted immediately and billing will be prorated."
                    },
                    {
                        "question": "Is there a student discount?",
                        "answer": "CodeSage is built for students! Our Pro plan is already heavily discounted by 70% compared to standard developer tools. If you need institutional support, contact your university for Classroom billing."
                    },
                    {
                        "question": "What languages are supported?",
                        "answer": "We support Python, JavaScript, Java, C++, TypeScript, Go, Rust, and many other programming languages. Auto-detection is built into our analyzer."
                    },
                    {
                        "question": "How does the weakness report work?",
                        "answer": "Every time you analyze code, we categorize the errors. Over time, the weakness engine generates reports showing patterns like confusion in loop conditions or unhandled boundary cases, complete with targeted exercises."
                    }
                ]
            }
            self._safe_write(json.dumps(pricing_data).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self._safe_write(json.dumps({"detail": "Not Found"}).encode('utf-8'))

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/analyze":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                code = data.get("code", "")
                language = data.get("language", "Python")
                mode = data.get("mode", "Beginner")
                filename = data.get("filename", "untitled.py")
                
                if not code:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self._safe_write(json.dumps({"detail": "Code cannot be empty"}).encode('utf-8'))
                    return
                
                # Run analyzer (try Gemini AI first, fall back to local heuristics)
                result = analyze_with_gemini(code, language, mode) or analyze_code(code, language, mode)
                
                # Append to dynamic history
                new_sub_id = str(len(SUBMISSION_HISTORY) + 1)
                new_sub = {
                    "id": new_sub_id,
                    "filename": filename if filename else f"code_{new_sub_id}.py",
                    "language": language,
                    "timestamp": "Just now",
                    "errors_count": len(result["errors"]),
                    "suggestions_count": len(result["suggestions"]),
                    "code": code,
                    "analysis": result
                }
                SUBMISSION_HISTORY.insert(0, new_sub)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response_data = {
                    "success": True,
                    "id": new_sub_id,
                    "filename": new_sub["filename"],
                    "errors_count": len(result["errors"]),
                    "suggestions_count": len(result["suggestions"]),
                    "analysis": result
                }
                self._safe_write(json.dumps(response_data).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self._safe_write(json.dumps({"detail": str(e)}).encode('utf-8'))
        elif path == "/api/create-subscription":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                email = data.get("email", "")
                plan = data.get("plan", "Pro")
                cycle = data.get("billingCycle", "monthly")
                amount = data.get("amount", 299)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response_data = {
                    "success": True,
                    "message": f"Successfully subscribed {email} to {plan} plan ({cycle})!",
                    "subscription": {
                        "plan": plan,
                        "billingCycle": cycle,
                        "amount": amount,
                        "status": "Active"
                    }
                }
                self._safe_write(json.dumps(response_data).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self._safe_write(json.dumps({"detail": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self._safe_write(json.dumps({"detail": "Not Found"}).encode('utf-8'))

def run_server(port=None):
    if port is None:
        port = int(os.getenv("BACKEND_PORT", 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, CodeSageHTTPHandler)
    print(f"CodeSage Native Python Server running on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Server stopped.")

if __name__ == '__main__':
    run_server()
