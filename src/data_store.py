class DataStore():    
    def __init__(self):
        print("Init data store")

        self.varIdeal={
            "id_experimento":-1,
            "id_electrodo":-1,
            "carga_catalizador":-1,
            "d_corriente":-1,
            "intensidad":-1,
            "caudal_co2":-1,
            "concentracion_co2":-1,
            "humedad_co2":-1,
            "caudal_anolito":-1,
            "caudal_catolito":-1,
            "concentracion_anolito":-1,
            "concentracion_catolito":-1,
            "caudal_central":-1,
            

            #Variables de salida (valores medios de ejecuaciones previas):
            
            "concentracion_hcoo":-1,
            "caudal_hcoo":-1,
            "potencial_celda":-1,
            "produccion_hcoo_gmin":-1,
            "produccion_hcoo_molmin":-1,
            "FE":-1,
            "consumo_energetico":-1,
            "potencia":-1,

            #Otras variables de proceso:
            'caudal_co2_out':-1,
            'concentracion_co2_out':-1,
            'presion_in':-1,
            'presion_out':-1,
            'temperatura_in':-1,
            'temperatura_out':-1,
            'concentracion_h2_in':-1,
            'concentracion_h2_out':-1,
            'pH':-1,

        }

        self.varElectrodo={
            "area":-1,
           
        }
        
        self.varReal={
            "datetime": -1,
            #"id_experimento":-1,
            "carga_catalizador":-1,
            "d_corriente":-1,
            "intensidad":-1,
            "caudal_co2":-1,
            "concentracion_co2":-1,
            "humedad_co2":-1,
            "caudal_anolito":-1,
            "caudal_catolito":-1,
            "concentracion_anolito":-1,
            "concentracion_catolito":-1,
            "caudal_central":-1,

            #Variables de salida:
            
            "concentracion_hcoo":-1,
            "caudal_hcoo":-1,
            "potencial_celda":-1,
            "produccion_hcoo_gmin":-1,
            "produccion_hcoo_molmin":-1,
            "FE":-1,
            "consumo_energetico":-1,
            "potencia":-1,

            #Otras variables de proceso:
            'caudal_co2_out':-1,
            'concentracion_co2_out':-1,
            'presion_in':-1,
            'presion_out':-1,
            'temperatura_in':-1,
            'temperatura_out':-1,
            'concentracion_h2_in':-1,
            'concentracion_h2_out':-1,
            'pH':-1,
        }

        self.varEst={
            "datetime": -1,
            "id_experimento":-1,
            "carga_catalizador":-1,
            "d_corriente":-1,
            "intensidad":-1,
            "caudal_co2":-1,
            "concentracion_co2":-1,
            "humedad_co2":-1,
            "caudal_anolito":-1,
            "caudal_catolito":-1,
            "concentracion_anolito":-1,
            "concentracion_catolito":-1,
            "caudal_central":-1,

            #Variables de_salida:
            
            "concentracion hcoo":-1,
            "caudal_hcoo":-1,
            "potencial_celda":-1,
            "produccion_hcoo_gmin":-1,
            "produccion_hcoo_molmin":-1,
            "FE":-1,
            "consumo_energetico":-1,
            "potencia":-1,

            #Otras variables de proceso:
            'caudal_co2_out':-1,
            'concentracion_co2_out':-1,
            'presion_in':-1,
            'presion_out':-1,
            'temperatura_in':-1,
            'temperatura_out':-1,
            'concentracion_h2_in':-1,
            'concentracion_h2_out':-1,
            'pH':-1,
        }
    
    def resetReal(self):
        print("Reset data")
        for x in self.varReal:
            self.varReal[x]=-1

    def resetEst(self):
        print("Reset data")
        for x in self.var:
            self.var[x]=-1
    
    def getKeysIdeal(self):
        return(self.varReal.keys())
    
    def getKeysReal(self):
        return(self.varReal.keys())

    def getKeysEst(self):
        return(self.varEst.keys())

    def readEst(self,var):
        return(self.varEst[var])
    
    def writeEst(self, var, value):
        if var in self.varEst:
            self.varEst[var]=value
        else:
            print("Variable does not exist: ", var)
    
    def readReal(self,var):
        return(self.varReal[var])
    
    def writeReal(self, var, value):
        if var in self.varReal:
            self.varReal[var]=value
        else:
            print("Variable does not exist: ", var)

    def readIdeal(self,var):
        return(self.varIdeal[var])
    
    def writeIdeal(self, var, value):
        if var in self.varIdeal:
            self.varIdeal[var]=value
        else:
            print("Variable does not exist: ", var)

    def writeElec(self, var, value):
        if var in self.varElectrodo:
            self.varElectrodo[var]=value
        else:
            print("Variable does not exist: ", var)
    
    def readElec(self,var):
        return(self.varElectrodo[var])
            
    def printEst(self):
        print(self.var)

    def printReal(self):
        print(self.varReal)