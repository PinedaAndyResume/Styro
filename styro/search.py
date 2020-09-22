import main_window
import tkinter as tk 
import mysql.connector as mysql




def search_user(user_name):

    ''' Takes a search query and searches the mods database and returns a list with results ''' 

   
    #connect specfically to the mod_downlaoder database 
    db = mysql.connect(host = "localhost", user="root", passwd ="password", database = 'Downloads')
    #cursor for mySQL
    cursor = db.cursor(buffered = True)



    
    # Collecting data from the all columns in the mods folder that are similar to the search query  
    cursor.execute("SELECT * FROM mods WHERE developer LIKE %s  ", (user_name, ))
    data = cursor.fetchall()


    results = []

    for result in data:
      results.append(result)
   
    
    return results 
    
    
    
    #source: https://www.datacamp.com/community/tutorials/mysql-python#CAC




def find_mod(query):
  """ finds search id and returns data per row  """ 
  db = mysql.connect(host = "localhost", user="root", passwd ="password", database = 'Downloads')

  cursor = db.cursor(buffered = True)

  cursor.execute("SELECT * FROM mods WHERE id = %s", (query,))
  data = cursor.fetchall()

  
  return data




def search_mods(request):


    ''' Takes a search query and searches the mods database and returns a list with results ''' 

   
    #connect specfically to the mod_downlaoder database 
    db = mysql.connect(host = "localhost", user="root", passwd ="password", database = 'Downloads')
    #cursor for mySQL
    cursor = db.cursor(buffered = True)



    
    # Collecting data from the all columns in the mods folder that are similar to the search query  
    cursor.execute("SELECT * FROM mods WHERE file_name LIKE %s ", (request, ))
    data = cursor.fetchall()


    results = []

    for result in data:
      results.append(result)
   
    
    return results 
    
    
    
    #source: https://www.datacamp.com/community/tutorials/mysql-python#CAC
    

  
    
def search_custom_content(request):
  "Prints the search result for custom content"

  print('IT worked CC;', request)



def search_both(request):
  ''' Searches both mods and cc content and returns a combined list ''' 

  search_mods(request)
  search_custom_content(request)
  print("It worked both:")











if __name__ == "__main__":
  pass 
  
