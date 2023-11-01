from tkinter import *
import tkinter as tk
from  tkinter import ttk
#import subprocess 
#
class ApiGatewayInstanceWindow:
    def __init__(self,frame,profilo,lista_api,lista_reso,lista_metodi,lista_dist,reload_method,to_clipboard):
        self.profilo=profilo
        self.frame=frame
        self.distribuzione={}
        self.id=''
        self.lista_api=lista_api
        self.lista_reso=lista_reso
        self.lista_metodi=lista_metodi
        self.lista_dist=lista_dist
        self.reload_method=reload_method
        self.to_clipboard=to_clipboard
        self.crea_window()

    def crea_window(self):
        #grid # https://www.geeksforgeeks.org/python-grid-method-in-tkinter/
        #grid see https://tkdocs.com/tutorial/grid.html
        self.frame.columnconfigure(2)
        self.frame1 = ttk.Frame(self.frame, width=550, height=630)
        self.frame1.grid(row = 1, column = 2, sticky = tk.W, padx = 2) 
        self.frame1.pack(side=LEFT, expand = 1)
        self.frame2 = ttk.Frame(self.frame, width=650, height=630)
        self.frame2.grid(row = 1, column = 2, sticky = tk.E, padx = 2) 
        self.frame2.pack(side=LEFT, expand = 1)
        self.scroll = Scrollbar(self.frame1)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.tree = ttk.Treeview(self.frame1,yscrollcommand=self.scroll.set,height=30)
        self.tree['columns'] = ('Nome', 'Id', 'Created')
        self.tree.column("#0", width=0,  stretch=NO)
        self.tree.column("Nome", width=200)
        self.tree.column("Id",anchor=CENTER,width=150)
        self.tree.column("Created",width=150)
        self.tree.heading("#0",text="",anchor=CENTER)
        self.tree.heading("Nome",text="Nome",anchor=CENTER)
        self.tree.heading("Id",text="Id",anchor=CENTER)
        self.tree.heading("Created",text="Created",anchor=CENTER)
        i=1
        for dis in self.lista_api:
            id=dis['id']
            nome=dis['name']
            createdDate=str(dis['createdDate'])
            self.tree.insert(parent='',index='end',iid=i,text='',
                values=(nome,id,createdDate))
            i=i+1
        self.tree.bind("<Double-1>", self.open_detail)
        self.tree.pack(side=LEFT, expand = 1)
        self.free2_loaded=False
        #return tab

    def open_detail(self, event): #(frame,profilo,lista_istanze,istanza):
        item = self.tree.selection()[0]
        api_selezionata_id = self.tree.item(item)['values'][1]
        api_selezionata={}
        for distribuzione_ciclo in self.lista_api:
            if api_selezionata_id==distribuzione_ciclo['id']:
                api_selezionata=distribuzione_ciclo
        self.api_selezionata=api_selezionata
        self.api_selezionata_id=api_selezionata_id
        if self.free2_loaded==True:
            self.frame2.pack_forget()# or frm.grid_forget() depending on whether the frame was packed or grided. #self.frame2.Destroy()
            self.frame2 = ttk.Frame(self.frame)
        Label(self.frame2, text="Id: " + api_selezionata_id ).pack()
        Label(self.frame2, text="Nome: " + api_selezionata['name'] ).pack()
        Label(self.frame2, text="(doppio click sulla risorsa per copiare l'url)" ).pack()
        #servizi
        resouce_list = self.lista_reso(self.profilo,self.api_selezionata_id)
        stage_list=self.lista_dist(self.profilo,self.api_selezionata_id) 
        #Lista risorse
        self.frame2a = ttk.Frame(self.frame2,height=100)
        self.scroll2 = Scrollbar(self.frame2a)
        self.scroll2.pack(side=RIGHT, fill=Y)
        self.free2_loaded=True
        self.tree2 = ttk.Treeview(self.frame2a,yscrollcommand=self.scroll2.set,height=15)
        self.tree2['columns'] = ('Risorsa', 'Metodo','Url')
        self.tree2.column("#0", width=0,  stretch=NO)
        self.tree2.column("Risorsa", width=150)
        self.tree2.column("Metodo",anchor=CENTER,width=80)
        self.tree2.column("Url",width=450)
        self.tree2.heading("#0",text="",anchor=CENTER)
        self.tree2.heading("Risorsa",text="Risorsa")
        self.tree2.heading("Metodo",text="Metodo",anchor=CENTER)
        self.tree2.heading("Url",text="Url",anchor=CENTER)
        i=0
        for key in resouce_list:
            if 'resourceMethods' in key:
                for metods in key['resourceMethods']:
                    url="https://" + api_selezionata_id + ".execute-api.eu-west-1.amazonaws.com/" +stage_list[0]['stageName'] + key['path']
                    self.tree2.insert(parent='',index='end',iid=i,text='',values=(key['path'],metods,url)) 
                    i=i+1
        self.tree2.bind("<Double-1>", self.copy_url)
        self.tree2.pack()
        self.frame2b = ttk.Frame(self.frame2,height=300)
        l_name= Label(self.frame2b, text="Stages")
        l_name.pack()
        #TODO click to invalidare
        #l_name.bind("<Button-1>", lambda e:self.open_window_set_tag())
        #Lista stage 
        self.scroll2b = Scrollbar(self.frame2b)
        self.scroll2b.pack(side=RIGHT, fill=Y)
        self.tree3 = ttk.Treeview(self.frame2b,yscrollcommand=self.scroll2b.set,height=10)
        self.tree3['columns'] = ('Stage', 'Chiave','Valore')
        self.tree3.column("#0", width=0,  stretch=NO)
        self.tree3.column("Stage", width=50)
        self.tree3.column("Chiave", width=150)
        self.tree3.column("Valore",anchor=CENTER,width=480)
        self.tree3.heading("#0",text="",anchor=CENTER)
        self.tree3.heading("Stage",text="Stage",anchor=CENTER)
        self.tree3.heading("Chiave",text="Chiave",anchor=CENTER)
        self.tree3.heading("Valore",text="Valore")
        i=0
        for stage in stage_list:
            for key in stage:
                self.tree3.insert(parent='',index='end',iid=i,text='',values=( stage['stageName'] ,key,str(stage[key])) )
                i=i+1
        #self.tree3.bind("<Double-1>", self.open_detail_tag)
        self.tree3.pack()
        self.frame2a.pack()
        self.frame2b.pack()
        self.frame2.pack(side=LEFT)
    
    def copy_url(self, event):
        self.to_clipboard(self.tree2,2)
        
if __name__ == '__main__':
    print("Error")