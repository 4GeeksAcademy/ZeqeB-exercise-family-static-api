"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def post_member():
    body = request.get_json(force=True)
    if 'first_name' not in body or 'age' not in body or 'lucky_numbers' not in body:
        return jsonify({'message': 'Faltan datos necesarios (first_name, age, lucky_numbers)'}), 400
    
    if not jackson_family.add_member(body):
        return jsonify({'message': "Error al registrar el miembro de la familia"}), 400
    
    return jsonify({'message': 'Miembro agregado correctamente'}), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Miembro no encontrado"}), 404

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id): 
    member = jackson_family.get_member(member_id)
    if member:
        jackson_family.delete_member(member_id)
        return jsonify({'done': True}), 200 
    else:
        return jsonify({'message': 'Miembro de la familia no encontrado'}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
