from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
#from sqlalchemy import create_engine

import boto3

# some_file.py
import sys
sys.path.insert(1, '/grabit_ai/scripts/')
import utils

app = Flask(__name__)
api = Api(app)

nombre_db = 'grabit_ai'
sFichero_ID_proyecto = '/grabit_ai/conf/proyecto_id.json'
nombre_columnas=[
    "id",
    "nombre",
    "tipo",
    "ruta_s3"
]

#creamos un diccionario que tendra todos los datos de la query
configuracion_deepstream = {}

#se lee el cluster_arn y secret_arn del fichero de config
proyecto_id_dict = utils.leer_parametros_configuración(sFichero_ID_proyecto)
cluster_arn = proyecto_id_dict['cluster_arn']
secret_arn = proyecto_id_dict['secret_arn']
"""
rdsData = boto3.client('rds-data')
response = rdsData.execute_statement(
            resourceArn = cluster_arn,
            secretArn = secret_arn,
            database = nombre_db,
            sql = "select * from proyecto"
        )
proyectos = {}
num_record = 0
proyectos['total']=800
proyectos['totalNoFiltered'] = 800
proyectos['rows'] = []
for record in response['records']:
    fila = {}
    i = 0
    for component in record:
        for k,v in component.items():
            fila[nombre_columnas[i]] = v
        i += 1
    proyectos['rows'].append(fila)
print(proyectos)
"""        

"""
for record in response['records']:
    proyectos[str(num_record)] = {}
    i = 0
    for component in record:
        for k, v in component.items():
            proyectos[str(num_record)][nombre_columnas[i]] = v
        i += 1
    num_record += 1

"""

class proyectos(Resource):
    def get(self):
        rdsData = boto3.client('rds-data')
        response = rdsData.execute_statement(
            resourceArn = cluster_arn,
            secretArn = secret_arn,
            database = nombre_db,
            sql = "select * from proyecto"
        )
        """
        proyectos = {}
        num_record = 0
        for record in response['records']:
            proyectos[str(num_record)] = {}
            i = 0
            for component in record:
                for k, v in component.items():
                    proyectos[str(num_record)][nombre_columnas[i]] = v
                i += 1
            num_record += 1
        """
        proyectos = {}
        num_record = 0
        proyectos['total']=800
        proyectos['totalNoFiltered'] = 800
        proyectos['rows'] = []
        for record in response['records']:
            fila = {}
            i = 0
            for component in record:
                for k,v in component.items():
                    fila[nombre_columnas[i]] = v
                i += 1
            proyectos['rows'].append(fila)
        """
        proyectos ={
          "total": 800,
          "totalNotFiltered": 800,
          "rows": [
                {
              "id": 0,
              "name": "Item 0",
              "price": "$0"
                },
                {
              "id": 1,
              "name": "Item 1",
              "price": "$1"
            }
          ]
        }
        """
        return proyectos
api.add_resource(proyectos, '/proyectos')  # Route_1
@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
"""

    def post(self):
        conn = db_connect.connect()
        last_name = request.json['LastName']
        first_name = request.json['FirstName']
        title = request.json['Title']
        reports_to = request.json['ReportsTo']
        birth_date = request.json['BirthDate']
        hire_date = request.json['HireDate']
        address = request.json['Address']
        city = request.json['City']
        state = request.json['State']
        country = request.json['Country']
        postal_code = request.json['PostalCode']
        phone = request.json['Phone']
        fax = request.json['Fax']
        email = request.json['Email']
        query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}', \
                             '{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}', \
                             '{13}')".format(last_name,first_name,title,
                                             reports_to, birth_date, hire_date, address,
                                             city, state, country, postal_code, phone, fax,
                                             email))
        return {'status': 'Nuevo empleado añadido'}
"""
