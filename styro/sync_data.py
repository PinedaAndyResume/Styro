import main_window
import mysql.connector as mysql
import dropbox







def load_to_sql(file_name,developer,file_location,type,overview,date):
   
   """ loads data into column  """ 
   #Strip any quotes
   file_name = file_name.replace('"',"")
   developer = developer.replace('"',"")
   file_location = file_location.replace('"',"")
   type = type.replace('"',"")
   

   db = mysql.connect(host = "localhost", user="root", passwd ="password", database = 'Downloads')
   cursor = db.cursor(buffered = True)

   #mySQL script to inject data into datagrame
   query = 'INSERT INTO mods (file_name,developer,file_location,type,overview,date) VALUES (%s,%s,%s,%s,%s,%s)'
   
   #tuple values to insert into database 
   receiving_tuple = (file_name,developer,file_location,type,overview,date)

   #execute data entry 
   cursor.execute(query,receiving_tuple)

   #confrim and commit the changes 
   db.commit()

   
   print('Data Successfully Updated')

   #close cursor and database 
   cursor.close()
   db.close()




def update_for_file(id_num,update_name,new_file_path,date,new_update_info):
   
   """ Takes new_file_name, new update information, date """

   #sends message to update file name
   #wasnt working in single line of code 
   


   db = mysql.connect(host = "localhost", user="root", passwd ="password", database = 'Downloads')
   cursor = db.cursor(buffered = True)

   

   #Update date amd update info 
   query = "UPDATE mods SET file_name = %s, file_location = %s, overview = %s, date = %s WHERE id = %s;"
   
   #tuple values to insert into database 
   receiving_tuple = (update_name,new_file_path,new_update_info,date,id_num)

   #execute data entry 
   cursor.execute(query,receiving_tuple)

   #confrim and commit the changes 
   db.commit()





   
   print('Data Successfully Updated')

   #close cursor and database 
   cursor.close()
   db.close()























if __name__ == "__main__":
   pass 
