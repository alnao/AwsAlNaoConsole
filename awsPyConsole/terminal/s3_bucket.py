#import numpy as np

class BucketInstanceTerminal:
    profilo=""
    lista_bucket=[]
    nome_bucket_selezionato=""
    select_terminal_option=None
    load_path_method=None
    lista_files_bucket=[]
    #self.lista_o1=self.get_objects_method(self.bucket_name,"")

    def __init__(self,profilo,select_terminal_option,load_profile_method,load_path_method):
        self.profilo=profilo
        self.lista_bucket=load_profile_method(profilo)
        self.load_path_method=load_path_method
        self.select_terminal_option=select_terminal_option
        self.select_terminal_option("Selezione il bucket del profilo " + profilo
            , [e['Name'] for e in self.lista_bucket] #  np.array([[new_val[z] for z in ['stu_name', 'last_nam','skills']] for key, new_val in n.items()])
            , self.show_bucket_content)
        
    def show_bucket_content(self, nome_bucket_selezionato):
        self.nome_bucket_selezionato=nome_bucket_selezionato
        lista=self.load_path_method(nome_bucket_selezionato,"")
        self.lista_files_bucket=lista['folders']+lista['objects']
        #{'Prefix': 'datalakeCedacri/'}
        #{'Key': 'styles.css', 'LastModified': datetime.datetime(2022, 3, 8, 10, 28, 12, tzinfo=tzutc()), 'ETag': '"80a6599447a69a17ff6b7995a4801952"', 'Size': 160217, 'StorageClass': 'STANDARD'}
        self.select_terminal_option("Bucket " + self.nome_bucket_selezionato + " del profilo " + self.profilo
            ,[ e["Key"] if "Key" in e else e["Prefix"] for e in self.lista_files_bucket ]
                #.append({"Key" : "Alla lista dei bucket"})
            ,self.show_path_content                       
        )

    def show_path_content(self, nome_path):
        print(nome_path)
        #TODO

