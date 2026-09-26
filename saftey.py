import tkinter as tk
from tkinter import ttk


class ButtonLockout:

    def __init__(self, button, duration_ms=1000):
        self.button = button
        #self.duration_ms = duration_ms
        self.locked = False
        #self.after_id = None

    def lock(self):
        print("LOCKOUT: lock() called, locked =", self.locked)

        if self.locked:
            print("LOCKOUT: already locked, rejected press")
            return False

        self.locked = True
        self.button.config(state="disabled")
        print("LOCKOUT: BUTTON DISABLED")

        #self.after_id = self.button.after(
        #    self.duration_ms,
        #    self.unlock
        #)

        return True

    def unlock(self):

        self.locked = False
        self.button.config(state="normal")
        #self.after_id = None
        print("LOCKOUT, BUTTON ENABLED")
