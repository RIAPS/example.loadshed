Loadshed application 
====================

The loadshed application demonstrates how loadshedding algorithm can be implemented in RIAPS. The application 
uses the GridlabD interface to connect to a simulated power network, receive simulated measurement data from it, 
and control various switched loads in the simulation. 

There are 3 variants of the loadshed example application:
- app/simple: Simple control of one load switch, based on a fixed duty cycle. [OBSOLETE]
- app/multi:  Multi-level control of 1+ load switches, based on thresholds. [OBSOLOTE]
- app/robust: Multi-level control of 1+ load switches, based on thresholds and priorities. Also demonstrates how fault-tolerance can be implemented in an app. 

The app parameters in the depl files control what 'sensor' and 'actuator' signal/s is/are the controller/s connected to. 
These signals must be available in the system model that is 'running' under the control of the GridlabD agent.
See the corresponding models and configurations in the /models/<modelname>.yaml files.  

Note that some app variants may not work out of the box, due to configuration and other changes. 

List of working apps and models:

| App in /app/...       |  GL model in models/... | Deployment in /app/...     | Description            | Mininet hosts, script | 
| ----------------------|-------------------------| -----------------------    |------------------------|-----------------------|
| multi/loadshed.riaps  | loadshed32              | multi/loadshed1.depl       | 1 load + 1 host        | N/A                   |
|                       | loadshed32              | multi/loadshed2-mn.depl    | 1 load + 2 mininet     | 4, loadshed2.mn       |
|                       | loadshed32              | multi/loadshed8-mn.depl    | 8 loads + 8 mininet    | 8, loadshed8.mn      | 
| robust/loadshed.riaps | loadshed32              | robust/loadshed4.depl      | 4 loads + 1 host       | N/A                   | 
|                       | loadshed32              | robust/loadshded4-mn.depl  | 4 loads + 4 mininet    | 4, loadshed4.mn       |
|                       | loadshed32              | robust/loadshded8-mn.depl  | 8 loads + 8 mininet    | 8, loadshed8.mn       |
|                       | loadshed32              | robust/loadshed32-bbb.depl | 32 loads + on 32 bbb-s | N/A                   | 

Recommend: use only the app in robust/, with mininet (see below) and 4 or 8 nodes. 
 
The folders:
- /app: app variants
- /models: power system models
- /mn: mininet scripts to launch the simulation and RIAPS tools to run the app. 

Running the app with Mininet
----------------------------

The apps can run on the development VM (that has RIAPS installed) under mininet. 

Note: rpyc_registry, and riaps services (e.g. riaps_deplo) must NOT be running on the VM.
These can be halted as follows:
	systemctl disable riaps-deplo.service
	systemctl stop riaps-deplo.service || true
	systemctl disable riaps-rpyc-registry.service
	systemctl stop riaps-rpyc-registry.service || true

Note: edit the file setup-mn to point to the correct location of the GridlabdD agent.

To start a mininet-based run (in this directory).
   source setup-mn
   riaps-mn N
where N is the number of virtual mininet hosts to be launched.
 At the mininet prompt:
    mininet> source mn/SCRIPT
 where SCRIPT is the name of the .mn script. (e.g. loadshed4.mn).
 Note: mininet does not handle exceptions well, so if the last command fails it may leave the 
 (virtual) network intefaces behind - and a restart of the VM may be necessary.
 Note: the starup on the virtual nodes can take a few seconds.
 
 The simulation logs changes into InfluxDB (as specified in models/*/loadshed.gll), 
 the results can be accessed using the Grafana on localhost:3000.
 
 Running the app with Mininet in a RIAPS development environment
 ----------------------------------------------------------------
 
The app can be run on a VM that is being used to develop RIAPS as follows.
Assume $RIAPS points to the root folder of the RIAPS source tree, and $APP points to this folder.
	cd $RIAPS 
	source setup
	cd $APP
	souce setup-mn.dev
	riaps-mn N
where N is the number of virtual mininet hosts to be launched.


	
	
  
  
  
 
  
