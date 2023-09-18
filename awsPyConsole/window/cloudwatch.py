from urllib import request
from tkinter import *
import tkinter as tk
from  tkinter import ttk
from tkinter.filedialog import asksaveasfile #https://www.geeksforgeeks.org/python-asksaveasfile-function-in-tkinter/

class CloudWatchWindow:
    larghezza_blocco1=450
    larghezza_blocco2=900
    altezza=600
    larghezza_blocco2_mol1=12/2 #larghezza colonne 
    larghezza_blocco2_mol2=12/10

    def __init__(self,frame,profilo,lista_metriche,get_log_object,reload_method):
        for widget in frame.winfo_children():
            widget.destroy()
        self.lista_metriche=sorted(lista_metriche, key=lambda x:x['Dimensions'][0]['Value']) #lista_metriche
        self.profilo=profilo
        self.frame=frame
        self.get_log_object=get_log_object
        self.reload_method=reload_method
        self.crea_window()
        self.lista_log=[]

    def crea_window(self):
        #grid # https://www.geeksforgeeks.org/python-grid-method-in-tkinter/
        #grid see https://tkdocs.com/tutorial/grid.html
        self.frame.columnconfigure(2)
        self.frame1 = ttk.Frame(self.frame, width=self.larghezza_blocco1+10, height=self.altezza)
        self.frame1.grid(row = 1, column = 1, sticky = tk.NW, padx = 2) 
        self.frame1.pack(side=LEFT, expand = 1)
        self.frame2 = ttk.Frame(self.frame, width=self.larghezza_blocco2+10, height=self.altezza)
        self.frame2.grid(row = 1, column = 2, sticky = tk.NW, padx = 2) 
        self.frame2.pack(side=LEFT, expand = 1)

        self.scroll = Scrollbar(self.frame1)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.tree = ttk.Treeview(self.frame1,yscrollcommand=self.scroll.set,height=50)
        self.tree['columns'] = ('Nome')
        self.tree.column("#0", width=0,  stretch=NO)
        self.tree.column("Nome", width=self.larghezza_blocco1)
        self.tree.heading("#0",text="",anchor=CENTER)
        self.tree.heading("Nome",text="Nome",anchor=CENTER)
        i=1
        for b in self.lista_metriche:
            self.tree.insert(parent='',index='end',iid=i,text='',values=(b['Dimensions'][0]['Value']))
            i=i+1
        self.tree.bind("<Double-1>", self.open_log)
        self.tree.pack()
        self.free2_loaded=False
        self.free3_loaded=False
        #return tab

    def open_log(self, event): #(frame,profilo,lista_istanze,istanza):
        item = self.tree.selection()[0]
        self.log_name_selected = self.tree.item(item)['values'][0]
        #print ("Apro "+ self.bucket_name)
        self.lista_log=self.get_log_object(self.profilo,self.log_name_selected,24)
        if self.free2_loaded==True:
            for widget in self.frame2.winfo_children():
                widget.destroy()
            self.frame2.pack_forget()# or frm.grid_forget() depending on whether the frame was packed or grided. #self.frame2.Destroy()
            print ("refresh frame2")
            self.frame2 = ttk.Frame(self.frame, width=self.larghezza_blocco2-10, height=self.altezza-10)
            self.frame2.grid(row = 1, column = 2, sticky = tk.NW, padx = 2) 

        label=Label(self.frame2, text="Log ultime 24 ore (click to download): " + self.log_name_selected )
        label.bind("<Double-1>", self.download_file)
        label.pack()
        self.frame2a = ttk.Frame(self.frame2,height=100)
        self.scroll2 = Scrollbar(self.frame2a)
        self.scroll2.pack(side=RIGHT, fill=Y)
        self.free2_loaded=True
        self.frame2b = ttk.Frame(self.frame2)
        #l_name= Label(self.frame2b, text="Log:" + self.log_name_selected )
        #l_name.pack()
        #l_name.bind("<Button-1>", lambda e:self.open_window_set_tag())
        self.scroll2b = Scrollbar(self.frame2b)
        self.scroll2b.pack(side=RIGHT, fill=Y)
        self.tree2b = ttk.Treeview(self.frame2b,yscrollcommand=self.scroll2b.set,height=self.altezza)
        self.tree2b['columns'] = ('Time','Nome')
        self.tree2b.column("#0", width=0,  stretch=NO)
        self.tree2b.column("Time",anchor=CENTER,width=  int(self.larghezza_blocco2/self.larghezza_blocco2_mol1))
        self.tree2b.column("Nome", width=               int(self.larghezza_blocco2/self.larghezza_blocco2_mol2))
        self.tree2b.heading("#0",text="",anchor=CENTER)
        self.tree2b.heading("Time",text="Time",anchor=CENTER)
        self.tree2b.heading("Nome",text="Nome",anchor=CENTER)
        i=0
        for riga in self.lista_log: #[e[0]['value']+" " + e[1]['value']
            self.tree2b.insert(parent='',index='end',iid=i,text='',
                    values=(str(riga[0]['value']),str(riga[1]['value']) ) )
            i=i+1
        self.tree2b.pack()
        self.frame2b.pack(side=BOTTOM)
        self.frame2.pack(side=LEFT, expand = 1)

    def download_file(self,event):
        lista_log=self.lista_log
        #print( object )
        file_dest = asksaveasfile(defaultextension = ".txt",initialfile ="log.txt")#filetypes = "log.txt", 
        print("To save file : " + file_dest.name)
        #only text files
        with open(file_dest.name, "w") as f: # https://www.codingem.com/learn-python-how-to-write-to-a-file/
            for riga in lista_log:
                f.write( str(riga[0]['value']) +" > "+ str(riga[1]['value']) ) 
                f.write("\n")
        #print (item)
        
if __name__ == '__main__':
    print("Error")