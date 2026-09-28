import heapq
from collections import defaultdict

POLYNOMIALS = {"CRC-12": "1100000001111", "CRC-16": "11000000000000101", "CRC-CCITT": "10001000000100001"}

def frame_message(message):
    flag, esc = "FLAG", "ESC"
    stuffed = message.replace("ESC", esc + esc).replace("#", esc + "#")
    bits = "".join(f"{ord(c):08b}" for c in message)
    out, run = [], 0
    for bit in bits:
        out.append(bit)
        run = run + 1 if bit == "1" else 0
        if run == 5:
            out.append("0"); run = 0
    return {"character_count": f"{len(message)} {message}", "character_stuffing": f"{flag} {stuffed} {flag}", "bit_stuffing": f"01111110 {''.join(out)} 01111110", "binary": bits}

def _xor(dividend, divisor):
    return "".join("0" if a == b else "1" for a, b in zip(dividend, divisor))

def crc_result(data, kind):
    data = "".join(c for c in str(data) if c in "01") or "0"
    poly = POLYNOMIALS.get(kind, POLYNOMIALS["CRC-16"])
    padded = data + "0" * (len(poly) - 1)
    work = padded[:len(poly)]
    steps = []
    for i in range(len(poly), len(padded) + 1):
        divisor = poly if work[0] == "1" else "0" * len(poly)
        work = _xor(work, divisor)[1:]
        steps.append(f"Step {i - len(poly) + 1}: remainder {work or '0'}")
        if i < len(padded): work += padded[i]
    remainder = work.zfill(len(poly)-1)
    return {"type": kind, "data": data, "polynomial": poly, "remainder": remainder, "codeword": data + remainder, "steps": steps[:8]}

def go_back_n(frames, window, lost):
    frames, window = max(1, min(frames, 30)), max(1, window)
    lost = int(lost) if str(lost).isdigit() and 1 <= int(lost) <= frames else None
    events = []
    for start in range(1, frames + 1, window):
        group = list(range(start, min(start + window, frames + 1)))
        for frame in group:
            events.append({"frame": frame, "state": "lost" if frame == lost else "sent"})
        if lost in group:
            events.append({"frame": lost, "state": "timeout"})
            for frame in range(lost, group[-1] + 1): events.append({"frame": frame, "state": "retransmitted"})
            lost = None
        else:
            events.append({"frame": group[-1], "state": "acknowledged"})
    return {"events": events, "summary": "Go-Back-N simulation complete"}

def parse_edges(text):
    graph = defaultdict(dict)
    for line in str(text).splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 3:
            a, b, cost = parts
            try: cost = int(cost)
            except ValueError: continue
            graph[a][b] = graph[b][a] = cost
    return graph

def dijkstra(edge_text, source, target):
    graph = parse_edges(edge_text)
    if source not in graph or target not in graph: return {"error": "Source and destination must be nodes in the graph."}
    distances, previous, queue = {source: 0}, {}, [(0, source)]
    while queue:
        cost, node = heapq.heappop(queue)
        if cost != distances[node]: continue
        for nxt, weight in graph[node].items():
            new = cost + weight
            if new < distances.get(nxt, float("inf")):
                distances[nxt], previous[nxt] = new, node; heapq.heappush(queue, (new, nxt))
    if target not in distances: return {"error": "No route exists."}
    path = [target]
    while path[-1] != source: path.append(previous[path[-1]])
    return {"path": list(reversed(path)), "cost": distances[target], "distances": distances}

def distance_vector(edge_text):
    graph = parse_edges(edge_text); nodes = sorted(graph)
    table = {n: {d: (0 if n == d else graph[n].get(d, 999)) for d in nodes} for n in nodes}
    rounds = 0
    while rounds < len(nodes):
        changed = False; updated = {n: dict(v) for n, v in table.items()}
        for node in nodes:
            for neighbor, weight in graph[node].items():
                for dest in nodes:
                    candidate = weight + table[neighbor][dest]
                    if candidate < updated[node][dest]: updated[node][dest] = candidate; changed = True
        table = updated; rounds += 1
        if not changed: break
    return {"nodes": nodes, "tables": table, "rounds": rounds, "infinity": 999}

def broadcast_edges(nodes, root):
    nodes = list(dict.fromkeys(nodes)); root = root if root in nodes else nodes[0]
    others = [n for n in nodes if n != root]
    return [[root, n] for n in others]

def caesar(message, shift):
    def transform(text, amount):
        result = []
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a'); result.append(chr((ord(ch)-base+amount)%26+base))
            else: result.append(ch)
        return ''.join(result)
    encrypted = transform(message, shift)
    return {"plain": message, "shift": shift, "encrypted": encrypted, "decrypted": transform(encrypted, -shift)}

def leaky_bucket(arrivals, capacity, rate):
    level = dropped = 0; history = []
    for tick, incoming in enumerate(arrivals, 1):
        accepted = min(incoming, max(0, capacity-level)); dropped_now = incoming-accepted; level += accepted
        sent = min(level, rate); level -= sent; dropped += dropped_now
        history.append({"tick": tick, "incoming": incoming, "sent": sent, "remaining": level, "dropped": dropped_now})
    return {"history": history, "total_dropped": dropped, "capacity": capacity, "rate": rate}

def sort_frames(frames):
    buffer, delivered = [], []
    expected = 1
    for frame in frames:
        buffer.append(frame); buffer.sort()
        while expected in buffer:
            buffer.remove(expected); delivered.append(expected); expected += 1
    return {"received": frames, "delivered": delivered, "buffer_remaining": buffer}
