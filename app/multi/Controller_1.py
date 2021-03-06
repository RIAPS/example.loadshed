'''
    Example controller that uses GridlabD device
'''

from riaps.run.comp import Component
import os
import time
import random

class Controller(Component):
    def __init__(self, sensor,actuator,priority):
        super(Controller, self).__init__()
        self.logger.info("Controller.__init__ ()")
        self.sObj,self.sAttr,self.sUnit = sensor.split('.')
        self.aObj,self.aAttr,self.aUnit = actuator.split('.')
        self.control_counter = 0
        self.control_period = 20    # random.randint(20,30)
        self.control_duty = 10      # random.randint(10,20)
        self.pending = 0 
        self.first = True
        self.lastValue = None
        self.global_status = {}
        self.status = '1'
        self.priority = priority
        self.threshold = 4e06
        self.retrycount = 0
    
    def handleActivate(self):
        self.logger.info("handleActivate()")
        self.trigger.setDelay(5.0)
        self.trigger.launch()
        
    def on_trigger(self):
        self.logger.info("on_trigger()")
        _discard = self.trigger.recv_pyobj()
        self.trigger.halt()
        self.updatestatus.send_pyobj({self.priority : self.status})
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
    
    def controlswitch(self, power):  
        if power > self.threshold:
            self.logger.info("Power consumption threshold exceeded !!!!")
            wait = False
            for key,value in self.global_status.items():
                if key > self.priority and value == '1':
                    self.logger.info("Waiting for lower priority switch")
                    wait = True
                    break
            if wait:
                val = '1'

            else:
                if self.retrycount == 3:
                    val = '0'
                    self.status = val
                    self.retrycount = 0
                else:
                    self.retrycount += 1
                    val = self.status
                    self.logger.info("waiting for actuation to take effect")
        else:
            val = self.status
        
    def on_data(self):
        msg = self.data.recv_pyobj()
        self.logger.info("on_data(): recv=%s" % str(msg))
        self.updatestatus.send_pyobj({self.priority : self.status})
#         value = self.control()
#         if value != self.lastValue:
#             while self.pending > 0: self.on_command()
#             cmd = ['pub', (self.aObj,self.aAttr,value,self.aUnit)]
#             self.command.send_pyobj(cmd)
#             self.pending += 1
#             self.lastValue = value
        power = complex(msg[3])
        if power.real > self.threshold:
            value =self.controlswitch(power.real)
            cmd = ['pub', (self.aObj,self.aAttr,value,self.aUnit)]  
            self.logger.info("%s" % str(cmd))
            self.command.send_pyobj(cmd)
        else:
            self.logger.info("status : ok")
            
    def on_receivestatus(self):
        msg = self.receivestatus.recv_pyobj()
        priority = list(msg.keys())
        priority = int(priority[0])
        if priority == self.priority:
            return
        else:
            self.global_status[priority] = msg[priority]
            self.logger.info("received information on other switches")
        
    def __destroy__(self):
        self.logger.info("Controller.__destroy__()")

                         
                    
                         