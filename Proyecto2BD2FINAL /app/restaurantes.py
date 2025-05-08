from flask import Blueprint, request, jsonify
from app.db import db
from bson import ObjectId

restaurantes_bp = Blueprint('restaurantes', __name__)
restaurantes_collection = db["restaurantes"]

# Funciones CRUD
def insertar_restaurante(data):
    resultado = restaurantes_collection.insert_one(data)
    return str(resultado.inserted_id)

def obtener_restaurantes():
    return list(restaurantes_collection.find())

def obtener_restaurante_por_id(restaurante_id):
    try:
        # Intenta buscar como ObjectId
        _id = ObjectId(restaurante_id)
        restaurante = restaurantes_collection.find_one({"_id": _id})
        if restaurante:
            return restaurante
    except:
        pass

    # Intenta como string si ObjectId falla o no encontró nada
    return restaurantes_collection.find_one({"_id": restaurante_id})

def actualizar_restaurante(restaurante_id, nuevos_datos):
    resultado = restaurantes_collection.update_one(
        {"_id": ObjectId(restaurante_id)},
        {"$set": nuevos_datos}
    )
    return resultado.modified_count

def eliminar_restaurante(restaurante_id):
    resultado = restaurantes_collection.delete_one({"_id": ObjectId(restaurante_id)})
    return resultado.deleted_count

# Rutas (endpoints)
@restaurantes_bp.route('/restaurantes', methods=['POST'])
def crear_restaurante():
    data = request.json
    try:
        id_insertado = insertar_restaurante(data)
        return jsonify({"mensaje": "Restaurante insertado", "id": id_insertado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurantes_bp.route('/restaurantes', methods=['GET'])
def listar_restaurantes():
    try:
        restaurantes = obtener_restaurantes()
        for r in restaurantes:
            r["_id"] = str(r["_id"])
        return jsonify(restaurantes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurantes_bp.route('/restaurantes/<restaurante_id>', methods=['GET'])
def ver_restaurante(restaurante_id):
    restaurante = obtener_restaurante_por_id(restaurante_id)
    # print("\n\n\n\nRecibido ID:", restaurante_id)
    # print("Restaurante encontrado:", restaurante)
    if restaurante:
        restaurante["_id"] = str(restaurante["_id"])
        return jsonify(restaurante)
    return jsonify({"error": "Restaurante no encontrado"}), 404

@restaurantes_bp.route('/restaurantes/<restaurante_id>', methods=['PUT'])
def editar_restaurante(restaurante_id):
    data = request.json
    actualizados = actualizar_restaurante(restaurante_id, data)
    if actualizados:
        return jsonify({"mensaje": "Restaurante actualizado"})
    return jsonify({"error": "No se actualizó ningún restaurante"}), 404

@restaurantes_bp.route('/restaurantes/<restaurante_id>', methods=['DELETE'])
def borrar_restaurante(restaurante_id):
    eliminados = eliminar_restaurante(restaurante_id)
    if eliminados:
        return jsonify({"mensaje": "Restaurante eliminado"})
    return jsonify({"error": "No se eliminó ningún restaurante"}), 404

@restaurantes_bp.route("/test-db")
def test_db():
    try:
        docs = list(db.restaurantes.find())
        return jsonify({"ok": True, "total": len(docs)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500