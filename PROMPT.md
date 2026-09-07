# Zum Kopieren: Claude in Codex einbauen

Zwei Fassungen. Die erste ist die kurze, wenn das Repo schon geladen ist. Die zweite ist die lange,
die Codex alles selbst machen laesst, ohne dass vorher etwas heruntergeladen wurde.

---

## Fassung A: mit dem Repo (empfohlen)

Erst im Terminal laden:

```bash
git clone https://github.com/manunalu/claude-codex-bridge.git ~/claude-codex-bridge && sh ~/claude-codex-bridge/install.sh
```

Danach die ChatGPT-App einmal schliessen und neu oeffnen. Fertig.

---

## Fassung B: Codex macht es selbst

Diesen Text in einen neuen Codex-Chat einfuegen und abschicken:

```
Baue mir die Bruecke zwischen Codex und Claude Code. Arbeite in dieser Reihenfolge und zeige mir am
Ende eine kurze Zusammenfassung, was du geaendert hast.

1. Pruefe, ob Claude Code installiert ist: `command -v claude` (sonst auch `~/.local/bin/claude`
   probieren). Wenn nicht vorhanden, brich ab und sage mir, dass ich Claude Code installieren muss.

2. Lege eine Sicherung von ~/.codex/config.toml an (Endung .bak plus Datum).

3. Trage Claude als Werkzeug ein, indem du ans Ende von ~/.codex/config.toml anhaengst
   (den Pfad zu claude aus Schritt 1 einsetzen, den Arbeitsordner auf mein Projekt setzen):

   [mcp_servers.claude]
   command = "<voller Pfad zu claude>"
   args = ["mcp", "serve"]
   cwd = "<mein Projektordner>"
   startup_timeout_sec = 120

4. Trage umgekehrt Codex als Werkzeug in Claude ein:
   `claude mcp add --scope user --transport stdio codex -- codex mcp-server`

5. Lege den Skill an unter ~/.agents/skills/claude-codex/SKILL.md. Inhalt: die Weiche, wer was macht.
   Kopiere sie aus https://github.com/manunalu/claude-codex-bridge/blob/main/SKILL.md
   Wenn du keinen Netzzugriff hast, sage mir Bescheid, dann gebe ich dir den Text.

6. Haenge die Kurzfassung der Weiche an ~/.codex/AGENTS.md an, damit du sie in jeder Sitzung liest.
   Quelle: https://github.com/manunalu/claude-codex-bridge/blob/main/AGENTS-block.md

7. Sage mir zum Schluss: welche Dateien du geaendert hast, wo die Sicherungen liegen, und dass ich
   die ChatGPT-App einmal neu starten muss.

Wichtig: nichts loeschen, nur anhaengen. Keine Zugangsdaten anfassen. Wenn ein Eintrag schon
existiert, nicht doppelt schreiben.
```

---

## Danach testen

Neuen Codex-Chat aufmachen und fragen:

```
Hast du einen MCP-Server namens claude? Wenn ja, nenne fuenf seiner Werkzeuge und rufe sein
Werkzeug Bash auf mit dem Befehl `echo VERBINDUNG-OK`.
```

Richtige Antwort: Er nennt unter anderem `Agent`, `Bash`, `Read`, `Edit`, `Write` und zeigt
`VERBINDUNG-OK`.

---

## Was das kostet

- `Bash`, `Read`, `Edit`, `Write`, `Skill`: kein Claude-Modell denkt dabei, also nur Codex-Token.
- `Agent`, `Workflow`: hier denkt ein echtes Claude-Modell, das laeuft ueber das Claude-Abo.

---

## Wieder entfernen

1. In ~/.codex/config.toml den Block `[mcp_servers.claude]` loeschen.
2. `claude mcp remove codex`
3. `rm -rf ~/.agents/skills/claude-codex`
4. In ~/.codex/AGENTS.md den Abschnitt zwischen den beiden Zeilen `<!-- claude-codex-bridge -->` loeschen.

Oder einfach die Sicherungen zurueckspielen, die `install.sh` angelegt hat.
