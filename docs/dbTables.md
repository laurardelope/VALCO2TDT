# VALCO2T Digital Twin



## Data Base Tables

VALCO2T DT requires of access to a MySQL data base with the following tables structure:

### experimentosDT

Each row represent a configuration of an experiment to be run by the DT. The required table structure is the following:
* id (int): DT experiment identifier
* id_experimento (int): Base experiment identifier. Base experiments are defined in "experimentos" table
* intensidad (float): Current intensity [A]
* caudal_co2 (float): CO2 flow  input [mL/min]
* concentracion_co2(float): CO2 concentration input [%]

### experimentos

Each row represent a preconfigured experiment to be use as a baseline for future experiments configurations. The required table structure is the following:
* id (int):  Base experiment identifier
* id_electrodo (int): Electrode identifier. Electrodes are defined in "electrodos" table
* caudal anolito (float): Anolite flow [mL/min]
* caudal_catolito (float): Catolite flow [mL/min]

### electrodos

Each row represent a diferent electrode to be used by the experiment. The required table structure is the following:
* id (int):  Electrode identifier
* area (int): Electrode size [cm2]


### ejecucionesDT

Each row represents a discrete state of the experiment, containing the output variables estimated by the DT at a specific timestamp. The required table structure is the following:

* datetime (datetime): Timestamp of the estimation, in "yyyy-MM-dd hh:mm:ss" format.
* id_experimento (int): DT experiment identifier with the configuration parameters
* intensidad_corriente (float): Current intensity [A]
* densidad_corriente (float): Current density [A/cm2]
* caudal_co2(float): CO2 flow  input [mL/min]
* concentracion_co2(float): CO2 concentration input [%]
* caudal_anolito (float): Anolite flow [mL/min]
* caudal_catolito(float): Catolite flow [mL/min]
* concentracion_hcoo (float): HCOOH concentration output [%]
* caudal_hcoo (float): HCOOH flow output [%]
* potencial_celda (float): Voltage [V]
* produccion_hcoo_gmin (float): HCOOH production [g/min]
* produccion_hcoo_molmin (float): HCOOH production [mol/min]
* FE (float): faraday Efficiency
* consumo_energetico (float): Energy consumption [kWh/kmol]
* potencia (float): Power [W]
* concentracion_co2_out (float): CO2 concentration output [%]
* pH (float): pH




