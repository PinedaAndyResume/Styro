import tkinter as tk 
import search as se 
import sync_data as sd
import datetime 
import os 

#Modules for importing,downloading files 
import dropbox
import requests
from tkinter.filedialog import asksaveasfile 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import zipfile 

from tkinter import messagebox



















class home():

    def __init__(self):

        'ROOT FOR TKINTER'

        self.root = tk.Tk()


        ''' Global ''' 


        self.download_list = []
        self.is_file_selected = False 
        self.upload_selected_file = ''

        self.current_date = datetime.datetime.now()


        #developer id in use 
        self.my_developer_id = 12312345



        ''''Dropbox ''' 
        self.dropbox_access_token = 'DropBox Access Token HERE'
        self.mod_path = '/Mods/'
        self.cc_path = '/CC/'

        #Connecting to dropbox
        self.dbx = dropbox.Dropbox(self.dropbox_access_token)





        ' MAIN WINDOW '

        #window 
        'Creates the basic application window'

        self.root.title('Styro') #Title of the window 
        self.root.geometry('696x440') # sets the size of the application window 

        #background for app 
        background = tk.Label(self.root, bg = 'white')
        background.pack(fill ='both', expand = True)
 





















        ' SEARCH FRAME '


        'Create search area frame' 
        self.search_area_frame = tk.Frame(self.root, height = 84, width = 468)
        self.search_area_frame.place(x = 7, y = 7) #we place to be more specfic and set frames compared to griding items 
        





        #Search bar
        'Update - search bar bind, need to assign a value and search dataframe for it and display results'
        self.search_query = tk.StringVar()
        self.search_bar = tk.Entry(self.search_area_frame, width=48)
        self.search_bar.focus()
        self.search_bar.bind("<Return>",self.search)
        self.search_bar.place(x=6, y=19)


        #search button 

       
        
        










        #options for search bar 
            #Based off the review of sydney and players desire to view specfic content 
            #mod - (default) searches only for mods 
            #cc - searches only for custom content 

        #assigns a variable value to check buttons
        self.mod_checked = tk.BooleanVar()
        self.cc_checked = tk.BooleanVar()

        #Creates the check button 
        self.mod_checkbutton = tk.Checkbutton(self.search_area_frame,text ='Mod', variable = self.mod_checked, onvalue = True , offvalue = False) 
        self.cc_checkbutton = tk.Checkbutton(self.search_area_frame,text ='CC', variable = self.cc_checked, onvalue = True , offvalue = False) 

        # Positioning the mod and cc check buttons 
        self.mod_checkbutton.place(x=7, y=56)
        self.cc_checkbutton.place(x=63, y=56)

        #auto selects the mod checkbutton
        self.mod_checkbutton.select() # makes the both check button the default value

        
        #get status of checked buttons 
        self.value_mod_checkbutton = self.mod_checked.get()
        self.value_cc_checkbutton =self.cc_checked.get()


        # Practice to check status of buttons if they're working 
        #print(self.value_mod_checkbutton)
        #print(self.value_cc_checkbutton)










        ' MAIN RESULTS CANVAS'


        'Create main result canvas'
        
      

        # Created a canvas instead of a frame in order to create a scrollable canvas to display all results 
        self.main_result_canvas = tk.Canvas(self.root, height = 330, width = 466, scrollregion=(0, 0, 2000, 2000), cursor = 'trek')
        self.main_result_canvas.place(x = 7, y = 97)
        #vscrollbar.config(add_button = self.main_result_canvas.yview) yscrolladd_button = vscrollbar.set


        # Created a list box to insert results from search query and then add them to the download list
        # will clear with each search 


        #Scroll Bar for listbox 
        self.lb_scrollbar = tk.Scrollbar(self.root, orient="vertical")

        #listbox 
        self.results_listbox = tk.Listbox(self.main_result_canvas, yscrollcommand=self.lb_scrollbar.set, width = 50, height = 17, exportselection = False)
        self.lb_scrollbar.config(command=self.results_listbox.yview)
        self.results_listbox.pack(fill=tk.BOTH,expand=True)  
        self.results_listbox.bind('<<ListboxSelect>>',self.link_select)

        #sample input
        #self.display_onto_canvas('name')
       

























        ''' DOWNLOAD FRAME ''' 



        'Create download info frame'
        self.download_info_frame = tk.Frame(self.root, height = 347, width = 200)
        self.download_info_frame.place(x=483, y=7)





        'name of user'
        self.user_name = 'AndyPineda' #example, replace with actual student name 
        user = tk.Label(self.download_info_frame, text = self.user_name)
        user.place(x = 59, y =19)






        'my downloads listbox'

        self.downloads_listbox = tk.Listbox(self.download_info_frame, height = 15, width = 20, exportselection = False )
        self.downloads_listbox.pack(fill=tk.BOTH,expand=True)  
        self.downloads_listbox.bind('<<ListboxSelect>>',self.clear_from_download)
        





        'download button'
        self.download_button = tk.Button(self.download_info_frame, text="DOWNLOAD", command=self.download, width = 10)
        self.download_button.pack(side = 'bottom')





        ' EXTRA FUTURES FRAME'


        'Extra futures button frame'
        self.extra_futures_frame = tk.Frame(self.root, height = 64, width = 200)
        self.extra_futures_frame.place(x=483, y=363)



        self.update_button = tk.Button(self.extra_futures_frame, text='Update a File', command= self.update_a_file, width = 10)
        self.update_button.grid(row =1 , column =1)

        self.add_file_button = tk.Button(self.extra_futures_frame, text='Add a File', command= self.add_file_window, width = 10)
        self.add_file_button.grid(row =1 , column =2)


        #Check button to check for new updates on any of your files
        self.check_for_update_button = tk.Button(self.extra_futures_frame, text='Check For Updates', command= print('Checking for updates'), width = 14)
        self.check_for_update_button.grid(row =2 , columnspan  = 3, ipady = 7)







        




        self.root.mainloop()




        


            

    def display_onto_canvas(self,name):
        #will input the result to the last line 
        self.results_listbox.insert('end',name)


    def download(self):
        #file = asksaveasfile(mode='w', defaultextension=".txt")
        save_location = askdirectory()

        for id_num in self.download_list:

            id_row = se.find_mod(id_num) # searches the mod in the database 
            file_path = id_row[0][3] #path to dropbox file for program 
            file_name = id_row[0][1]

            
            self.download_from_dropbox(save_location,file_path,file_name)
         
            #run download 

             

        
    def search(self,*args):
        
        ' takes the entry and searches the database for a matching name and returns a list' 

        #clears the previous search screen
        self.results_listbox.delete(0,tk.END)


        #takes the entry from the search bar and turns it into a string 
        request = self.search_bar.get()
        request = str(request) 
        
        #Makes sure you enter a search
        if len(request) < 3:
            print('Needs to be atleast three characters')

        else: 
            


            # Checks to see if searching for mods,cc or both 
            cc = self.cc_checked.get()
            mod = self.mod_checked.get()


            # Searches query based on decesion of mod or cc or both; Default is both 
            
            if cc and mod == True: # search both
                se.search_both(request)

            elif cc == True and mod == False: # search custom content
                se.search_custom_content(request)

            elif cc == False and mod == True: # search mods 
                results = se.search_mods(request)


            elif cc == False and mod == False: # if none selected, default is both 
                self.mod_checkbutton.select()
                self.cc_checkbutton.select()
                se.search_both(request)


            """ Takes the search result and prints it on the display """ 
               #prints none if no results were found
            if len(results) < 1:
                    self.display_onto_canvas('No Search Found')

            #prints the names of the results 
            else: 
            
                for result in results:
                        
                    #content 
                    content_id = result[0]
                    file_name = result[1]
                    developer = result[2]
                    #file_path = result[3]
                        
                    #text to display result 
                    text_input = str( str(content_id) + "  ,  " +file_name + "  ,  "+ developer ) 

                    self.display_onto_canvas(text_input) # sends the text to printed on to the canvas 
                

    def link_select(self,*args):

        """" Takes the selected links from the search results and appends them to your download list and displays onbox """


        value = self.results_listbox.get(self.results_listbox.curselection())

        #checks to see if the download is already added and will pass if added 
        if value not in self.download_list:
            
            #appends the id number to download list 
            names = value.split(',')
            id_num  = names[0]
            self.download_list.append(id_num)


            self.downloads_listbox.insert('end',value)
            

        else:  # passes if the value was already in your download list 
            pass 
        

    def clear_from_download(self,*args):
        
        """ Removes a link from your download list incase you change your mind """ 
            #UPGADE - Make sure it can't delete if theres none left, tried an if statement with download list but didnt work
                     #It doesnt cause anny malfunction with program but pops error
                     # check populating tuples or checking if tuples are populated before continuning 

        #Gets the position of the your selection from your cursor 
        
        value = self.downloads_listbox.curselection()
            
        #gets the name value in order to remove the name from download list
        name = self.downloads_listbox.get(self.downloads_listbox.curselection())

        #if its in the downloadlist we want to remove it first, (in case you wish to readd the link)
        if name in self.download_list:

            self.download_list.remove(name)
        else: pass 


        self.downloads_listbox.delete(value)

        
    def add_file_window(self,):
        #creates a new window instance to enter file information to upload 

        self.upload_window = tk.Toplevel(self.root)
        self.upload_window.geometry('400x319')

        #Creates name label
        name_label = tk.Label(self.upload_window, text = 'Name:')
        name_label.grid(row =  1)

        #Creates name entry 
        self.file_name = tk.Entry(self.upload_window,width = 30)
        self.file_name.grid(row =  1, columnspan = 3, column = 1)


        ##Creates name label
        developer_name_label = tk.Label(self.upload_window, text = 'Developer:')
        developer_name_label.grid(row =  2)


        #developer entry
        self.developer_entry = tk.Entry(self.upload_window,width = 30)
        self.developer_entry.grid(row =  2, columnspan = 3, column = 1)




        #Create mod/cc type selection 
        
        #Variables to store selected  
        self.checked_type_update_window = tk.StringVar()
        self.checked_type_update_window.set('both') #sets the default to both for mods 
       
        #label for type: 
        mod_cc_type_label  = tk.Label(self.upload_window, text = 'Type:')
        mod_cc_type_label.grid(row =  3)

        #Creates the check buttons for both,mod, and cc 
        both_checkbutton = tk.Radiobutton(self.upload_window, text ='Both', variable = self.checked_type_update_window, value = 'both')
        mod_checkbutton = tk.Radiobutton(self.upload_window, text ='Mod', variable = self.checked_type_update_window, value = 'mod')
        cc_checkbutton = tk.Radiobutton(self.upload_window, text ='CC', variable = self.checked_type_update_window, value = 'cc')

        #grid check buttons 
        both_checkbutton.grid(row =  3, column = 1)
        mod_checkbutton.grid(row =  3, column = 2)
        cc_checkbutton.grid(row =  3, column = 3)


        #overview label 
        description = tk.Label(self.upload_window, text = 'Description (500 char max)')
        description.grid(row =4, column = 2)

        #description textbox
        self.description_textbox = tk.Text(self.upload_window, height = 10, width =30 , bg = 'black', fg = 'white')
        self.description_textbox.grid(row = 5, rowspan = 2, column = 1, columnspan = 3)


        #select to download button 

        
        #Select file button 
        self.select_file = tk.Button(self.upload_window,width = 10, text = 'Select a File', command = self.select_a_file )
        self.select_file.grid(column = 2)
     

        #Upload Button
        self.upload_button = tk.Button(self.upload_window,width = 10, text = 'Upload File', command = self.upload_file_to_dropbox )
        self.upload_button.grid(column = 2)
        
        









        self.upload_window.mainloop()
    

    def select_a_file(self):
        #asks the user to open directory and select a folder to upload 
        file = askopenfilename(filetypes =[('Zipped Folders', '*.zip')]) #allows for only zipped folders to be uploaded 
       


        if file is not None: #if theres content in the file 
        
            print('File Selected')# Shows me that a file is selected 
            self.upload_selected_file = file #selected file upload equals the selected file path 
            
            return file 

        else:
            pass 



    def upload_file_to_dropbox(self):
        """ Uploads the selected file onto dropbox and updates the database with the new file information """




       #checks to see if theres an actual file selected 
       #check = len(self.upload_selected_file) + 1  #used to check if thers a file 
        file_name = self.file_name.get()
        developer_name = self.developer_entry.get()
        type_checked = self.checked_type_update_window.get()
        overview = self.description_textbox.get('1.0',tk.END)
        #id_num = self.my_developer_id 

    


        #Checks to see if the names meet the required conditions before passing the data
         
        if len(overview) > 500: #500 character max for name 
            messagebox.showerror('Exceeded 500 Char', "Your overview must be 500 characters or less")
        else:
            pass 
        

        if len(file_name) > 100: #255 character max for name 
            messagebox.showerror('Exceeded 100 Char', "Your file name must be 100 characters or less")
        else:
            pass 





        """ Uploads the file to dropbox """ 

        #upload the file with mod tag
        if type_checked == 'mod':

            path = self.mod_path + 'mod_'+file_name + '_' + str(developer_name.lower()) + '.zip' #gives you the saving name of the file 
            self.dbx.files_upload(open(self.upload_selected_file, "rb").read(), path) # upload the file

        else: 

            pass 


        #uploads the file with cc tag 
        if type_checked == 'cc':

            path = self.mod_path + 'cc_'+file_name+ '.zip' #gives you the saving name of the file 
            self.dbx.files_upload(open(self.upload_selected_file, "rb").read(), path) # upload the file

        else: 
            
            pass 


        #uploads the file with both tag

        if type_checked == 'both':

            path = self.mod_path + 'both_'+file_name +'.zip' #gives you the saving name of the file 
            self.dbx.files_upload(open(self.upload_selected_file, "rb").read(), path) # upload the file

        else: 
            
            pass 

        



        """ Uploads data to mysql """ 

        #Upload data to SQL
        sd.load_to_sql(file_name, developer_name, path, type_checked, overview, self.current_date)
        





        """ Prints Success """ 

        #Sucess print Window 
        messagebox.showinfo("Success","File Successfully Uploaded")
        
        #clears entries after upload 
        self.description_textbox.delete('1.0',tk.END) #clears textbox
        self.file_name.delete(0,len(file_name)) #clears file name 
        self.developer_entry.delete(0,len(developer_name)) #clears developer name 
        self.upload_selected_file = ''




        self.upload_window.destroy() # closes window after upload
       

    def download_from_dropbox(self,save_location,path,file_name):
        """Downloads files from dropbox based on the link """ 


        file_name = file_name + ".zip"
        orginal = save_location
        save_location = save_location + file_name 

        try:
            # Opens the folder to save files to 
            with open(save_location,"wb") as f:
                metadata,res = self.dbx.files_download(path)
                f.write(res.content)

            #Extracts zip files onto folder 
            with zipfile.ZipFile(save_location,"r") as zip_ref:
                zip_ref.extractall(orginal)

        except:
            print('Error with download')


        messagebox.showinfo("Success","Successfully Downloaded Files")
   


    def show_update_link(self, *args):

        "Change the entry bar to update to the selected link"

        value = self.myfiles_listbox.get(self.myfiles_listbox.curselection())
        names = value.split(',')
                
        self.update_window_selected_link_var.set(names)
        


    def update_file(self):

        """Goes into sql database and updates the system with the new updated file """ 


        #Entries being sent to database to update file information 
        
        #selected file name 
        value = self.myfiles_listbox.get(self.myfiles_listbox.curselection())
        value = str(value)
        update_information = self.update_file_textbox.get('1.0',tk.END)
        new_name = str(self.file_name.get())
       
    
        
        #checks for your selected files in your files folder
        #searches the database and updates the content with new information 
  
        for line in self.orginal_results:
            file_name = line[2]
            num = line[0]
            type = line[1]
            developer_name = line[3]
            path = line[4]

            new_file_path = "/" + str(type.lower()) + "_" + new_name + "_" + str(developer_name.lower())
            
            if file_name == value:
            
                #Sends new file_name , new update info , the current date, and the users id to identify and update the file with the 
                #new update and information 
                sd.update_for_file(num,new_name,new_file_path,self.current_date, update_information)

                #Moves the old file to an old versions folder 
                # tried to do delete but thats a business feature for the dropbox api 
                #and im not paying 
                self.dbx.files_move(from_path= path, to_path= "/old_versions/ " + str(file_name.lower()) + "_" + str(developer_name.lower()) + "_" + str(self.current_date))


                #loads the new file onto dropbox 
                save_path = "/Mods/" + str(type.lower()) + "_" + str(new_name.lower()) + "_" + str(developer_name.lower())
                self.dbx.files_upload(open(self.upload_selected_file, "rb").read(), save_path) # upload the file


                print("Job Complete")




    def update_a_file(self):

        """ Creates a window for user to pick files they've
             uploaded and upate them with the new one   """ 


        #Creates update window 
        self.update_file_window = tk.Toplevel(self.root)
        self.update_file_window.geometry('210x620')



        #creates selected file text 
        select_file_text = tk.Label(self.update_file_window,text = 'Select File')
        select_file_text.grid(row = 1, column = 2, columnspan = 2)

        #blank
        blank_label = tk.Label(self.update_file_window)
        blank_label.grid(column = 1, row =1)
        
        #blank 
        blank_label = tk.Label(self.update_file_window)
        blank_label.grid(column = 1, row =2)


        #files listbox
        self.myfiles_lb_scrollbar = tk.Scrollbar(self.root, orient="vertical")

        self.myfiles_listbox = tk.Listbox(self.update_file_window, yscrollcommand=self.lb_scrollbar.set, width = 20, height = 16, exportselection = False)
        self.myfiles_lb_scrollbar.config(command=self.myfiles_listbox.yview)
        self.myfiles_listbox.grid(column = 2,columnspan = 2, row = 2, rowspan = 2, ipadx = 5)
        self.myfiles_listbox.bind('<<ListboxSelect>>',self.show_update_link)

      
        #Load user files onto textbox
        self.orginal_results = se.search_user(self.user_name)
        results = se.search_user(self.user_name)


        self.my_user_files = results #appends your files to a user id

        
        #prints no file if result is less than 1 
        if len(results) < 1:

            name = "No Files"
            self.myfiles_listbox.insert('end',name)

        else: 
            
            for result in results:
                name = result[2]
                print(result)
                self.myfiles_listbox.insert('end',name) # sends the text to printed on to the canvas 
                
















        #Textbox to show selected link
        self.update_window_selected_link_var = tk.StringVar()
        self.update_window_selected_link = tk.Entry(self.update_file_window, width = 20 , bg = 'black', fg = 'white', state = "disabled", textvariable =self.update_window_selected_link_var )
        self.update_window_selected_link.grid(row = 6, rowspan = 1, column = 1, columnspan = 3, ipady = 5)


       
        #Creates new name label
        name_label = tk.Label(self.update_file_window, text = 'Name')
        name_label.grid(column = 2, columnspan = 2)

        #Creates new name entry 
        self.file_name = tk.Entry(self.update_file_window,width = 20)
        self.file_name.grid(column = 2, columnspan = 2)


        ##Creates Update notes label
        update_notes_label = tk.Label(self.update_file_window, text = 'Update Notes')
        update_notes_label.grid(column = 2, columnspan = 2)


        #Update textbox
        self.update_file_textbox = tk.Text(self.update_file_window, height = 10, width = 20 , bg = 'black', fg = 'white')
        self.update_file_textbox.grid(column = 2, columnspan = 4)



        #select a file button
        self.select_an_update_file_button = tk.Button(self.update_file_window,text = 'Select A File', command = self.select_a_file , width = 20)
        self.select_an_update_file_button.grid(row = 12,column = 2, columnspan = 2)

        #update button
        self.update_file_button = tk.Button(self.update_file_window,text = 'Update', command = self.update_file , width = 20)
        self.update_file_button.grid(row = 13,column = 2, columnspan = 2)

       

        
            






        self.update_file_window.mainloop()





    def check_for_update(self):
        pass 

   

         
       
        

        






   








if __name__ == "__main__":
    start = home()
    start
