# select_audio_output

A command-line tool for macOS that allows you to quickly and easily switch between different audio output devices.

## Features

- List all available audio output devices
- Display the currently active audio output device
- Switch to a specific audio output device by name
- Toggle mute/unmute
- Control volume directly from the command line
- Interactive mode for selecting devices with arrow keys
- Intelligent fuzzy matching for device names (automatically detects and corrects typos)

## Requirements

- macOS
- Python 3.6 or higher
- [SwitchAudioSource](https://github.com/deweller/switchaudio-osx) (installable via Homebrew)

## Installation

1. Make sure Python 3 is installed:
   ```
   python3 --version
   ```

2. Install SwitchAudioSource via Homebrew:
   ```
   brew install switchaudio-osx
   ```

3. Clone this repository or download the files.

4. Install the required Python dependencies:
   ```
   pip3 install -r requirements.txt
   ```

5. Make the script executable:
   ```
   chmod +x select_audio_output.py
   ```

## Usage

### List all available audio output devices

```
./select_audio_output.py
```

Output:
```
Available output devices:
  • MacBook Pro Speakers (active)
  • AirPods Pro
  • External Speakers
  • HDMI Output
```

### Display the currently active audio output device

```
./select_audio_output.py -c
```

or

```
./select_audio_output.py --current
```

Output:
```
MacBook Pro Speakers
```

### Switch to a specific audio output device

```
./select_audio_output.py "Device name"
```

Examples:
```
# Exact name
./select_audio_output.py "MacBook Pro Speakers"

# With fuzzy matching (partial name)
./select_audio_output.py "Speakers"

# With fuzzy matching (typos)
./select_audio_output.py "MacBok Spekers"

# With fuzzy matching (case insensitive)
./select_audio_output.py "airpods"

# With fuzzy matching (abbreviations)
./select_audio_output.py "AP Pro"  # Finds "AirPods Pro"

# With fuzzy matching (partial words)
./select_audio_output.py "extern"  # Finds "External Speakers"

# With fuzzy matching (numbers and special characters)
./select_audio_output.py "hdmi2"   # Finds "HDMI Output 2"
```

### Toggle mute

```
./select_audio_output.py -m
```

or

```
./select_audio_output.py --toggle-mute
```

Output:
```
Audio muted
```
or
```
Audio unmuted
```

### Volume control

#### Display current volume

```
./select_audio_output.py -g
```

or

```
./select_audio_output.py --get-volume
```

Output:
```
Current volume: 75%
```

#### Set volume to a specific value (0-100)

```
./select_audio_output.py -v 50
```

or

```
./select_audio_output.py --volume 50
```

Output:
```
Volume set to 50%
```

#### Increase volume

```
./select_audio_output.py -u 10
```

or

```
./select_audio_output.py --volume-up 10
```

Output:
```
Volume set to 60%
```

#### Decrease volume

```
./select_audio_output.py -d 10
```

or

```
./select_audio_output.py --volume-down 10
```

Output:
```
Volume set to 40%
```

### Interactive mode (selection with arrow keys)

```
./select_audio_output.py -i
```

or

```
./select_audio_output.py --interactive
```

In interactive mode, you can navigate through the available devices using the arrow keys ↑ and ↓ and select with Enter:

```
? Please select audio output device: (Use arrow keys)
 > MacBook Pro Speakers (active)
   AirPods Pro
   External Speakers
   HDMI Output
   -- Toggle mute --
   -- Display volume --
   -- Increase volume (+10%) --
   -- Decrease volume (-10%) --
   -- Adjust volume... --
```

### Combined commands and workflows

#### Switch device and adjust volume

You can execute multiple commands in sequence to perform complex actions:

```bash
# Switch to AirPods and set volume to 40%
./select_audio_output.py "AirPods" && ./select_audio_output.py -v 40

# Switch to external speakers and increase volume
./select_audio_output.py "External" && ./select_audio_output.py -u 20

# Switch to MacBook speakers and mute
./select_audio_output.py "MacBook" && ./select_audio_output.py -m
```

#### Usage in shell scripts

Example of a simple shell script that switches the audio output device based on the time of day:

```bash
#!/bin/bash

HOUR=$(date +%H)

if [ $HOUR -ge 22 ] || [ $HOUR -lt 8 ]; then
    # Evening/Night: Switch to headphones and reduce volume
    ./select_audio_output.py "AirPods" && ./select_audio_output.py -v 30
    echo "Night mode: AirPods with reduced volume"
else
    # Daytime: Switch to speakers with normal volume
    ./select_audio_output.py "Speakers" && ./select_audio_output.py -v 70
    echo "Day mode: Speakers with normal volume"
fi
```

#### Usage with shell aliases

Add these lines to your `.zshrc` or `.bashrc` to create convenient aliases:

```bash
# Quick audio device switching
alias speakers="~/path/to/select_audio_output.py 'MacBook Pro Speakers'"
alias airpods="~/path/to/select_audio_output.py 'AirPods' && ~/path/to/select_audio_output.py -v 40"
alias hdmi="~/path/to/select_audio_output.py 'HDMI'"
alias extspk="~/path/to/select_audio_output.py 'External Speakers' && ~/path/to/select_audio_output.py -v 60"

# Volume control
alias vol="~/path/to/select_audio_output.py -g"
alias vol50="~/path/to/select_audio_output.py -v 50"
alias vol+="~/path/to/select_audio_output.py -u 10"
alias vol-="~/path/to/select_audio_output.py -d 10"
alias mute="~/path/to/select_audio_output.py -m"

# Interactive mode
alias audio="~/path/to/select_audio_output.py -i"
```

### Integration with other tools

#### Usage with AppleScript

```applescript
-- AppleScript to switch to AirPods when they are connected
tell application "System Events"
    set airpodsConnected to do shell script "system_profiler SPBluetoothDataType | grep -q 'AirPods.*Connected' && echo 'yes' || echo 'no'"
    
    if airpodsConnected is "yes" then
        do shell script "~/path/to/select_audio_output.py 'AirPods'"
    else
        do shell script "~/path/to/select_audio_output.py 'MacBook Pro Speakers'"
    end if
end tell
```

#### Usage with Automator

Create an Automator shortcut that switches the audio output device based on the connected device:

1. Open Automator and create a new shortcut
2. Add the "Run Shell Script" action
3. Add the following code:

```bash
# Check if HDMI is connected
if system_profiler SPDisplaysDataType | grep -q "HDMI"; then
    ~/path/to/select_audio_output.py "HDMI"
# Check if AirPods are connected
elif system_profiler SPBluetoothDataType | grep -q "AirPods.*Connected"; then
    ~/path/to/select_audio_output.py "AirPods"
# Otherwise switch to MacBook speakers
else
    ~/path/to/select_audio_output.py "MacBook Pro Speakers"
fi
```

4. Save the shortcut and run it when you want to automatically switch your audio output device

#### Usage with Keyboard Maestro

Create a Keyboard Maestro macro that switches the audio output device with a keyboard shortcut:

1. Create a new macro in Keyboard Maestro
2. Add a trigger (e.g., keyboard shortcut ⌥⌘A for AirPods)
3. Add the "Execute Shell Script" action:

```bash
~/path/to/select_audio_output.py "AirPods"
```

4. Create additional macros for other devices with different keyboard shortcuts

#### Usage with Alfred or Raycast

Create workflows or scripts for Alfred or Raycast:

```bash
# Alfred/Raycast script for quick device switching
case "$1" in
  "speakers")
    ~/path/to/select_audio_output.py "MacBook Pro Speakers"
    ;;
  "airpods")
    ~/path/to/select_audio_output.py "AirPods"
    ;;
  "hdmi")
    ~/path/to/select_audio_output.py "HDMI"
    ;;
  "external")
    ~/path/to/select_audio_output.py "External Speakers"
    ;;
  *)
    ~/path/to/select_audio_output.py -i
    ;;
esac
```

### Advanced use cases

#### Automatic switching when Bluetooth devices connect

Create a LaunchAgent that responds to Bluetooth connections:

1. Create a script `~/Library/Scripts/audio_switch.sh`:

```bash
#!/bin/bash

# Check if AirPods are connected
if system_profiler SPBluetoothDataType | grep -q "AirPods.*Connected"; then
    ~/path/to/select_audio_output.py "AirPods"
    # Optional: Adjust volume
    ~/path/to/select_audio_output.py -v 40
    exit 0
fi

# If no AirPods are connected, switch to default device
~/path/to/select_audio_output.py "MacBook Pro Speakers"
```

2. Make the script executable:

```bash
chmod +x ~/Library/Scripts/audio_switch.sh
```

3. Create a LaunchAgent `~/Library/LaunchAgents/com.user.audio_switch.plist`:

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

4. Load the LaunchAgent:

```bash
launchctl load ~/Library/LaunchAgents/com.user.audio_switch.plist
```

#### Time-controlled switching for day/night mode

Create a cron job that adjusts the audio output device and volume based on the time of day:

```bash
# Crontab entry (crontab -e)
# At 8 AM, switch to speakers with higher volume
0 8 * * * ~/path/to/select_audio_output.py "MacBook Pro Speakers" && ~/path/to/select_audio_output.py -v 70

# At 10 PM, switch to headphones with lower volume
0 22 * * * ~/path/to/select_audio_output.py "AirPods" && ~/path/to/select_audio_output.py -v 30
```

#### Usage with Focus modes in macOS

Create automations for different Focus modes:

1. Open System Settings > Focus
2. Select a Focus mode (e.g., "Work")
3. Click "Add Automation"
4. Select "Focus starts" as the trigger
5. Select "Open App" and choose "Automator"
6. Create an Automator workflow that switches your audio output device

### Troubleshooting

#### SwitchAudioSource not found

```
Error: SwitchAudioSource not found. Install via `brew install switchaudio-osx`.
```

Solution:
```bash
# Install SwitchAudioSource via Homebrew
brew install switchaudio-osx

# If Homebrew is not installed, install it first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Permission issues with volume control

```
Volume control is not available on this system.
Additional permissions may be required.
```

Solutions:

1. Make sure your terminal has access to accessibility features:
   - System Settings > Security & Privacy > Privacy > Accessibility
   - Add your terminal (Terminal.app or iTerm) to the list

2. Grant permission manually:
   ```bash
   osascript -e 'tell application "System Events" to set volume output volume 50'
   ```
   (Confirm the permission request)

#### Device not found

```
No matching device found for 'Device name'.
```

Solutions:

1. List all available devices to see the exact name:
   ```bash
   ./select_audio_output.py
   ```

2. Use interactive mode to select the device:
   ```bash
   ./select_audio_output.py -i
   ```

3. Try using a part of the name (fuzzy matching):
   ```bash
   ./select_audio_output.py "Part of the name"
   ```

#### Python dependencies missing

```
ModuleNotFoundError: No module named 'questionary'
```

Solution:
```bash
pip3 install -r requirements.txt
```

## Tips

- The tool has an intelligent matching system for device names:
  - Case is ignored (e.g., "airpods" finds "AirPods")
  - Partial names are recognized (e.g., "speaker" finds "MacBook Pro Speakers")
  - Typos are automatically corrected (e.g., "airpod" finds "AirPods")
  - With multiple similar matches, the shortest/most specific device is selected
- In interactive mode, the currently active device is marked with "(active)".
- The interactive mode also offers options for volume control and muting.
- You can add the script to your system PATH or create an alias in your shell configuration to call it from anywhere.

### Keyboard shortcuts in interactive mode

| Key | Function |
|-------|----------|
| ↑ / ↓ | Navigate through the list |
| Enter | Confirm selection |
| Esc | Cancel |
| Ctrl+C | Cancel |

### Practical examples for everyday use

#### Quick switching between devices during a meeting

```bash
# Before the meeting: Switch to headset
./select_audio_output.py "Headset"

# During the meeting: Mute for a short interruption
./select_audio_output.py -m

# After the meeting: Back to speakers with comfortable volume
./select_audio_output.py "Speakers" && ./select_audio_output.py -v 60
```

#### Automation for different applications

```bash
# Script for music playback with optimal volume
music_mode() {
    ~/path/to/select_audio_output.py "External Speakers" && ~/path/to/select_audio_output.py -v 70
    echo "Music mode activated: External speakers with optimal volume"
}

# Script for video calls with optimal settings
call_mode() {
    ~/path/to/select_audio_output.py "AirPods Pro" && ~/path/to/select_audio_output.py -v 50
    echo "Call mode activated: AirPods Pro with medium volume"
}

# Script for movie night with HDMI output
movie_mode() {
    ~/path/to/select_audio_output.py "HDMI" && ~/path/to/select_audio_output.py -v 80
    echo "Movie mode activated: HDMI output with high volume"
}
```

#### Integration into workflow

```bash
# At computer startup: Default device with comfortable volume
~/path/to/select_audio_output.py "MacBook Pro Speakers" && ~/path/to/select_audio_output.py -v 50

# Before a meeting: Run meeting script
pre_meeting() {
    # Switch to headset
    ~/path/to/select_audio_output.py "Headset"
    
    # Display notification
    osascript -e 'display notification "Audio switched to headset" with title "Meeting preparation"'
    
    # Optional: Other meeting preparations
    open "https://zoom.us"
}

# After work: Entertainment mode
after_work() {
    # Switch to high-quality speakers
    ~/path/to/select_audio_output.py "External Speakers" && ~/path/to/select_audio_output.py -v 65
    
    # Optional: Start music
    open -a "Spotify"
}
```

#### Usage with multiple monitors and audio outputs

```bash
# Script to switch to external monitor with matching audio
external_display_mode() {
    # Check if external monitor is connected
    if system_profiler SPDisplaysDataType | grep -q "DELL"; then
        # Switch to HDMI audio
        ~/path/to/select_audio_output.py "HDMI"
        echo "Switched to external monitor and HDMI audio"
    else
        echo "No external monitor found"
    fi
}

# Script to switch back to internal monitor with internal audio
internal_display_mode() {
    # Switch to internal speakers
    ~/path/to/select_audio_output.py "MacBook Pro Speakers"
    echo "Switched to internal monitor and internal speakers"
}
