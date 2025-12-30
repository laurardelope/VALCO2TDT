from src.db_connect import *
from src.DTelectroreduction import *
from src.data_store import *
import time
from datetime import timedelta
import json

class Master:
    def __init__(self):
        
        jsonfile=open('./config/config.json')
        json_str=jsonfile.read()
        self.param=json.loads(json_str)
        
        

        # self.param={
            
        #     # Data Base Connection Parameters #
        #     "db_host":"localhost",
        #     "db_user":"administrator",
        #     "db_password":"telematica@VALCO2T",
        #     "db_name":"valco2t",
          
        #     "outputfileDT":"data/Output/outputDT.txt", # Fichero de salida

        #     "n_iter":60,
        #     "t_check": 2, #Tiempo entre chequeos de actualizacaiones de la base de datos (s)
        #     "t_samples_PLC":10, # Segs. # PLC: Tiempo entre muestras
        #     "t_samples_DT":1, # Segs. # Tiempo entre estimaciones del DT

        #     # Parametros del proceso
        #     "Mw_hcoo":45, # (g/mol) Masa molar del HCOO
        #     "F":96485.33, # (C/mol) constante de Faraday
        #     "z_hcoo":2, # (mol) cantidad de electrones intercambiados en la reacción de producción de ácido fórmico/formiato
            
        #     "Mw_h2":2, # (g/mol) Masa molar del H2
        #     "z_h2":2, # (mol) cantidad de electrones intercambiados
            
        #     "R":0.08314, # (bar·L)/(K·mol) constante de los gases ideales
            
        #     "area":100,
            
        #     # NN model parameters #
        #     "model_pH":"models/DNN_pH_model.keras",
        #     "model_CH2":"models/DNN_CH2_model.keras",
        #     "model_V":"models/DNN_V_model.keras",
        #     "model_CCO2":"models/DNN_CCO2_model.keras"

        # }

        self.dataStore=DataStore()
        self.db_conn=DB_Connection(self.param)
        self.DTelectroreduction=DTelectroreduction(self.param)

    def run(self):
        
        n_exp_ini=self.db_conn.read_nexp(self.dataStore,self.param)
        print("Initial experiment number:",n_exp_ini)
        
        while True:
            n_exp=self.db_conn.read_nexp(self.dataStore,self.param)
            if(n_exp>n_exp_ini):
                n_exp_ini=n_exp
                self.db_conn.read_exp(self.dataStore,self.param)
                self.param["area"]=self.dataStore.readElec('area')
                self.db_conn.read_expDT(self.dataStore,self.param)
                print("New experiment detected:",n_exp)
                self.dataStore.writeIdeal('id_experimento',n_exp)
                
                self.ct=datetime.datetime.now()

                i=0
                while(i<self.param["n_iter"]):
                    
                    print(i)
                    self.dataStore.writeReal('datetime',self.ct)
                    
                    self.DTelectroreduction.run(self.dataStore)
                    self.db_conn.write_ejecucion_DT(self.dataStore,self.param)
                    
                    new_ct = self.ct+ datetime.timedelta(seconds=self.param["t_samples_PLC"])
                    self.ct=new_ct
                    i+=1
                    time.sleep(self.param["t_samples_DT"])  # Espera el tiempo de muestreo del PLC
                
            time.sleep(self.param["t_check"])  # Espera el tiempo de muestreo de la base de datos
               
                
                    
       
            
        
        