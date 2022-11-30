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

def take_third(POS):
    return POS[3]

def updatePositions():
    POSITIONS.clear()
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
                POSITIONS.append(pos)
                #print(POSITIONS)
                

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
        
        pos = getId(id, POSITIONS)
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
    sorted_pos = sorted(POSITIONS, key=take_third)
    checkPosition()
    #print(sorted_pos)
    resp = "{\"data\":" + positionsToJSON(sorted_pos) + "}"
    #print(resp)
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
