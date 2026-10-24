from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(message="Hello from the DevSecOps pipeline demo")


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    # Bound to all interfaces so the container port mapping works.
    app.run(host="0.0.0.0", port=8080)  # nosec B104
