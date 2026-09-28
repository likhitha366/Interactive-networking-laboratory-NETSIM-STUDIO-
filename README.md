# CN Activity (NetSim Studio)

## Run from VS Code on Windows

1. Open this project folder in VS Code.
2. Choose **Terminal → Run Task… → CN Activity: Start server**. You can also press **Ctrl+Shift+B** and select that task.
3. Wait for `NetSim Studio is running at http://127.0.0.1:5000` in the terminal.
4. Open http://127.0.0.1:5000 in a browser.
5. Leave the server task running while using the site. Press Ctrl+C in its terminal to stop it.

The launcher uses the project-local JDK when available. If you clone the repository, install JDK 21 and set `JAVA_HOME` to its folder before running. The browser simulations work offline.

## Run outside VS Code

Double-click `run-java.bat` from File Explorer and open http://127.0.0.1:5000. Keep its command window open while using the site.

## Optional Flask backend

The project also contains a Flask API in `app.py`. Install Python 3, then run:

```powershell
py -3 -m pip install -r requirements.txt
py -3 app.py
```
