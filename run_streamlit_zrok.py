#!/usr/bin/env python3
import subprocess, time, socket, re, signal, sys

APP_FILE = "frontend/app.py"
PORT = 8501

# Set to True if you want to use a reserved share instead of ephemeral
USE_RESERVED = False
RESERVED_TOKEN = "YOUR_RESERVED_SHARE_TOKEN"  # only if USE_RESERVED is True

def wait_for_port(port, host="127.0.0.1", timeout=30):
    for _ in range(timeout):
        with socket.socket() as s:
            try:
                s.connect((host, port))
                return True
            except OSError:
                time.sleep(1)
    return False

def main():
    # Start Streamlit
    streamlit_cmd = [
        "streamlit", "run", APP_FILE,
        "--server.port", str(PORT),
        "--server.headless", "true"
    ]
    print("Starting Streamlit...")
    streamlit_proc = subprocess.Popen(streamlit_cmd)

    if not wait_for_port(PORT):
        print("Streamlit did not start within timeout.", file=sys.stderr)
        streamlit_proc.terminate()
        return

    # Start zrok share
    if USE_RESERVED:
        zrok_cmd = ["zrok", "share", "reserved", RESERVED_TOKEN]
    else:
        zrok_cmd = ["zrok", "share", "public", str(PORT)]

    print("Starting zrok share...")
    zrok_proc = subprocess.Popen(
        zrok_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    public_url = None
    try:
        # Read zrok output until we find the URL
        url_pattern = re.compile(r'https://\S+zrok\.io')
        for line in zrok_proc.stdout:
            print("[zrok]", line, end="")
            match = url_pattern.search(line)
            if match:
                public_url = match.group(0)
                print(f"\n✅ Public URL: {public_url}\nPress Ctrl+C to stop.\n")
                break

        # Keep processes alive until Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # Clean up
        for proc, name in [(zrok_proc, "zrok"), (streamlit_proc, "streamlit")]:
            if proc.poll() is None:
                try:
                    proc.send_signal(signal.SIGINT)
                    proc.wait(timeout=5)
                except Exception:
                    proc.kill()
        print("All processes stopped.")

if __name__ == "__main__":
    main()
