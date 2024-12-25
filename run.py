from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

API_KEY = "AIzaSyClJtgCTgqrGZ7q5q1mfZFLZuhq7-0yM_8"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/ask', methods=['POST'])
def ask_gemini():
    try:
        # Get question from request body
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({"error": "Question is required"}), 400

        # Prepare Gemini API payload
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{question}"
                }]
            }]
        }

        # Call Gemini API
        response = requests.post(
            GEMINI_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        
        result = response.json()
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        
        return jsonify({"answer": answer})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Gemini API error: {str(e)}"}), 500
    except KeyError as e:
        return jsonify({"error": f"Error parsing response: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    # Remove the direct Flask run
    # app.run(debug=True, port=5000)
    
    # The app variable will be used by Gunicorn
    pass
