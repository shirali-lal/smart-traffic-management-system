from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

# Home route (loads website)
@app.route("/")
def home():
    return render_template("index.html")

# Traffic data route
@app.route("/traffic")
def traffic():
    try:
        # Read latest data from detection.py
        with open("data.json") as f:
            data = json.load(f)

        l1 = data.get("lane1", 0)
        l2 = data.get("lane2", 0)
        l3 = data.get("lane3", 0)
        l4 = data.get("lane4", 0)
        emergency = data.get("emergency", 0)

        # 🚑 Emergency override
        if emergency == 1:
            result = "Emergency → GREEN SIGNAL"
        else:
            # Find lane with max vehicles
            lanes = [l1, l2, l3, l4]
            green_lane = lanes.index(max(lanes)) + 1
            result = f"Green Signal Lane: {green_lane}"

        # Add result to response
        data["result"] = result

    except:
        # If file not ready yet
        data = {
            "lane1": 0,
            "lane2": 0,
            "lane3": 0,
            "lane4": 0,
            "result": "Waiting for data..."
        }

    return jsonify(data)


# Run server
if __name__ == "__main__":
    app.run(debug=True)