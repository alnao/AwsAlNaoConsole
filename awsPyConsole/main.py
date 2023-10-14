import tkinter as tk
from tkinter import *
import window.menu as menu
import sdk.profiles as AwsProfiles
import sdk.ec2_instances as AwsInstances
import sdk.s3_bucket as AwsBucket
import sdk.cloudwatch as AwsCloudwatch
import window.ec2_instances as w_ec2_instances
import window.s3_bucket as w_s3_bucket
import window.cloudwatch as w_cloudwatch
from tkinter import Label
from tkinter import Label
from tkinter import ttk
import yaml

#see example tk https://realpython.com/python-gui-tkinter/

class AwsPyConsole:
    larghezza=1500
    altezza=700
    def __init__(self,configuration):
        self.profilo='default'
        self.root = tk.Tk()
        self.configuration=configuration
        # Create window
        self.root.title('Aws Py Console')
        x=0 #ex 10 ex root.winfo_screenwidth() // 6
        y=0 #ex 10 ex int(root.winfo_screenheight() * 0.1)
        self.root.geometry (''+str(self.larghezza)+'x'+str(self.altezza)+'+' + str(x) + "+" + str(y) ) #WIDTHxHEIGHT+TOP+LEFT
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
            self.frame1=tk.Frame(root,width=self.larghezza-24,height=self.altezza-24,bg="#EEEEEE")
            self.frame1.grid(row=0,column=0)
            self.add_text_to_frame(self.frame1,"Selezionare un profilo") # Label(frame1, text="Selezionare un profilo").pack()
            #frame1.pack_propagate(False)
            return
        profilo_conf={}
        profilo_con_conf=False
        for e in self.configuration:
            if e==self.profilo:
                profilo_conf=self.configuration[e]
                profilo_con_conf=True
        self.frame1=tk.Frame(root,width=self.larghezza-25,height=self.altezza-25,bg="#EEEEEE")
        self.frame1.grid(row=0,column=0)
        #tabs window
        self.tabs = ttk.Notebook(self.frame1, width=self.larghezza-30, height=self.altezza-30)
        self.tabs.pack(fill=BOTH, expand=TRUE)
        self.frameT_profile = ttk.Frame(self.tabs)
        self.frameT_ec2 = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2)
        self.frameT_s3  = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2c
        self.frameT_cloudWatch = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2e
#TABS 
        self.tabs.add(self.frameT_profile, text="Profilo " + self.profilo)
        self.add_text_to_frame(self.frameT_profile,"TODO" + self.profilo)
        self.frameT_profile.pack_propagate(False)
        self.tabs.add(self.frameT_ec2, text="Ec2")
        self.add_text_to_frame(self.frameT_ec2,"Lista istanze del profilo "+self.profilo)
        self.load_ec2_instance_window()
        self.tabs.add(self.frameT_s3, text="S3")
        self.add_text_to_frame(self.frameT_s3,"Lista bucket del profilo "+self.profilo)
        self.load_s3_instance_window(self.frameT_s3,"","")
        if profilo_con_conf:
            if 'bucket1' in profilo_conf:
                self.frameT_s3_1 = ttk.Frame(self.tabs)
                label=profilo_conf['path1'] if len(profilo_conf['path1'])>0 else profilo_conf['bucket1']
                self.tabs.add(self.frameT_s3_1, text="S3 " + label)
                self.add_text_to_frame(self.frameT_s3_1,"S3 " + label + " "+self.profilo)
                self.load_s3_instance_window(self.frameT_s3_1,profilo_conf['bucket1'],profilo_conf['path1'])
            if 'bucket2' in profilo_conf:
                self.frameT_s3_2 = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2d
                label=profilo_conf['path2'] if len(profilo_conf['path2'])>0 else profilo_conf['bucket2']
                self.tabs.add(self.frameT_s3_2, text="S3 " + label)
                self.add_text_to_frame(self.frameT_s3_2,"S3 " + label + " "+self.profilo)
                self.load_s3_instance_window(self.frameT_s3_2,profilo_conf['bucket2'],profilo_conf['path2'])
            if 'bucket3' in profilo_conf:
                self.frameT_s3_3 = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2d
                label=profilo_conf['path3'] if len(profilo_conf['path3'])>0 else profilo_conf['bucket3']
                self.tabs.add(self.frameT_s3_3, text="S3 " + label)
                self.add_text_to_frame(self.frameT_s3_3,"S3 " + label + " "+self.profilo)
                self.load_s3_instance_window(self.frameT_s3_3,profilo_conf['bucket3'],profilo_conf['path3'])
        
        self.tabs.add(self.frameT_cloudWatch, text="CloudWatch")
        self.add_text_to_frame(self.frameT_cloudWatch,"CloudWatch del profilo "+self.profilo)
        self.load_cloudwatch_instance_window(self.frameT_cloudWatch)
        self.tabs.pack(expand=1, fill="both")

#PROFILE
    def load_profile(self,root,profilo):
        self.main_frame(root,profilo)
#S3
    def load_s3_instance_window(self,frame,bucket,path):
        frame.pack_propagate(False)
        w_s3_bucket.BucketInstanceWindow(frame,self.profilo
            ,AwsBucket.bucket_list(self.profilo)
            ,AwsBucket.object_list_paginator
            ,AwsBucket.content_object_text
            ,AwsBucket.content_object_presigned
            ,AwsBucket.write_test_file
            ,self.reload_s3_instance_window , bucket,path)
    def reload_s3_instance_window(self,frame):#print ("reload_s3_instance_window")
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_s3_instance_window(frame)
#EC2
    def load_ec2_instance_window(self):
        self.frameT_ec2.pack_propagate(False)
        w_ec2_instances.Ec2InstanceWindow(self.frameT_ec2,self.profilo
            ,AwsInstances.get_lista_istanze(self.profilo)
            ,AwsInstances.set_tag
            ,AwsInstances.stop_instance
            ,AwsInstances.start_instance
            ,self.reload_ec2_instance_window )
    def reload_ec2_instance_window(self):#print ("reload_ec2_instance_window")
        for widget in self.frameT_ec2.winfo_children():
            widget.destroy()
        #self.frame2b.pack_forget() # or frm.grid_forget() depending on whether the frame was packed or grided. #self.frame2.Destroy()
        #self.frame2b = ttk.Frame(self.tabs)
        self.load_ec2_instance_window()
        #self.tabs.pack(expand=1, fill="both")
#Cloudwatch
    def load_cloudwatch_instance_window(self,frame):
        frame.pack_propagate(False)
        w_cloudwatch.CloudWatchWindow(frame,self.profilo
            , AwsCloudwatch.get_metrics(self.profilo)
            , AwsCloudwatch.get_metric_log
            ,self.reload_cloudwatch_instance_window )
    def reload_cloudwatch_instance_window(self,frame):#print ("reload_s3_instance_window")
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_cloudwatch_instance_window(frame)

#MAIN AwsPyConsole
if __name__ == '__main__':
    config = yaml.safe_load(open("./config.yaml"))
    AwsPyConsole(config)
