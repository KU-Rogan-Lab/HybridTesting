import tkinter as tk
from tkinter import ttk
from gui_components.i2c_control import I2CControlFrame
from gui_components.metadata import MetadataFrame
from gui_components.safety import ButtonLockout



# ============================================================
# Main Application
# ============================================================

class MeasurementApp(tk.Tk):

    def __init__(self, powersupply=None):

        super().__init__()
        
        self.powersupply = powersupply
        
        self.title("I2C Measurement System")
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
        # Metadata
        # ----------------------------------------------------

        self.metadata = MetadataFrame(main)

        self.metadata.pack(
            fill="x"
        )

        # ----------------------------------------------------
        # I2C 
        # ----------------------------------------------------

        self.i2c_control = I2CControlFrame(main,self.metadata,powersupply)

        self.i2c_control.pack(
            fill="x",
            pady=(0, 10)
        )
        


        
        
 

# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    #MOTORS_PORT = 'COM4'
    #motors = motion.motion(port=MOTORS_PORT, emulate=False)
    #do this for power supply
    powersupply = None
    
  
    
    app = MeasurementApp(powersupply)
    app.mainloop()
