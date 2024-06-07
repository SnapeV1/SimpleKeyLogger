# Keylogger with Screenshot Capture

This project implements a keylogger that captures keyboard input and takes screenshots when it detects a potential login event. The captured screenshots are then sent to a specified email address.

## Features

- Logs all keystrokes
- Detects potential login attempts
- Takes screenshots upon detecting a login
- Sends screenshots to a specified email address

## Requirements

- Python 3.x
- `pynput` library for capturing keystrokes
- `Pillow` library for taking screenshots
- `smtplib` for sending emails
- `ssl` for secure email sending
