import tkinter as tk
from tkinter import ttk
from motor_control import MotorControlFrame
from voltage_control import VoltageControlFrame
from landing_sequence import LandingSequenceFrame
from metadata import MetadataFrame
from saftey import ButtonLockout
import motion
import keithley


# ============================================================
# Main Application
# ============================================================

class MeasurementApp(tk.Tk):

    def __init__(self,motors,keithley):

        super().__init__()
        
       
        self.motors = motors
        self.keithley = keithley
        
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

        self.motor_control = MotorControlFrame(main, motors)

        self.motor_control.pack(
            fill="x",
            pady=(0, 10)
        )
        
        self.landing_control = LandingSequenceFrame(main, motors)
        self.landing_control.pack(
            fill="x",
            pady=(0,10)
        )

        # ----------------------------------------------------
        # Voltage
        # ----------------------------------------------------

        self.voltage_control = VoltageControlFrame(main, keithley)

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

    MOTORS_PORT = 'COM4'
    motors = motion.motion(port=MOTORS_PORT, emulate=False)
    
    KEITHLEY_PORT = 'COM13'
    keithley = keithley.Keithley(port=KEITHLEY_PORT, emulate=False)
    keithley.reset()
    keithley.on()
    
    app = MeasurementApp(motors, keithley)
    app.mainloop()
