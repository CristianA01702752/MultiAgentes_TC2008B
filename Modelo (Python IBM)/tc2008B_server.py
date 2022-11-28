# TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
# Python server to interact with Unity via POST
# Sergio Ruiz-Loza, Ph.D. March 2021

""" Importamos el modelo del archivo en que lo definimos. """
from retomultiagentes import RoadModel
from retomultiagentes import get_ids
from retomultiagentes import get_grid

""" Importamos los siguientes paquetes para el mejor manejo de valores
    numéricos."""
import numpy as np

from flask import Flask, request
import json, os

WIDTH = 30
HEIGHT = 1000
POSITIONS = []

model = RoadModel(WIDTH, HEIGHT)

def updatePositions():
    global model
    model.step()
    matrix = np.array(get_grid(model))
    matrix_ids = np.array(get_ids(model))
    #print(matrix)
    for x in range(WIDTH):
        for z in range(HEIGHT):
            if (matrix[x, z] != 0):
                #print(matrix[x,z])
                pos = [x, z, 0, matrix_ids[x, z]]
                POSITIONS.append(pos)
                #print(positions)

def getPositionById(id, ps):
    maxZ = 0
    pos = None
    for p in ps:
        if p[3] == id and p[1] > maxZ:
            maxZ = p[1]
            pos = p
    
    return pos


def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : p[2],
            "val" : p[3]
        }
        posDICT.append(pos)
        #print(json.dumps(posDICT))
    return json.dumps(posDICT)

app = Flask(__name__, static_url_path='')

port = int(os.getenv('PORT', 8585))

@app.route('/', methods=['GET'])
def root():
    resp = "Inicio exitoso del server"
    return resp

@app.route('/position', methods=['GET'])
def modelPosition():
    args = request.args
    id = args.get('id')
    if id is not None:
        id = float(id)
        pos = getPositionById(id, POSITIONS)
        if pos is not None:
            pos = positionsToJSON([pos])
            return pos
        else:
            resp = "Agente llego a final"
        return resp
    else:
        resp = "No se ingreso id"
        return resp

@app.route('/step', methods=['GET'])
def modelStep():
    updatePositions()
    modelPosition()
    resp = "{\"data\":" + positionsToJSON(POSITIONS) + "}"
    print(resp)
    return resp




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port, debug=True)
