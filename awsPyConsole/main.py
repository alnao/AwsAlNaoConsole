import tkinter as tk
from tkinter import *
import window.menu as menu
import sdk.profiles as AwsProfiles
import sdk.ec2_instances as AwsInstances
import window.ec2_instances as ec2_instances
from tkinter import Label
from tkinter import ttk

#see example tk https://realpython.com/python-gui-tkinter/

def main_window_start():
    root = tk.Tk()
    #strvar = StringVar(root, name ="str") #see https://www.geeksforgeeks.org/python-setting-and-retrieving-values-of-tkinter-variable/
    #root.setvar(name ="profilo_selezionato", value ="loading")#profilo_selezionato=StringVar(root,name="profilo_selezionato",value="loading")
    # Create window
    root.title('Aws Py Console')
    x=10#root.winfo_screenwidth() // 6
    y=10#int(root.winfo_screenheight() * 0.1)
    root.geometry ('1000x700+' + str(x) + "+" + str(y) ) #WIDTHxHEIGHT+TOP+LEFT

    #get AWS profiles
    lista_profili_aws=AwsProfiles.get_lista_profili()

    #crete menu
    menu.create_menu(root,lista_profili_aws,reload_profile)
    main_frame(root,"")
    root.mainloop()
    
def add_text_to_frame(frame,text):
    Label(frame, text=text).pack()
    frame.pack_propagate(False)

def main_frame(root,profilo): #nota: funziona solo se c'è un iframe nella main
    #if '!frame' in root.children: #nota: funziona solo se c'è un iframe nella main
    #    print ( root.children )
    if profilo=="": #nessun profilo selezionato dal menu
        frame1=tk.Frame(root,width=975,height=675,bg="#EEEEEE")
        frame1.grid(row=0,column=0)
        add_text_to_frame(frame1,"Selezionare un profilo") # Label(frame1, text="Selezionare un profilo").pack()
        #frame1.pack_propagate(False)
        return
    frame1=tk.Frame(root,width=975,height=675,bg="#EEEEEE")
    frame1.grid(row=0,column=0)
    #tabs 
    tabs = ttk.Notebook(frame1, width=950, height=650)
    #style = ttk.Style()
    #style.theme_settings("default", {"TNotebook.Tab": {"configure": {"padding": [30, 30]}}})
    tabs.pack(fill=BOTH, expand=TRUE)
    frame1 = ttk.Frame(tabs)
    frame2 = ttk.Frame(tabs)
    tabs.add(frame1, text="Profilo " + profilo)
    add_text_to_frame(frame1,"TODO" + profilo)
    tabs.add(frame2, text="Ec2")
    add_text_to_frame(frame2,"Lista istanze del profilo "+profilo)
    ec2_instances.crea_lista_istanze(frame2,profilo,AwsInstances.get_lista_istanze(profilo))
    tabs.pack(expand=1, fill="both")
    #frame1=tk.Frame(root,width=975,height=675,bg="#EEEEEE")
    #frame1.grid(row=0,column=0)
    #l = Label(frame1, text="Profilo selezionato: " + profilo).pack()
    #frame1.pack_propagate(False)

def reload_profile(root,profilo):
    main_frame(root,profilo)
    #root.setvar(name ="profilo_selezionato",value =profilo)
    #print(profilo)

def main():
    main_window_start()


if __name__ == '__main__':
    main()

