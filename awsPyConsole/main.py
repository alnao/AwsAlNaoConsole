import tkinter as tk
from tkinter import *
import window.menu as menu
import sdk.profiles as AwsProfiles
import sdk.ec2_instances as AwsInstances
import sdk.s3_bucket as AwsBucket
import window.ec2_instances as ec2_instances
import window.s3_bucket as s3_bucket
from tkinter import Label
from tkinter import Label
from tkinter import ttk


#see example tk https://realpython.com/python-gui-tkinter/

class AwsPyConsole:
    def __init__(self,):
        self.profilo='default'
        self.root = tk.Tk()
        #strvar = StringVar(root, name ="str") #see https://www.geeksforgeeks.org/python-setting-and-retrieving-values-of-tkinter-variable/
        #root.setvar(name ="profilo_selezionato", value ="loading")#profilo_selezionato=StringVar(root,name="profilo_selezionato",value="loading")
        # Create window
        self.root.title('Aws Py Console')
        x=10#root.winfo_screenwidth() // 6
        y=10#int(root.winfo_screenheight() * 0.1)
        self.root.geometry ('1000x700+' + str(x) + "+" + str(y) ) #WIDTHxHEIGHT+TOP+LEFT
        #get AWS profiles
        lista_profili_aws=AwsProfiles.get_lista_profili()
        #crete menu
        menu.create_menu(self.root,lista_profili_aws,self.load_profile)
        self.main_frame(self.root,"")
        self.root.mainloop()
        
    def add_text_to_frame(self,frame,text):
        Label(frame, text=text).pack()
        frame.pack_propagate(False)

    def main_frame(self,root,profilo): #nota: funziona solo se c'è un iframe nella main
        self.profilo=profilo
        if self.profilo=="": #nessun profilo selezionato dal menu
            self.frame1=tk.Frame(root,width=975,height=685,bg="#EEEEEE")
            self.frame1.grid(row=0,column=0)
            self.add_text_to_frame(self.frame1,"Selezionare un profilo") # Label(frame1, text="Selezionare un profilo").pack()
            #frame1.pack_propagate(False)
            return
        self.frame1=tk.Frame(root,width=975,height=675,bg="#EEEEEE")
        self.frame1.grid(row=0,column=0)
        #tabs window
        self.tabs = ttk.Notebook(self.frame1, width=950, height=670)
        self.tabs.pack(fill=BOTH, expand=TRUE)
        self.frame2a = ttk.Frame(self.tabs)
        self.frame2b = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2)
        self.frame2c = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2)
        self.tabs.add(self.frame2a, text="Profilo " + self.profilo)
        self.add_text_to_frame(self.frame2a,"TODO" + self.profilo)
        self.frame2a.pack_propagate(False)
        self.tabs.add(self.frame2b, text="Ec2")
        self.add_text_to_frame(self.frame2b,"Lista istanze del profilo "+self.profilo)
        self.load_ec2_instance_window()
        self.tabs.add(self.frame2c, text="S3")
        self.add_text_to_frame(self.frame2c,"Lista bucket del profilo "+self.profilo)
        self.load_s3_instance_window()
        self.tabs.pack(expand=1, fill="both")
        #frame1=tk.Frame(root,width=975,height=675,bg="#EEEEEE")
        #frame1.grid(row=0,column=0)
        #l = Label(frame1, text="Profilo selezionato: " + profilo).pack()
        #frame1.pack_propagate(False)
#S3
    def load_s3_instance_window(self):
        self.frame2c.pack_propagate(False)
        s3_bucket.BucketInstanceWindow(self.frame2c,self.profilo
            ,AwsBucket.bucket_list(self.profilo)
            ,AwsBucket.object_list_paginator
            ,AwsBucket.content_object_text
            ,AwsBucket.content_object_presigned
            ,AwsBucket.write_test_file
            ,self.reload_s3_instance_window )
    def reload_s3_instance_window(self):#print ("reload_s3_instance_window")
        for widget in self.frame2c.winfo_children():
            widget.destroy()
        self.load_s3_instance_window()
#EC2
    def load_ec2_instance_window(self):
        self.frame2b.pack_propagate(False)
        ec2_instances.Ec2InstanceWindow(self.frame2b,self.profilo
            ,AwsInstances.get_lista_istanze(self.profilo)
            ,AwsInstances.set_tag
            ,AwsInstances.stop_instance
            ,AwsInstances.start_instance
            ,self.reload_ec2_instance_window )
    def reload_ec2_instance_window(self):#print ("reload_ec2_instance_window")
        for widget in self.frame2b.winfo_children():
            widget.destroy()
        #self.frame2b.pack_forget() # or frm.grid_forget() depending on whether the frame was packed or grided. #self.frame2.Destroy()
        #self.frame2b = ttk.Frame(self.tabs)
        self.load_ec2_instance_window()
        #self.tabs.pack(expand=1, fill="both")
#PROFILE
    def load_profile(self,root,profilo):
        self.main_frame(root,profilo)

#MAIN AwsPyConsole
if __name__ == '__main__':
    AwsPyConsole()