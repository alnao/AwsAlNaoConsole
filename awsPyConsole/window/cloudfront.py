from tkinter import *
import tkinter as tk
from  tkinter import ttk
#
class CloudFrontInstanceWindow:
    def __init__(self,frame,profilo,lista_distribuzioni,dettaglio_distribuzione,invalida_distribuzione,reload_method):
        self.lista_distribuzioni=lista_distribuzioni
        self.profilo=profilo
        self.frame=frame
        self.distribuzione={}
        self.id=''
        self.dettaglio_distribuzione=dettaglio_distribuzione
        self.invalida_distribuzione=invalida_distribuzione
        self.reload_method=reload_method
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
        self.tree['columns'] = ('Nome', 'Id', 'Stato')
        self.tree.column("#0", width=0,  stretch=NO)
        self.tree.column("Nome", width=340)
        self.tree.column("Id",anchor=CENTER,width=130)
        self.tree.column("Stato",width=80)
        self.tree.heading("#0",text="",anchor=CENTER)
        self.tree.heading("Nome",text="Nome",anchor=CENTER)
        self.tree.heading("Id",text="Id",anchor=CENTER)
        self.tree.heading("Stato",text="Stato",anchor=CENTER)
        i=1
        for dis in self.lista_distribuzioni:
            id=dis['Id']
            nome=dis['Origins']['Items'][0]['DomainName']
            stato=dis['Status']

            self.tree.insert(parent='',index='end',iid=i,text='',
                values=(nome,id,stato))
            i=i+1
        self.tree.bind("<Double-1>", self.open_detail)
        self.tree.pack(side=LEFT, expand = 1)
        self.free2_loaded=False
        #return tab

    def open_detail(self, event): #(frame,profilo,lista_istanze,istanza):
        item = self.tree.selection()[0]
        id_distribuzione = self.tree.item(item)['values'][1]
        distribuzione={}
        nome=''
        stato=''
        for distribuzione_ciclo in self.lista_distribuzioni:
            if id_distribuzione==distribuzione_ciclo['Id']:
                distribuzione=distribuzione_ciclo
                stato=distribuzione['Status']
                nome=distribuzione['Origins']['Items'][0]['DomainName']
        self.distribuzione=distribuzione
        self.id=id_distribuzione
        if self.free2_loaded==True:
            self.frame2.pack_forget()# or frm.grid_forget() depending on whether the frame was packed or grided. #self.frame2.Destroy()
            self.frame2 = ttk.Frame(self.frame)
        Label(self.frame2, text="Id: " + id_distribuzione ).pack()
        Label(self.frame2, text="Stato: " + stato ).pack()
        Label(self.frame2, text="Nome: " + nome ).pack()

        self.frame2a = ttk.Frame(self.frame2,height=100)
        self.scroll2 = Scrollbar(self.frame2a)
        self.scroll2.pack(side=RIGHT, fill=Y)
        self.free2_loaded=True
        self.tree2 = ttk.Treeview(self.frame2a,yscrollcommand=self.scroll2.set,height=15)
        self.tree2['columns'] = ('Chiave', 'Valore')
        self.tree2.column("#0", width=0,  stretch=NO)
        self.tree2.column("Chiave", width=200)
        self.tree2.column("Valore",anchor=CENTER,width=480)
        self.tree2.heading("#0",text="",anchor=CENTER)
        self.tree2.heading("Chiave",text="Chiave",anchor=CENTER)
        self.tree2.heading("Valore",text="Valore",anchor=CENTER)
        i=0
        for key in distribuzione:
            self.tree2.insert(parent='',index='end',iid=i,text='',
                    values=(key,distribuzione[key]) )
            i=i+1
        self.tree2.pack()
        self.frame2b = ttk.Frame(self.frame2,height=300)
        l_name= Label(self.frame2b, text="Origine")
        l_name.pack()
        #TODO click to invalidare
        #l_name.bind("<Button-1>", lambda e:self.open_window_set_tag())
        self.scroll2b = Scrollbar(self.frame2b)
        self.scroll2b.pack(side=RIGHT, fill=Y)
        self.tree3 = ttk.Treeview(self.frame2b,yscrollcommand=self.scroll2b.set,height=10)
        self.tree3['columns'] = ('Chiave', 'Valore')
        self.tree3.column("#0", width=0,  stretch=NO)
        self.tree3.column("Chiave", width=200)
        self.tree3.column("Valore",anchor=CENTER,width=480)
        self.tree3.heading("#0",text="",anchor=CENTER)
        self.tree3.heading("Chiave",text="Chiave",anchor=CENTER)
        self.tree3.heading("Valore",text="Valore",anchor=CENTER)
        i=0
        for valore in distribuzione['Origins']['Items'][0]:
            self.tree3.insert(parent='',index='end',iid=i,text='',
                    #values=( str(valore['Key']),str(valore['Value'])) )
                values=( str(valore),distribuzione['Origins']['Items'][0][valore]) )
            i=i+1
        #self.tree3.bind("<Double-1>", self.open_detail_tag)
        self.tree3.pack()
        self.frame2a.pack()
        self.frame2b.pack()
        self.frame2.pack(side=LEFT)
    

if __name__ == '__main__':
    print("Error")