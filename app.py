from flask import Flask, jsonify, render_template, request
from algorithms.networking import (
    crc_result, dijkstra, distance_vector, frame_message, leaky_bucket,
    sort_frames, caesar, broadcast_edges, go_back_n
)

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/framing")
def framing():
    data = request.get_json() or {}
    return jsonify(frame_message(data.get("message", "HELLO#WORLD")))

@app.post("/api/crc")
def crc():
    data = request.get_json() or {}
    return jsonify(crc_result(data.get("data", "1101011011"), data.get("type", "CRC-16")))

@app.post("/api/sliding-window")
def sliding_window():
    data = request.get_json() or {}
    return jsonify(go_back_n(int(data.get("frames", 8)), int(data.get("window", 4)), data.get("lost")))

@app.post("/api/dijkstra")
def shortest_path():
    data = request.get_json() or {}
    edges = data.get("edges", "A,B,4\nA,C,2\nB,C,1\nB,D,5\nC,D,8\nC,E,10\nD,E,2")
    return jsonify(dijkstra(edges, data.get("source", "A"), data.get("target", "E")))

@app.post("/api/distance-vector")
def vector():
    data = request.get_json() or {}
    edges = data.get("edges", "A,B,4\nA,C,2\nB,C,1\nB,D,5\nC,D,8\nC,E,10\nD,E,2")
    return jsonify(distance_vector(edges))

@app.post("/api/broadcast")
def broadcast():
    data = request.get_json() or {}
    nodes = [x.strip() for x in data.get("nodes", "A,B,C,D,E").split(",") if x.strip()]
    return jsonify({"root": data.get("root", nodes[0] if nodes else "A"), "edges": broadcast_edges(nodes, data.get("root", "A"))})

@app.post("/api/encryption")
def encryption():
    data = request.get_json() or {}
    return jsonify(caesar(data.get("message", "NETWORKS"), int(data.get("shift", 3))))

@app.post("/api/leaky-bucket")
def bucket():
    data = request.get_json() or {}
    arrivals = [int(x) for x in str(data.get("arrivals", "4,8,2,9,3,6")).split(",") if x.strip()]
    return jsonify(leaky_bucket(arrivals, int(data.get("capacity", 10)), int(data.get("rate", 4))))

@app.post("/api/sort-frames")
def sorting():
    data = request.get_json() or {}
    frames = [int(x) for x in str(data.get("frames", "4,1,6,2,5,3")).split(",") if x.strip()]
    return jsonify(sort_frames(frames))

if __name__ == "__main__":
    app.run(debug=True)
