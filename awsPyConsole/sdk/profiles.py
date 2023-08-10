import boto3
s3 = boto3.resource('s3')

def get_lista_profili():
    lista_profili=boto3.session.Session().available_profiles
    return lista_profili

def get_lista_bucket_default():
    list=s3.buckets.all()
    return list

def main():
    print("Aws Py Console - Profiles START")
    lista_profili=get_lista_profili()
    print("------------------")
    print("lista profili:")
    for profilo in lista_profili:
        print(profilo)
    print("------------------")
    print("lista bucket:")
    for bucket in get_lista_bucket_default():
        print(bucket.name)
    print("------------------")
    print("Aws Py Console - Profiles END")

if __name__ == '__main__':
    main()


