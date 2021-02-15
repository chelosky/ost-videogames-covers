'''
BIBLIOTECAS UTILIZADAS
pandas
'''
import pandas as pd
import requests 

''' VARIABLES GLOBALES '''

url_api = "http://localhost:3500/api/"
file_path = "db-base-info.xlsx"
sheets_name = ['Videogame','Ost']

''' CARGAR INFORMACIÓN DEL EXCEL '''
print('Precargando Excel')
df_VIDEOGAMES = pd.read_excel(file_path, sheets_name[0])
df_SOUNDTRACKS = pd.read_excel(file_path, sheets_name[1])

''' VIDEOGAMES '''
print('Registrando VGs')
# Diccionario para encontrar los id en base a su nombre asociado
vgDictionary = {}
# ITERAMOS POR TODOS LOS VIDEOGAMES DEL DATAFRAME
for index, row in df_VIDEOGAMES.iterrows():
    # data to be sent to api 
    body = {'title':row['title']} 
    # VERIFICAR SI EXISTE EL VIDEOJUEGO
    r = requests.post(url = url_api + 'videogames/name', data=body)
    data = r.json() 
    if(data['videogame'] == None):
        # LO REGISTRAMOS EN EL SISTEMA, Y OBTENEMOS SU ID ASOCIADO
        body = {
                    'title':row['title'],
                    'saga':row['saga'],
                    'description':row['description'],
                    'image':row['image']
                }  
        rCreate = requests.post(url = url_api + 'videogames/', data=body)
        dataCreate = rCreate.json()
        vgDictionary[row['title']] = dataCreate['videogame']['_id']
    else:
        # YA EXISTE, ENTONCES OBTENEMOS SU ID ASOCIADO
        vgDictionary[row['title']] = data['videogame']['_id']
    print('Registrado: '+ row['title'])

''' SOUNDTRACKS '''
print('Limpiando Soundtracks')
# ELIMINAR TODOS LOS SOUNDTRACKS
rClean = requests.delete(url = url_api + 'soundtracks/clean/db')
dataClean = rClean.json()
print('Registrando Soundtracks')
print('TOTAL OST',len(df_SOUNDTRACKS))
# INGRESAR LOS SOUNDSTRACK DEL DATAFRAME
for index, row in df_SOUNDTRACKS.iterrows():
    # LO REGISTRAMOS EN EL SISTEMA, Y OBTENEMOS SU ID ASOCIADO
    body = {
                'idVideogame':vgDictionary[row['title']],
                'name':row['name'],
                'information':row['information'],
                'url':row['url']
            }  
    rCreateOST = requests.post(url = url_api + 'soundtracks/', data=body)
    dataCreateOST = rCreateOST.json()
    print('Progreso: ' +str(format(float((index+1))/float(len(df_SOUNDTRACKS)) * 100, '.2f')) + '%')
# PROCESO COMPLETADO
print('Proceso Completado')
