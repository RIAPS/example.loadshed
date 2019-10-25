'''
    Example controller that uses GridlabD device
'''

from riaps.run.comp import Component
import os
import time
import random

class Controller(Component):
    def __init__(self, sensor,actuator):
        super(Controller, self).__init__()
        self.logger.info("Controller.__init__ ()")
        self.sObj,self.sAttr,self.sUnit = sensor.split('.')
        self.aObj,self.aAttr,self.aUnit = actuator.split('.')
        self.control_counter = 0
        self.control_period = random.randint(20,30)
        self.control_duty = random.randint(10,20)
        self.pending = 0 
        self.first = True
        self.lastValue = None
    
    def handleActivate(self):
        self.logger.info("handleActivate()")
        self.trigger.setDelay(5.0)
        self.trigger.launch()
        
    def on_trigger(self):
        self.logger.info("on_trigger()")
        _discard = self.trigger.recv_pyobj()
        self.trigger.halt()
        if self.pending == 0: 
            msg = ['sub', (self.sObj,self.sAttr,self.sUnit)]
            self.command.send_pyobj(msg)
            self.logger.info("on_trigger: msg=%s" % str(msg))
            self.pending += 1
    
    def on_command(self):
        _msg = self.command.recv_pyobj()
        self.logger.info("on_command(): resp = %s" % str(_msg))
        self.pending -= 1 
    
    def control(self):  
        value = '1' if self.control_counter < self.control_duty else '0'
        self.control_counter = (self.control_counter + 1) % self.control_period
        return value
        
    def on_data(self):
        msg = self.data.recv_pyobj()
        self.logger.info("on_data(): recv=%s" % str(msg))
        value = self.control()
        if value != self.lastValue:
            while self.pending > 0: self.on_command()
            cmd = ['pub', (self.aObj,self.aAttr,value,self.aUnit)]
            self.command.send_pyobj(cmd)
            self.pending += 1
            self.lastValue = value
        
    def __destroy__(self):
        self.logger.info("Controller.__destroy__()")

                         
                    
                         