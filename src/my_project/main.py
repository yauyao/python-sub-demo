from flask import Flask, jsonify
from src.my_project.subscriber import Subscriber

app = Flask(__name__)
sub = Subscriber()

@app.route("/subscribe/<channel>", methods=["POST"])
def switch_channel(channel):
    sub.subscribe(channel)
    return jsonify({"message": f"已切換到頻道 {channel}"}), 200

@app.route("/stop", methods=["POST"])
def stop():
    sub.stop()
    return jsonify({"message": "訂閱已停止"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)