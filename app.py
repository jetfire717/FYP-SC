from flask import Flask, request, jsonify
from optiguide_sc_v3 import process_query  # import the function you created

app = Flask(__name__)

@app.route("/optiguide", methods=["POST"])
def optiguide_endpoint():
    payload = request.get_json(force=True, silent=True) or {}
    user_text = payload.get("text") or payload.get("query") or ""
    if not user_text:
        return jsonify({"error": "Missing 'text' in JSON body"}), 400

    try:
        # Optionally allow reinit via a flag for dev: payload.get("reinit_files", False)
        result = process_query(user_text, reinit_files=False)
        return jsonify(result), 200
    except Exception as e:
        # Return a helpful error message (avoid leaking secrets)
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

if __name__ == "__main__":
    # For local testing only; in production use a WSGI server (gunicorn/uvicorn)
    app.run(host="0.0.0.0", port=5000, debug=True)