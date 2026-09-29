# NetSim Studio

NetSim Studio is an interactive computer networking laboratory project designed to visualize and explain core networking concepts through browser-based simulations. It is intended for academic use, lab demonstrations, and viva preparation.

The project includes a lightweight Java web server and a Flask-based API layer for common lab activities such as framing, CRC, routing, sliding window control, encryption, and congestion buffering.

## Features

- Data link layer framing
  - Character count
  - Character stuffing
  - Bit stuffing
- CRC generation and verification
  - CRC-12
  - CRC-16
  - CRC-CCITT
- Go-Back-N sliding window simulation
- Shortest path routing with Dijkstra
- Distance vector routing simulation
- Broadcast tree generation
- Caesar cipher demonstration
- Leaky bucket congestion control
- Frame sorting buffer simulation
- Safe educational examples for packet capture and network scanning concepts

## Project structure

```text
.
├── app.py                     # Flask API endpoints
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── run-java.bat              # Windows launcher for the Java server
├── algorithms/
│   └── networking.py         # Networking logic and simulations
├── java/
│   └── NetSimServer.java     # Local Java HTTP server
├── static/
│   ├── script.js             # Frontend logic for UI interactions
│   └── style.css            # Styling for the interface
├── templates/
│   └── index.html            # Main web application UI
└── build/                    # Generated Java build output (created at runtime)
```

## Requirements

- Windows OS (project is configured for Windows batch launch)
- JDK 21
- Python 3 (optional if using the Flask backend)

## Run the project

### Option 1: Run from VS Code

1. Open the project folder in VS Code.
2. Open the Command Palette and run the task named `CN Activity: Start server`.
3. Alternatively, use Terminal → Run Task… and select `CN Activity: Start server`.
4. Wait for the server message:

```text
NetSim Studio is running at http://127.0.0.1:5000
```

5. Open http://127.0.0.1:5000 in your browser.
6. Keep the terminal running while using the app.

### Option 2: Run directly from Windows Explorer

1. Double-click `run-java.bat`.
2. Open http://127.0.0.1:5000.
3. Keep the command window open while the app is in use.

### Option 3: Use the Flask backend directly

If you want to run the Python API independently, install dependencies and start Flask:

```powershell
py -3 -m pip install -r requirements.txt
py -3 app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Notes

- The project uses local browser-based simulations and does not require external internet access.
- The Java launcher automatically uses a project-local JDK when available.
- The app is educational and safe for lab use; packet capture and scanning examples are simulated rather than real network monitoring.

## Intended use

This project is suitable for:

- Computer Networks lab activities
- mini-project demonstration
- viva/practical explanation of networking algorithms
- visual learning of data link and routing concepts

## License

This project is intended for academic and educational use.

