from tkinter import *
import tkinter as tk
from  tkinter import ttk

#see https://www.pythontutorial.net/tkinter/tkinter-menu/
#see https://pythonguides.com/python-tkinter-table-tutorial/
def crea_lista_istanze(frame,profilo,lista_istanze):#,load_profile_function
    frame1 = ttk.Frame(frame)
    frame1.pack()

    scroll = Scrollbar(frame1)
    scroll.pack(side=RIGHT, fill=Y)
    tab = ttk.Treeview(frame1,yscrollcommand=scroll.set)

    tab['columns'] = ('Nome', 'Id', 'Tipo', 'Stato')
    tab.column("#0", width=0,  stretch=NO)
    tab.column("Nome", width=250)
    tab.column("Id",anchor=CENTER,width=120)
    tab.column("Tipo",width=80)
    tab.column("Stato",width=80)
    tab.heading("#0",text="",anchor=CENTER)
    tab.heading("Nome",text="Nome",anchor=CENTER)
    tab.heading("Id",text="Id",anchor=CENTER)
    tab.heading("Tipo",text="Tipo",anchor=CENTER)
    tab.heading("Stato",text="Stato",anchor=CENTER)
    #for reservation in lista_istanze['Reservations']:
    #    for istanza in reservation['Instances']:
    #        for k in istanza:
    #            print (k)
    i=1
    for reservation in lista_istanze['Reservations']:
        for istanza in reservation['Instances']:
            nome=''
            if 'Tags' in istanza: #len(istanza.Tags)>0 :
                for tag in istanza['Tags']:
                    print (tag)
                    if tag['Key']=='Name':
                        nome=tag['Value']
            tab.insert(parent='',index='end',iid=i,text='',
                values=(nome,istanza['InstanceId'],istanza['InstanceType'], istanza['State']['Name']))
            i=i+1
    tab.pack()
    #return tab

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Aws Py Console - only ec2_instances')
    root.geometry ('700x450') #WIDTHxHEIGHT+TOP+LEFT
    crea_lista_istanze(root,"default",
        {'Reservations':[{'Instances':[{'InstanceId':'i1','InstanceType':'t2','State':{'Name':'main'} } ] }] } 
    )
    root.mainloop()