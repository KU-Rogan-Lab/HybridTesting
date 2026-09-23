import tkinter as tk
from tkinter import ttk
from motor_control import MotorControlFrame
from voltage_control import VoltageControlFrame
from landing_sequence import LandingSequenceFrame
from metadata import MetadataFrame
from saftey import ButtonLockout

# ============================================================
# Main Application
# ============================================================

class MeasurementApp(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Hybrid Measurement System")
        self.geometry("900x800")

        self.create_layout()

    def create_layout(self):

        main = ttk.Frame(
            self,
            padding=15
        )

        main.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Motor / Stage
        # ----------------------------------------------------

        self.motor_control = MotorControlFrame(main)

        self.motor_control.pack(
            fill="x",
            pady=(0, 10)
        )
        
        self.landing_control = LandingSequenceFrame(main)
        self.landing_control.pack(
            fill="x",
            pady=(0,10)
        )

        # ----------------------------------------------------
        # Voltage
        # ----------------------------------------------------

        self.voltage_control = VoltageControlFrame(main)

        self.voltage_control.pack(
            fill="x",
            pady=(0, 10)
        )

        # ----------------------------------------------------
        # Metadata
        # ----------------------------------------------------

        self.metadata = MetadataFrame(main)

        self.metadata.pack(
            fill="x"
        )


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    app = MeasurementApp()
    app.mainloop()
