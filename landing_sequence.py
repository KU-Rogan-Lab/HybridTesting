import tkinter as tk
from tkinter import ttk
from saftey import ButtonLockout
BUTTON_LOCKOUT_MS = 1000

#=============================================================
# Landing Sequence Control
#=============================================================


class LandingSequenceFrame(ttk.LabelFrame):

    def __init__(self, parent, motor=None):
        super().__init__(
            parent,
            text="Landing Sequence",
            padding=10
        )

        self.motor = motor

        # Sequence state
        self.sequence = []
        self.current_index = 0
        self.sequence_active = False

        self.create_widgets()
        self.create_layout()

    # ========================================================
    # Widgets
    # ========================================================

    def create_widgets(self):

        self.sequence_var = tk.StringVar()

        self.sequence_entry = ttk.Entry(
            self,
            textvariable=self.sequence_var,
            width=35
        )

        self.previous_label = ttk.Label(
            self,
            text="--",
            anchor="center"
        )

        self.current_label = ttk.Label(
            self,
            text="--",
            anchor="center"
        )

        self.next_label = ttk.Label(
            self,
            text="--",
            anchor="center"
        )
        
        self.load_button = ttk.Button(
           self,
           text="Load Sequence",
           command=self.load_sequence
        )

        self.step_button = ttk.Button(
            self,
            text="Raise Current Step",
            command=self.execute_current_step
        )
        
        self.step_lockout = ButtonLockout(
    		self.step_button,
    		duration_ms=BUTTON_LOCKOUT_MS
		)

        self.cancel_button = ttk.Button(
            self,
            text="Cancel Sequence",
            command=self.cancel_sequence
        )

    # ========================================================
    # Layout
    # ========================================================

    def create_layout(self):

        # ----------------------------------------------------
        # Sequence entry
        # ----------------------------------------------------

        ttk.Label(
            self,
            text="Sequence (mm):"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="e"
        )

        self.sequence_entry.grid(
            row=0,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # ----------------------------------------------------
        # Previous / Current / Next headings
        # ----------------------------------------------------

        ttk.Label(
            self,
            text="Previous"
        ).grid(
            row=1,
            column=1,
            padx=10,
            pady=(10, 2)
        )

        ttk.Label(
            self,
            text="Current"
        ).grid(
            row=1,
            column=2,
            padx=10,
            pady=(10, 2)
        )

        ttk.Label(
            self,
            text="Next"
        ).grid(
            row=1,
            column=3,
            padx=10,
            pady=(10, 2)
        )

        # ----------------------------------------------------
        # Values
        # ----------------------------------------------------

        self.previous_label.grid(
            row=2,
            column=1,
            padx=10,
            pady=5
        )

        self.current_label.grid(
            row=2,
            column=2,
            padx=10,
            pady=5
        )

        self.next_label.grid(
            row=2,
            column=3,
            padx=10,
            pady=5
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        # ----------------------------------------------------
        # Load sequence
        # ----------------------------------------------------

        self.load_button.grid(
            row=3,
            column=1,
            columnspan=2,
            padx=5,
            pady=10,
            sticky="ew"
        )   

    # ----------------------------------------------------
    # Execute / Cancel  
    # ----------------------------------------------------

        self.step_button.grid(
            row=4,
            column=1,
            padx=5,
            pady=10,
            sticky="ew"
        )

        self.cancel_button.grid(
            row=4,
            column=2,
            padx=5,
            pady=10,
            sticky="ew"
        )
    # ========================================================
    # Sequence handling
    # ========================================================

    def load_sequence(self):

        sequence_text = self.sequence_var.get().strip()

        try:

            sequence = [
                float(step.strip())
                for step in sequence_text.split(";")
                if step.strip() != ""
            ]

        except ValueError:

            print("Invalid landing sequence.")
            return

        if not sequence:
            print("Landing sequence is empty.")
            return

        # Store the validated sequence
        self.sequence = sequence

        # Start at the first step
        self.current_index = 0
        self.sequence_active = True

        self.update_display()

        print(f"Loaded landing sequence: {self.sequence}")

    # ========================================================
    # Display
    # ========================================================

    def update_display(self):

        if not self.sequence_active:
            self.previous_label.config(text="--")
            self.current_label.config(text="--")
            self.next_label.config(text="--")
            return

        # Previous
        if self.current_index == 0:
            previous = "--"
        else:
            previous = self.sequence[self.current_index - 1]

        # Current
        current = self.sequence[self.current_index]

        # Next
        if self.current_index + 1 >= len(self.sequence):
            next_step = "--"
        else:
            next_step = self.sequence[self.current_index + 1]

        self.previous_label.config(
            text=str(previous)
        )

        self.current_label.config(
            text=str(current)
        )

        self.next_label.config(
            text=str(next_step)
        )

    # ========================================================
    # Execute current step
    # ========================================================

    def execute_current_step(self):

        if not self.step_lockout.lock():
        	return
        
        if not self.sequence_active:
            print("No landing sequence loaded.")
            return

        current_step = self.sequence[self.current_index]

        print(f"Raising stage by {current_step} mm")

        # Your actual motor call:
        #
        # self.motor.raise_lift(current_step)

        self.current_index += 1

        # Sequence finished
        if self.current_index >= len(self.sequence):

            print("Landing sequence complete.")

            self.sequence_active = False

            self.previous_label.config(
                text=str(current_step)
            )

            self.current_label.config(
                text="Complete"
            )

            self.next_label.config(
                text="--"
            )

            return

        self.update_display()

    # ========================================================
    # Cancel
    # ========================================================

    def cancel_sequence(self):

        print("Landing sequence cancelled.")

        self.sequence = []
        self.current_index = 0
        self.sequence_active = False

        self.update_display()
