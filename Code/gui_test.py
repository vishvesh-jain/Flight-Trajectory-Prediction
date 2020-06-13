


from tkinter import *
import combine_run
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os

root = Tk(  )
name = "eror"
arr = ""
dest = ""
#This is where we lauch the file manager bar.
def OpenFile():
    name = askopenfilename(initialdir="C:/Users/Batman/Documents",
                           filetypes =(("CSV File", "*.csv"),("All Files","*.csv")),
                           title = "Choose a file."
                           )
    #print (name)
    file_entry_label.config(text = name)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name,'r') as UseFile:
        	print()

    except:
        print()

    return name

def GetText():
	arr = e1.get()
	dest = e2.get()

	print(arr)
	print(dest)

def printall():
	
	arr = e1.get()
	dest = e2.get()
	inputpath = file_entry_label.cget("text")

	#print("insidefunction")
	#print(arr)
	#print(dest)
	#print(inputpath)

	a = combine_run.run(arr,dest,inputpath)
	prediction_entry_label.config(text = a)


Title = root.title( "Airport Dialog")
label = ttk.Label(root, text ="Enter Departure Airport",foreground="black",font=("Arial", 16))
e1 = ttk.Entry(root)


label2 = ttk.Label(root, text ="Enter Arrival Airport",foreground="black",font=("Arial", 16))
label3 = ttk.Label(root, text ="File Selected : ",foreground="black",font=("Arial", 16))
file_entry_label = ttk.Label(root, text ="None",foreground="black",font=("Arial", 16))
prediction_entry_label = ttk.Label(root, text ="",foreground="black",font=("Arial", 16))
#label4 = ttk.Label(root, text ="Predicted Path : ",foreground="black",font=("Arial", 16))
#predict_path_text = Text(root)


e2 = ttk.Entry(root)
label.grid(row=1, column=1)
label2.grid(row=3, column=1)
label3.grid(row=5, column=1)
#label4.grid(row=10,column=1)

file_entry_label.grid(row=5, column=2)
prediction_entry_label.grid(row=10, column = 2)

#predict_path_text.grid(row=11,column=2)

#predict_path_text.insert(INSERT, "Name.....")  
#predict_path_text.insert(END, "Salary.....")  

e1.grid(row=1, column=2)
e2.grid(row=3, column=2)


ttk.Button(root, text='Select Input Flight Plan File',command=OpenFile).grid(row=8,column=1,sticky=W,pady=4)
#ttk.Button(root, text='get Values',command=GetText).grid(row=8,column=2,sticky=W,pady=4)

ttk.Button(root, text='Quit',command=root.quit).grid(row=8,column=4,sticky=W,pady=4)
ttk.Button(root, text='Submit',command=printall).grid(row=8,column=3,sticky=W,pady=4)








root.mainloop()