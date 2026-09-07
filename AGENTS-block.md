
## Claude und Codex arbeiten zusammen

Beide Agenten sind miteinander verdrahtet. Du entscheidest selbst, wer eine Aufgabe macht, und fragst
den Menschen nicht danach. Die ausfuehrliche Weiche steht im Skill `claude-codex`, lies ihn, bevor du
etwas abgibst.

**Merkregel:** Abgeben, was heisst "geh raus und finde X heraus" oder "mach diese klar umrissene
Sache". Behalten, was heisst "lass uns das zusammen durchdenken".

**Was nur Codex kann** (dorthin abgeben, ohne zu fragen): eingebauter Browser (schnell, ohne
Anmeldungen), Chrome mit echten Anmeldungen, den Rechner bedienen, geplante Aufgaben in der App,
PDF- und Tabellen- und Praesentations-Werkzeuge, Codex Cloud.

**Was nur Claude kann** (dorthin abgeben, ohne zu fragen): Artifacts (veroeffentlichbare Seiten mit
Zustand, Abhaklisten zum Mitschreiben), Unteragenten und Workflow (mehrere Pruefer parallel),
Gedaechtnis ueber Sitzungen, iOS-Simulator.

**Angebundene Dienste** (Slack, Notion, Gmail, Kalender, Drive, Figma, Canva) hat inzwischen jede
Seite selbst. Wer gefragt wird, macht es. Nur bei fehlender oder nicht angemeldeter Verbindung abgeben.

**Wo beide koennen** (Stand 09/2026, unabhaengige Messungen): Rechnen und Algorithmen, Sicherheits-
pruefung, lange klar umrissene Laeufe und Netzrecherche gehen an **Codex**. Texte, Planung,
mehrdeutige Aufgaben und alles mit mehreren Pruefern gehen an **Claude**. Terminal-Arbeit allgemein ist
Gleichstand, da bleibt es beim Rufenden. Bei **Design** ist kein Sieger belegt: Entwurf bei Codex,
Feinschliff bei Claude. Bei **Debugging und Refactoring** macht es, wer den Code kennt, der andere prueft.
Nach jedem langen selbstaendigen Lauf prueft der andere Agent, denn gruene Tests beweisen bei grossen
Codebasen nichts.

**Uebergabe.** Claude ruft Codex mit `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`
oder dem Werkzeug `mcp__codex__codex`. Codex ruft Claude mit `claude.Skill` (Wissen holen und
selbst arbeiten), `claude.Bash` / `Read` / `Edit` / `Write` / `WebSearch`, und fuer eine **ganze
Aufgabe** mit `claude -p "<vollstaendiger Auftrag>"` in der Shell. Das Werkzeug `claude.Agent`
funktioniert ueber die Bruecke nicht.

**Kosten.** `Skill`, `Bash`, `Read`, `Edit`, `Write` kosten nichts beim anderen Abo, weil dort kein
Modell denkt. `claude -p` schon. Also erst das Wissen holen, und nur abgeben, wenn das
Urteil des anderen Modells wirklich gebraucht wird.

**Eiserne Regeln.**
- Wer prueft, repariert nicht. Wer baut, benotet nicht.
- Hoechstens eine Reparaturrunde, danach entscheidet der Mensch.
- Kein Kreisverkehr: eine abgegebene Aufgabe wird nicht weitergereicht.
- Nie abgeben: Architekturentscheidungen, unklare Anforderungen, Geheimnisse, Commits, Pushes,
  Releases, Loeschungen, die letzte Abnahme.
- Nichts abgeben, was kleiner ist als der Weg hin und zurueck.
- Arbeiten beide gleichzeitig am selben Projekt, bekommt der zweite einen eigenen `git worktree`.
- Der Auftrag muss allein stehen: Pfade, Ziel, Grenzen, und was "fertig" heisst.
- Lange Laeufe in den Hintergrund legen, nicht wartend blockieren.
