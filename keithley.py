from pymeasure.instruments.keithley import Keithley2400
from pymeasure import * 
import numpy as np
from scipy.optimize import curve_fit

from time import sleep

class Keithley:
    """Class to control the Keithley 2410"""

    def __init__(self, port='ASRL/dev/ttyUSB0::INSTR', emulate=False, vmax=10, accuracy=1):
        self.port = port
        self.vmax = vmax
        self.emulate = emulate
        self.accuracy = accuracy
        self.mode = None
        self.keithley = Keithley2400(port)
        if not self.emulate:
            self.keithley.write("*RST")
            print(self.keithley.ask("*IDN?"))

        else:
            print("Emulation mode")
        
        print("Keithley Initialized")
    
    def step_voltage( self, starting_voltage=1., target_voltage=2., compliance=1e-9, stepsize=1.):
    	self.keithley.apply_voltage(voltage_range=target_voltage, compliance_current=compliance)
        self.keithley.source_voltage = 0.
        self.on()
        current_set = [] #store current at each voltage step
        numstep = int((target_voltage - starting_voltage) / stepsize) + 1
		voltage_steps = np.linspace(starting_voltage, target_voltage, num=num)
        
        print("Keithley Ramping - Starting: {voltage_steps[0]}   Target: {voltage_steps[-1]} [V]   V_step: {stepsize}    Compl.:{compliance_current}")
        for v in voltage_steps:
            self.keithley.source_voltage = v
            sleep(1)
            current = self.keithley.current
            current_set.append(current)
            print(f"Voltage: {v} V, Current: {current} A")
            #check for compliance abort if exceeded
            if current >= compliance :
            	print("-- Compliance hit, aborting voltage step! --" )
            	break
        
        #always measure current and return the set of V,I
        print("Ramping Complete")
        return voltage_steps, current_set    
    
    def reset_voltage( self ):
    	self.keithley.source_voltage = 0.
        self.off
    
    def RunKeithleyAndWait(self, rampVoltage=1, compliance=1e-9, steps=10):
        self.keithley.apply_voltage(voltage_range=rampVoltage, compliance_current=compliance)
        self.keithley.source_voltage = 0.
        self.on()
        steps = np.linspace(0,rampVoltage,steps)
        for v in steps:
            self.keithley.source_voltage = v
            sleep(2)
        while True:
            choice = input("Enter 'reset' to return to 0V/exit, or a number for for a new voltage: ").strip().lower()
            if choice == 'reset':
                self.keithley.source_voltage = 0.
                self.off
                break
            else:
                try:
                    new_v = float(choice)
                    self.keithley.source_voltage = new_v
                    print(f"Voltage set to {new_v}V")
                except ValueError:
                    print("enter valid input")
        
    def measureCurrentSet( self, VSet, voltage_range=1e-3, compliance_current=1.5e-3 ):#only measure in a single voltage/compliance range per call
        #voltage range and compliance rule of thumb (compliance should be 5% up to avoid clamping)
        #100mV to 1k Resitor -> I= 0.1mA  [200mV voltage range] & compliance current =1.05mA
        #1V to 1k Resistor ->  I= 1mA      [2V voltage range]   & compliance current =1.05
        #10V to 1k Resistor -> I= 10mA      [20V voltage range] & compliance current =10.5mA
        #it is possible to set up auto ranging with the keithley
        self.keithley.apply_voltage(voltage_range=voltage_range, compliance_current=compliance_current)
        self.keithley.source_voltage = 0. 
        self.on()
        ISet = []
        self.keithley.measure_current()
        for v in VSet:
            self.keithley.source_voltage = v
            sleep(2)
            current = self.keithley.current
            ISet.append(current)
            print(f"Voltage: {v} V, Current: {current} A")
        self.keithley.source_voltage = 0.
        self.off()
        return np.array(ISet)
    
     
    

    def reset(self): 
        return self.keithley.write("*RST")

    def on(self):
        self.keithley.enable_source()

    def off(self):
        self.keithley.disable_source()

