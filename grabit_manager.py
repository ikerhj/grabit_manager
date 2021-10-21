#-*-coding=utf-8-*-
#importamos librerias
from flask import Flask, render_template, request, json, jsonify
from datetime import datetime, date
import os
import sys
import boto3


#constantes
cluster_arn=""
secret_arn=""
nombre_db = 'grabit_ai'
nombre_columnas=[
    "id",
    "nombre",
    "tipo",
    "ruta_s3",
    "clases"
]
client =boto3.client('iotsitewise',region_name='eu-west-1') #Recordar que nuestros dispositivos estan configurados en Irlanda
#se creat la aplicacion flask
app = Flask(__name__)


############################################################## funciones de ayuda #########################################################
def insertar_datos_db(sql):
    rdsData = boto3.client('rds-data')
    response = rdsData.execute_statement(
        resourceArn=cluster_arn,
        secretArn=secret_arn,
        database=nombre_db,
        sql=sql
    )
    return response

def leer_datos_db(sql):
    rdsData = boto3.client('rds-data')
    response = rdsData.execute_statement(
        resourceArn=cluster_arn,
        secretArn=secret_arn,
        database=nombre_db,
        sql=sql
    )
    return response


# Conseguimos la lista de modelos creados en el IoT SiteWise
def conseguir_modelos():
    modelos = client.list_asset_models(
        maxResults=123
    )

    # Extraemos la informacion necesaria de los modelos para utilizarlos mas adelante
    contenido_modelos = []
    for i in modelos['assetModelSummaries']:
        info_modelos = {
            'id': i['id'],
            'arn': i['arn'],
            'name': i['name']
        }
        contenido_modelos.append(info_modelos)
    return contenido_modelos


# Conseguimos los diferentes assets que puede tener un modelo especifico
def conseguir_assets(id_modelo):
    assets = client.list_assets(
        maxResults=123,
        assetModelId=id_modelo,
        filter='ALL'
    )
    return assets


# Conseguimos toda la informacion de un asset especifico
def conseguir_asset(id_asset):
    asset = client.describe_asset(
        assetId=id_asset
    )
    return asset


# Obtenemos la informacion de una propiedad especifica de un asset
def propiedad_asset(id_asset, fecha_inicio, id_propiedad):
    dt = datetime.today()
    response = client.get_asset_property_value_history(
        assetId=id_asset,
        propertyId=id_propiedad,
        startDate=fecha_inicio,
        endDate=datetime(dt.year, dt.month, dt.day),
        timeOrdering='ASCENDING',
        maxResults=123
    )
    return response


####EXTRAER TODA LA INFORMACION DE UN ASSET####
def conseguir_info_total_asset(asset, id_asset):
    info_total_asset = []  # Donde se almacena toda la informacion obtenida de un asset

    # Repasamos todas las propiedades de un asset especifico
    for j in asset['assetProperties']:

        # Obtenemos la informacion de una propiedad especifica de un asset
        propiedad = propiedad_asset(id_asset, datetime(2020, 10, 18), j['id'])

        # Pasamos la informacion conseguida de una propiedad a una lista de diccionarios
        content = []
        for valores in propiedad['assetPropertyValueHistory']:
            info = {
                'valores': valores['value'],
                'hora': datetime.fromtimestamp(valores['timestamp']['timeInSeconds'])  # .strftime('%Y-%m-%d %H:%M:%S')
            }
            content.append(info)

        # Conseguimos una lista de diccionarios con toda la informacion recibida de cada propiedad
        propiedades = {
            'nombre': j['name'],
            'id': j['id'],
            'contenido': content
        }

        info_total_asset.append(propiedades)
    return info_total_asset

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/leer_datos')
def leer_datos():
    filas = []
    c = request.args.get('c','pordefecto',type=str)
    if c == "Proyecto":
        sql = "select * from proyecto where id in (22,23)"
        response = leer_datos_db(sql)
        # creamos un diccionario que tendra todos los datos de la query
        for i in range(len(response['records'])):
            fila = {}
            for j in range(len(response['records'][i])):
                for k, v in response['records'][i][j].items():
                    fila[nombre_columnas[j]] = v
                    # print(configuracion_deepstream)
            filas.append(fila)
    else:
        filas.append("nada")
    return  jsonify(result = filas)

@app.route('/insertar', methods=['POST'])
def insertar():

    tabla = request.form['tabla']
    if tabla == "proyecto":
        proyectoID =  request.form['inputProyectoID']
        proyectoNombre = request.form['inputProyectoNombre']
        proyectoTipo = request.form['inputProyectoTipo']
        proyectoRutaS3 = request.form['inputProyectoRutaS3']
        proyectoClases = request.form['inputProyectoClases']
        sql = "insert into proyecto values ('{0}','{1}','{2}','{3}','{4}')".format(proyectoID,proyectoNombre,proyectoTipo,proyectoRutaS3,proyectoClases)
        response = insertar_datos_db(sql)

    print(response)
    print(proyectoID,proyectoNombre,proyectoTipo,proyectoRutaS3,proyectoClases)
    return jsonify({'status':'OK'})

@app.route('/leer_datos_sideways')
def leer_datos_sideways():
    contenido_modelos = conseguir_modelos()
    modelo_elegido = contenido_modelos[1]  # Usamos el id del modelo 'SiteWise Tutorial Device Model'
    assets = conseguir_assets(modelo_elegido['id'])

    asset_elegido = assets['assetSummaries'][1]  # Usamos el id del modelo 'SiteWise Tutorial Device 3'
    asset = conseguir_asset(asset_elegido['id'])

    info_total_asset = conseguir_info_total_asset(asset, asset_elegido['id'])

    informacion_completa = {
        'model_name': modelo_elegido['name'],
        'model_id': modelo_elegido['id'],
        'asset_name': asset_elegido['name'],
        'asset_id': asset_elegido['id'],
        'info_total_asset': info_total_asset
    }

    informacion_especifica={
        'nombre_propiedad':informacion_completa['info_total_asset'][0]
        'CPU1':informacion_completa['info_total_asset'][1]
        'RAM_usage':informacion_completa['info_total_asset'][9]
        'GPU': informacion_completa['info_total_asset'][11]
        'CPU_temp':informacion_completa['info_total_asset'][12]
        'GPU_temp':informacion_completa['info_total_asset'][13]
        'thermal':informacion_completa['info_total_asset'][14]
    }
    """
    Orden de las propiedades del asset:
        nombre
        CPU 1 usage
        CPU 2 usage
        CPU 3 usage
        CPU 4 usage
        CPU 5 usage
        CPU 7 usage
        CPU 8 usage
        RAM usage
        RAM total
        GPU usage
        CPU Temp
        GPU Temp
        Thermal
        TempAO
        TempPPL
        IP
        Jetpack version
    """

    return jsonify(result=informacion_completa)

if __name__=="__main__":
    app.run()




