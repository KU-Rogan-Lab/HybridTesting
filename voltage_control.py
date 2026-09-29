import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# ============================================================
# Voltage Control
# ============================================================

class VoltageControlFrame(ttk.LabelFrame):

    def __init__(self, parent, keithley, metadataFrame):
        super().__init__(
            parent,
            text="Voltage Control",
            padding=10
        )
        self.keithley = keithley
        self.metadataFrame = metadataFrame
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):

        self.vmax_var = tk.StringVar(value="240")
        self.vstep_var = tk.StringVar(value="5")
        self.compliance_var = tk.StringVar(value="1.0")
        self.vhold_var = tk.StringVar(value="220")

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

        ttk.Label(
            parameters,
            text="Vstep (V)"
        ).grid(
            row=0,
            column=4,
            padx=5
        )

        self.vstep_entry = ttk.Entry(
            parameters,
            textvariable=self.vstep_var,
            width=12
        )

        self.vstep_entry.grid(
            row=0,
            column=5,
            padx=5
        )

        ttk.Label(
            parameters,
            text="Max Compliance [uA]"
        ).grid(
            row=0,
            column=6,
            padx=5
        )

        self.compliance_entry = ttk.Entry(
            parameters,
            textvariable=self.compliance_var,
            width=12
        )

        self.compliance_entry.grid(
            row=0,
            column=7,
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
            "compliance": float(self.compliance_var.get()),
            "vhold": float(self.vhold_var.get())
        }

    def measure_iv_reset(self):
        print("Measure IV and reset")
        parameters = self.get_parameters()
        print(parameters)
        V, I = self.keithley.step_voltage( 0.0, parameters.vmax, parameters.compliance*1e-6, parameters.vstep )
        self.get_IV_curve(V, I)
        self.keithley.reset_voltage()

    def measure_iv_hold(self):
        print("Measure IV and hold")
        parameters = self.get_parameters()
        print(parameters)
        V, I = self.keithley.step_voltage( 0.0, parameters.vmax, parameters.compliance*1e-6, parameters.vstep )
        self.get_IV_curve(V, I)
        print("Stepping down to Vhold")
        self.keithley.set_voltage( parameters.vmax, parameters.vhold, parameters.compliance*1e-6, parameters.vstep )
        print("Holding at {parameters.vhold}, manually reset when finished")
        
    def step_and_hold(self):
        print("Step voltage and hold")
        parameters = self.get_parameters()
        print(parameters)
        V, I = self.keithley.step_voltage( 0.0, parameters.vmax, parameters.compliance*1e-6, parameters.vstep )
        print("Holding at {parameters.vhold}, manually reset when finished")

    def reset_voltage(self):
        print("Reset voltage to 0 V")
        self.keithley.reset_voltage()
        
    def get_IV_curve(self, Vset, ISet):
        #embed hybrid metadata info into the plot
        metadata = self.metadataFrame.get_metadata()
        self.metadata.create_workspace() #make directories if they are not present

        I_uA = ISet*1e6
        #drop first noisy measurement at 0V
        currents = np.array(I_uA[1:])
        voltages = np.array(Vset[1:])
        combined_data = np.column_stack((voltages, currents))
        target_directory = metadata.parent_directory + '/' + metadata.hybrid_name + '/'
        csvname = target_directory + metadata.hybrid_name + '_' + metadata.tag + '.csv'
        np.savetxt(csvname, combined_data, delimiter=",", header="voltage,current", comments="")


        fig, ax = plt.subplots()
        ax.scatter(voltages,currents, label='Current Measurements')
        ax.set_ylabel('Measured Current [$\mu$A]')
        ax.set_xlabel('Applied Voltage [V]')
        ax.set_title('Hybrid Reverse Bias ' + metadata.hybrid_name)
        ax.legend()
        figname = target_directory + metadata.hybrid_name + '_' + metadata.tag + '.png'
        plt.savefig("my_plot.png", dpi=300, bbox_inches="tight")
        plt.show()
        print("IV analysis completed")

