from flask import Flask, request, render_template_string
import json
import random
import string
import os

app = Flask(__name__)

# Set to False for production
app.config['DEBUG'] = False

# Use a secret key for sessions/cookies (generate a random one)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)

def generate_random_string(length=8):
    """Generate a random string of capital letters and numbers."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def get_browser_info():
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr
    
    # Parse user agent string to get browser type and version
    browser_type = "Unknown"
    browser_version = "Unknown"
    
    if "Firefox" in user_agent:
        browser_type = "Firefox"
        version_start = user_agent.index("Firefox/") + 8
        browser_version = user_agent[version_start:].split()[0]
    elif "Chrome" in user_agent:
        browser_type = "Chrome"
        version_start = user_agent.index("Chrome/") + 7
        browser_version = user_agent[version_start:].split()[0]
    elif "Safari" in user_agent:
        browser_type = "Safari"
        version_start = user_agent.index("Version/") + 8
        browser_version = user_agent[version_start:].split()[0]
    
    # Generate random string
    random_string = generate_random_string()
    
    info = {
        "Browser Type": browser_type,
        "Browser Version": browser_version,
        "User Agent": user_agent,
        "IP Address": ip_address,
        "Random String": random_string
    }
    
    return render_template_string(HTML_TEMPLATE, info=info)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Browser Info</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            width: 80%;
            max-width: 600px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 20px;
        }
        .info-item {
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
        .info-item strong {
            color: #007bff;
        }
        .random-string {
            text-align: center;
            font-size: 1.2em;
            margin-top: 20px;
            padding: 10px;
            background-color: #e9ecef;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Browser Information</h1>
        {% for key, value in info.items() %}
            {% if key != "Random String" %}
                <div class="info-item">
                    <strong>{{ key }}:</strong> {{ value }}
                </div>
            {% endif %}
        {% endfor %}
        <div class="random-string">
            <strong>Random String:</strong> {{ info["Random String"] }}
        </div>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    # Use environment variables for host and port
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host=host, port=port, threaded=True)
