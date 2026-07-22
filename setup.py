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
    info("تثبيت الحزم المطلوبة...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", requirements],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        err(f"فشل تثبيت الحزم:\n{result.stderr}")
    ok("الحزم مثبتة")

def ensure_config():
    config_py = os.path.join(ROOT, "backend", "config.py")
    example_py = os.path.join(ROOT, "backend", "config.example.py")
    if os.path.exists(config_py):
        ok("config.py موجود")
        return
    if not os.path.exists(example_py):
        err("ملف config.example.py غير موجود")
    shutil.copy2(example_py, config_py)
    info(f"تم إنشاء {config_py} من القالب")
    print(f"\n  {clr(36)}→ افتح الملف: backend/config.py{clr(0)}")
    print(f"  {clr(36)}→ ضع مفتاح Gemini API مكان:{clr(0)} AIzaSyYourActualKeyGoesHere")
    print(f"  {clr(36)}→ احصل على مفتاح من:{clr(0)} https://ai.google.dev\n")
    input("  بعد ما تحفظ المفتاح، اضغط Enter للمتابعة... ")

def ensure_chromadb():
    chroma_db = os.path.join(ROOT, "chroma_db")
    if os.path.isdir(chroma_db) and os.listdir(chroma_db):
        ok("قاعدة البيانات المتجهة موجودة")
        return
    info("chroma_db غير موجودة. جارٍ تشغيل ingest.py...")
    ingest_path = os.path.join(ROOT, "backend", "ingest.py")
    if not os.path.exists(ingest_path):
        err("ملف ingest.py غير موجود")
    result = subprocess.run([sys.executable, ingest_path], cwd=os.path.join(ROOT, "backend"))
    if result.returncode != 0:
        err("فشل تشغيل ingest.py")
    ok("تم بناء قاعدة البيانات")

def print_instructions():
    print(f"\n{'='*50}")
    print(f"  {clr(36)}KFS AI Assistant — جاهز للتشغيل{clr(0)}")
    print(f"{'='*50}")
    print(f"\n  شغّل السيرفر:")
    print(f"\n    {clr(36)}cd backend && {sys.executable} -m uvicorn app:app --reload{clr(0)}")
    print(f"\n  أو على ويندوز:")
    print(f"\n    {clr(36)}cd backend{clr(0)}")
    print(f"    {clr(36)}python -m uvicorn app:app --reload{clr(0)}")
    print(f"\n  ثم افتح {clr(36)}http://localhost:8000{clr(0)} في المتصفح\n")

def main():
    print(f"\n{clr(36)}بدء تجهيز KFS AI Assistant...{clr(0)}\n")

    if sys.version_info < (3, 10):
        err("مطلوب Python 3.10 أو أحدث")

    req_path = os.path.join(ROOT, "backend", "requirements.txt")
    if not os.path.exists(req_path):
        err("ملف requirements.txt غير موجود")
    pip_install(req_path)

    ensure_config()
    ensure_chromadb()
    print_instructions()

if __name__ == "__main__":
    main()
