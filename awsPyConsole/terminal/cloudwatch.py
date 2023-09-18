class CloudWatchInstanceTerminal:
    label_lista_bucket="Torna alla lista dei bucket"
    profilo=""
    lista_metriche=[]
    metrica_selezionata=""
    select_terminal_option=None
    lista_log=[]
    #self.lista_o1=self.get_objects_method(self.bucket_name,"")

    def __init__(self,profilo,select_terminal_option,load_metric_method,load_log_method):
        self.profilo=profilo
        self.select_terminal_option=select_terminal_option
        self.load_metric_method=load_metric_method
        self.load_log_method=load_log_method
        #load metrics
        self.lista_metriche=self.load_metric_method(self.profilo)
        self.show_metric_list()

    def show_metric_list(self):
        self.select_terminal_option("CloudWatch (" + self.profilo + ")"
            , [e['Dimensions'][0]['Value'] for e in self.lista_metriche] #  np.array([[new_val[z] for z in ['stu_name', 'last_nam','skills']] for key, new_val in n.items()])
            , self.show_metric_log)

    def show_metric_log(self,nome_metric):
        lista=self.load_log_method(self.profilo,nome_metric ,24)
        self.select_terminal_option("CloudWatch (" + self.profilo + ")"
            , [e[0]['value']+" " + e[1]['value'] for e in lista] #  np.array([[new_val[z] for z in ['stu_name', 'last_nam','skills']] for key, new_val in n.items()])
            , print)
    