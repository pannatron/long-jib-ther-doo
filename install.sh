#!/usr/bin/env bash
# long-jib-ther-doo installer for Claude Code
# Usage: curl -sSL https://github.com/pannatron/long-jib-ther-doo/raw/main/install.sh | bash
set -euo pipefail

SKILL_NAME="long-jib-ther-doo"
SKILL_PARENT="$HOME/.claude/skills"
SKILL_DIR="$SKILL_PARENT/$SKILL_NAME"
RELEASE_URL="https://github.com/pannatron/${SKILL_NAME}/releases/latest/download/${SKILL_NAME}.skill"

c_green=$'\033[0;32m'
c_yellow=$'\033[0;33m'
c_red=$'\033[0;31m'
c_dim=$'\033[2m'
c_off=$'\033[0m'

err() { printf "${c_red}error:${c_off} %s\n" "$1" >&2; exit 1; }
info() { printf "${c_dim}→${c_off} %s\n" "$1"; }
ok() { printf "${c_green}✓${c_off} %s\n" "$1"; }

if ! command -v python3 >/dev/null 2>&1; then
    err "python3 not found. Install Python 3.10+ first (e.g. brew install python)."
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
    err "Python 3.10+ required, found $PY_VERSION"
fi

if ! command -v unzip >/dev/null 2>&1; then
    err "unzip not found. Install with 'brew install unzip' or your package manager."
fi

if ! command -v curl >/dev/null 2>&1; then
    err "curl not found."
fi

info "Python $PY_VERSION ✓"
info "Target: $SKILL_DIR"

if [ -d "$SKILL_DIR" ]; then
    printf "${c_yellow}!${c_off} Existing install found at $SKILL_DIR\n"
    printf "  Overwrite? [y/N] "
    read -r confirm </dev/tty
    case "$confirm" in
        [yY]|[yY][eE][sS]) ;;
        *) err "Aborted." ;;
    esac
    rm -rf "$SKILL_DIR"
fi

mkdir -p "$SKILL_PARENT"

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

info "Downloading latest release..."
if ! curl -fsSL -o "$TMPDIR/skill.zip" "$RELEASE_URL"; then
    err "Failed to download from $RELEASE_URL — no release published yet?"
fi

info "Extracting..."
unzip -q "$TMPDIR/skill.zip" -d "$SKILL_PARENT"

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    err "Install looks broken — SKILL.md not found in $SKILL_DIR"
fi

if [ -d "$SKILL_DIR/bin" ]; then
    chmod +x "$SKILL_DIR/bin/"* 2>/dev/null || true
fi

ok "Installed at $SKILL_DIR"
echo ""
echo "Test it:"
echo "  $SKILL_DIR/bin/analyze \"ทำไมไม่ทักมาบ้าง\""
echo ""
echo "Start a new Claude Code session and try:"
echo "  ${c_dim}>${c_off} \"ช่วยดูข้อความที่ผมจะส่งหน่อย: ...\""
echo "  ${c_dim}>${c_off} \"นี่แชตที่คุยกัน ช่วยอ่านสัญญาณให้หน่อย\""
