from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

@app.route('/')
def greeting():
    return 'Amazon Prime Z'


##Example
@app.route('/DRL/resources/medicaldevice/reserved/supplier/<int:supplier_id>', methods = ['GET'])
def getAllReservedMedDevicesBySupplierId(supplier_id):
    return MedDeviceHandler().getAllReservedMedDevicesBySupplierId(supplier_id)

if __name__ == '__main__':
    app.run(debug=True)