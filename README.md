# claude-codex-bridge

Codex und Claude Code arbeiten zusammen, und du musst nicht entscheiden, wer was macht.

Du redest mit einem von beiden. Der holt sich den anderen dazu, wenn der andere besser ist.
Die Regel dafuer steht in einer Datei, die beide bei jedem Start lesen.

## Warum

Beide koennen fast alles, aber nicht gleich gut, und beide haben Faehigkeiten, die der andere
gar nicht hat. Codex hat einen eingebauten Browser und kann den Rechner bedienen. Claude hat
Artifacts, Skills, Unteragenten und ein Gedaechtnis ueber Sitzungen hinweg. Wer beides von Hand
mischt, wechselt staendig das Fenster. Diese Bruecke nimmt dir das ab.

## Was eingerichtet wird

1. **Claude als Werkzeug in Codex.** Codex bekommt 26 Werkzeuge, darunter `Agent` (ganze Aufgabe
   an einen Claude-Agenten abgeben), `Skill` (Claudes Skills lesen und selbst anwenden), `Bash`,
   `Read`, `Edit`, `Write`, `Artifact`, `Workflow`, `WebSearch`.
2. **Codex als Werkzeug in Claude.** Claude kann Codex fuer Zweitmeinungen, Code und Browserarbeit rufen.
3. **Der Skill `claude-codex`** in `~/.agents/skills`, den beide lesen. Er enthaelt die ausfuehrliche
   Weiche und die Regeln fuer die Uebergabe.
4. **Die Kurzfassung der Weiche** in `~/.codex/AGENTS.md`, damit Codex sie in jeder Sitzung kennt.

## Einrichten

```bash
git clone https://github.com/manunalu/claude-codex-bridge.git ~/claude-codex-bridge
sh ~/claude-codex-bridge/install.sh
```

Danach die ChatGPT-App einmal schliessen und neu oeffnen.

Der eigene Arbeitsordner laesst sich vorgeben:

```bash
CLAUDE_CODEX_WORKDIR=~/dev/mein-projekt sh ~/claude-codex-bridge/install.sh
```

Wer es lieber von Codex selbst einrichten laesst: der fertige Text zum Einfuegen steht in
[PROMPT.md](PROMPT.md).

## Voraussetzungen

- Claude Code (angemeldet)
- Codex CLI und die ChatGPT-App (angemeldet)
- macOS oder Linux. Auf Windows funktionieren die Eintraege, das Skript nicht.

## Testen

In einem neuen Codex-Chat:

```
Hast du einen MCP-Server namens claude? Wenn ja, nenne fuenf seiner Werkzeuge und rufe sein
Werkzeug Bash auf mit dem Befehl `echo VERBINDUNG-OK`.
```

Erwartet: er nennt unter anderem `Agent`, `Bash`, `Read`, `Edit`, `Write` und zeigt `VERBINDUNG-OK`.

## Was das kostet

| Was gerufen wird | Denkt ein Claude-Modell? | Kontingent |
|---|---|---|
| `Bash`, `Read`, `Edit`, `Write` | nein, reine Ausfuehrung | nur Codex |
| `Skill` | nein, die Anleitung wandert in Codex' Kontext | nur Codex |
| `Agent`, `Workflow` | ja | Claude-Abo |

Der guenstige Normalfall ist deshalb: Codex liest Claudes Skills und arbeitet selbst damit.
Erst wenn Claudes Urteil gebraucht wird, geht die ganze Aufgabe an `Agent`.

## Sicherheit

- Ueber Claudes `Bash` umgeht Codex seine eigene Sandbox. Das ist der Sinn der Sache, aber es heisst:
  dieselben Regeln gelten weiter. Keine Geheimnisse in Dateien, kein force-push, geschuetzte Zweige
  nur per Pull Request.
- Das Skript aendert nur `~/.codex/config.toml`, `~/.codex/AGENTS.md`, `~/.claude` und
  `~/.agents/skills`. Von jeder Datei wird vorher eine Sicherung angelegt. Nichts wird geloescht.

## Wieder entfernen

Siehe [PROMPT.md](PROMPT.md), Abschnitt "Wieder entfernen", oder die Sicherungen zurueckspielen.

## Lizenz

MIT
