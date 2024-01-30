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
import sdk.dynamodb as AWSDynamoDB
import sdk.rds as AWSRds
import sdk.elastic_ip as AWSElasticIP
import sdk.glue_job as AWSGlueJob
import sdk.sns as AWSSnsJob
import sdk.sqs as AWSSqs
import window.ec2_instances as w_ec2_instances
import window.s3_bucket as w_s3_bucket
import window.cloudwatch as w_cloudwatch
import window.cloudfront as w_cloudfront
import window.stepfunctions as w_stepfunctions
import window.eventbridge as w_eventBridge
import window.ssm_parameters as w_ssm_parameters 
import window.apigateway as w_apigateway 
import window.dynamodb as w_dynamodb 
import window.rds as w_rds
import window.elastic_ip as w_elastic_ip
import window.glue_job as w_glue_job
import window.sns as w_sns
import window.sqs as w_sqs
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
        self.status.set( str(text) )

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
        self.frame1=tk.Frame(root,width=self.larghezza-25,height=self.altezza-25,bg="#EEEEEE")
        self.status = StatusBar(self.frame1, self.profilo)
        self.frame1.grid(row=0,column=0)
        #tabs window
        self.tabs = ttk.Notebook(self.frame1, width=self.larghezza-30, height=self.altezza-30)
        self.tabs.pack(fill=BOTH, expand=TRUE)
        for e in self.lista_funzionalita:
            e_frame= ttk.Frame(self.tabs)
            self.tabs.add(e_frame , text=e['title'] ) #self.tabs.add(self.frameT_elastic_ip, text="Elastic IP")
            self.add_text_to_frame(e_frame,e['desc']+ " " + self.profilo) #self.add_text_to_frame(self.frameT_elastic_ip,"Elastic IP "+self.profilo)
            e['metodo'](self,frame=e_frame) #self.load_elastic_ip_window(self.frameT_elastic_ip)
            self.tabs.pack(expand=1, fill="both")

#PROFILE
    def load_profile(self,root,profilo):
        self.main_frame(root,profilo)
#S3
    def load_s3_instance_window(self,frame): #,bucket,path
        frame.pack_propagate(False)
        w_s3_bucket.BucketInstanceWindow(frame,self.profilo,self.configuration
            ,AwsBucket.bucket_list(self.profilo)
            ,AwsBucket.object_list_paginator
            ,AwsBucket.content_object_text
            ,AwsBucket.content_object_presigned
            ,AwsBucket.write_file #write_test_file
            ,self.reload_s3_instance_window,"","" ) #, bucket,path
    def reload_s3_instance_window(self,frame):#print ("reload_s3_instance_window")
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_s3_instance_window(frame)
#EC2
    def load_ec2_instance_window(self,frame):
        frame.pack_propagate(False)
        w_ec2_instances.Ec2InstanceWindow(frame,self.profilo
            ,AwsInstances.get_lista_istanze(self.profilo)
            ,AwsInstances.set_tag
            ,AwsInstances.stop_instance
            ,AwsInstances.start_instance
            ,self.reload_ec2_instance_window )
    def reload_ec2_instance_window(self,frame):#print ("reload_ec2_instance_window")
        for widget in frame.winfo_children():
            widget.destroy()
        #self.frame2b.pack_forget() # or frm.grid_forget() depending on whether the frame was packed or grided. #self.frame2.Destroy()
        #self.frame2b = ttk.Frame(self.tabs)
        self.load_ec2_instance_window(frame)
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
#DYNAMO
    def load_dynamodb_window(self,frame):
        frame.pack_propagate(False)
        w_dynamodb.DynamoDBInstanceWindow(frame,self.profilo,
            AWSDynamoDB.table_list(self.profilo),
            AWSDynamoDB.full_scan_table,
            AWSDynamoDB.write_element_with_id,
            AWSDynamoDB.delete_element_by_id,
            self.reload_dynamodb_window , self.list_to_clipboard)
    def reload_dynamodb_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_dynamodb_window(frame)
#RDS load_rds_window(self.frameT_rds)
    def load_rds_window(self,frame):
        frame.pack_propagate(False)
        w_rds.RDSInstanceWindow(frame,self.profilo,
            AWSRds.db_instances_list(self.profilo),
            self.reload_rds_window , self.list_to_clipboard)
    def reload_rds_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_rds_window(frame)

#ElasticCIP load_rds_window(self.frameT_rds)
    def load_elastic_ip_window(self,frame):
        frame.pack_propagate(False)
        w_elastic_ip.ElasticIpInstanceWindow(frame,self.profilo,
            AWSElasticIP.get_elastic_addresses(self.profilo),
            self.reload_elastic_ip_window , self.list_to_clipboard)
    def reload_elastic_ip_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_elastic_ip_window(frame)

#GLUE JOB
    def load_glue_job_window(self,frame):
        frame.pack_propagate(False)
        w_glue_job.GlueJobWindow(frame,self.profilo,"",#selezionato,lista,dettaglio,esecuzioni,ececusione_dett,esegui,reload_method)
            AWSGlueJob.jobs_list(self.profilo),
            AWSGlueJob.job_detail,
            AWSGlueJob.job_execution_list,
            AWSGlueJob.job_execution_detail,
            AWSGlueJob.job_start,
            self.reload_glue_job_window )
    def reload_glue_job_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_glue_job_window(frame)

#SNS
    def load_sns_window(self,frame):
        frame.pack_propagate(False)
        w_sns.SnsWindow(frame,self.profilo,"",#selezionato,lista,dettaglio,esecuzioni,ececusione_dett,esegui,reload_method)
            AWSSnsJob.get_sns_list(self.profilo),
            AWSSnsJob.get_subscriptions,
            AWSSnsJob.publish,
            self.reload_sns_window )
    def reload_sns_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_sns_window(frame)
#SQS
    def load_sqs_window(self,frame):
        frame.pack_propagate(False)
        w_sqs.SQSWindow(frame,self.profilo,"",#selezionato,lista,dettaglio,esecuzioni,ececusione_dett,esegui,reload_method)
            AWSSqs.get_sns_list(self.profilo),
            AWSSqs.get_queue,
            AWSSqs.send_queue_message,
            AWSSqs.receive_queue_messages,
            AWSSqs.delete_queue_message,
            self.reload_sqs_window )
    def reload_sqs_window(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
        self.load_sqs_window(frame)

# lista_funzionalita
    lista_funzionalita=[ 
            {'title':'EC2','desc':'Lista istanze EC2 del profilo','metodo':load_ec2_instance_window}
            ,{'title':'S3','desc':'Lista bucket S3 del profilo','metodo':load_s3_instance_window}
            ,{'title':'CloudWatch','desc':'Lista CloudWatch del profilo','metodo':load_cloudwatch_window}
            ,{'title':'CloudFront','desc':'Lista CloudFront del profilo','metodo':load_cloudfront_window}
            ,{'title':'StepFunction','desc':'Lista StepFunction del profilo','metodo':load_stepfunction_window}
            ,{'title':'EventBridge','desc':'Lista EventBridge del profilo','metodo':load_eventBridge_window}
            ,{'title':'SSM parameter','desc':'Lista SSM parameter del profilo','metodo':load_ssmParameter_window}
            ,{'title':'Api gateway','desc':'Lista API del profilo','metodo':load_apiGateway_window}
            ,{'title':'DynamoDB','desc':'Lista tabelle dynamo del profilo','metodo':load_dynamodb_window}
            ,{'title':'RDS','desc':'Lista database RDS del profilo','metodo':load_rds_window}
            ,{'title':'Elastic IP','desc':'Lista Elastic IP del profilo','metodo':load_elastic_ip_window}
            ,{'title':'Glue Job','desc':'Lista job di Glue','metodo':load_glue_job_window}
            ,{'title':'SNS','desc':'Lista topic SNS','metodo':load_sns_window}
            ,{'title':'SQS','desc':'Lista code SQS','metodo':load_sqs_window}
        ]
    
#MAIN
#MAIN
#MAIN AwsPyConsole
if __name__ == '__main__':
    try:
        config = yaml.safe_load(open("./config.yaml"))
    except: 
        try:
            config = yaml.safe_load(open("C:\\temp\\configConsole.yaml"))
        except: 
            print("Nessun file di configurazione")
            config = {}
    #print(config)
    AwsPyConsole(config)
