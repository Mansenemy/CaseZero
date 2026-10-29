"""
CaseZero Main Launcher.
Starts the local Python standard library HTTP server and launches the browser.
Run with:
    python main.py
"""

import sys
import time
import webbrowser
import threading
from server import run_server

def main():
    print("=" * 60)
    print("  CASEZERO — ALGORITHMIC FORENSIC INVESTIGATION")
    print("  Powered by Data Structures & Algorithms")
    print("=" * 60)

    try:
        server, port = run_server(8000)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

    url = f"http://127.0.0.1:{port}"
    print(f"\n[+] Local Server running at: {url}")
    print("[+] Launching interface in your default browser...")
    print("[!] Press Ctrl+C in this terminal to stop the server.\n")

    # Start server in daemon thread
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # Open browser
    time.sleep(0.5)
    webbrowser.open(url)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping CaseZero server. Goodbye, Detective.")
        server.shutdown()
        server.server_close()
        sys.exit(0)

if __name__ == "__main__":
    main()
