#-*-coding=utf-8-*-

import os
import sys

import boto3
#import utils


nombre_db = 'grabit_ai'

nombre_columnas=[
    "id",
    "nombre",
    "tipo",
    "ruta_s3",
    "clases"
]

cluster_arn="arn:aws:rds:eu-west-2:936810513177:cluster:grabit"
secret_arn="arn:aws:secretsmanager:eu-west-2:936810513177:secret:rds-db-credentials/cluster-ZYD4OUSXSHYWHZJBNN4Y5ZWHZ4/admin-BXS1VO"



proyectoID =  22
proyectoNombre = "test"
proyectoTipo = "tipo test"
proyectoRutaS3 = "s3 test"
proyectoClases = "clases test"
#sql = "insert into proyecto values ('{0}','{1}','{2}','{3}','{4}')".format(proyectoID,proyectoNombre,proyectoTipo,proyectoRutaS3,proyectoClases)
sql = "select * from proyecto where id in (22,23)"
rdsData = boto3.client('rds-data')
response = rdsData.execute_statement(
            resourceArn = cluster_arn,
            secretArn = secret_arn,
            database = nombre_db,
            sql = sql
    )
#creamos un diccionario que tendra todos los datos de la query
records = []

for i in range(len(response['records'])):
    configuracion_deepstream = {}
    for j in range(len(response['records'][i])):
        for k,v in response['records'][i][j].items():
            configuracion_deepstream[nombre_columnas[j]] = v
            #print(configuracion_deepstream)
    records.append(configuracion_deepstream)

print(records)


