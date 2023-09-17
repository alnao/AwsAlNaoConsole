import os
import sys
import time
from time import sleep
import sdk.profiles as AwsProfiles
import sdk.s3_bucket as AwsBucket
import terminal.s3_bucket as s3_bucket

class AwsTerminalPyConsole:
    separatore="------------------- "
    lista_profili_aws=[]
    profilo_selezionato=""
    funzioni_disponibili=["Bucket s3","Istanze Ec2"]

    def clear(self,):
        os.system('cls') # Clear screen for windows
        os.system('clear')

    def __init__(self,):
        self.lista_profili_aws=AwsProfiles.get_lista_profili()
        self.run_profiles_selection()
        print("Termine console")
# metodo per la selezione di una opzione
    def select_terminal_option(self,nome_funzione,lista_opzioni,callback_selezionato):
        while True:
            text=""
            i=0
            text=self.separatore + nome_funzione
            text=text+"\n0 : Indietro alla lista dei profili, e : exit"
            for p in lista_opzioni:
                i=i+1
                text=text+"\n"+ str(i) + " : " + str(p)
            self.scrollTxt(text)
            selection = input("\n" + self.separatore)
            if selection == "e":
                exit()
            if selection == "0":
                self.clear()
                self.run_profiles_selection()
            else:
                try:
                    index=int(selection)
                    if index<=i:
                        selezionato=lista_opzioni[index-1]
                        #print("Selezionato:" + selezionato )
                        self.clear()
                        callback_selezionato(selezionato)
                        return
                    else:
                        self.clear()
                        print("No.. non fare lo stupido, valore non ammesso: " + selection)
                except ValueError:
                    self.clear()
                    print("No.. non fare lo stupido, valore non numerico: " + selection)
#metodi per i profili
    def run_profiles_selection(self,):
        self.select_terminal_option("Seleziona il profilo",self.lista_profili_aws,self.profiles_selection)
    
    def profiles_selection(self, profilo):
        self.profilo_selezionato=profilo
        print("Profilo selezionato :" + self.profilo_selezionato)
        self.select_terminal_option("Seleziona cosa fare",self.funzioni_disponibili,self.enter_service)

    def enter_service(self,servizio_selezionato):
        if servizio_selezionato==self.funzioni_disponibili[1]:
            print("Servizio selezionato : Ec2 TODO") 
            #TODO
        if servizio_selezionato==self.funzioni_disponibili[0]:
            #print ("Servizio selezionato : S3")
            s3_bucket.BucketInstanceTerminal(
                self.profilo_selezionato,
                self.select_terminal_option,
                AwsBucket.bucket_list,
                AwsBucket.object_list_paginator,
                AwsBucket.content_object_presigned
            )     
        
    def scrollTxt(self,text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)
            
if __name__ == '__main__':
    AwsTerminalPyConsole()

