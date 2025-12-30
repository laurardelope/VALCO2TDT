from src.base_module import *

import mysql.connector


class DB_Connection(Module):

    def __init__(self,param):
         #Connectar con la base de datos
        print ("init db_connection...")

        cnx = mysql.connector.connect(user=param["db_user"], password=param["db_password"],  database=param["db_name"])
        print ("init db_connection OK")
        cnx.close()

        #self.idExp=param["experiment_id"]
    
    def read_exp(self,ds,param):
        
        self.idExp=ds.readIdeal('id_experimento')
               
        try:
            connection = mysql.connector.connect(host=param["db_host"],
                                                database=param["db_name"],
                                                user=param["db_user"],
                                                password=param["db_password"])

            sql_select_Query = "select * from experimentos WHERE id=" + str(self.idExp)
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            

            if(len(records)>1):
                print("Number of experiments with the same id: ", cursor.rowcount)
         
            id_electrodo=records[0][1]
            ds.writeIdeal('id_electrodo', records[0][1])
            ds.writeIdeal('intensidad', records[0][4])
            ds.writeIdeal('caudal_co2', records[0][5])
            ds.writeIdeal('concentracion_co2', records[0][6])
            ds.writeIdeal('caudal_anolito', records[0][8])
            ds.writeIdeal('caudal_catolito', records[0][9])
            ds.writeIdeal('concentracion_h2_in', records[0][11])
            ds.writeIdeal('concentracion_anolito', records[0][12])
            ds.writeIdeal('concentracion_catolito', records[0][13])

            sql_select_Query = "SELECT area FROM electrodos WHERE id=" + str(id_electrodo)
            
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            if(len(records)>1):
                print("Number of electrodes with the same id: ", cursor.rowcount)
            area=records[0][0]

            print(area)
            
            ds.writeElec('area', area)
        
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")


    
    def read_expMean(self,ds,param):
               
        try:
            connection = mysql.connector.connect(host=param["db_host"],
                                                database=param["db_name"],
                                                user=param["db_user"],
                                                password=param["db_password"])

            sql_select_Query = "select * from media_ejecuciones WHERE id_experimento=" + str(self.idExp)
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            # get all records
            records = cursor.fetchall()
            
            if(len(records)>1):
                print("Number of experiments with the same id: ", cursor.rowcount)
            
            ds.writeIdeal('concentracion_hcoo', records[0][2])
            ds.writeIdeal('caudal_hcoo', records[0][3])
            ds.writeIdeal('potencial_celda', records[0][4])
            ds.writeIdeal('produccion_hcoo', records[0][5])
            ds.writeIdeal('FE', records[0][6])
            ds.writeIdeal('consumo_energetico', records[0][7])
            ds.writeIdeal('potencia', records[0][8])
            
        
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
    
    
    def write_ejecucion_DT(self,ds,param):

        print("Writing data in MySQL table")
               
        try:
            connection = mysql.connector.connect(host=param["db_host"],
                                                database=param["db_name"],
                                                user=param["db_user"],
                                                password=param["db_password"])

            sql_Query = "INSERT INTO ejecucionesDT (datetime, datetimeServer, id_experimento, tiempo_medida, intensidad_corriente, densidad_corriente, caudal_co2,"\
                " concentracion_co2, caudal_co2_out, caudal_anolito, caudal_catolito, concentracion_co2_out, concentracion_hcoo, caudal_hcoo, potencial_celda," \
                "produccion_hcoo_gmin, produccion_hcoo_molmin, FE, consumo_energetico, potencia, concentracion_h2o_in, concentracion_h2o_out, pH) VALUES ('" \
           + str(ds.readReal('datetime')) +"', '"+ str(ds.readReal('datetime')) +"', "+  str(ds.readIdeal('id_experimento')) +",0 , "+  str(ds.readReal('intensidad')) +", "  \
           + str(ds.readReal('d_corriente')) +", "+  str(ds.readReal('caudal_co2')) +", "+  str(ds.readReal('concentracion_co2')) +", "\
           + str(ds.readReal('caudal_co2_out'))+", "+  str(ds.readReal('caudal_anolito'))+", "+  str(ds.readReal('caudal_catolito'))+", " \
           + str(ds.readReal('concentracion_co2_out'))+", "+ str(ds.readReal('concentracion_hcoo'))+", "+  str(ds.readReal('caudal_hcoo'))+","\
           + str(ds.readReal('potencial_celda'))+", "+ str(ds.readReal('produccion_hcoo_gmin'))+", "+ str(ds.readReal('produccion_hcoo_molmin'))+", "+ str(ds.readReal('FE'))+","\
           + str(ds.readReal('consumo_energetico'))+", "+ str(ds.readReal('potencia'))+", "+ str(ds.readReal('concentracion_h2_in'))+", "+ str(ds.readReal('concentracion_h2_out'))+", "+ str(ds.readReal('pH'))+");"
            
            cursor = connection.cursor()
            cursor.execute(sql_Query)
            connection.commit()
            cursor.close()
            
        
        except mysql.connector.Error as e:
            print("Error writing data in MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")


    def read_nexp(self, ds,param):
        try:
            connection = mysql.connector.connect(host=param["db_host"],
                                                database=param["db_name"],
                                                user=param["db_user"],
                                                password=param["db_password"])

            sql_select_Query = "select id, id_experimento from experimentosDT ORDER BY id DESC LIMIT 1;"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            # get all records
            records = cursor.fetchall()
            
            print("Number of experiments:", records[0][0])
            
            ds.writeIdeal('id_experimento', records[0][1])
            return(records[0][0])
            
        
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
        
    
    def read_expDT(self, ds,param):
        try:
            connection = mysql.connector.connect(host=param["db_host"],
                                                database=param["db_name"],
                                                user=param["db_user"],
                                                password=param["db_password"])

            sql_select_Query = "select * from experimentosDT ORDER BY id DESC LIMIT 1;"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            
            print("Number of experiments:", records[0][0])
            
            if(len(records)>1):
                print("Number of experiments with the same id: ", cursor.rowcount)
            
            ds.writeIdeal('id_experimento', records[0][1])
            ds.writeIdeal('intensidad', records[0][5])
            ds.writeIdeal('concentracion_co2', records[0][7])
            ds.writeIdeal('caudal_co2', records[0][6])
            ds.writeIdeal('concentracion_h2_in', records[0][12])
            

        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
        
    

        
        