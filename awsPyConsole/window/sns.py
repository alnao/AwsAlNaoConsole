from tkinter import *
import tkinter as tk
from  tkinter import ttk
import json 
from .json_viewer import JSONViewer

class SnsWindow:
    def __init__(self,frame,profilo,selezionato,lista,sottoscrizioni,send_message,reload_method):
        self.profilo=profilo
        self.frame=frame
        self.distribuzione={}
        self.id=''
        self.selezionato=selezionato
        self.lista=lista
        #self.dettaglio=dettaglio
        self.sottoscrizioni=sottoscrizioni
        self.send_message=send_message
        self.reload_method=reload_method
        self.crea_window()

    def crea_window(self):
        #grid # https://www.geeksforgeeks.org/python-grid-method-in-tkinter/
        #grid see https://tkdocs.com/tutorial/grid.html
        self.frame.columnconfigure(2)
        self.frame1 = ttk.Frame(self.frame, width=350, height=630)
        self.frame1.grid(row = 1, column = 2, sticky = tk.W, padx = 2) 
        self.frame1.pack(side=LEFT, expand = 1)
        self.frame2 = ttk.Frame(self.frame, width=550, height=630)
        self.frame2.grid(row = 1, column = 2, sticky = tk.E, padx = 2) 
        self.frame2.pack(side=LEFT, expand = 1)
        #self.frame3 = ttk.Frame(self.frame, width=350, height=630)
        #self.frame3.grid(row = 1, column = 2, sticky = tk.E, padx = 2) 
        #self.frame3.pack(side=LEFT, expand = 1)
        self.scroll = Scrollbar(self.frame1)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.tree = ttk.Treeview(self.frame1,yscrollcommand=self.scroll.set,height=50)
        self.tree['columns'] = ('TopicArn', 'Nome')
        self.tree.column("#0", width=0,  stretch=NO)
        self.tree.column("TopicArn", width=50)
        self.tree.column("Nome",width=380)
        self.tree.heading("#0",text="",anchor=CENTER)
        self.tree.heading("TopicArn",text="TopicArn",anchor=CENTER)
        self.tree.heading("Nome",text="Nome",anchor=CENTER)
        i=1
        for sm in self.lista:
            name=sm['TopicArn'].split(":")[-1]
            self.tree.insert(parent='',index='end',iid=i,text='',values=(sm['TopicArn'],name ) )
            i=i+1
        self.tree.bind("<Double-1>", self.open_detail)
        self.tree.pack(side=LEFT, expand = 1)
        self.free2_loaded=False
        #return tab

    def open_detail(self, event): #(frame,profilo,lista_istanze,istanza):
        item = self.tree.selection()[0]
        self.sns_selezionata = self.tree.item(item)['values'][0]
        self.sns_selezionata_arn=""
        for sns in self.lista:
            if sns['TopicArn']==self.sns_selezionata:
                self.sns_selezionata_arn=sns['TopicArn']
            self.dettaglio_valore=sns
        if self.sns_selezionata_arn=="":
            print("ERRORE")
            return
        
        #self.dettaglio_valore=self.dettaglio(self.profilo,self.sns_selezionata_arn)
        if self.free2_loaded==True:
            self.frame2.pack_forget()# or frm.grid_forget() depending on whether the frame was packed or grided. #self.frame2.Destroy()
            self.frame2 = ttk.Frame(self.frame)
        Label(self.frame2, text="Job: " + self.sns_selezionata ).pack()
        #Label(self.frame2, text="Stato: " + istanza['State']['Name'] ).pack()
        #if istanza['State']['Name']=='running':
        #    Button(self.frame2, text = "Stop", command=self.send_stop).pack()
        #else:
        #    Button(self.frame2, text = "Start", command=self.send_start).pack()
        self.frame2a = ttk.Frame(self.frame2,height=500)
        self.scroll2 = Scrollbar(self.frame2a)
        self.scroll2.pack(side=RIGHT, fill=Y)
        self.free2_loaded=True
        self.tree2 = ttk.Treeview(self.frame2a,yscrollcommand=self.scroll2.set,height=10)
        self.tree2['columns'] = ('Chiave', 'Valore')
        self.tree2.column("#0", width=0,  stretch=NO)
        self.tree2.column("Chiave", width=200)
        self.tree2.column("Valore",anchor=CENTER,width=580)
        self.tree2.heading("#0",text="",anchor=CENTER)
        self.tree2.heading("Chiave",text="Chiave",anchor=CENTER)
        self.tree2.heading("Valore",text="Valore",anchor=CENTER)
        i=0
        
        for key in self.dettaglio_valore:
            self.tree2.insert(parent='',index='end',iid=i,text='',
                    values=(key,self.dettaglio_valore[key]) )
            i=i+1
        self.tree2.pack()
        self.frame2b = ttk.Frame(self.frame2)
        #Button(self.frame2b, text = "Definizione", command=self.show_definition).pack()
        l_name= Label(self.frame2b, text="Sottoscrizione" )
        l_name.pack()
        #l_name.bind("<Button-1>", lambda e:self.open_window_set_tag())
        self.scroll2b = Scrollbar(self.frame2b)
        self.scroll2b.pack(side=RIGHT, fill=Y)
        self.tree3 = ttk.Treeview(self.frame2b,yscrollcommand=self.scroll2b.set,height=15)
        self.tree3['columns'] = ('Owner', 'Protocol' ,'Endpoint')
        self.tree3.column("#0", width=0,  stretch=NO)
        self.tree3.column("Owner", width=150)
        self.tree3.column("Protocol",anchor=CENTER,width=200)
        self.tree3.column("Endpoint",anchor=CENTER,width=500)
        self.tree3.heading("#0",text="",anchor=CENTER)
        self.tree3.heading("Owner",text="Owner",anchor=CENTER)
        self.tree3.heading("Protocol",text="Protocol",anchor=CENTER)
        self.tree3.heading("Endpoint",text="Endpoint",anchor=CENTER)
        i=0
        self.sottoscrizioni_list=self.sottoscrizioni(self.profilo,self.sns_selezionata_arn)
        for es in self.sottoscrizioni_list:
            self.tree3.insert(parent='',index='end',iid=i,text='',
                values=( es['Owner'] , es['Protocol'] , str(es['Endpoint']) ) )
            i=i+1
        Button(self.frame2, text = "Send message to topic", command=self.send_content_window).pack()
        self.tree3.pack()
        self.frame2a.pack()
        self.frame2b.pack()
        self.frame2.pack(side=LEFT)
    
    def send_content_window(self): #(frame,profilo,lista_istanze,istanza):
        w_tag_child=Toplevel(self.frame2) # Child window 
        w_tag_child.geometry("600x300" )#+ str(x) + "+" + str(y))  # Size of the window 
        w_tag_child.title("Set tag to " + self.sns_selezionata_arn ) #min = a if a < b else b
        self.window_modifica={}
        l = Label(w_tag_child, text =  "Testo:")
        l.grid(row = 0, column = 0, sticky = W, pady = 2)
        entry_text = tk.StringVar()
        entry_text.set( str( self.sns_selezionata_arn ) ) #e.insert( 0 , str( element[e] ) )
        en = Entry(w_tag_child,textvariable=entry_text )
        en.grid(row = 0, column = 1, padx=20, pady=2, ipadx=150 , ipady=20)
        self.window_modifica["text"]=en
        self.w_tag_child=w_tag_child
        b1 = Button(w_tag_child, text = "Send to SNS topic", command=self.send_content_exec)
        b1.grid(row = 1, column = 1, sticky = E)


    def send_content_exec(self):
        testo=self.window_modifica["text"].get()
        self.send_message(self.profilo,self.sns_selezionata_arn,testo)
        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.open_detail( event=None )
       

if __name__ == '__main__':
    print("Error")