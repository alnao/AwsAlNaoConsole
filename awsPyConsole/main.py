import tkinter as tk
from tkinter import *
import window.menu as menu
import sdk.profiles as AwsProfiles
import sdk.ec2_instances as AwsInstances
import sdk.s3_bucket as AwsBucket
import sdk.cloudwatch as AwsCloudwatch
import sdk.cloudfront as AWSCloudfront
import sdk.stepfunctions as AWSstepfunctions
import sdk.eventbridge as AWSeventBridge
import sdk.ssm_parameters as AWSSSMParameter
import sdk.apigateway as AWSAPIGateway
import window.ec2_instances as w_ec2_instances
import window.s3_bucket as w_s3_bucket
import window.cloudwatch as w_cloudwatch
import window.cloudfront as w_cloudfront
import window.stepfunctions as w_stepfunctions
import window.eventbridge as w_eventBridge
import window.ssm_parameters as w_ssm_parameters #AWSSSMParameter
import window.apigateway as w_apigateway #AWSSSMParameter
from tkinter import Label
from tkinter import Label
from tkinter import ttk
import yaml #pip install pyyaml

#see example tk https://realpython.com/python-gui-tkinter/
class StatusBar(tk.Frame):
    def __init__(self, master,profilo):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self)
        self.label.pack(side=tk.LEFT)
        self.pack(side=tk.BOTTOM, fill=tk.X)
        self.profilo=profilo
        self.label.config(text="Profilo " + self.profilo )
    def set(self, newText):
        self.label.config(text="Profilo " + self.profilo + " - " + newText)

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
        self.root.geometry (''+str(self.larghezza)+'x'+str(self.altezza+30)+'+' + str(x) + "+" + str(y) ) #WIDTHxHEIGHT+TOP+LEFT
        #get AWS profiles
        lista_profili_aws=AwsProfiles.get_lista_profili()
        #crete menu
        menu.create_menu(self.root,lista_profili_aws,self.load_profile)
        self.main_frame(self.root,lista_profili_aws[0])
        self.root.mainloop()
        
    def list_to_clipboard(self, list, index):
        item = str ( list.selection()[0] )
        text = list.item(item)['values'][index]
        self.root.clipboard_clear()
        self.root.clipboard_append(str(text))
        self.status.set(text)

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
        #profilo_conf={}
        #profilo_con_conf=False
        #for e in self.configuration:
        #    if e==self.profilo:
        #        profilo_conf=self.configuration[e]
        #        profilo_con_conf=True
        self.frame1=tk.Frame(root,width=self.larghezza-25,height=self.altezza-25,bg="#EEEEEE")
        self.status = StatusBar(self.frame1, self.profilo)
        self.frame1.grid(row=0,column=0)
        #tabs window
        self.tabs = ttk.Notebook(self.frame1, width=self.larghezza-30, height=self.altezza-30)
        self.tabs.pack(fill=BOTH, expand=TRUE)
        self.frameT_profile = ttk.Frame(self.tabs)
        self.frameT_ec2 = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2)
        self.frameT_s3  = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2c
        self.frameT_cloudWatch = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2e
        self.frameT_cloudFront = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2e
        self.frameT_stepFunctions = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2e
        self.frameT_eventBridge  = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2e
        self.frameT_ssmParameter  = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2e
        self.frameT_apigateway  = ttk.Frame(self.tabs)#.grid(row=1, columnspan=2) #frame2e
#TABS 
        #self.tabs.add(self.frameT_profile, text="Profilo " + self.profilo)
        #self.add_text_to_frame(self.frameT_profile,"TODO" + self.profilo)
        #self.frameT_profile.pack_propagate(False)
        self.tabs.add(self.frameT_ec2, text="Ec2")
        self.add_text_to_frame(self.frameT_ec2,"Lista istanze del profilo "+self.profilo)
        self.load_ec2_instance_window()
        self.tabs.add(self.frameT_s3, text="S3")
        self.add_text_to_frame(self.frameT_s3,"Lista bucket del profilo "+self.profilo)
        self.load_s3_instance_window(self.frameT_s3,"","")
        self.tabs.add(self.frameT_cloudWatch, text="CloudWatch")
        self.add_text_to_frame(self.frameT_cloudWatch,"CloudWatch del profilo "+self.profilo)
        self.load_cloudwatch_window(self.frameT_cloudWatch)
        self.tabs.add(self.frameT_cloudFront, text="CloudFront")
        self.add_text_to_frame(self.frameT_cloudFront,"CloudFront del profilo "+self.profilo)
        self.load_cloudfront_window(self.frameT_cloudFront)
        self.tabs.add(self.frameT_stepFunctions, text="StepFunctions")
        self.add_text_to_frame(self.frameT_stepFunctions,"StepFunctions del profilo "+self.profilo)
        self.load_stepfunction_window(self.frameT_stepFunctions)
        self.tabs.pack(expand=1, fill="both")
        self.tabs.add(self.frameT_eventBridge, text="EventBridge")
        self.add_text_to_frame(self.frameT_eventBridge,"EventBridge del profilo "+self.profilo)
        self.load_eventBridge_window(self.frameT_eventBridge)
        self.tabs.pack(expand=1, fill="both")
        self.tabs.add(self.frameT_ssmParameter, text="SSM Parameters")
        self.add_text_to_frame(self.frameT_ssmParameter,"SSM Parameters "+self.profilo)
        self.load_ssmParameter_window(self.frameT_ssmParameter)
        self.tabs.pack(expand=1, fill="both")
        self.tabs.add(self.frameT_apigateway, text="API Gateway")
        self.add_text_to_frame(self.frameT_apigateway,"API Gateway "+self.profilo)
        self.load_apiGateway_window(self.frameT_apigateway)
        self.tabs.pack(expand=1, fill="both")
        
#PROFILE
    def load_profile(self,root,profilo):
        self.main_frame(root,profilo)
#S3
    def load_s3_instance_window(self,frame,bucket,path):
        frame.pack_propagate(False)
        w_s3_bucket.BucketInstanceWindow(frame,self.profilo,self.configuration
            ,AwsBucket.bucket_list(self.profilo)
            ,AwsBucket.object_list_paginator
            ,AwsBucket.content_object_text
            ,AwsBucket.content_object_presigned
            ,AwsBucket.write_file #write_test_file
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
    def load_cloudwatch_window(self,frame):
        frame.pack_propagate(False)
        w_cloudwatch.CloudWatchWindow(frame,self.profilo
            , AwsCloudwatch.get_metrics(self.profilo)
            , AwsCloudwatch.get_metric_log
            ,self.reload_cloudwatch_window )
    def reload_cloudwatch_window(self,frame):#print ("reload_s3_instance_window")
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_cloudwatch_window(frame)
#CloudFront
    def load_cloudfront_window(self,frame):
        frame.pack_propagate(False)
        w_cloudfront.CloudFrontInstanceWindow(frame,self.profilo,
            AWSCloudfront.list_distributions(self.profilo),
            AWSCloudfront.get_distribution,
            AWSCloudfront.invalid_distribuzion,
            self.reload_cloudfront_window )
    def reload_cloudfront_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_cloudfront_window(frame)
#step functions
    def load_stepfunction_window(self,frame):
        frame.pack_propagate(False)
        w_stepfunctions.StepFunctionsWindow(frame,self.profilo,"",#selezionato,lista,dettaglio,esecuzioni,ececusione_dett,esegui,reload_method)
            AWSstepfunctions.state_machine_list(self.profilo),
            AWSstepfunctions.state_machine_detail,
            AWSstepfunctions.state_machine_execution,
            AWSstepfunctions.state_machine_execution_detail,
            AWSstepfunctions.state_machine_start,
            self.reload_stepfunction_window )
    def reload_stepfunction_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_stepfunction_window(frame)
#eventbridge load_eventBridge_window
    def load_eventBridge_window(self,frame):
        frame.pack_propagate(False)
        w_eventBridge.EventBridgeWindow(frame,self.profilo,"",#selezionato,lista,dettaglio,disattiva,attiva,reload_method)
            AWSeventBridge.get_lista_regole(self.profilo,""),
            AWSeventBridge.describe_rule,
            AWSeventBridge.disable_role,
            AWSeventBridge.enable_role,
            self.reload_eventBridge_window )
    def reload_eventBridge_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_eventBridge_window(frame)

#ssm_parameters #AWSSSMParameter
    def load_ssmParameter_window(self,frame): #self.load_ssmParameter_window(self.frameT_ssmParameter)
        frame.pack_propagate(False)
        w_ssm_parameters.SsmParameterInstanceWindow ( frame,self.profilo,
            AWSSSMParameter.get_parameters_by_path(self.profilo,"/"),
            AWSSSMParameter.put_parameter, #(profile_name, name, value, type, description)
            self.reload_ssmParameter_window )
    def reload_ssmParameter_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_ssmParameter_window(frame)
#API GATEWAY
    def load_apiGateway_window(self,frame):
        frame.pack_propagate(False)
        w_apigateway.ApiGatewayInstanceWindow(frame,self.profilo,
            AWSAPIGateway.api_list(self.profilo),
            AWSAPIGateway.resouce_list,
            AWSAPIGateway.method_detail,
            AWSAPIGateway.stage_list,
            self.reload_apiGateway_window , self.list_to_clipboard)
    def reload_apiGateway_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_apiGateway_window(frame)

#MAIN AwsPyConsole
if __name__ == '__main__':
    try:
        config = yaml.safe_load(open("./config.yaml"))
    except: 
        try:
            config = yaml.safe_load(open("C:\\Transito\\000_FILES\\configConsole.yaml"))
        except: 
            print("Nessun file di configurazione")
            config = {}
    #print(config)
    AwsPyConsole(config)
