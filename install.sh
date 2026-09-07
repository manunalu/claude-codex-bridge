#!/bin/sh
# Claude-Codex-Bruecke: Einrichtung in einem Befehl.
#
# Was passiert:
#   1. Claude wird als Werkzeug in Codex eingetragen (~/.codex/config.toml, MCP-Server "claude").
#   2. Codex wird als Werkzeug in Claude eingetragen (MCP-Server "codex").
#   3. Der Skill "claude-codex" wird nach ~/.agents/skills gelegt (Codex und Claude lesen ihn).
#   4. Die Weiche wird an ~/.codex/AGENTS.md und ~/.claude/CLAUDE.md angehaengt.
#
# Alles ist wiederholbar: bestehende Eintraege werden erkannt und nicht doppelt geschrieben.
# Von jeder geaenderten Datei wird vorher eine Sicherung angelegt (.bak-JJJJ-MM-TT-HHMMSS).
# Nichts wird geloescht. Rueckgaengig: siehe README, Abschnitt "Wieder entfernen".

set -u
HIER="$(cd "$(dirname "$0")" && pwd)"
STEMPEL="$(date +%Y-%m-%d-%H%M%S)"
ok() { printf '  ok   %s\n' "$1"; }
info() { printf '  ...  %s\n' "$1"; }
warn() { printf '  !    %s\n' "$1"; }

sichern() { [ -f "$1" ] && cp "$1" "$1.bak-$STEMPEL" && info "Sicherung: $(basename "$1").bak-$STEMPEL"; }

echo "Claude-Codex-Bruecke wird eingerichtet."
echo

# ---------- 0. Voraussetzungen ----------
CLAUDE="$(command -v claude 2>/dev/null || true)"
[ -z "$CLAUDE" ] && [ -x "$HOME/.local/bin/claude" ] && CLAUDE="$HOME/.local/bin/claude"
CODEX="$(command -v codex 2>/dev/null || true)"
[ -z "$CODEX" ] && [ -x "$HOME/.local/bin/codex" ] && CODEX="$HOME/.local/bin/codex"

if [ -z "$CLAUDE" ]; then
  warn "Claude Code nicht gefunden. Installieren, dann erneut ausfuehren."
  exit 1
fi
if [ -z "$CODEX" ]; then
  warn "Codex CLI nicht gefunden. 'npm install -g @openai/codex', dann erneut ausfuehren."
  exit 1
fi
ok "Claude Code: $CLAUDE"
ok "Codex CLI:  $CODEX"

ARBEITSORDNER="${CLAUDE_CODEX_WORKDIR:-$HOME}"
info "Arbeitsordner fuer die Bruecke: $ARBEITSORDNER (aendern mit CLAUDE_CODEX_WORKDIR=...)"
echo

# ---------- 1. Claude als Werkzeug in Codex ----------
echo "1. Claude als Werkzeug in Codex"
CFG="$HOME/.codex/config.toml"
mkdir -p "$HOME/.codex"
if [ -f "$CFG" ] && grep -q '^\[mcp_servers.claude\]' "$CFG"; then
  ok "schon eingetragen"
else
  sichern "$CFG"
  {
    printf '\n'
    printf '# Claude Code als Werkzeug fuer Codex (claude-codex-bridge).\n'
    printf '# Codex bekommt damit Claudes Werkzeuge: Agent (ganze Aufgabe abgeben), Skill,\n'
    printf '# Bash/Read/Edit/Write, Artifact, Workflow, WebSearch.\n'
    printf '[mcp_servers.claude]\n'
    printf 'command = "%s"\n' "$CLAUDE"
    printf 'args = ["mcp", "serve"]\n'
    printf 'cwd = "%s"\n' "$ARBEITSORDNER"
    printf 'startup_timeout_sec = 120\n'
  } >> "$CFG"
  ok "in $CFG eingetragen"
fi
echo

# ---------- 2. Codex als Werkzeug in Claude ----------
echo "2. Codex als Werkzeug in Claude"
if "$CLAUDE" mcp get codex >/dev/null 2>&1; then
  ok "schon eingetragen"
else
  if "$CLAUDE" mcp add --scope user --transport stdio codex -- "$CODEX" mcp-server >/dev/null 2>&1; then
    ok "als Benutzer-Server eingetragen"
  else
    warn "konnte nicht eingetragen werden, bitte von Hand:"
    printf '       claude mcp add --scope user --transport stdio codex -- codex mcp-server\n'
  fi
fi
echo

# ---------- 3. Skill ablegen ----------
echo "3. Skill 'claude-codex' ablegen"
SKILLS="$HOME/.agents/skills/claude-codex"
mkdir -p "$SKILLS"
cp "$HIER/SKILL.md" "$SKILLS/SKILL.md" && ok "$SKILLS/SKILL.md"
mkdir -p "$SKILLS/scripts"
cp "$HIER/scripts/faden.py" "$SKILLS/scripts/faden.py" && chmod +x "$SKILLS/scripts/faden.py" && ok "$SKILLS/scripts/faden.py"
# Claude liest ~/.claude/skills; falls das kein Symlink auf ~/.agents/skills ist, dort zusaetzlich verlinken
if [ -d "$HOME/.claude/skills" ] && [ ! -e "$HOME/.claude/skills/claude-codex" ]; then
  ln -s "$SKILLS" "$HOME/.claude/skills/claude-codex" 2>/dev/null && ok "auch fuer Claude verlinkt"
fi
echo

# ---------- 4. Weiche in die Regel-Dateien ----------
echo "4. Weiche in die Regel-Dateien"
MARKE="<!-- claude-codex-bridge -->"
anhaengen() {
  ZIEL="$1"
  if [ -f "$ZIEL" ] && grep -qF "$MARKE" "$ZIEL"; then
    ok "$(basename "$ZIEL"): schon vorhanden"
    return
  fi
  sichern "$ZIEL"
  mkdir -p "$(dirname "$ZIEL")"
  printf '\n%s\n' "$MARKE" >> "$ZIEL"
  cat "$HIER/AGENTS-block.md" >> "$ZIEL"
  printf '%s\n' "$MARKE" >> "$ZIEL"
  ok "$(basename "$ZIEL"): Weiche angehaengt"
}
anhaengen "$HOME/.codex/AGENTS.md"
# Claude: nur wenn CLAUDE.md keine Verweis-Datei auf AGENTS.md ist
CM="$HOME/.claude/CLAUDE.md"
if [ -L "$CM" ]; then
  ok "CLAUDE.md ist ein Symlink auf die Codex-Datei, nichts weiter noetig"
elif [ -f "$CM" ] && [ "$(tr -d '[:space:]' < "$CM")" = "@AGENTS.md" ]; then
  ok "CLAUDE.md verweist auf AGENTS.md, nichts weiter noetig"
else
  anhaengen "$CM"
fi
echo

echo "Fertig."
echo
echo "Noch zwei Schritte von Hand:"
echo "  a) ChatGPT-App (Codex) einmal schliessen und neu oeffnen."
echo "  b) Testen: in Codex fragen \"Hast du einen MCP-Server namens claude?\""
echo
echo "Kosten im Blick behalten: Codex' Aufrufe von Claudes Werkzeug 'Agent' laufen ueber das"
echo "Claude-Abo. Bash/Read/Edit/Write und Skill kosten nur Codex-Token."
