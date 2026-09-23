import tkinter as tk
from tkinter import ttk


class ButtonLockout:

    def __init__(self, button, duration_ms=1000):
        self.button = button
        self.duration_ms = duration_ms
        self.locked = False
        self.after_id = None

    def lock(self):

        if self.locked:
            return False

        self.locked = True
        self.button.config(state="disabled")

        self.after_id = self.button.after(
            self.duration_ms,
            self.unlock
        )

        return True

    def unlock(self):

        self.locked = False
        self.button.config(state="normal")
        self.after_id = None
