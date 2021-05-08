'''
BIBLIOTECAS UTILIZADAS
pandas
'''
import pandas as pd
import requests 
from dotenv import dotenv_values

''' VARIABLES GLOBALES '''

config = dotenv_values(".env")
url_api = config['URL']
file_path = config['FILE_PATH']
access_token = config['ADMIN_TOKEN']
sheets_name = ['Videogame','Ost']
headers_token ={'Content-Type':'application/x-www-form-urlencoded','Authorization': 'Bearer {}'.format(access_token)}

''' CARGAR INFORMACIÓN DEL EXCEL '''
print('Precargando Excel')
df_VIDEOGAMES = pd.read_excel(file_path, sheets_name[0])
df_SOUNDTRACKS = pd.read_excel(file_path, sheets_name[1])

print('Limpiando Soundtracks')
# ELIMINAR TODOS LOS SOUNDTRACKS
rClean = requests.delete(url = url_api + 'soundtrack/clean/db',headers=headers_token)
dataClean = rClean.json()
print('Limpiando VGs')
# ELIMINAR TODOS LOS SOUNDTRACKS
rClean = requests.delete(url = url_api + 'videogame/clean/db',headers=headers_token)
dataClean = rClean.json()
''' VIDEOGAMES '''
print('Registrando VGs')
# Diccionario para encontrar los id en base a su nombre asociado
vgDictionary = {}
# ITERAMOS POR TODOS LOS VIDEOGAMES DEL DATAFRAME
for index, row in df_VIDEOGAMES.iterrows():
    # data to be sent to api 
    body = {'title':row['title']} 
    # VERIFICAR SI EXISTE EL VIDEOJUEGO
    r = requests.get(
            url = url_api + 'videogame/', 
            params=body,
            headers=headers_token)
    data = r.json()
    if(data['count'] == 0):
        # LO REGISTRAMOS EN EL SISTEMA, Y OBTENEMOS SU ID ASOCIADO
        body = {
                    'title':row['title'],
                    'saga':row['saga'],
                    'description':row['description'],
                    'correlative':row['correlative'],
                    'image':row['image']
                }  
        rCreate = requests.post(url = url_api + 'videogame/', data=body, headers=headers_token)
        dataCreate = rCreate.json()
        vgDictionary[row['title']] = dataCreate['videogame']['_id']
    else:
        # YA EXISTE, ENTONCES OBTENEMOS SU ID ASOCIADO
        vgDictionary[row['title']] = data['videogames'][0]['_id']
    print('Registrado: '+ row['title'])

# ''' SOUNDTRACKS '''
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
    rCreateOST = requests.post(url = url_api + 'soundtrack/', data=body,headers=headers_token)
    dataCreateOST = rCreateOST.json()
    print('Progreso: ' +str(format(float((index+1))/float(len(df_SOUNDTRACKS)) * 100, '.2f')) + '%')
# PROCESO COMPLETADO
print('Proceso Completado')
