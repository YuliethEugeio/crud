from flask import Flask
from flask_cors import CORS
from flask import jsonify, request
import pymysql

app = Flask(__name__) 

CORS(app)

# Función para conectarse a la base de datos MySQL
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

# Ruta para consulta general del baúl de contraseñas
@app.route("/")
def consulta_general():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM baul""")
        datos = cur.fetchall()
        data = []

        for row in datos:
            dato = {'id_baul': row[0], 'Plataforma': row[1], 'usuario': row[2], 'clave': row[3]}
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baúl de contraseñas'})
    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})

# consulta individual de un registro en el baúl
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM baul where id_baul='{}'""".format(codigo))
        datos = cur.fetchone()

        cur.close()
        conn.close()
        
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

@app.route("/registro/",methods=['POST'])
def registro():
    try:
        conn=conectar('localhost','root','','gestor_contrasena')
        cur = conn.cursor()
        x=cur.execute(""" insert into baul (plataforma,usuario,clave) values \
            ('{0}','{1}','{2}')""".format(request.json['plataforma'],\
                request.json['usuario'],request.json['clave']))
        conn.commit() ## para confirmar la insercion de la informacion
        cur.close()
        conn.close()
        return jsonify({'mensaje':'registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'Error'})

@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute("""
            DELETE FROM baul WHERE id_baul=%s
        """, (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    try:
       
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()

       
        x = cur.execute("""
            UPDATE baul
            SET plataforma=%(plataforma)s, usuario=%(usuario)s, clave=%(clave)s
            WHERE id_baul=%(id_baul)s
        """, {
            'plataforma': request.json['plataforma'],
            'usuario': request.json['usuario'],
            'clave': request.json['clave'],
            'id_baul': codigo
        })

        # Confirmar los cambios
        conn.commit()
        cur.close()
        conn.close()

       
        return jsonify({'mensaje': 'Registro Actualizado'})

    except Exception as ex:
        
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
if __name__ == '__main__':
    app.run(debug=True)