#!/usr/bin/env python3
"""Themen-Faeden: ein dauerhafter Claude-Chat je Thema, den Codex fortsetzen kann.

Warum: Wenn Codex eine Aufgabe an Claude abgibt, entsteht sonst jedes Mal ein neuer, leerer Chat.
Mit Themen-Faeden landet alles zum selben Thema im selben Chat. Der Mensch oeffnet ihn in seiner
Claude-App und sieht die ganze Geschichte: was Codex beauftragt hat, was Claude getan hat, was
zurueckging.

Jeder Faden ist eine echte Claude-Sitzung mit fester Kennung. `claude -p --resume <kennung>` haengt
einen Zug an. In der Claude-App taucht der Faden unter dem passenden Projektordner auf.

Aufrufe:
  faden.py liste                                  Faeden zeigen
  faden.py <thema> "<auftrag>" [--modell opus]    Auftrag in den Faden geben (legt ihn bei Bedarf an)
  faden.py lesen <thema> [--anzahl 3]             letzte Antworten aus dem Faden lesen
  faden.py <thema> ... --ordner /pfad             Arbeitsordner beim Anlegen festlegen

Der Faden gehoert zu einem Ordner, weil Claude-Sitzungen pro Projektordner liegen. Ohne --ordner
wird der aktuelle Ordner genommen.
"""
import argparse, glob, json, os, subprocess, sys, uuid

REGISTER = os.path.expanduser('~/.claude-codex-bridge/faeden.json')


def lade():
    try:
        with open(REGISTER, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def sichere(d):
    os.makedirs(os.path.dirname(REGISTER), exist_ok=True)
    with open(REGISTER, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def sitzungsdatei(kennung, ordner):
    for pfad in glob.glob(os.path.expanduser(f'~/.claude/projects/*/{kennung}.jsonl')):
        return pfad
    return None


def letzte_antworten(kennung, ordner, anzahl=3):
    pfad = sitzungsdatei(kennung, ordner)
    if not pfad:
        return []
    out = []
    try:
        for zeile in open(pfad, encoding='utf-8'):
            try:
                d = json.loads(zeile)
            except Exception:
                continue
            m = d.get('message') or {}
            if d.get('type') == 'assistant' and isinstance(m.get('content'), list):
                text = ''.join(c.get('text', '') for c in m['content'] if c.get('type') == 'text')
                if text.strip():
                    out.append(text.strip())
    except Exception:
        return []
    return out[-anzahl:]


def hole_faden(name, ordner_arg):
    reg = lade()
    if name in reg:
        return reg[name], reg
    eintrag = {
        'kennung': str(uuid.uuid4()),
        'ordner': os.path.abspath(os.path.expanduser(ordner_arg or os.getcwd())),
        'neu': True,
    }
    reg[name] = {'kennung': eintrag['kennung'], 'ordner': eintrag['ordner']}
    sichere(reg)
    return eintrag, reg


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('befehl', nargs='?')
    ap.add_argument('rest', nargs='*')
    ap.add_argument('--modell', default=None, help='opus (Standard), fable, sonnet, haiku')
    ap.add_argument('--ordner', default=None)
    ap.add_argument('--anzahl', type=int, default=3)
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()

    if a.help or not a.befehl:
        print(__doc__)
        return

    if a.befehl == 'liste':
        reg = lade()
        if not reg:
            print('Noch keine Faeden. Einer entsteht beim ersten Auftrag.')
            return
        for name, e in sorted(reg.items()):
            pfad = sitzungsdatei(e['kennung'], e['ordner'])
            zeilen = sum(1 for _ in open(pfad, encoding='utf-8')) if pfad else 0
            print(f"  {name:14} {e['kennung']}  {zeilen:>4} Zeilen  {e['ordner']}")
        return

    if a.befehl == 'lesen':
        if not a.rest:
            sys.exit('Thema fehlt: faden.py lesen <thema>')
        name = a.rest[0]
        reg = lade()
        if name not in reg:
            sys.exit(f'Faden "{name}" gibt es nicht. faden.py liste zeigt alle.')
        e = reg[name]
        for t in letzte_antworten(e['kennung'], e['ordner'], a.anzahl):
            print('---'); print(t)
        return

    # Auftrag in einen Faden geben
    name = a.befehl
    auftrag = ' '.join(a.rest).strip()
    if not auftrag:
        sys.exit('Auftrag fehlt: faden.py <thema> "<auftrag>"')
    e, _ = hole_faden(name, a.ordner)
    ordner = e['ordner']
    if not os.path.isdir(ordner):
        sys.exit(f'Ordner gibt es nicht: {ordner}')
    neu = e.get('neu') or sitzungsdatei(e['kennung'], ordner) is None

    cmd = ['claude', '-p']
    if a.modell:
        cmd += ['--model', a.modell]
    cmd += (['--session-id', e['kennung']] if neu else ['--resume', e['kennung']])
    cmd += [auftrag]

    print(f'Faden "{name}" ({"neu" if neu else "fortgesetzt"}), Ordner {ordner}', file=sys.stderr)
    r = subprocess.run(cmd, cwd=ordner)
    if r.returncode == 0:
        print(f'\n[Faden: {name} · {e["kennung"]}]', file=sys.stderr)
    sys.exit(r.returncode)


if __name__ == '__main__':
    main()
