Loadshed application 
====================

The loadshed application demonstrates how loadshedding can be implemented in RIAPS. The application 
uses the GridlabD interface to connect to a simulated power network,
receive simulated measurement data from it, and to control various switched loads in the simulation. 

There are 3 variants of the loadshed example application:
- app/simple: Simple control of one load switch, based on a fixed duty cycle.
- app/multi:  Multi-level control of 1+ load switches, based on thresholds.
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

The folders:
- /app: app variants
- /models: power system models
- /mn: mininet scripts to launch the simulation and RIAPS tools to run the app. 

To start a mininet-based run:
- $ source setup-mn
- Start mininet (with an optional argument indicating the number of virtual hosts to be create) under RIAPS.
- At the mininet prompt:
  mininet> source PATH/mn/SCRIPT
  where PATH is the full pathname of the root folder and SCRIPT is the name of the .mn script 
  
