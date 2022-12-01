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
MAIN_POS = []
#TEST_SCENARIO = 0
MAIN_SPEED =[]
MAIN_VEHICLE = []


model = RoadModel(WIDTH, HEIGHT)


def return_ID(POS):
    return POS[3]

def updatePositions():
    MAIN_POS.clear()
    global model
    model.step()
    matrix = np.array(get_grid(model))
    matrix_ids = np.array(get_ids(model))
    #print(matrix)
    for x in range(WIDTH):
        for z in range(HEIGHT):
            if (matrix[x, z] != 0):
                #print(matrix[x,z])
                pos = [x, z, 0, matrix_ids[x, z], matrix[x, z]]
                MAIN_POS.append(pos)
                #print(MAIN_POS)
                

def getId(id, ps):
    pos = None
    for p in ps:
        if p[3] == id:
            pos = p
    
    return pos


def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : p[2],
            "id" : p[3],
            "s":p[4]
        }
        posDICT.append(pos)
        #print(json.dumps(posDICT))
    return json.dumps(posDICT)

#To Adquire highspeed array of the model
def getCheckPointSpeed():
    aux = 0
    MAIN_SPEED.clear()
    global model
    for i in range(3):
        for j in range(5):
             speed = [model.highwaySpeed[i][j], aux]
             MAIN_SPEED.append(speed)
             aux += 1
             #print(MAIN_SPEED)

def speedToJSON(ps):
    speDICT = []
    for p in ps:
        spe = {
            "s": int(p[0]),
            "id": p[1]
        }
        speDICT.append(spe)
        #print(json.dumps(speDICT))
    return json.dumps(speDICT)

#To Adquire vehicle array of the model
def getCheckPointVehicle():
    aux = 0
    MAIN_VEHICLE.clear()
    global model
    for i in range(3):
        for j in range(5):
             speed = [model.highwayVehicles[i][j], aux]
             MAIN_VEHICLE.append(speed)
             aux += 1
             #print(MAIN_VEHICLE)

def vehicleToJSON(ps):
    vehDICT = []
    for p in ps:
        veh = {
            "v": int(p[0]),
            "id": p[1]
        }
        vehDICT.append(veh)
        #print(json.dumps(vehDICT))
    return json.dumps(vehDICT)

def getCheckPointsID(id, arr):
    val = None
    for p in arr:
        if p[1] == id:
            val = p
    
    return val




"""
Hello World app for running Python apps on Bluemix
"""
app = Flask(__name__, static_url_path='')

port = int(os.getenv('PORT', 8585))

@app.route('/', methods=['GET'])
def root():
    resp = "Inicio exitoso del server"
    return resp

@app.route('/position', methods=['GET'])
def checkPosition():
    args = request.args
    id = args.get('id')
    if id is not None:
        id = float(id)
        
        pos = getId(id, MAIN_POS)
        if pos is not None:
            pos = positionsToJSON([pos])
            return pos
        else:
            resp = "Not created yet"
        return resp
    else:
        resp = "Error with the id ¿?"
        return resp

@app.route('/step', methods=['GET'])
def modelStep():
    updatePositions()
    sorted_pos = sorted(MAIN_POS, key=return_ID)
    checkPosition()
    #print(sorted_pos)
    resp = "{\"data\":" + positionsToJSON(sorted_pos) + "}"
    #print(resp)
    return resp

#CODE for checkpoints
@app.route('/speed', methods=['GET'])
def checkSpeed():
    args = request.args
    id = args.get('id')
    if id is not None:
        id = float(id)
        
        spe = getCheckPointsID(id, MAIN_SPEED)
        if spe is not None:
            spe = speedToJSON([spe])
            return spe
        else:
            resp = "Speedn't"
        return resp
    else:
        resp = "What did you break?"
        return resp

@app.route('/vehicle', methods=['GET'])
def checkVehicle():
    args = request.args
    id = args.get('id')
    if id is not None:
        id = float(id)
        
        veh = getCheckPointsID(id, MAIN_VEHICLE)
        if veh is not None:
            veh = vehicleToJSON([veh])
            return veh
        else:
            resp = "No vehicles?"
        return resp
    else:
        resp = "What did you break, again?"
        return resp


@app.route('/speeds', methods=['GET'])
def speedStep():
    getCheckPointSpeed()
    resp = "{\"data\":" + speedToJSON(MAIN_SPEED) + "}"
    return resp

@app.route('/vehicles', methods=['GET'])
def vehicleStep():
    getCheckPointVehicle()
    resp = "{\"data\":" + vehicleToJSON(MAIN_VEHICLE) + "}"
    return resp



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port, debug=True)


# class Server(BaseHTTPRequestHandler):

#     def _set_response(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()

#     def do_GET(self):
#         logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
#         self._set_response()
#         self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

#     def do_POST(self):
#         positions = updatePositions()
#         resp = "{\"data\":" + positionsToJSON(positions) + "}"
#         self.wfile.write(resp.encode('utf-8'))


# def run(server_class=HTTPServer, handler_class=Server, port=8585):
#     logging.basicConfig(level=logging.INFO)
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#     logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
#     try:
#         httpd.serve_forever()
#     except KeyboardInterrupt:   # CTRL+C stops the server
#         pass
#     httpd.server_close()
#     logging.info("Stopping httpd...\n")

# if __name__ == '__main__':
#     from sys import argv

#     if len(argv) == 2:
#         run(port=int(argv[1]))
#     else:
#         run()
