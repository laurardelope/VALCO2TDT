# VALCO2T Digital Twin

## Configuration File 

The digital twin can be configured through the config.json file located in the data folder. The file structure is following described:

### Data base configuration parameters:
* "db_host":MySQL data base host address.
* "db_user": MySQL data base user.
* "db_password":MySQL data base password.
* "db_name":MySQL data base name.

* "outputfileDT":path to the output file with the values of the variables estimated by the digital twin. 
* "n_iter":: number of iterations to be run by the digital twin.
* "t_check":  Time between checkings of the data base [seconds], currently 2 seconds. 
* "t_samples_PLC": Time between samples [seconds], currently 10 seconds.
* "t_samples_DT": Time between samples [seconds], currently 1 seconds. 

### Process configuration parameters:            
* "Mw_hcoo": HCOO molar mass [g/mol] (45)
* "F": Faraday constant [C/mol](96485.33). 
* "z_hcoo": exchanged electrons for HCOO production [mol] (2),        
* "Mw_h2":: H2 molar mass  [g/mol] (2),
* "z_h2":exchanged electrons for H2 production [mol] (2),          
* "R": ideal gas constant [bar*L/(K*mol)] (0.08314),           
  
### Models configuration parameters:             
* "model_pH": path to the Keras neural network model for pH predictions
* "model_CH2": path to the Keras neural network model for H2 output concentration prediction
* "model_V": path to the Keras neural network model for voltage concentration prediction
* "model_CCO2": path to the Keras neural network model for CO2 output concentration prediction









