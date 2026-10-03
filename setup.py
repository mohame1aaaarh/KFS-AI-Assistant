#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

def clr(code): return f"\033[{code}m" if os.name != "nt" else ""

def info(msg):  print(f"{clr(36)}[INFO]{clr(0)} {msg}")
def ok(msg):    print(f"{clr(32)}[OK]{clr(0)} {msg}")
def err(msg):   print(f"{clr(31)}[ERROR]{clr(0)} {msg}"); sys.exit(1)

def pip_install(requirements):
    info("Installing required packages...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", requirements],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        err(f"Failed to install packages:\n{result.stderr}")
    ok("Packages installed successfully")

def ensure_config():
    config_py = os.path.join(ROOT, "backend", "config.py")
    example_py = os.path.join(ROOT, "backend", "config.example.py")
    if os.path.exists(config_py):
        ok("config.py already exists")
        return
    if not os.path.exists(example_py):
        err("config.example.py file not found")
    shutil.copy2(example_py, config_py)
    info(f"Created {config_py} from template")
    print(f"\n  {clr(36)}→ Open the file: backend/config.py{clr(0)}")
    print(f"  {clr(36)}→ Replace placeholder with your Gemini API key:{clr(0)} AIzaSyYourActualKeyGoesHere")
    print(f"  {clr(36)}→ Get an API key from:{clr(0)} https://ai.google.dev\n")
    input("  After saving your API key, press Enter to continue... ")

def ensure_chromadb():
    chroma_db = os.path.join(ROOT, "chroma_db")
    if os.path.isdir(chroma_db) and os.listdir(chroma_db):
        ok("Vector database already exists")
        return
    info("chroma_db not found. Running ingest.py...")
    ingest_path = os.path.join(ROOT, "backend", "ingest.py")
    if not os.path.exists(ingest_path):
        err("ingest.py file not found")
    result = subprocess.run([sys.executable, ingest_path], cwd=os.path.join(ROOT, "backend"))
    if result.returncode != 0:
        err("Failed to run ingest.py")
    ok("Database built successfully")

def start_server():
    print(f"\n{'='*50}")
    print(f"  {clr(36)}KFS AI Assistant — Starting server...{clr(0)}")
    print(f"{'='*50}\n")
    print(f"  Server is running at: {clr(36)}http://localhost:8000{clr(0)}\n")
    
    backend_dir = os.path.join(ROOT, "backend")
    
    # Run uvicorn directly and keep the script listening for requests
    try:
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "app:app", "--reload"],
            cwd=backend_dir
        )
    except KeyboardInterrupt:
        print(f"\n{clr(31)}Server stopped.{clr(0)}")

def main():
    print(f"\n{clr(36)}Preparing KFS AI Assistant...{clr(0)}\n")

    if sys.version_info < (3, 10):
        err("Python 3.10 or newer is required")

    req_path = os.path.join(ROOT, "backend", "requirements.txt")
    if not os.path.exists(req_path):
        err("requirements.txt file not found")
    pip_install(req_path)

    ensure_config()
    ensure_chromadb()
    
    # Start the server immediately instead of just printing instructions
    start_server()

if __name__ == "__main__":
    main()