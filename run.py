from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "AIzaSyClJtgCTgqrGZ7q5q1mfZFLZuhq7-0yM_8"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/ask', methods=['POST'])
def ask_gemini():
    try:
        print("hello")
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
    app.run(debug=True, port=5000)
