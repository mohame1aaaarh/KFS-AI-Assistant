#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
err()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

info "بدء تجهيز KFS AI Assistant..."

# ── 1. التأكد من Python ──
command -v python3 &>/dev/null || err "Python 3 غير موجود. حمّله من https://python.org"
info "✅ Python 3 موجود"

# ── 2. تثبيت الحزم ──
if [ ! -f "backend/requirements.txt" ]; then err "ملف requirements.txt غير موجود"; fi
pip3 install -q -r backend/requirements.txt 2>/dev/null || pip install -q -r backend/requirements.txt
ok "الحزم مثبتة"

# ── 3. التأكد من config.py ──
if [ ! -f "backend/config.py" ]; then
    cp backend/config.example.py backend/config.py
    info "تم إنشاء backend/config.py من القالب"
    echo ""
    echo -e "  ${CYAN}→ افتح backend/config.py${NC}"
    echo -e "  ${CYAN}→ ضع مفتاح Gemini API مكان:${NC} AIzaSyYourActualKeyGoesHere"
    echo -e "  ${CYAN}→ احصل على مفتاح من:${NC} https://ai.google.dev"
    echo ""
    read -rp "هل وضعت المفتاح؟ اضغط Enter للمتابعة بعد الحفظ... "
else
    ok "config.py موجود"
fi

# ── 4. التأكد من ChromaDB ──
if [ -d "chroma_db" ] && [ "$(ls -A chroma_db 2>/dev/null)" ]; then
    ok "قاعدة البيانات المتجهة موجودة"
else
    info "لم يتم العثور على chroma_db. جارٍ تشغيل ingest.py..."
    cd backend && python3 ingest.py && cd "$ROOT_DIR"
    ok "تم بناء قاعدة البيانات"
fi

# ── 5. تشغيل السيرفر ──
echo ""
info "🚀 شغّل السيرفر:"
echo ""
echo -e "  ${CYAN}cd backend && uvicorn app:app --reload${NC}"
echo ""
echo -e "  ثم افتح ${CYAN}http://localhost:8000${NC} في المتصفح"
echo ""
