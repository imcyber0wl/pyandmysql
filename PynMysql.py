#Made by @imcyber0wl on github. 24 Sep 2023


import tkinter as tk
from tkinter import ttk,Menu
from tkinter.messagebox import askyesno,showerror
import mysql.connector

root=tk.Tk()
root.geometry('600x400+50+50')
root.title("test window") 

style = ttk.Style(root)
style.theme_use('xpnative')

conn = mysql.connector.connect(host='localhost',
                               user='root',password='root',
                               database='world')

cursor=conn.cursor(buffered=True)

table_key=[((700,460),5,'city'),
           ('ID','int','Id'),
           ('Name','str','Name'),
           ('CountryCode','str','Country Code'),
           ('District','str','District'),
           ('Population','int','Population number'), ]

#### Create a window with given width and height and return wndow object
def insert_window(xy):
    window = tk.Toplevel(root)
    window.geometry(str(xy[0])+'x'+str(xy[1])+'+300+100')
    window.title('edit table: city')
    return window


####return last id in table
def getid(table):
    print(table)
    cursor.execute('SELECT ID FROM '+table+' ORDER BY ID DESC')
    row=cursor.fetchall()
    for id in row:
        row=id[0]
        break
    if row==None or row==[]:
        row=0
    return row

####Delete a row from given table 
def delete_this(key,id):
    answer = askyesno(icon='warning' ,title='confirmation',
                      message='Deleting a record can effect on other records. You cant undo this, are you sure you want to delete?')
    if answer==False:
        return 0
    
    table=key[0]
    table=table[2]
    cursor.execute('DELETE FROM '+table+' WHERE ID='+str(id))
    conn.commit()       



def edit(keys):
    global canvas, canvas2
    
    xy=keys[0]
    xyz=xy[0]
    table=xy[2] #table name
    window=insert_window(xy[0]) #create new window
    title_label=tk.Label(window,text='Show'+table)
    cursor.execute('SELECT * FROM '+table+' ORDER BY ID DESC')
    data=cursor.fetchall()

    #fields to search using id or name 
    search_id=tk.IntVar()
    search_name=tk.StringVar()
    idsearch=ttk.Entry(window, textvariable=search_id, width=17)

    id_2_insert=getid(table) #get last id     
    idsearch.insert(0,id_2_insert) #on opening, show last record 

    maxbtn=ttk.Button(window,text='>>',width=3,command=lambda: max_id()) #button for max id
    nextbtn=ttk.Button(window,text='>',width=3,command=lambda: next_id())
    minbtn=ttk.Button(window,text='<<',width=3,command=lambda: min_id()) #button for id 1 
    pervbtn=ttk.Button(window,text='<',width=3,command=lambda: prev_id())

    
    def max_id():
        idsearch.delete(0,'end')
        idsearch.insert(0,getid(table))
        id_lookup(scrollable_frame,search_id.get(),keys,namesearch,scrollable_frame,scrollable_frame2,window)

    def next_id():
        self=search_id.get()+1
        idsearch.delete(0,'end')
        idsearch.insert(0,self)
        id_lookup(scrollable_frame,search_id.get(),keys,namesearch,scrollable_frame,scrollable_frame2,window)

    def min_id():
        idsearch.delete(0,'end')
        idsearch.insert(0,1)
        id_lookup(scrollable_frame,search_id.get(),keys,namesearch,scrollable_frame,scrollable_frame2,window)
        
    def prev_id():
        self=search_id.get()-1
        if self<=0:
            self=1
        idsearch.delete(0,'end')
        idsearch.insert(0,self)
        id_lookup(scrollable_frame,search_id.get(),keys,namesearch,scrollable_frame,scrollable_frame2,window)

        
    idsearch.place(y=40,x=55)
    maxbtn.place(x=141,y=5)
    nextbtn.place(x=106,y=5)
    minbtn.place(x=35,y=5)
    pervbtn.place(x=70,y=5)

    ids_label=tk.Label(window,text="Id: ")
    ids_button=ttk.Button(window, text='Search id',width=8,command= lambda:id_lookup(scrollable_frame,int(search_id.get()),
                                                                                     keys,namesearch,scrollable_frame,
                                                                                     scrollable_frame2,window))
    ids_label.place(y=40,x=30)
    ids_button.place(y=5,x=195)

    namesearch=ttk.Entry(window, textvariable=search_name, width=17)
    name_label=tk.Label(window,text="Name: ")
    name_button=ttk.Button(window, text='Search',width=6,command= lambda:name_lookup(scrollable_frame,search_name,keys,
                                                                                     idsearch,scrollable_frame,scrollable_frame2,window))

    new_button=ttk.Button(window,text='New', width=6,command=lambda: add_new_doc(namesearch,search_name)) #add new record button 
    del_button=ttk.Button(window,text='Delete', width=7,command=lambda:delete_show()) #delete record button 

    #delete record
    def delete_show():
        fake_key=[(0,0,table),0]
        delete_this(fake_key,search_id.get())

    #add a new record
    def add_new_rec(namesearch,search_name):
        max_id()
        next_id()
        namesearch.delete(0,'end')
        
    namesearch.place(y=40,x=450)
    name_label.place(y=40,x=406)
    name_button.place(y=5,x=410)
    new_button.place(y=5,x=460)
    del_button.place(y=5,x=510)



    #create canvases
    canvas = tk.Canvas(window,width=xyz[0]-10,height=xyz[1]-5,bg='white')
    canvas2 = tk.Canvas(window,width=xyz[0]-10,height=17)
    #create frames 
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame2 = ttk.Frame(canvas2)
    #create canvas windows
    canvas.create_window((0, 17), window=scrollable_frame)
    canvas2.create_window((0, 0), window=scrollable_frame2)
    
    scrollable_frame.bind("<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all") ) )

    scrollable_frame2.bind("<Configure>",
    lambda e: canvas2.configure(
        scrollregion=canvas2.bbox("all") ) )


    def move2(*args):
        global canvas, canvas2
        eval('canvas.xview(*args)')
        eval('canvas2.xview(*args)')    
   
    scrly = ttk.Scrollbar(window, orient="vertical", command=canvas.yview) #only data fields scroll up and down, column names dont
    scrlx = ttk.Scrollbar(window, orient="horizontal", command=move2) #both data fields and column names scroll horizontally

    canvas.configure(yscrollcommand=scrly.set)
    canvas.configure(xscrollcommand=scrlx.set)
    canvas2.configure(xscrollcommand=scrlx.set)
    #the above makes canvases scrollable

    #place everything
    canvas2.place(x=15,y=70)
    canvas.place(x=15,y=90)
    scrly.place(x=1,y=0,height=xyz[1]-13)
    scrlx.place(x=15,y=xyz[1]-17,width=xyz[0]-17)

    max_id()


# Find record based on given ID 
def id_lookup(frame,ID,keys,namesearch,scrollable_frame,scrollable_frame2,window):
    if ID==0:
        ID=1 #do not lookup ID if it is 0

    #destroy table in canvas
    for widget in frame.winfo_children():
        widget.destroy()

    x=keys[1]
    x=x[0]    #get first field of table
    table=keys[0]
    table=table[2] #get name of the table

    namesearch.delete(0,'end')

    cursor.execute('SELECT * FROM '+table+' WHERE ID='+str(ID))
    data=cursor.fetchall()

    if data==None or data==[]:
        data=[] #if no records
    else:
        row=data[0] 
        namesearch.insert(0,row[1]) #first field (name field) is inserted to name box
        list_rows(data,keys,scrollable_frame,scrollable_frame2,window)

    return 0
            


### Find record based on name   
def name_lookup(frame,name,keys,idsearch,scrollable_frame,scrollable_frame2,window):
    #destroy table in canvas
    for widget in frame.winfo_children():
        widget.destroy()

    #get value in name box
    name=name.get()
    column_name=key[1]
    column_name=column_name[0] #get first column name (the name column)
    table=key[0]
    table=table[2] #get table name
    
    cursor.execute("SELECT * FROM "+table+" WHERE "+column_name+" = "+"'"+name+"'")
    data=cursor.fetchall()
    id2i=[]
    for row in data:
        id2i=row
        break 

    #put the record id in the ID box
    if id2i!=0:
        id2i=id2i[len(id2i)-1] 
        idsearch.delete(0,'end')
        idsearch.insert(0,id2i)
        list_rows(data,keys,scrollable_frame,scrollable_frame2,window)

    return 0 



def list_rows(data,keys,frame1, frame2,window):
    scrollable_frame2=frame2
    scrollable_frame=frame1 
    table_name=''
    columns=[] #store names of columns, used in edits
    no_of_columns=0
    data_pointers=[] #store pointers to entry fields
    list_of_ids=[] #where ids of each printed row are stored
    data_2_insert=[] #where inserted rows are stored (in case any were)

    c=-1  #counter for grid
    r=-1  #counter for grid

    #grid column names
    for key in keys:
        c+=1
        #this if condiiton skips first key which contains table name
        if c>0:
            label=ttk.Label(scrollable_frame2,text=key[2],width=25,borderwidth=3, relief="solid")
            label.grid(row=0,column=c) #place column
            columns.append(key[0]) #save column name

        elif c==0:
            table_name=key[2] #get table name
            no_of_columns=key[1] #number of columns

    r=-1
    if data==None:
        data=[]

    for row in data:
        r+=1 #row counter for grid
        c=-1 #column counter for grid
        counter=0 #counter for row array
        for key in keys:
            c+=1
                
            #skip first key
            if type(key[1])==int:
                c-=1
                #counter-=1

            else:
                if key[1]=='str': #if field type is string
                    text=tk.StringVar()
                else:             #if field type is integer
                    text=tk.IntVar()

                default=row[counter] #get value from row
                if default==None:
                    default=''
                if key[0]=='ID':    #if it is an id 
                    list_of_ids.append(default) #append it to ids list of its an id


                textbox=tk.Entry(scrollable_frame,textvariable=text,width=25)
                textbox.grid(row=r,column=c)
                textbox.delete(0,'end')
                textbox.insert(0,default)
                
                if key[0]!='add_date' and key[0]!='ID':
                    data_pointers.append(text)

                counter+=1

    global row_num
    row_num=r+1 #row_num keeps track of total number of rows
        
    btn=ttk.Button(window,text='Save',width=6,command=lambda: save(list_of_ids,data_2_insert,row_num,
                                                                table_name,columns,no_of_columns,data_pointers))
    btn.place(x=565,y=5)


    def nothing(event):
        return 0

    #adds a new empty row to the table GUI 
    def insert_new(window,keys,data_2_insert):

        def handle_click(event):
            global textboxes
            textboxes.bind("<1>", nothing)
            global row_num
            row_num+=1
            insert_new(window,keys,data_2_insert)

        c=-1
        counter=0
        while counter!=1:
            counter+=1
            for key in keys:
                c+=1
                if type(key[1])==int:
                    c-=1
                    
                else:
                    if key[1]=='str':
                        text=tk.StringVar()
                    else:
                        text=tk.IntVar()

                    textbox=tk.Entry(window,textvariable=text,width=25)
                    textbox.grid(row=row_num,column=c)
                    data_2_insert.append(text) #append the pointer to its value to the data_2_insert array

                    if key[0]=='add_date':
                        textbox.insert(0,str(datetime.date.today()))
                    
                if c==0: #if first column shown, bind it to handle_click
                    global textboxes
                    textboxes=textbox
                    textbox.bind("<1>", handle_click)

    insert_new(scrollable_frame,keys,data_2_insert)

def save(list_of_ids,data_2_insert,row_num,table_name,columns,no_of_columns,data_pointers):
    #insert first
    insert_query="INSERT INTO "+table_name+"("
    values=') VALUES('
    for column in columns:
        insert_query=insert_query+column+','
        values=values+'%s,'
    insert_query=insert_query[0:len(insert_query)-1]+values[0:len(values)-1]+')'
    print(insert_query)

    counter=len(data_2_insert)/no_of_columns #this counts how many rows to insert
    if round(counter)>counter:
        counter-=1

    total_items_counter=0 #used to read from data_2_insert
    ids_counter=getid(table_name)+1 #counts new ids
    while counter>0:
        item_counter=0 #counts how many items have been read for a row
        values=[] #where values will be stored
        while item_counter<no_of_columns:
            if total_items_counter>=len(data_2_insert):
                break

            item=data_2_insert[total_items_counter]
            if (item.get()=='' or item.get()==0) and item_counter==1:
                #if first field (after ID) is empty, ignore this row
                total_items_counter+=no_of_columns-1 #skip all row
                values=[]
            else:
                if item_counter==0:
                    values.append(ids_counter)
                    ids_counter+=1
                else:
                    values.append(item.get())

                total_items_counter+=1
                item_counter+=1

        if values!=[]: #if row was not ignored
            print(insert_query,values)
            try:
                cursor.execute(insert_query,values)
                conn.commit()
            except:
                showerror("Insert failed", "Something went wrong. Couldn't insert new rows into table "+table_name)

        counter-=1

    #editing process 
    counter=len(data_2_insert)/no_of_columns #this counts how many rows to insert
    if round(counter)>counter:
        counter-=1

    update_query='UPDATE '+table_name+' SET '

    for column in columns:
        if column!='add_date' and column!='ID':
            update_query=update_query+column+'=%s,'
     
    update_query=update_query[0:len(update_query)-1]+' '

    values=[]
    total_items_counter=0
    id_counter=0
    while counter>=0:
        values=[]
        item_counter=0
        removal_flag=0
        while item_counter<no_of_columns-1: #-1 because we ignore ID
            if total_items_counter<=len(data_pointers)-1:
                item=data_pointers[total_items_counter]

            else: #this should happen when inserting new data into non-document
                counter=-1
                break

            if item.get()=='' and item_counter==0: #if first item is empty
                total_items_counter+=no_of_columns 
                item_counter=no_of_columns #drop all row
                removal_flag=1 #dont add brackets

            else:
                item=data_pointers[total_items_counter]
                item=item.get()
                values.append(item)
                item_counter+=1
                total_items_counter+=1            

        if removal_flag==0:
            if id_counter<=len(list_of_ids)-1:
                id_part=" WHERE ID="+str(list_of_ids[id_counter])
            else:
                coutner=-1
                break
            print(update_query+id_part,values)
            cursor.execute(update_query+id_part,values)
            conn.commit()
            id_counter+=1
            counter-=1


menubar = Menu(root)
root.config(menu=menubar)

edit_menu = Menu(menubar)
edit_menu.add_command(
    label='Example table',
    command=lambda: edit(table_key),
)

menubar.add_cascade(
    label="Edit table",
    menu=edit_menu,
    underline=0
)

root.mainloop()
