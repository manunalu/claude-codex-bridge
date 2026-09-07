---
name: claude-codex
description: Weiche zwischen Claude Code und OpenAI Codex. Nutzen, sobald eine Aufgabe ansteht, die der jeweils andere Agent besser oder ueberhaupt nur kann, und bevor eine Aufgabe abgegeben wird. Enthaelt die Zustaendigkeiten, die Uebergabe-Befehle, die Kostenregeln und die bekannten Fallen.
---

# Claude und Codex: wer macht was

**Grundsatz:** Was nur einer kann, geht ohne Diskussion dorthin. Wo beide koennen, entscheidet die
Art der Aufgabe, nicht der Geschmack. Der Mensch soll nicht gefragt werden, wer arbeitet.

**Die Merkregel, wenn die Tabelle nicht weiterhilft:** Abgeben, was heisst "geh raus und finde X
heraus" oder "mach diese klar umrissene Sache". Behalten, was heisst "lass uns das zusammen
durchdenken".

---

## 1. Was nur einer kann (harte Weiche)

### Nur Codex

| Faehigkeit | Warum |
|---|---|
| **Eingebauter Browser** | Nur die ChatGPT-App hat ihn. Gemessen etwa doppelt so schnell wie Chrome (25 s gegen 45 s fuer dieselbe Aufgabe). Startet ohne Anmeldungen und ohne Cookies. |
| **Chrome mit echten Anmeldungen** | Ueber die Codex-Erweiterung. Der Weg fuer Portale, Behoerden, Shop-Verwaltung, alles mit Login. |
| **Den Rechner bedienen** | Fenster, Menues, fremde Programme (Computer Use). |
| **Geplante Aufgaben in der App** | Laufen selbstaendig zur Uhrzeit, Ergebnis landet im Posteingang der App. |
| **Dokumentwerkzeuge** | PDF, Tabellen, Praesentationen, Vorlagen als App-Plugins. |
| **Codex Cloud** | Laenger laufende Arbeit ausserhalb des eigenen Rechners. |

### Nur Claude

| Faehigkeit | Warum |
|---|---|
| **Artifacts** | Veroeffentlichbare Seiten mit eigener Adresse, mit Zustand und Datenbank. Abhaklisten, an denen der Mensch Haken setzt und kommentiert, die der Agent spaeter wieder liest. **Kein Ersatz bauen:** wer eine Abhakliste braucht, gibt sie ab (`claude -p`), statt sie als GitHub-Issue oder Textliste nachzubilden. |
| **Unteragenten und Workflow** | Mehrere Pruefer parallel, ein Verifizierer dagegen. Fuer Audits und Konzile. |
| **Gedaechtnis ueber Sitzungen** | Entscheidungen und Vorlieben bleiben, ohne dass jemand sie erneut erklaert. |
| **iOS-Simulator** | App starten, tippen, Screenshot pruefen. |

Wenn eine Aufgabe eine dieser Faehigkeiten braucht, geht sie dorthin. Auch dann, wenn der andere
Agent gerade vorne sitzt.

### Beide koennen es, keine Uebergabe noetig

**Angebundene Dienste:** Slack, Notion, Gmail, Kalender, Drive, Figma und Canva gibt es fuer beide
Seiten als eigene Verbindung. Wer gefragt wird, macht es selbst. Nur wenn die eigene Verbindung fehlt
oder nicht angemeldet ist, gibt er ab und sagt das dazu.

---

## 2. Wo beide koennen

Stand der Belege: September 2026. Nur unabhaengige Messungen, keine Werbezahlen. Wo nichts belegt
ist, steht das ausdruecklich da.

| Aufgabe | Wer | Beleg |
|---|---|---|
| **Rechnen, Algorithmen, Krypto, alles Formale** | **Codex** | FrontierMath Tier 4: 97,6 gegen 87,8 Prozent. GPQA Diamond: 96,0 gegen 93,7. Vorsprung zu gross fuer Messfehler. |
| **Sicherheitspruefung, Exploits, Betriebsstoerungen** | **Codex** | ExploitBench 100 gegen 70 Prozent, SRE-Bench 88 gegen 12,5. Deutlichster Abstand im ganzen Vergleich. |
| **Lange, klar umrissene Laeufe** (Massenaenderungen, Tests, Migrationen) | **Codex** | Braucht rund ein Fuenftel der Token. Haelt in langen Laeufen Notizen ueber Kontextfenster hinweg. |
| **Recherche im Netz** | **Codex, knapp** | BrowseComp 91,5 gegen 90,8 Prozent. Der Abstand ist klein, die Aufbauten sind ungleich. |
| **Texte, Copy, Ton treffen** | **Claude** | arena.ai Text mit 8 Millionen Blindstimmen: Claude auf vier der ersten neun Plaetze. |
| **Planung, Architektur, mehrdeutige Aufgaben** | **Claude** | Unabhaengige Gesamt-Indizes: 66 gegen 61 und 68,83 gegen 66,61. OpenAI raeumt das in der eigenen Tabelle ein. |
| **Mehrere Pruefer parallel, Audits, Konzil** | **Claude** | Coding-Agent-Index 70 gegen 67. Koordinierte Unteragenten gibt es auf der anderen Seite so nicht. |
| **Terminal-Arbeit allgemein** | **Gleichstand** | Terminal-Bench 4.0: 58,2 gegen 57,9 Prozent bei Fehlerbalken von rund 3. Kein Unterschied. |
| **Design und Oberflaeche** | **nicht belegt** | Es gibt keinen verlaesslichen Beleg, dass einer schoeneres UI baut. Einziges wiederkehrendes Muster aus Handtests: **Codex liefert den besseren ersten Wurf, Claude das bessere Ergebnis nach mehreren Runden.** Danach handeln: Entwurf bei Codex, Feinschliff und Umsetzung bei Claude, weil dort auch die Design-Skills und die Artifacts liegen. |
| **Debugging, Refactoring** | **umstritten** | Drei unabhaengige Auswerter, drei verschiedene Reihenfolgen. Harness und Prompt wiegen schwerer als das Modell. **Regel: wer den Code kennt, macht es. Der andere prueft.** |

**Ein harter Befund, der fuer beide gilt:** Bei langen selbstaendigen Laeufen wachsen die Fehler, die
die eigenen Tests nicht sehen, mit der Groesse der Codebasis. Ab etwa 25.000 Zeilen sagt eine gruene
Testsuite nichts mehr ueber Korrektheit. Deshalb: **nach jedem langen autonomen Lauf prueft der
andere Agent, und der Mensch nimmt ab.**

---

## 3. Wie die Uebergabe geht

### Claude ruft Codex

| Zweck | Befehl |
|---|---|
| Zweitmeinung zum Diff | `/codex:review` |
| Angriff auf Annahmen und Entwurf | `/codex:adversarial-review` |
| Untersuchung, Fehlersuche, laengere Arbeit | `/codex:rescue` |
| Feiner steuerbar | Werkzeug `mcp__codex__codex` mit `sandbox`, `approval-policy`, `model`, `effort` |
| Browser-Auftrag in der App | Skill `astra-uebergabe` |

### Codex ruft Claude

| Zweck | Wie |
|---|---|
| Claudes Wissen nutzen, selbst arbeiten | `claude.Skill` mit dem Skill-Namen. Die Anleitung wandert in den eigenen Kontext. |
| Dateien lesen und schreiben | `claude.Read`, `claude.Edit`, `claude.Write`, `claude.Bash` |
| Im Netz suchen | `claude.WebSearch` |
| **Ganze Aufgabe abgeben** | **`claude -p "<vollstaendiger Auftrag>"` in der Shell** (oder ueber `claude.Bash`). Das startet einen kompletten Claude mit Skills, Projektregeln und Gedaechtnis. |

**Wichtig:** Das Werkzeug `claude.Agent` funktioniert ueber die Bruecke **nicht** (der kopflose Claude
kennt keine Agenten-Typen, Antwort "Available agents: none"). Fuer ganze Aufgaben immer `claude -p`
benutzen. Geprueft am 07.09.2026, Antwort in rund 16 Sekunden, mit Zugriff auf die geteilten Skills
und die Projektregeln.

**Der guenstige Normalfall ist `Skill`, nicht `claude -p`.** `Skill` laesst den rufenden Agenten mit
dem Wissen des anderen arbeiten und kostet nichts beim anderen Abo. `claude -p` ist fuer die Faelle,
in denen das Urteil des anderen Modells gebraucht wird.

---

## 4. Eiserne Regeln der Uebergabe

- **Wer prueft, repariert nicht.** Wer eine Review anfordert, setzt sie selbst um. Wer eine Review
  liefert, aendert keinen Code. Sonst entsteht eine Schleife, in der zwei Agenten sich gegenseitig
  ueberschreiben.
- **Wer baut, benotet nicht.** Hat Claude gebaut, prueft Codex. Hat Codex gebaut, prueft Claude.
- **Hoechstens eine Reparaturrunde.** Danach entscheidet der Mensch. Ohne diese Grenze laeuft es
  endlos.
- **Kein Kreisverkehr.** Wer eine Aufgabe abgegeben bekommen hat, gibt sie nicht weiter. Der
  Ruecklauf endet beim Menschen, nicht beim ersten Agenten.
- **Nie abgeben:** Architekturentscheidungen, unklare Anforderungen (wo das Klaeren die eigentliche
  Arbeit ist), Geheimnisse, Commits, Pushes, Releases, Loeschungen, die letzte Abnahme.
- **Nie abgeben, was kleiner ist als der Weg.** Hin und zurueck kostet mehr als die Aenderung selbst.
- **Ein Arbeitsordner, ein Agent.** Arbeiten beide gleichzeitig am selben Projekt, bekommt der zweite
  einen eigenen `git worktree` daneben. Sonst ueberschreibt einer die Datei des anderen.
- **Der Auftrag muss allein stehen.** Ueber die Grenze geht ein einzelner Text, keine Sitzung. Pfade,
  Ziel, Grenzen und was "fertig" heisst gehoeren hinein.
- **Lange Laeufe in den Hintergrund.** Warten kostet doppelt, siehe Fallen.

---

## 5. Kosten

| Was gerufen wird | Denkt ein Modell des anderen? | Kontingent |
|---|---|---|
| `Bash`, `Read`, `Edit`, `Write` | nein | nur der Rufende |
| `Skill` | nein | nur der Rufende |
| `claude -p`, `Workflow` | ja | das andere Abo |
| `/codex:review`, `/codex:rescue`, `mcp__codex__codex` | ja | ChatGPT-Abo |

Vor jedem Lauf Modell und Denkstufe bewusst waehlen. Fuer Fliessbandarbeit die niedrige Stufe.

---

## 6. Bekannte Fallen (belegt)

| Falle | Was passiert | Gegenmittel |
|---|---|---|
| **Review-Tor** | Der Stop-Hook des Codex-Plugins unterscheidet nicht zwischen "Codex sagt Nein" und "Codex lief gar nicht" (Zeitlimit, Kontingent leer). Beides blockt, Claude wacht auf, es beginnt von vorne. Offenes Problem im Plugin. | Das Review-Tor aus lassen. Es ist standardmaessig aus. |
| **Kontext wird neu berechnet** | Claudes Zwischenspeicher haelt nur wenige Minuten. Ein langer Codex-Lauf ueberschreitet das, danach wird der ganze Kontext neu abgerechnet. Der leiseste Kostenfresser. | Codex-Laeufe im Hintergrund starten und weiterarbeiten, statt zu warten. |
| **Codex liest im Kreis** | Bei Reviews ueber viele Dateien faengt er wieder von vorne an. | Hartes Zeitlimit setzen, Auftrag eng fassen. |
| **Zeitlimit zu kurz** | Standard sind 60 Sekunden pro Werkzeugaufruf. Echte Auftraege dauern laenger und brechen ab. Ein Artifact oder ein Build braucht mehrere Minuten. | `tool_timeout_sec = 900` in der Codex-Konfiguration. |
| **Sitzung geht verloren** | Ueber die Bruecke geht ein Text, kein Gespraech. Rueckfragen im selben Faden sind unzuverlaessig. | Auftrag vollstaendig formulieren. Ergebnis holen, nicht nachverhandeln. |
| **Dateikonflikte** | Beide schreiben dieselbe Datei. | Worktree, siehe Regeln. |
| **Stille API-Abrechnung** | Ist `ANTHROPIC_API_KEY` gesetzt, laeuft Claude nicht ueber das Abo, sondern zu API-Preisen. | Variable nicht setzen. |
| **Bruecken ohne Rueckfragen** | Manche Fremdprojekte starten beide Agenten mit abgeschalteten Sicherheitsabfragen. | Vor dem Installieren nachsehen, mit welchen Schaltern eine Bruecke die Agenten startet. |

---

## 7. Sicherheit

Ueber `claude.Bash` umgeht Codex seine eigene Sandbox, und Claude fragt dabei nicht nach. Das ist der
Sinn der Bruecke, heisst aber: dieselben Regeln gelten weiter. Keine Geheimnisse in Dateien oder
Chats, kein force-push, geschuetzte Zweige nur per Pull Request, keine Loeschungen ohne Rueckfrage.
