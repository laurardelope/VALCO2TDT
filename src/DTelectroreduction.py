from src.base_module import *
import numpy as np
import tensorflow as tf
from tensorflow import keras
layers = tf.keras.layers
import tensorflow_datasets as tfds
import tensorflow_probability as tfp
import pandas as pd
import mysql.connector


class DTelectroreduction(Module):

    def __init__(self,param):
        print ("init DT electroreduction...")
        #self.exp_id=param["experiment_id"]
        # Parametros del proceso
        self.Mw_hcoo=param["Mw_hcoo"]
        self.z_hcoo=param["z_hcoo"]
        
        self.Mw_h2=param["Mw_h2"]
        self.z_h2=param["z_h2"]
        
        
        self.F=param["F"]
        self.R=param["R"]
       
        self.area=param["area"]
        
        print ("init DT electroreduction OK")
        
        self.model_pH=tf.keras.models.load_model(param["model_pH"])
        self.model_CH2=tf.keras.models.load_model(param["model_CH2"])
        self.model_V=tf.keras.models.load_model(param["model_V"])
        self.model_CCO2=tf.keras.models.load_model(param["model_CCO2"])
        
        #Connectar con la base de datos
       
     

    def run(self,ds):

        self.runBNN(ds)


       
    
    def runBNN(self, ds):
        try:
               
            # Variables de entrada
            A=self.area
                        
            I= ds.readIdeal("intensidad") # Intensidad de corriente (A)
            Q_co2=ds.readIdeal("caudal_co2") # Caudal de entrada de CO2 (mL/min)
            C_co2=ds.readIdeal("concentracion_co2") # Concentración de entrada de CO2  entrada(%)
            C_h2_in=ds.readIdeal("concentracion_h2_in") # Concentración de entrada de H2 (%)  

            Q_an=ds.readIdeal("caudal_anolito") # Caudal de entrada de anolito (mL/min)
            Q_cat=ds.readIdeal("caudal_catolito") # Caudal de entrada de catolito (mL/min)
            C_an=ds.readIdeal("concentracion_anolito") # Concentración de entrada de anolito (%)
            C_cat=ds.readIdeal("concentracion_catolito") # Concentración de entrada de catolito (%)
            
            # Validate critical input parameters
            critical_params = {
                'intensidad': I,
                'caudal_anolito': Q_an,
                'caudal_catolito': Q_cat,
                'concentracion_anolito': C_an,
                'concentracion_catolito': C_cat
            }
            
            for param_name, param_value in critical_params.items():
                if param_value is None or (isinstance(param_value, (int, float)) and param_value <= 0):
                    print(f"Warning: Invalid value for {param_name}: {param_value}")
            

            ###Variables de salida estimadas por el BNN
            
            E_cell=self.BNN(ds, "potencial_celda") # Potencial de celda (V)
            C_h2=self.BNN(ds, "concentracion_h2_out") # Concentración de salida de H2 (%)  
            C_co2_out=self.BNN(ds,"concentracion_co2_out") # Concentración de salida de Co2 (%)  
            pH=self.BNN(ds,"pH") # pH anolito
            
            print("E_cell:",E_cell)
            print("C_h2:",C_h2)
            print("C_co2_out:",C_co2_out)
            print("pH:",pH)

            #Otras variables calculadas:
            
            Q_h2=ds.readIdeal("caudal_catolito") # Caudal de salida de H2 (mL/min)           =caudal del catolito 
            Q_hcoo=ds.readIdeal("caudal_catolito") # Caudal de salida de HCOO (mL/min)          =caudal del catolito
            
            P_out=1*1.01325 # Presión de salida (bar)
            TK_out=25+273.15 # Temperatura de salida (K)
            
            #E1:    Densidad de corriente (A/cm2)
            j=I*1000/A if A > 0 else 0
            
            # E2: Producción H2 (g/min)
            C_h2_gl= C_h2/100*self.Mw_h2*P_out/(self.R*TK_out) # Concentración de salida de H2 (g/L)
            m_h2=C_h2_gl*Q_h2/1000 if Q_h2 > 0 else 0
            print("m_h2: ",m_h2)
        
            # E4: Eficiencia de Faraday de la reacción de H2 (%)
            n_h2=m_h2/self.Mw_h2 if self.Mw_h2 > 0 else 0
            print("n_h2: ",n_h2)
            FE_H2=(self.z_h2*self.F*(n_h2/60)*100)/I if I > 0 else 0
            print("FE_H2: ",FE_H2)
            FE_hcoo=100-FE_H2
            
            n_hcoo=(FE_hcoo*I)/(self.z_hcoo*self.F)*(60/100) if self.z_hcoo > 0 and self.F > 0 else 0 # mol/min
            m_hcoo=n_hcoo*self.Mw_hcoo if self.Mw_hcoo > 0 else 0 # g/min
            C_hcoo=(m_hcoo*1000)/Q_hcoo if Q_hcoo > 0 else 0 # g/L

        
            # E5: Potencia de celda (w)
            P=E_cell*I

            #E6: Consumo energético (kW/kmol de HCOO producido)
            CE=P/(n_hcoo*60) if n_hcoo > 0 else 0

            #### Write in the database
            
            ds.writeReal('intensidad',I)
            ds.writeReal('caudal_co2',Q_co2)
            ds.writeReal('concentracion_co2',C_co2)
            ds.writeReal('concentracion_h2_in',C_h2_in)
            ds.writeReal('concentracion_h2_out',C_h2)
            ds.writeReal('concentracion_co2_out',C_co2_out)
            ds.writeReal('potencial_celda',E_cell)
            ds.writeReal('caudal_anolito',Q_an)
            ds.writeReal('caudal_catolito',Q_cat)
            ds.writeReal('concentracion_anolito',C_an)
            ds.writeReal('concentracion_catolito',C_cat)
          
            ds.writeReal('d_corriente',j)
            ds.writeReal('concentracion_hcoo',C_hcoo)
            ds.writeReal('caudal_hcoo',Q_hcoo)
            ds.writeReal('produccion_hcoo_gmin',m_hcoo)
            ds.writeReal('produccion_hcoo_molmin',n_hcoo)
            ds.writeReal('FE',FE_hcoo)
            ds.writeReal('consumo_energetico',CE)
            ds.writeReal('potencia',P)
            
            ds.writeReal('pH',pH)
            
        except Exception as e:
            print(f"Error in runBNN method: {e}")
            # Write default/safe values in case of error
            try:
                ds.writeReal('intensidad',0)
                ds.writeReal('caudal_co2',0)
                ds.writeReal('concentracion_co2',0)
                ds.writeReal('concentracion_h2_in',0)
                ds.writeReal('concentracion_h2_out',0)
                ds.writeReal('concentracion_co2_out',0)
                ds.writeReal('potencial_celda',0)
                ds.writeReal('caudal_anolito',0)
                ds.writeReal('caudal_catolito',0)
                ds.writeReal('concentracion_anolito',0)
                ds.writeReal('concentracion_catolito',0)
            
            
                ds.writeReal('d_corriente', 0)
                ds.writeReal('concentracion_hcoo', 0)
                ds.writeReal('caudal_hcoo', 0)
                ds.writeReal('produccion_hcoo_gmin', 0)
                ds.writeReal('produccion_hcoo_molmin', 0)
                ds.writeReal('FE', 0)
                ds.writeReal('consumo_energetico', 0)
                ds.writeReal('potencia', 0)
                ds.writeReal('pH', 7)
            except Exception as write_error:
                print(f"Error writing default values: {write_error}")


    

    def writeOutputFile(self,ds):
        # Write the output to a file

        with open(self.outputfileDT, "a") as f:
            f.write(f"{ds.readReal('datetime')}, {ds.readIdeal('id_experimento')}, {ds.readReal('intensidad')}, {ds.readReal('d_corriente')}, "
                f"{ds.readReal('potencial_celda')}, {ds.readReal('caudal_anolito')},{ds.readReal('caudal_catolito')},{ds.readReal('caudal_central')}, "
                f"{ds.readReal('humedad_co2')}, {ds.readReal('caudal_co2')},{ds.readReal('concentracion_co2')},{ds.readReal('caudal_central')}, "
                f"{ds.readReal('caudal_co2_out')}, {ds.readReal('concentracion_co2_out')},{ds.readReal('presion_in')},{ds.readReal('presion_out')}, "
                f"{ds.readReal('temperatura_in')}, {ds.readReal('temperatura_out')},{ds.readReal('concentracion_h2o_in')},"
                f"{ds.readReal('concentracion_h2o_out'),ds.readReal('pH')}, "
                f"{ds.readReal('concentracion_hcoo')}, {ds.readReal('caudal_hcoo')}, "
                f"{ds.readReal('produccion_hcoo_gmin')}, {ds.readReal('produccion_hcoo_molmin')}, "
                f"{ds.readReal('FE')}, {ds.readReal('potencia')}, {ds.readReal('consumo_energetico')}\n")
            
         
    
    def BNN(self, dataStore, feature_name):
        # Define feature columns
        df=pd.DataFrame()
        
        batch_size = 256
        
        if (feature_name=="potencial_celda"):
            
            for i in range(0, batch_size * 10):
                df_row = {
                    "I": dataStore.readIdeal("intensidad"), 
                    "V": 10, 
                    "Q_an": dataStore.readIdeal("caudal_anolito"),
                    "Q_cat": dataStore.readIdeal("caudal_catolito"),
                    "C_an": dataStore.readIdeal("concentracion_anolito"),
                    "C_cat": dataStore.readIdeal("concentracion_catolito")
                }
                
                # Validate that all values are not None/NaN
                if all(val is not None for val in df_row.values()):
                    df = pd.concat([df, pd.DataFrame([df_row])], ignore_index=True)
                else:
                    print(f"Warning: Skipping row {i} due to missing data")
                    
            # Check if DataFrame has any valid data
            if df.empty:
                print("Error: No valid data available to create dataset")
                return 0
                
            df_y = df['V']
            
            try:
                loaded_model = self.model_V
               
                print("Model V loaded successfully")
            except FileNotFoundError:
                print("Error: Model file 'models/DNN_V_model.keras' not found")
                return 0
            except Exception as e:
                print(f"Error loading model: {e}")
                return 0
            
            
            
        elif(feature_name=="concentracion_h2_out"):
                for i in range(0, batch_size * 10):
                    df_row = {
                        "C_H2_out": 0,
                        "C_CO2_in": dataStore.readIdeal("concentracion_co2"),
                        "I": dataStore.readIdeal("intensidad"),  # Intensidad de corriente (A)
                        "Q_co2_in": dataStore.readIdeal("caudal_co2"),
                        "Q_cat": dataStore.readIdeal("caudal_catolito"),
                        "C_cat": dataStore.readIdeal("concentracion_catolito")
                    }
                    
                    # Validate that all values are not None/NaN
                    if all(val is not None for val in df_row.values()):
                        df = pd.concat([df, pd.DataFrame([df_row])], ignore_index=True)
                    else:
                        print(f"Warning: Skipping row {i} due to missing data")
                        
                # Check if DataFrame has any valid data
                if df.empty:
                    print("Error: No valid data available to create dataset")
                    return 0
                    
                df_y = df['C_H2_out']
                try:
                    loaded_model = self.model_CH2
                    print("Model CH2 loaded successfully")
                except FileNotFoundError:
                    print("Error: Model file 'models/DNN_CH2_model.keras' not found")
                    return 0
                except Exception as e:
                    print(f"Error loading model: {e}")
                    return 0

        elif(feature_name=="concentracion_co2_out"):
            
            for i in range(0, batch_size * 10):
                df_row = {
                    "C_CO2_out": 0,
                    "C_CO2_in": dataStore.readIdeal("concentracion_co2"),
                    "I": dataStore.readIdeal("intensidad"),  
                    "Q_co2_in": dataStore.readIdeal("caudal_co2"),
                    "Q_cat": dataStore.readIdeal("caudal_catolito"),
                    "C_cat": dataStore.readIdeal("concentracion_catolito")
                }
                
                # Validate that all values are not None/NaN
                if all(val is not None for val in df_row.values()):
                    df = pd.concat([df, pd.DataFrame([df_row])], ignore_index=True)
                else:
                    print(f"Warning: Skipping row {i} due to missing data")
                    
            # Check if DataFrame has any valid data
            if df.empty:
                print("Error: No valid data available to create dataset")
                return 0
            df_y = df['C_CO2_out']
            
            try:
                loaded_model = self.model_CCO2
                print("Model CCO2 loaded successfully")
            except FileNotFoundError:
                print("Error: Model file 'models/DNN_CCO2_model.keras' not found")
                return 0
            except Exception as e:
                print(f"Error loading model: {e}")
                return 0

        
        elif(feature_name=="pH"):
            
            for i in range(0, batch_size * 10):
                df_row = {
                    "pH": 7,
                    "I": dataStore.readIdeal("intensidad"),  
                    "Q_an": dataStore.readIdeal("caudal_anolito"),
                    "C_an": dataStore.readIdeal("concentracion_anolito")
                }
                
                # Validate that all values are not None/NaN
                if all(val is not None for val in df_row.values()):
                    df = pd.concat([df, pd.DataFrame([df_row])], ignore_index=True)
                else:
                    print(f"Warning: Skipping row {i} due to missing data")
                    
            # Check if DataFrame has any valid data
            if df.empty:
                print("Error: No valid data available to create dataset")
                return 0
            df_y = df['pH']
            
            try:
                loaded_model = self.model_pH
                print("Model pH loaded successfully")
            except FileNotFoundError:
                print("Error: Model file 'models/DNN_pH_model.keras' not found")
                return 0
            except Exception as e:
                print(f"Error loading model: {e}")
                return 0

        else:
                # Handle other feature types or unsupported features
                print(f"Warning: Feature '{feature_name}' is not currently supported. Returning default value.")
                return 0
        
        try:
            test_dataset = (tf.data.Dataset.from_tensor_slices((dict(df), df_y))).batch(batch_size)
            dataset_length = len(list(test_dataset.as_numpy_iterator()))
                        
            if dataset_length == 0:
                print("Error: Dataset is empty after processing")
                return 0
                
        except Exception as e:
            print(f"Error creating TensorFlow dataset: {e}")
            return 0       




        sample = 1
        
        # Convert test_dataset to list and check if it's empty
        dataset_list = list(test_dataset.unbatch().shuffle(batch_size*10).batch(sample))
        if not dataset_list:
            print("Error: Dataset is empty. Cannot make predictions.")
            return 0  # Return default value if no data available
            
        try:
            examples, targets = dataset_list[0]
        except IndexError:
            print("Error: IndexError - Dataset does not contain any batches.")
            return 0  # Return default value if index error occurs

        try:
            predicted = loaded_model(examples).numpy()
            if(predicted<0).any():
               predicted = np.abs(predicted)
            for idx in range(sample):
                print(f"Predicted: {round(float(predicted[idx][0]), 3)} - Actual: {targets[idx]}")
            
            # Return the first prediction value instead of 0
            if len(predicted) > 0 and len(predicted[0]) > 0:
                return float(predicted[0][0])
            else:
                return 0  # Fallback return value
                
        except Exception as e:
            print(f"Error during prediction: {e}")
            return 0  # Return default value if prediction fails
          
            

 