import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import sys

# ============================================================
# I2C Control
# ============================================================

class I2CControlFrame(ttk.LabelFrame):

    def __init__(self, parent, metadataFrame,  powersupply):
        super().__init__(
            parent,
            text="I2C Control",
            padding=10
        )
        self.powersupply = powersupply
        self.metadataFrame = metadataFrame
        self.i2c_process = None
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):

        self.vhold_var = tk.StringVar(value="220")

        self.i2c_0V_button = ttk.Button(
            self,
            text="Measure BL/NW @ 0V",
            command=self.measure_nw0
        )

        self.i2c_vhold_button = ttk.Button(
            self,
            text="Measure BL/NW @ Vhold",
            command=self.measure_nw
        )

        self.reset_button = ttk.Button(
            self,
            text="Cancel I2C",
            command=self.cancel_nw
        )

    def create_layout(self):

        # --------------------------------------------------------
        # Voltage parameter inputs
        # --------------------------------------------------------

        parameters = ttk.Frame(self)

        parameters.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 10)
        )
   
        ttk.Label(
            parameters,
            text="Vhold(V)"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.vhold_entry = ttk.Entry(
            parameters,
            textvariable=self.vhold_var,
            width=12
        )

        self.vhold_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        
        # --------------------------------------------------------
        # Control buttons
        # --------------------------------------------------------

        self.i2c_0V_button.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.i2c_vhold_button.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        self.reset_button.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

    def get_parameters(self):
        return {
            "vhold": float(self.vhold_var.get())
        }

    def measure_nw0(self):
        print(f"Measure I2C @ 0V")
        self.launch_i2c_process(0)
    def measure_nw(self):
        parameters = self.get_parameters()
        print(f"Measure I2C @ {parameters['vhold']}V")
        self.launch_i2c_process(parameters['vhold'])
    
    def launch_i2c_process(self, vhold):
        #launch the process that can be cancelled with another method
        # Don't allow another measurement to start
    	# while one is already running.
    	if self.i2c_process is not None:
        	if self.i2c_process.poll() is None:
        	    print("I2C process is already running.")
        	    return

    	print(f"Launching I2C process with Vhold = {vhold} V")

    	# This is the temporary test program.
    	test_code = """
import time
for i in range(1, 21):
    print(f"I2C test: {i}", flush=True)
    time.sleep(1)

print("I2C test finished.", flush=True)
    """

    	self.i2c_process = subprocess.Popen(
        	[
        	    sys.executable,
        	    "-u",
        	    "-c",
         	   test_code
        	]
    	)

    	# Check periodically whether the process has finished.
    	self.check_i2c_process()
    
    def check_i2c_process(self):

    	if self.i2c_process is None:
        	return

    	return_code = self.i2c_process.poll()

    	if return_code is None:
       	 # Still running. Check again in 100 ms.
        	self.after(100, self.check_i2c_process)

    	else:
        	print(f"I2C process finished with return code {return_code}")
        	self.i2c_process = None
       
    def cancel_nw(self):
        #code to cancel the i2c process
    
    	if self.i2c_process is None:
        	print("No I2C process is running.")
        	return

    	if self.i2c_process.poll() is None:

        	print("Cancelling I2C process...")

        	self.i2c_process.terminate()

        	try:
        	    self.i2c_process.wait(timeout=1)

        	except subprocess.TimeoutExpired:
        	    print("Process did not terminate. Killing it.")
        	    self.i2c_process.kill()
        	    self.i2c_process.wait()

        	print("I2C process cancelled.")

    	else:
        	print("I2C process has already finished.")

    	self.i2c_process = None

    #def measure_iv_hold(self):
    #    print("Measure IV and hold")
    #    parameters = self.get_parameters()
    #    print(parameters)
    #    V, I = self.keithley.step_voltage( 0.0, parameters['vmax'], parameters['compliance']*1e-6, parameters['vstep'] )
    #    self.get_IV_curve(V, I)
    #    print("Stepping down to Vhold")
    #    self.keithley.step_to_hold( parameters['vmax'], parameters['vhold'], parameters['compliance']*1e-6, parameters['vstep'] )
    #    print(f"Holding at {parameters['vhold']}, manually reset when finished")
        
    
