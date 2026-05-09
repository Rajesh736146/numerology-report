"""Start both the FastAPI backend and Next.js frontend concurrently."""

import subprocess
import sys
import os
import signal
import threading

BACKEND_CMD = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
FRONTEND_CMD = ["npm", "run", "dev"]
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")


def stream(proc: subprocess.Popen, prefix: str):
    """Stream process output with a prefix label."""
    for line in iter(proc.stdout.readline, b""):
        print(f"[{prefix}] {line.decode(errors='replace').rstrip()}", flush=True)


def main():
    procs = []

    try:
        backend = subprocess.Popen(
            BACKEND_CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=os.path.dirname(__file__),
        )
        procs.append(backend)
        threading.Thread(target=stream, args=(backend, "backend"), daemon=True).start()
        print("[run] Backend started on http://localhost:8000", flush=True)

        frontend = subprocess.Popen(
            FRONTEND_CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=FRONTEND_DIR,
            shell=sys.platform == "win32",
        )
        procs.append(frontend)
        threading.Thread(target=stream, args=(frontend, "frontend"), daemon=True).start()
        print("[run] Frontend started on http://localhost:3000", flush=True)

        # Wait for either process to exit
        for proc in procs:
            proc.wait()

    except KeyboardInterrupt:
        print("\n[run] Shutting down…", flush=True)
    finally:
        for proc in procs:
            if proc.poll() is None:
                if sys.platform == "win32":
                    proc.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    proc.terminate()
        for proc in procs:
            proc.wait()
        print("[run] All processes stopped.", flush=True)


if __name__ == "__main__":
    main()
