#!/usr/bin/env python3
"""
select_audio_output.py - A command-line tool for macOS to easily switch between audio output devices.

This script provides functionality to:
- List all available audio output devices
- Display the currently active audio output device
- Switch to a specific audio output device by name
- Toggle mute/unmute
- Control volume directly from the command line
- Interactive mode for selecting devices with arrow keys
- Smart fuzzy matching for device names (automatically detects and corrects typos)
"""
import argparse
import subprocess
import sys
import questionary
import difflib  # For similarity comparisons of device names

def list_devices():
    """
    Return a list of available audio output devices.
    
    Uses the SwitchAudioSource command-line tool to get all available output devices.
    
    Returns:
        list: A list of strings containing the names of all available audio output devices.
    """
    try:
        result = subprocess.run(
            ['SwitchAudioSource', '-t', 'output', '-a'],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
    except FileNotFoundError:
        print("Error: SwitchAudioSource not found. Install via `brew install switchaudio-osx`.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error listing devices: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    # Each line is a device name
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]

def get_current_device():
    """
    Determines the currently active audio output device.
    
    Returns:
        str: The name of the current audio output device, or None if it couldn't be determined.
    """
    try:
        result = subprocess.run(
            ['SwitchAudioSource', '-c', '-t', 'output'],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_volume():
    """
    Determines the current volume level (0-100).
    
    Tries multiple AppleScript commands to get the current volume level.
    
    Returns:
        int: The current volume level (0-100), or None if it couldn't be determined.
    """
    try:
        # Try different AppleScript commands to determine the volume
        commands = [
            # Standard command
            'output volume of (get volume settings)',
            # Alternative with System Events
            'tell application "System Events" to get output volume of (get volume settings)',
            # Simple command
            'output volume of (get volume settings)'
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run(
                    ['osascript', '-e', cmd],
                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True
                )
                output = result.stdout.strip()
                if output and output != "missing value":
                    return int(output)
            except (subprocess.CalledProcessError, ValueError):
                continue
                
                # If none of the methods worked, output an error message
        print("Volume control is not available on this system.", file=sys.stderr)
        print("Additional permissions may be required.", file=sys.stderr)
        print("The device switching functionality is not affected and continues to work.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error determining volume: {e}", file=sys.stderr)
        print("The device switching functionality is not affected and continues to work.", file=sys.stderr)
        return None

def set_volume(level):
    """
    Sets the volume to a specific level (0-100).
    
    Args:
        level (int): The volume level to set (0-100).
        
    Returns:
        bool: True if successful, False otherwise.
    """
    # Ensure the value is within the valid range
    level = max(0, min(100, level))
    
    try:
        # Try different AppleScript commands to set the volume
        commands = [
            # Standard command
            f'set volume output volume {level}',
            # Alternative with System Events
            f'tell application "System Events" to set volume output volume {level}',
            # Simple command (macOS uses 0-10 for simple volume setting)
            f'set volume {level/10}'  # macOS verwendet 0-10 für einfache Lautstärkeeinstellung
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run(
                    ['osascript', '-e', cmd],
                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True
                )
                # If no error occurred, the command was successful
                print(f"Volume set to {level}%")
                return True
            except subprocess.CalledProcessError:
                continue
                
                # If none of the methods worked, output an error message
        print("Volume control is not available on this system.", file=sys.stderr)
        print("Additional permissions may be required.", file=sys.stderr)
        print("The device switching functionality is not affected and continues to work.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error setting volume: {e}", file=sys.stderr)
        print("The device switching functionality is not affected and continues to work.", file=sys.stderr)
        return False

def adjust_volume(delta):
    """
    Increases or decreases the volume by a specific amount.
    
    Args:
        delta (int): The amount to change the volume by (positive to increase, negative to decrease).
        
    Returns:
        bool: True if successful, False otherwise.
    """
    current_volume = get_volume()
    if current_volume is None:
        print("Volume could not be adjusted because the current volume could not be determined.", file=sys.stderr)
        print("The device switching functionality is not affected and continues to work.", file=sys.stderr)
        return False
    
    new_volume = max(0, min(100, current_volume + delta))
    return set_volume(new_volume)

def toggle_mute():
    """
    Toggles mute/unmute for the audio output.
    
    Attempts to determine the current mute state and then toggle it.
    
    Returns:
        bool: The new mute state (True for muted, False for unmuted), or None if unsuccessful.
    """
    try:
        # Try different AppleScript commands to check the mute state
        commands_check = [
            # Standard command
            'output muted of (get volume settings)',
            # Alternative with System Events
            'tell application "System Events" to get output muted of (get volume settings)'
        ]
        
        is_muted = None
        for cmd in commands_check:
            try:
                check_mute = subprocess.run(
                    ['osascript', '-e', cmd],
                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True
                )
                output = check_mute.stdout.strip()
                if output and output != "missing value":
                    is_muted = (output == 'true')
                    break
            except subprocess.CalledProcessError:
                continue
        
        if is_muted is None:
            print("Mute control is not available on this system.", file=sys.stderr)
            print("Additional permissions may be required.", file=sys.stderr)
            print("The device switching functionality is not affected and continues to work.", file=sys.stderr)
            return None
        
        # Toggle mute state
        state = 'false' if is_muted else 'true'
        
        # Try different AppleScript commands to set the mute state
        commands_set = [
            # Standard command
            f'set volume output muted {state}',
            # Alternative with System Events
            f'tell application "System Events" to set volume output muted {state}'
        ]
        
        for cmd in commands_set:
            try:
                subprocess.run(
                    ['osascript', '-e', cmd],
                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True
                )
                print(f"Audio {'unmuted' if is_muted else 'muted'}")
                return not is_muted
            except subprocess.CalledProcessError:
                continue
        
        print("Mute state could not be toggled.", file=sys.stderr)
        print("Additional permissions may be required.", file=sys.stderr)
        print("The device switching functionality is not affected and continues to work.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error toggling mute state: {e}", file=sys.stderr)
        print("The device switching functionality is not affected and continues to work.", file=sys.stderr)
        return None

def find_closest_device(name, devices):
    """
    Finds the most similar device name when no exact match is found.
    
    Uses multiple matching strategies:
    1. Exact match (case-insensitive)
    2. Substring matching (checks if the name is contained in a device name)
    3. Fuzzy matching with difflib for typo tolerance
    
    Args:
        name (str): The device name to search for
        devices (list): List of available devices
        
    Returns:
        str: The most similar device, or None if no matching device was found
    """
    if not devices:
        return None
    
    # Strategy 1: Case-insensitive exact match
    name_lower = name.lower()
    for device in devices:
        if device.lower() == name_lower:
            return device
    
    # Strategy 2: Substring matching (checks if the name is contained in a device name)
    matching_devices = []
    for device in devices:
        if name_lower in device.lower():
            matching_devices.append(device)
    
    # If exactly one device was found by substring matching, use it
    if len(matching_devices) == 1:
        return matching_devices[0]
    
    # If multiple devices were found, use the shortest one (likely the most specific)
    elif len(matching_devices) > 1:
        return min(matching_devices, key=len)
    
    # Strategy 3: Fuzzy matching with difflib for typo tolerance
    # Lower cutoff value (0.3) for more tolerance with typos
    matches = difflib.get_close_matches(name, devices, n=3, cutoff=0.3)
    return matches[0] if matches else None

def switch_device(name: str):
    """
    Switch the audio output device to the given name.
    
    If the exact device name is not found, attempts to find the closest match
    using fuzzy matching algorithms.
    
    Args:
        name (str): The name of the audio output device to switch to
    """
    # First get all available devices
    devices = list_devices()
    
    # Check if the exact device exists
    if name in devices:
        # Exact device found, switch directly
        try:
            subprocess.run(
                ['SwitchAudioSource', '-t', 'output', '-s', name],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True
            )
            print(f"Switched audio output to: {name}")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error switching device: {e.stderr}", file=sys.stderr)
            sys.exit(1)
    else:
        # No exact device found, search for a similar one
        closest_match = find_closest_device(name, devices)
        
        if closest_match:
            # Similar device found, switch automatically
            try:
                subprocess.run(
                    ['SwitchAudioSource', '-t', 'output', '-s', closest_match],
                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True
                )
                print(f"Similar device found: '{closest_match}'")
                print(f"Switched audio output to: {closest_match}")
                return
            except subprocess.CalledProcessError as e:
                print(f"Error switching device: {e.stderr}", file=sys.stderr)
                sys.exit(1)
        else:
            # No similar device found
            error_msg = f"No matching device found for '{name}'."
            error_msg += "\n\nAvailable devices:"
            for device in devices:
                error_msg += f"\n  • {device}"
            
            print(error_msg, file=sys.stderr)
            sys.exit(1)

def interactive_mode():
    """
    Interactive mode: Selection using arrow keys via questionary.
    
    Displays a list of available devices and additional options for volume control
    and mute toggling. The user can navigate through the list with arrow keys and
    select an option with Enter.
    """
    devices = list_devices()
    if not devices:
        print("No audio output devices found.", file=sys.stderr)
        sys.exit(1)

    # Determine current device
    current_device = get_current_device()
    
    # Create options with marking of the active device
    choices = []
    for device in devices:
        if device == current_device:
            choices.append(f"{device} (active)")
        else:
            choices.append(device)
    
    # Test if mute functionality is available
    # We perform a test without actually toggling
    test_mute = None
    try:
        test_mute = subprocess.run(
            ['osascript', '-e', 'output muted of (get volume settings)'],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        ).stdout.strip()
    except:
        pass
    
    # Only add mute option if the functionality is available
    if test_mute is not None and test_mute != "missing value":
        choices.append("-- Toggle mute --")
    
    # Only add volume options if the functionality is available
    # We test this by trying to determine the current volume
    test_volume = get_volume()
    if test_volume is not None:
        choices.append("-- Show volume --")
        choices.append("-- Increase volume (+10%) --")
        choices.append("-- Decrease volume (-10%) --")
        choices.append("-- Adjust volume... --")

    choice = questionary.select(
        "Please select audio output device:",
        choices=choices
    ).ask()

    if choice is None:
        # Abort with ESC or Ctrl+C
        print("Aborted.", file=sys.stderr)
        sys.exit(1)

    # Audio control options
    if choice == "-- Toggle mute --":
        toggle_mute()
        return
    elif choice == "-- Show volume --":
        volume = get_volume()
        if volume is not None:
            print(f"Current volume: {volume}%")
        return
    elif choice == "-- Increase volume (+10%) --":
        adjust_volume(10)
        return
    elif choice == "-- Decrease volume (-10%) --":
        adjust_volume(-10)
        return
    elif choice == "-- Adjust volume... --":
        # Ask user for volume value
        volume_input = questionary.text(
            "Enter volume (0-100%):",
            validate=lambda text: text.isdigit() and 0 <= int(text) <= 100
        ).ask()
        
        if volume_input is None:
            print("Aborted.", file=sys.stderr)
            return
            
        set_volume(int(volume_input))
        return
        
    # If "(active)" is part of the selection, remove it
    if " (active)" in choice:
        choice = choice.replace(" (active)", "")

    switch_device(choice)

def main():
    parser = argparse.ArgumentParser(
        description="Select a macOS audio output device by name and control volume settings."
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Interactive mode: Selection using arrow keys"
    )
    parser.add_argument(
        "-c", "--current",
        action="store_true",
        help="Shows the current audio output device"
    )
    parser.add_argument(
        "-m", "--toggle-mute",
        action="store_true",
        help="Toggles mute/unmute"
    )
    parser.add_argument(
        "-g", "--get-volume",
        action="store_true",
        help="Shows the current volume level"
    )
    parser.add_argument(
        "-v", "--volume",
        type=int,
        metavar="LEVEL",
        help="Sets the volume to a specific level (0-100)"
    )
    parser.add_argument(
        "-u", "--volume-up",
        type=int,
        metavar="AMOUNT",
        help="Increases the volume by a specific amount"
    )
    parser.add_argument(
        "-d", "--volume-down",
        type=int,
        metavar="AMOUNT",
        help="Decreases the volume by a specific amount"
    )
    parser.add_argument(
        "device",
        nargs="?",
        help="Name of the audio output device. If omitted, lists available devices."
    )
    args = parser.parse_args()

    # Process volume options
    if args.get_volume:
        volume = get_volume()
        if volume is not None:
            print(f"Current volume: {volume}%")
        sys.exit(0)
        
    if args.volume is not None:
        success = set_volume(args.volume)
        if not success:
            sys.exit(1)
        sys.exit(0)
        
    if args.volume_up is not None:
        success = adjust_volume(args.volume_up)
        if not success:
            sys.exit(1)
        sys.exit(0)
        
    if args.volume_down is not None:
        success = adjust_volume(-args.volume_down)
        if not success:
            sys.exit(1)
        sys.exit(0)

    if args.toggle_mute:
        result = toggle_mute()
        if result is None:
            sys.exit(1)
        sys.exit(0)

    if args.current:
        current = get_current_device()
        if current:
            print(f"{current}")
        else:
            print("Error determining the current device", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    if args.interactive:
        interactive_mode()
        sys.exit(0)

    if args.device is None:
        current = get_current_device()
        print("Available output devices:")  # This was already in English
        for dev in list_devices():
            marker = " (active)" if dev == current else ""
            print(f"  • {dev}{marker}")
        sys.exit(0)

    switch_device(args.device)

if __name__ == "__main__":
    main()
