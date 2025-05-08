from flask import Blueprint, request, jsonify
from app.db import db
from bson import ObjectId

resena_bp = Blueprint('resena', __name__)
resenas_collection = db["reseñas"]

# Funciones CRUD
def insertar_resena(data):
    resultado = resenas_collection.insert_one(data)
    return str(resultado.inserted_id)

def obtener_resenas():
    return list(resenas_collection.find())

def obtener_resena_por_id(resena_id):
    return resenas_collection.find_one({"_id": ObjectId(resena_id)})

def actualizar_resena(resena_id, nuevos_datos):
    resultado = resenas_collection.update_one(
        {"_id": ObjectId(resena_id)},
        {"$set": nuevos_datos}
    )
    return resultado.modified_count

def eliminar_resena(resena_id):
    # Intentar eliminar usando ObjectId
    try:
        resultado = resenas_collection.delete_one({"_id": ObjectId(resena_id)})
        if resultado.deleted_count:
            return resultado.deleted_count
    except:
        pass  # Si no es un ObjectId válido, ignoramos el error

    # Intentar eliminar como string
    resultado = resenas_collection.delete_one({"_id": resena_id})
    return resultado.deleted_count

# Rutas (endpoints)
@resena_bp.route('/resenas', methods=['POST'])
def crear_resena():
    data = request.json
    try:
        id_insertado = insertar_resena(data)
        return jsonify({"mensaje": "Reseña insertada", "id": id_insertado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resena_bp.route('/resenas', methods=['GET'])
def listar_resenas():
    try:
        resenas = obtener_resenas()
        for r in resenas:
            r["_id"] = str(r["_id"])
        return jsonify(resenas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resena_bp.route('/resenas/<resena_id>', methods=['GET'])
def ver_resena(resena_id):
    resena = obtener_resena_por_id(resena_id)
    if resena:
        resena["_id"] = str(resena["_id"])
        return jsonify(resena)
    return jsonify({"error": "Reseña no encontrada"}), 404

@resena_bp.route('/resenas/<resena_id>', methods=['PUT'])
def editar_resena(resena_id):
    data = request.json
    actualizados = actualizar_resena(resena_id, data)
    if actualizados:
        return jsonify({"mensaje": "Reseña actualizada"})
    return jsonify({"error": "No se actualizó ninguna reseña"}), 404

@resena_bp.route('/resenas/<resena_id>', methods=['DELETE'])
def borrar_resena(resena_id):
    eliminados = eliminar_resena(resena_id)
    if eliminados:
        return jsonify({"mensaje": "Reseña eliminada"})
    return jsonify({"error": "No se eliminó ninguna reseña"}), 404


@resena_bp.route('/resenas/usuario/<id_usuario>', methods=['GET'])
def listar_resenas_por_usuario(id_usuario):
    try:
        resenas = resenas_collection.find({ "IdUsuario": id_usuario })
        resultado = []
        for r in resenas:
            r["_id"] = str(r["_id"])
            resultado.append(r)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

