# select_audio_output

Ein Kommandozeilen-Tool für macOS, mit dem Sie schnell und einfach zwischen verschiedenen Audio-Ausgabegeräten wechseln können.

## Funktionen

- Auflisten aller verfügbaren Audio-Ausgabegeräte
- Anzeigen des aktuell aktiven Audio-Ausgabegeräts
- Wechseln zu einem bestimmten Audio-Ausgabegerät per Name
- Stummschaltung umschalten (mute/unmute)
- Lautstärkeregelung direkt über die Kommandozeile
- Interaktiver Modus zur Auswahl von Geräten mit Pfeiltasten
- Intelligentes Fuzzy-Matching für Gerätenamen (erkennt und korrigiert Tippfehler automatisch)

## Voraussetzungen

- macOS
- Python 3.6 oder höher
- [SwitchAudioSource](https://github.com/deweller/switchaudio-osx) (installierbar über Homebrew)

## Installation

1. Stellen Sie sicher, dass Python 3 installiert ist:
   ```
   python3 --version
   ```

2. Installieren Sie SwitchAudioSource über Homebrew:
   ```
   brew install switchaudio-osx
   ```

3. Klonen Sie dieses Repository oder laden Sie die Dateien herunter.

4. Installieren Sie die erforderlichen Python-Abhängigkeiten:
   ```
   pip3 install -r requirements.txt
   ```

5. Machen Sie das Skript ausführbar:
   ```
   chmod +x select_audio_output.py
   ```

## Verwendung

### Auflisten aller verfügbaren Audio-Ausgabegeräte

```
./select_audio_output.py
```

Ausgabe:
```
Available output devices:
  • MacBook Pro-Lautsprecher (aktiv)
  • AirPods Pro
  • Externe Lautsprecher
  • HDMI-Ausgang
```

### Anzeigen des aktuell aktiven Audio-Ausgabegeräts

```
./select_audio_output.py -c
```

oder

```
./select_audio_output.py --current
```

Ausgabe:
```
MacBook Pro-Lautsprecher
```

### Wechseln zu einem bestimmten Audio-Ausgabegerät

```
./select_audio_output.py "Gerätename"
```

Beispiele:
```
# Exakter Name
./select_audio_output.py "MacBook Pro-Lautsprecher"

# Mit Fuzzy-Matching (Teilname)
./select_audio_output.py "Lautsprecher"

# Mit Fuzzy-Matching (Tippfehler)
./select_audio_output.py "MacBok Lautsprecer"

# Mit Fuzzy-Matching (Groß-/Kleinschreibung)
./select_audio_output.py "airpods"

# Mit Fuzzy-Matching (Abkürzungen)
./select_audio_output.py "AP Pro"  # Findet "AirPods Pro"

# Mit Fuzzy-Matching (Teilwörter)
./select_audio_output.py "extern"  # Findet "Externe Lautsprecher"

# Mit Fuzzy-Matching (Zahlen und Sonderzeichen)
./select_audio_output.py "hdmi2"   # Findet "HDMI-Ausgang 2"
```

### Stummschaltung umschalten

```
./select_audio_output.py -m
```

oder

```
./select_audio_output.py --toggle-mute
```

Ausgabe:
```
Audio muted
```
oder
```
Audio unmuted
```

### Lautstärkeregelung

#### Aktuelle Lautstärke anzeigen

```
./select_audio_output.py -g
```

oder

```
./select_audio_output.py --get-volume
```

Ausgabe:
```
Aktuelle Lautstärke: 75%
```

#### Lautstärke auf einen bestimmten Wert setzen (0-100)

```
./select_audio_output.py -v 50
```

oder

```
./select_audio_output.py --volume 50
```

Ausgabe:
```
Lautstärke auf 50% gesetzt
```

#### Lautstärke erhöhen

```
./select_audio_output.py -u 10
```

oder

```
./select_audio_output.py --volume-up 10
```

Ausgabe:
```
Lautstärke auf 60% gesetzt
```

#### Lautstärke verringern

```
./select_audio_output.py -d 10
```

oder

```
./select_audio_output.py --volume-down 10
```

Ausgabe:
```
Lautstärke auf 40% gesetzt
```

### Interaktiver Modus (Auswahl mit Pfeiltasten)

```
./select_audio_output.py -i
```

oder

```
./select_audio_output.py --interactive
```

Im interaktiven Modus können Sie mit den Pfeiltasten ↑ und ↓ durch die verfügbaren Geräte navigieren und mit Enter auswählen:

```
? Bitte Audio-Ausgabegerät wählen: (Use arrow keys)
 > MacBook Pro-Lautsprecher (aktiv)
   AirPods Pro
   Externe Lautsprecher
   HDMI-Ausgang
   -- Stummschalten umschalten --
   -- Lautstärke anzeigen --
   -- Lautstärke erhöhen (+10%) --
   -- Lautstärke verringern (-10%) --
   -- Lautstärke anpassen... --
```

### Kombinierte Befehle und Workflows

#### Gerät wechseln und Lautstärke anpassen

Sie können mehrere Befehle nacheinander ausführen, um komplexe Aktionen durchzuführen:

```bash
# Zu AirPods wechseln und Lautstärke auf 40% setzen
./select_audio_output.py "AirPods" && ./select_audio_output.py -v 40

# Zu externen Lautsprechern wechseln und Lautstärke erhöhen
./select_audio_output.py "Externe" && ./select_audio_output.py -u 20

# Zu MacBook-Lautsprechern wechseln und stummschalten
./select_audio_output.py "MacBook" && ./select_audio_output.py -m
```

#### Verwendung in Shell-Skripten

Beispiel für ein einfaches Shell-Skript, das je nach Tageszeit das Audio-Ausgabegerät wechselt:

```bash
#!/bin/bash

HOUR=$(date +%H)

if [ $HOUR -ge 22 ] || [ $HOUR -lt 8 ]; then
    # Abends/Nachts: Zu Kopfhörern wechseln und Lautstärke reduzieren
    ./select_audio_output.py "AirPods" && ./select_audio_output.py -v 30
    echo "Nachtmodus: AirPods mit reduzierter Lautstärke"
else
    # Tagsüber: Zu Lautsprechern wechseln mit normaler Lautstärke
    ./select_audio_output.py "Lautsprecher" && ./select_audio_output.py -v 70
    echo "Tagmodus: Lautsprecher mit normaler Lautstärke"
fi
```

#### Verwendung mit Shell-Aliassen

Fügen Sie diese Zeilen zu Ihrer `.zshrc` oder `.bashrc` hinzu, um praktische Aliasse zu erstellen:

```bash
# Schnelle Audio-Geräteumschaltung
alias speakers="~/pfad/zu/select_audio_output.py 'MacBook Pro-Lautsprecher'"
alias airpods="~/pfad/zu/select_audio_output.py 'AirPods' && ~/pfad/zu/select_audio_output.py -v 40"
alias hdmi="~/pfad/zu/select_audio_output.py 'HDMI'"
alias extspk="~/pfad/zu/select_audio_output.py 'Externe Lautsprecher' && ~/pfad/zu/select_audio_output.py -v 60"

# Lautstärkeregelung
alias vol="~/pfad/zu/select_audio_output.py -g"
alias vol50="~/pfad/zu/select_audio_output.py -v 50"
alias vol+="~/pfad/zu/select_audio_output.py -u 10"
alias vol-="~/pfad/zu/select_audio_output.py -d 10"
alias mute="~/pfad/zu/select_audio_output.py -m"

# Interaktiver Modus
alias audio="~/pfad/zu/select_audio_output.py -i"
```

### Integration mit anderen Tools

#### Verwendung mit AppleScript

```applescript
-- AppleScript zum Umschalten auf AirPods, wenn sie verbunden sind
tell application "System Events"
    set airpodsConnected to do shell script "system_profiler SPBluetoothDataType | grep -q 'AirPods.*Connected' && echo 'yes' || echo 'no'"
    
    if airpodsConnected is "yes" then
        do shell script "~/pfad/zu/select_audio_output.py 'AirPods'"
    else
        do shell script "~/pfad/zu/select_audio_output.py 'MacBook Pro-Lautsprecher'"
    end if
end tell
```

#### Verwendung mit Automator

Erstellen Sie einen Automator-Schnellbefehl, der das Audio-Ausgabegerät basierend auf dem verbundenen Gerät wechselt:

1. Öffnen Sie Automator und erstellen Sie einen neuen Schnellbefehl
2. Fügen Sie die Aktion "Shell-Skript ausführen" hinzu
3. Fügen Sie folgenden Code ein:

```bash
# Prüfen, ob HDMI verbunden ist
if system_profiler SPDisplaysDataType | grep -q "HDMI"; then
    ~/pfad/zu/select_audio_output.py "HDMI"
# Prüfen, ob AirPods verbunden sind
elif system_profiler SPBluetoothDataType | grep -q "AirPods.*Connected"; then
    ~/pfad/zu/select_audio_output.py "AirPods"
# Sonst zu MacBook-Lautsprechern wechseln
else
    ~/pfad/zu/select_audio_output.py "MacBook Pro-Lautsprecher"
fi
```

4. Speichern Sie den Schnellbefehl und führen Sie ihn aus, wenn Sie Ihr Audio-Ausgabegerät automatisch wechseln möchten

#### Verwendung mit Keyboard Maestro

Erstellen Sie einen Keyboard Maestro-Makro, der mit einer Tastenkombination das Audio-Ausgabegerät wechselt:

1. Erstellen Sie ein neues Makro in Keyboard Maestro
2. Fügen Sie einen Auslöser hinzu (z.B. Tastenkombination ⌥⌘A für AirPods)
3. Fügen Sie die Aktion "Shell-Skript ausführen" hinzu:

```bash
~/pfad/zu/select_audio_output.py "AirPods"
```

4. Erstellen Sie weitere Makros für andere Geräte mit unterschiedlichen Tastenkombinationen

#### Verwendung mit Alfred oder Raycast

Erstellen Sie Workflows oder Skripte für Alfred oder Raycast:

```bash
# Alfred/Raycast-Skript für schnellen Gerätewechsel
case "$1" in
  "speakers")
    ~/pfad/zu/select_audio_output.py "MacBook Pro-Lautsprecher"
    ;;
  "airpods")
    ~/pfad/zu/select_audio_output.py "AirPods"
    ;;
  "hdmi")
    ~/pfad/zu/select_audio_output.py "HDMI"
    ;;
  "external")
    ~/pfad/zu/select_audio_output.py "Externe Lautsprecher"
    ;;
  *)
    ~/pfad/zu/select_audio_output.py -i
    ;;
esac
```

### Erweiterte Anwendungsfälle

#### Automatischer Wechsel bei Verbindung von Bluetooth-Geräten

Erstellen Sie ein LaunchAgent, der auf Bluetooth-Verbindungen reagiert:

1. Erstellen Sie ein Skript `~/Library/Scripts/audio_switch.sh`:

```bash
#!/bin/bash

# Prüfen, ob AirPods verbunden sind
if system_profiler SPBluetoothDataType | grep -q "AirPods.*Connected"; then
    ~/pfad/zu/select_audio_output.py "AirPods"
    # Optional: Lautstärke anpassen
    ~/pfad/zu/select_audio_output.py -v 40
    exit 0
fi

# Wenn keine AirPods verbunden sind, zu Standardgerät wechseln
~/pfad/zu/select_audio_output.py "MacBook Pro-Lautsprecher"
```

2. Machen Sie das Skript ausführbar:

```bash
chmod +x ~/Library/Scripts/audio_switch.sh
```

3. Erstellen Sie einen LaunchAgent `~/Library/LaunchAgents/com.user.audio_switch.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.audio_switch</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>~/Library/Scripts/audio_switch.sh</string>
    </array>
    <key>WatchPaths</key>
    <array>
        <string>/Library/Preferences/com.apple.Bluetooth.plist</string>
    </array>
</dict>
</plist>
```

4. Laden Sie den LaunchAgent:

```bash
launchctl load ~/Library/LaunchAgents/com.user.audio_switch.plist
```

#### Zeitgesteuerter Wechsel für Tag/Nacht-Modus

Erstellen Sie einen Cron-Job, der je nach Tageszeit das Audio-Ausgabegerät und die Lautstärke anpasst:

```bash
# Crontab-Eintrag (crontab -e)
# Um 8 Uhr morgens zu Lautsprechern mit höherer Lautstärke wechseln
0 8 * * * ~/pfad/zu/select_audio_output.py "MacBook Pro-Lautsprecher" && ~/pfad/zu/select_audio_output.py -v 70

# Um 22 Uhr abends zu Kopfhörern mit niedrigerer Lautstärke wechseln
0 22 * * * ~/pfad/zu/select_audio_output.py "AirPods" && ~/pfad/zu/select_audio_output.py -v 30
```

#### Verwendung mit Fokus-Modi in macOS

Erstellen Sie Automationen für verschiedene Fokus-Modi:

1. Öffnen Sie Systemeinstellungen > Fokus
2. Wählen Sie einen Fokus-Modus (z.B. "Arbeit")
3. Klicken Sie auf "Automation hinzufügen"
4. Wählen Sie "Fokus beginnt" als Auslöser
5. Wählen Sie "Öffne App" und wählen Sie "Automator"
6. Erstellen Sie einen Automator-Workflow, der Ihr Audio-Ausgabegerät wechselt

### Fehlerbehebung

#### SwitchAudioSource nicht gefunden

```
Error: SwitchAudioSource not found. Install via `brew install switchaudio-osx`.
```

Lösung:
```bash
# Installieren Sie SwitchAudioSource über Homebrew
brew install switchaudio-osx

# Wenn Homebrew nicht installiert ist, installieren Sie es zuerst
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Berechtigungsprobleme bei der Lautstärkeregelung

```
Die Lautstärkeregelung ist auf diesem System nicht verfügbar.
Möglicherweise werden zusätzliche Berechtigungen benötigt.
```

Lösungen:

1. Stellen Sie sicher, dass Ihr Terminal Zugriff auf Bedienungshilfen hat:
   - Systemeinstellungen > Sicherheit & Datenschutz > Datenschutz > Bedienungshilfen
   - Fügen Sie Ihr Terminal (Terminal.app oder iTerm) zur Liste hinzu

2. Erteilen Sie die Berechtigung manuell:
   ```bash
   osascript -e 'tell application "System Events" to set volume output volume 50'
   ```
   (Bestätigen Sie die Berechtigungsanfrage)

#### Gerät wird nicht gefunden

```
Kein passendes Gerät für 'Gerätename' gefunden.
```

Lösungen:

1. Listen Sie alle verfügbaren Geräte auf, um den exakten Namen zu sehen:
   ```bash
   ./select_audio_output.py
   ```

2. Verwenden Sie den interaktiven Modus, um das Gerät auszuwählen:
   ```bash
   ./select_audio_output.py -i
   ```

3. Versuchen Sie, einen Teil des Namens zu verwenden (Fuzzy-Matching):
   ```bash
   ./select_audio_output.py "Teil des Namens"
   ```

#### Python-Abhängigkeiten fehlen

```
ModuleNotFoundError: No module named 'questionary'
```

Lösung:
```bash
pip3 install -r requirements.txt
```

## Tipps

- Das Tool verfügt über ein intelligentes Matching-System für Gerätenamen:
  - Groß-/Kleinschreibung wird ignoriert (z.B. "airpods" findet "AirPods")
  - Teilnamen werden erkannt (z.B. "speaker" findet "MacBook Pro-Lautsprecher")
  - Tippfehler werden automatisch korrigiert (z.B. "airpod" findet "AirPods")
  - Bei mehreren ähnlichen Treffern wird das kürzeste/spezifischste Gerät ausgewählt
- Im interaktiven Modus wird das aktuell aktive Gerät mit "(aktiv)" gekennzeichnet.
- Der interaktive Modus bietet auch Optionen zur Lautstärkeregelung und Stummschaltung.
- Sie können das Skript in Ihr System-PATH aufnehmen oder einen Alias in Ihrer Shell-Konfiguration erstellen, um es von überall aufrufen zu können.

### Tastenkürzel im interaktiven Modus

| Taste | Funktion |
|-------|----------|
| ↑ / ↓ | Navigation durch die Liste |
| Enter | Auswahl bestätigen |
| Esc | Abbrechen |
| Strg+C | Abbrechen |

### Praktische Beispiele für den Alltag

#### Schneller Wechsel zwischen Geräten während eines Meetings

```bash
# Vor dem Meeting: Zu Headset wechseln
./select_audio_output.py "Headset"

# Während des Meetings: Stummschalten für eine kurze Unterbrechung
./select_audio_output.py -m

# Nach dem Meeting: Zurück zu Lautsprechern mit angenehmer Lautstärke
./select_audio_output.py "Lautsprecher" && ./select_audio_output.py -v 60
```

#### Automatisierung für verschiedene Anwendungen

```bash
# Skript für Musikwiedergabe mit optimaler Lautstärke
music_mode() {
    ~/pfad/zu/select_audio_output.py "Externe Lautsprecher" && ~/pfad/zu/select_audio_output.py -v 70
    echo "Musikmodus aktiviert: Externe Lautsprecher mit optimaler Lautstärke"
}

# Skript für Videoanrufe mit optimaler Einstellung
call_mode() {
    ~/pfad/zu/select_audio_output.py "AirPods Pro" && ~/pfad/zu/select_audio_output.py -v 50
    echo "Anrufmodus aktiviert: AirPods Pro mit mittlerer Lautstärke"
}

# Skript für Filmabend mit HDMI-Ausgang
movie_mode() {
    ~/pfad/zu/select_audio_output.py "HDMI" && ~/pfad/zu/select_audio_output.py -v 80
    echo "Filmmodus aktiviert: HDMI-Ausgang mit hoher Lautstärke"
}
```

#### Integration in den Arbeitsablauf

```bash
# Beim Start des Computers: Standardgerät mit angenehmer Lautstärke
~/pfad/zu/select_audio_output.py "MacBook Pro-Lautsprecher" && ~/pfad/zu/select_audio_output.py -v 50

# Vor einem Meeting: Meeting-Skript ausführen
pre_meeting() {
    # Zu Headset wechseln
    ~/pfad/zu/select_audio_output.py "Headset"
    
    # Benachrichtigung anzeigen
    osascript -e 'display notification "Audio auf Headset umgeschaltet" with title "Meeting-Vorbereitung"'
    
    # Optional: Andere Meeting-Vorbereitungen
    open "https://zoom.us"
}

# Nach Feierabend: Unterhaltungsmodus
after_work() {
    # Zu hochwertigen Lautsprechern wechseln
    ~/pfad/zu/select_audio_output.py "Externe Lautsprecher" && ~/pfad/zu/select_audio_output.py -v 65
    
    # Optional: Musik starten
    open -a "Spotify"
}
```

#### Verwendung mit mehreren Monitoren und Audio-Ausgängen

```bash
# Skript zum Umschalten auf externen Monitor mit passendem Audio
external_display_mode() {
    # Prüfen, ob externer Monitor verbunden ist
    if system_profiler SPDisplaysDataType | grep -q "DELL"; then
        # Zu HDMI-Audio wechseln
        ~/pfad/zu/select_audio_output.py "HDMI"
        echo "Auf externen Monitor und HDMI-Audio umgeschaltet"
    else
        echo "Kein externer Monitor gefunden"
    fi
}

# Skript zum Zurückschalten auf internen Monitor mit internem Audio
internal_display_mode() {
    # Zu internen Lautsprechern wechseln
    ~/pfad/zu/select_audio_output.py "MacBook Pro-Lautsprecher"
    echo "Auf internen Monitor und interne Lautsprecher umgeschaltet"
}
