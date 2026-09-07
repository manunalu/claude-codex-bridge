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
  faden.py suchen [wort]                          bestehende Claude-Sitzungen zeigen (zum Ansteuern)
  faden.py setzen <thema> <kennung>               Faden auf eine BESTEHENDE Sitzung zeigen lassen
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



def sitzungen(suchwort=None, grenze=25):
    """Alle Claude-Sitzungen mit erster Nutzerzeile, neueste zuerst."""
    treffer = []
    for pfad in glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')):
        try:
            groesse = os.path.getsize(pfad)
            if groesse < 400:
                continue
            erste = ''
            with open(pfad, encoding='utf-8') as f:
                for zeile in f:
                    try:
                        d = json.loads(zeile)
                    except Exception:
                        continue
                    m = d.get('message') or {}
                    if d.get('type') == 'user':
                        c = m.get('content')
                        if isinstance(c, str):
                            erste = c
                        elif isinstance(c, list):
                            erste = ' '.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
                        erste = ' '.join(erste.split())[:90]
                        if erste and not erste.startswith('<'):
                            break
                        erste = ''
            if not erste:
                continue
            ordner = ''
            try:
                with open(pfad, encoding='utf-8') as f2:
                    for z2 in f2:
                        d2 = json.loads(z2)
                        if d2.get('cwd'):
                            ordner = d2['cwd'].replace(os.path.expanduser('~'), '~')
                            break
            except Exception:
                ordner = os.path.basename(os.path.dirname(pfad))
            eintrag = {'kennung': os.path.basename(pfad)[:-6], 'zeit': os.path.getmtime(pfad),
                       'erste': erste, 'ordner_roh': os.path.dirname(pfad), 'ordner': ordner}
            if suchwort and suchwort.lower() not in erste.lower() and suchwort.lower() not in ordner.lower():
                continue
            treffer.append(eintrag)
        except Exception:
            continue
    treffer.sort(key=lambda e: e['zeit'], reverse=True)
    return treffer[:grenze]


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

    if a.befehl == 'suchen':
        import datetime
        wort = a.rest[0] if a.rest else None
        gefunden = sitzungen(wort)
        if not gefunden:
            print('Keine passende Sitzung gefunden.')
            return
        for e in gefunden:
            wann = datetime.datetime.fromtimestamp(e['zeit']).strftime('%d.%m. %H:%M')
            print(f"  {e['kennung']}  {wann}  {e['erste']}")
        print('\nEinen davon binden: faden.py setzen <thema> <kennung>')
        return

    if a.befehl == 'setzen':
        if len(a.rest) < 2:
            sys.exit('Aufruf: faden.py setzen <thema> <kennung>')
        name, kennung = a.rest[0], a.rest[1]
        pfad = sitzungsdatei(kennung, None)
        if not pfad:
            sys.exit(f'Sitzung {kennung} nicht gefunden. faden.py suchen zeigt alle.')
        reg = lade()
        reg[name] = {'kennung': kennung, 'ordner': os.getcwd()}
        # Ordner sauber aus dem Sitzungsinhalt holen
        try:
            with open(pfad, encoding='utf-8') as f:
                for zeile in f:
                    d = json.loads(zeile)
                    if d.get('cwd'):
                        reg[name]['ordner'] = d['cwd']
                        break
        except Exception:
            pass
        sichere(reg)
        print(f"Faden \"{name}\" zeigt jetzt auf {kennung}")
        print(f"  Ordner: {reg[name]['ordner']}")
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
