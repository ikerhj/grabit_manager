#-*-coding=utf-8-*-
from flask import Flask, render_template, request, json, jsonify
import os
import sys

import boto3
#sys.path.insert(1, '/grabit_ai/scripts/')
#import utils
app = Flask(__name__)

nombre_db = 'grabit_ai'
sFichero_ID_proyecto = '/grabit_ai/conf/proyecto_id.json'
nombre_columnas=[
    "id",
    "nombre",
    "tipo",
    "ruta_s3",
    "clases"
]




cluster_arn=""
secret_arn=""

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/leer_datos')
def leer_datos():
    #filas = []
    #fila = {}
    filas = []
    c = request.args.get('c','pordefecto',type=str)
    if c == "Proyecto":

        sql = "select * from proyecto where id in (22,23)"
        rdsData = boto3.client('rds-data')
        response = rdsData.execute_statement(
            resourceArn=cluster_arn,
            secretArn=secret_arn,
            database=nombre_db,
            sql=sql
        )
        # creamos un diccionario que tendra todos los datos de la query


        for i in range(len(response['records'])):
            fila = {}
            for j in range(len(response['records'][i])):
                for k, v in response['records'][i][j].items():
                    fila[nombre_columnas[j]] = v
                    # print(configuracion_deepstream)
            filas.append(fila)



        #fila["rank"] = 9
        #fila['content'] = 'Alon'
        #fila['uid'] = '5'
        #filas.append(fila)
    else:
        filas.append("joder")
    return  jsonify(result = filas)

@app.route('/input_datos', methods=['POST'])
def inputProyecto():
    proyectoID =  request.form['inputProyectoID']
    proyectoNombre = request.form['inputProyectoNombre']
    proyectoTipo = request.form['inputProyectoTipo']
    proyectoRutaS3 = request.form['inputProyectoRutaS3']
    proyectoClases = request.form['inputProyectoClases']
    sql = "insert into proyecto values ('{0}','{1}','{2}','{3}','{4}')".format(proyectoID,proyectoNombre,proyectoTipo,proyectoRutaS3,proyectoClases)
    rdsData = boto3.client('rds-data')
    response = rdsData.execute_statement(
            resourceArn = cluster_arn,
            secretArn = secret_arn,
            database = nombre_db,
            sql = sql
    )
    print(response)
    print(proyectoID,proyectoNombre,proyectoTipo,proyectoRutaS3,proyectoClases)
    return jsonify({'status':'OK'})

if __name__=="__main__":
    app.run()




