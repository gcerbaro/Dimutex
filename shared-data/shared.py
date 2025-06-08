from flask import Flask, request, jsonify
from logger import logger, Colors

app = Flask(__name__)
shared_data = {"value": 0}
NODE = "Server"

@app.route("/data", methods=["GET"])
def get_data():
    logger.info(f"{Colors.LIGHT_GRAY}[{NODE}] Sending Data: {shared_data["value"]}")
    return jsonify(shared_data)

@app.route("/data", methods=["POST"])
def set_data():
    content = request.json
    shared_data.update(content)
    logger.info(f"{Colors.LIGHT_GRAY}[{NODE}] Writing Data: {shared_data["value"]}")
    return jsonify({"status": "ok", "new_data": shared_data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
