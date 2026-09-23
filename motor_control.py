import tkinter as tk
from tkinter import ttk
from saftey import ButtonLockout
BUTTON_LOCKOUT_MS = 1000

# ============================================================
# Motor / Stage Control
# ============================================================

class MotorControlFrame(ttk.LabelFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            text="Motor / Stage Control",
            padding=10
        )

        # Create the two internal sections first
        self.xy_frame = ttk.LabelFrame(
            self,
            text="XY Stage",
            padding=10
        )

        self.lift_frame = ttk.LabelFrame(
            self,
            text="Lift Stage",
            padding=10
        )

        # Now create widgets that belong to those sections
        self.create_widgets()

        # Finally arrange everything
        self.create_layout()

    # --------------------------------------------------------
    # Widgets
    # --------------------------------------------------------

    def create_widgets(self):

        # Movement amounts
        self.xy_step_var = tk.StringVar(value="1.0")
        self.lift_step_var = tk.StringVar(value="1.0")

        # -------------------------
        # XY buttons
        # -------------------------

        self.up_button = ttk.Button(
            self.xy_frame,
            text="^('-')^",
            command=self.move_up
        )

        self.down_button = ttk.Button(
            self.xy_frame,
            text="v('-')v",
            command=self.move_down
        )

        self.left_button = ttk.Button(
            self.xy_frame,
            text="<('-'<)",
            command=self.move_left
        )

        self.right_button = ttk.Button(
            self.xy_frame,
            text="(>'-')>",
            command=self.move_right
        )

        # -------------------------
        # Lift buttons
        # -------------------------

        self.raise_button = ttk.Button(
            self.lift_frame,
            text="Raise",
            command=self.raise_lift
        )

        self.lower_button = ttk.Button(
            self.lift_frame,
            text="Lower",
            command=self.lower_lift
        )
        
        self.raise_lockout = ButtonLockout(
            self.raise_button,
            duration_ms=BUTTON_LOCKOUT_MS
        )
        
        self.step_lockout = ButtonLockout(
            self.lower_button,
            duration_ms=BUTTON_LOCKOUT_MS
        )
    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    def create_layout(self):

        # ====================================================
        # Create the two subsections FIRST
        # ====================================================

        self.xy_frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky="n"
        )

        self.lift_frame.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
            sticky="n"
        )

        # ====================================================
        # XY stage
        # ====================================================

        # Direction buttons
        self.up_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            ipadx=10,
            ipady=5
        )

        self.left_button.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            ipadx=10,
            ipady=5
        )

        self.right_button.grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            ipadx=10,
            ipady=5
        )

        self.down_button.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            ipadx=10,
            ipady=5
        )

        # Movement amount
        ttk.Label(
            self.xy_frame,
            text="Move (mm):"
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="e",
            padx=5,
            pady=(10, 5)
        )

        self.xy_step_entry = ttk.Entry(
            self.xy_frame,
            textvariable=self.xy_step_var,
            width=10
        )

        self.xy_step_entry.grid(
            row=3,
            column=2,
            padx=5,
            pady=(10, 5)
        )

        # ====================================================
        # Lift stage
        # ====================================================

        ttk.Label(
            self.lift_frame,
            text="Move (mm):"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=(5, 5)
        )

        self.lift_step_entry = ttk.Entry(
            self.lift_frame,
            textvariable=self.lift_step_var,
            width=10
        )

        self.lift_step_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=5,
            pady=(0, 10)
        )

        self.raise_button.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.lower_button.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        #self.landing_button.grid(
        #    row=3,
        #    column=0,
        #    columnspan=2,
        #    padx=5,
        #    pady=(15, 5),
        #    sticky="ew"
        #)

    # --------------------------------------------------------
    # Hardware callbacks
    # --------------------------------------------------------

    def get_xy_step(self):
        return float(self.xy_step_var.get())

    def get_lift_step(self):
        return float(self.lift_step_var.get())

    def move_up(self):
        distance = self.get_xy_step()
        print(f"Move UP {distance} mm")

        # Example:
        # self.motor.move_up(distance)

    def move_down(self):
        distance = self.get_xy_step()
        print(f"Move DOWN {distance} mm")

        # self.motor.move_down(distance)

    def move_left(self):
        distance = self.get_xy_step()
        print(f"Move LEFT {distance} mm")

        # self.motor.move_left(distance)

    def move_right(self):
        distance = self.get_xy_step()
        print(f"Move RIGHT {distance} mm")

        # self.motor.move_right(distance)

    def raise_lift(self):
        #distance = self.get_lift_step()
        if not self.raise_lockout.lock():
        	return

        distance = self.get_lift_step()
        print(f"RAISE stage {distance} mm")
        # self.motor.raise_lift(distance)

    def lower_lift(self):
        #distance = self.get_lift_step()
        if not self.raise_lockout.lock():
        	return

        distance = self.get_lift_step()
        print(f"LOWER stage {distance} mm")
        # self.motor.lower_lift(distance)

    
