import tkinter as tk
from tkinter import ttk


# ============================================================
# Voltage Control
# ============================================================

class VoltageControlFrame(ttk.LabelFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            text="Voltage Control",
            padding=10
        )

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):

    	self.vmax_var = tk.StringVar(value="240")
    	self.vstep_var = tk.StringVar(value="5")
    	self.compliance_var = tk.StringVar(value="1.0")

    	self.iv_reset_button = ttk.Button(
        	self,
        	text="Measure IV and Reset",
        	command=self.measure_iv_reset
    	)

    	self.iv_hold_button = ttk.Button(
        	self,
        	text="Measure IV and Hold",
        	command=self.measure_iv_hold
    	)

    	self.step_hold_button = ttk.Button(
        	self,
        	text="Step and Hold",
        	command=self.step_and_hold
    	)

    	self.reset_button = ttk.Button(
        	self,
        	text="Reset 0V",
        	command=self.reset_voltage
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
        	text="Vmax (V)"
    	).grid(
        	row=0,
        	column=0,
        	padx=5
    	)

    	self.vmax_entry = ttk.Entry(
        	parameters,
        	textvariable=self.vmax_var,
        	width=12
    	)

    	self.vmax_entry.grid(
        	row=0,
        	column=1,
        	padx=5
    	)

    	ttk.Label(
        	parameters,
        	text="Vstep (V)"
    	).grid(
        	row=0,
        	column=2,
        	padx=5
    	)

    	self.vstep_entry = ttk.Entry(
        	parameters,
        	textvariable=self.vstep_var,
        	width=12
    	)

    	self.vstep_entry.grid(
        	row=0,
        	column=3,
        	padx=5
    	)

    	ttk.Label(
        	parameters,
        	text="Max Compliance [uA]"
    	).grid(
        	row=0,
        	column=4,
        	padx=5
    	)

    	self.compliance_entry = ttk.Entry(
        	parameters,
        	textvariable=self.compliance_var,
        	width=12
    	)

    	self.compliance_entry.grid(
        	row=0,
        	column=5,
        	padx=5
    	)

    	# --------------------------------------------------------
    	# Control buttons
    	# --------------------------------------------------------

    	self.iv_reset_button.grid(
        	row=1,
        	column=0,
        	padx=5,
        	pady=5,
        	sticky="ew"
    	)

    	self.iv_hold_button.grid(
        	row=1,
        	column=1,
        	padx=5,
        	pady=5,
        	sticky="ew"
    	)

    	self.step_hold_button.grid(
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
            "vmax": float(self.vmax_var.get()),
            "vstep": float(self.vstep_var.get()),
            "compliance": float(self.compliance_var.get())
        }

    def measure_iv_reset(self):
        print("Measure IV and reset")
        print(self.get_parameters())

    def measure_iv_hold(self):
        print("Measure IV and hold")
        print(self.get_parameters())

    def step_and_hold(self):
        print("Step voltage and hold")
        print(self.get_parameters())

    def reset_voltage(self):
        print("Reset voltage to 0 V")

