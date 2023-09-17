#import numpy as np
from urllib import request
from tkinter.filedialog import asksaveasfile #https://www.geeksforgeeks.org/python-asksaveasfile-function-in-tkinter/

class BucketInstanceTerminal:
    label_lista_bucket="Torna alla lista dei bucket"
    profilo=""
    lista_bucket=[]
    nome_bucket_selezionato=""
    select_terminal_option=None
    load_path_method=None
    get_presigned_object_method=None
    lista_files_bucket=[]
    #self.lista_o1=self.get_objects_method(self.bucket_name,"")

    def __init__(self,profilo,select_terminal_option,load_profile_method,load_path_method,get_presigned_object_method):
        self.profilo=profilo
        self.lista_bucket=load_profile_method(profilo)
        self.load_path_method=load_path_method
        self.get_presigned_object_method=get_presigned_object_method
        self.select_terminal_option=select_terminal_option
        self.show_bucket_list()

    def show_bucket_list(self):
        self.select_terminal_option("S3 (" + self.profilo + ")"
            , [e['Name'] for e in self.lista_bucket] #  np.array([[new_val[z] for z in ['stu_name', 'last_nam','skills']] for key, new_val in n.items()])
            , self.show_bucket_content)
        
    def show_bucket_content(self, nome_bucket_selezionato):
        self.show_content(nome_bucket_selezionato,"")

    def show_path_content(self, nome_bucket_selezionato,path):
        self.show_content(nome_bucket_selezionato,path)

    def show_content(self, nome_bucket_selezionato,path):
        self.nome_bucket_selezionato=nome_bucket_selezionato
        lista=self.load_path_method(nome_bucket_selezionato,path)
        self.lista_files_bucket=lista['folders']+lista['objects'] #unisco cartelle e files in unica lista
        #{'Prefix': 'datalakeCedacri/'}
        #{'Key': 'styles.css', 'LastModified': datetime.datetime(2022, 3, 8, 10, 28, 12, tzinfo=tzutc()), 'ETag': '"80a6599447a69a17ff6b7995a4801952"', 'Size': 160217, 'StorageClass': 'STANDARD'}
        listaa=[]
        #aggiungo opzione per tornare
        if path=="":
            listaa=listaa+[{"Prefix":self.label_lista_bucket}]
        else:#cartella
            if path.count("/")>1:#
                listaa=listaa+[{"Prefix":path.replace( path.split("/")[-2] + "/" ,"")}]
            else:
                listaa=listaa+[{"Prefix":"../"}]
        listaa=listaa+self.lista_files_bucket
#TODO azione per caricare un file con U
        self.select_terminal_option("S3 (" + self.profilo + ") Bucket: " + self.nome_bucket_selezionato + " Path:" + path 
            ,[ e["Key"] if "Key" in e else e["Prefix"] for e in listaa ]
                #.append({"Key" : "Alla lista dei bucket"})
            ,self.select_path_content                       
        )

    def select_path_content(self, nome_path):
        if nome_path==self.label_lista_bucket: #opzione di tornare nella lista bucket
            self.show_bucket_list()
            return
        if nome_path=="../": #¢aso che devo tornare nella root del bucket
            self.show_path_content(self.nome_bucket_selezionato,"")
        if nome_path[-1]=="/" or nome_path=="":#cartella da aprire
            self.show_path_content(self.nome_bucket_selezionato,nome_path)
        else:
            self.download_file(nome_path)
            file_name=nome_path.split("/")[-1]
            path=nome_path.replace(file_name,"")
            self.show_path_content(self.nome_bucket_selezionato,path)

    def download_file(self,object):
        object_key=object
        file_name=object_key.split("/")[-1]
        files = [('File', file_name)]
        file_dest = asksaveasfile(filetypes = files, defaultextension = files,initialfile =file_name)
        print("To save file : " + file_dest.name)
        url=self.get_presigned_object_method(self.nome_bucket_selezionato,object_key )
        return request.urlretrieve(url, file_dest.name)
