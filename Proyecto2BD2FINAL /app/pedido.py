# from app.db import db
# from bson import ObjectId

# pedidos_collection = db["pedido"]

# def insertar_pedido(data):
#     resultado = pedidos_collection.insert_one(data)
#     return str(resultado.inserted_id)

# def obtener_pedidos():
#     return list(pedidos_collection.find())

# def obtener_pedido_por_id(pedido_id):
#     return pedidos_collection.find_one({"_id": ObjectId(pedido_id)})

# def actualizar_pedido(pedido_id, nuevos_datos):
#     resultado = pedidos_collection.update_one(
#         {"_id": ObjectId(pedido_id)},
#         {"$set": nuevos_datos}
#     )
#     return resultado.modified_count

# def eliminar_pedido(pedido_id):
#     resultado = pedidos_collection.delete_one({"_id": ObjectId(pedido_id)})
#     return resultado.deleted_count

from flask import Blueprint, request, jsonify
from app.db import db
from bson import ObjectId

pedido_bp = Blueprint('pedido', __name__)
pedidos_collection = db["pedido"]

# Funciones de lógica
def insertar_pedido(data):
    resultado = pedidos_collection.insert_one(data)
    return str(resultado.inserted_id)

def obtener_pedidos():
    return list(pedidos_collection.find())

def obtener_pedido_por_id(pedido_id):
    return pedidos_collection.find_one({"_id": ObjectId(pedido_id)})

def actualizar_pedido(pedido_id, nuevos_datos):
    resultado = pedidos_collection.update_one(
        {"_id": ObjectId(pedido_id)},
        {"$set": nuevos_datos}
    )
    return resultado.modified_count

def eliminar_pedido(pedido_id):
    resultado = pedidos_collection.delete_one({"_id": ObjectId(pedido_id)})
    return resultado.deleted_count

# Endpoints
@pedido_bp.route('/pedido', methods=['POST'])
def crear_pedido():
    data = request.json
    try:
        id_insertado = insertar_pedido(data)
        return jsonify({"mensaje": "Pedido agregado", "id": id_insertado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pedido_bp.route('/pedido', methods=['GET'])
def listar_pedidos():
    try:
        pedidos = obtener_pedidos()
        for p in pedidos:
            p["_id"] = str(p["_id"])
        return jsonify(pedidos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# def listar_pedidos():
#     try:
#         pedidos = list(pedidos_collection.find().sort("FechaDePedido", -1).limit(1))
#         for p in pedidos:
#             p["_id"] = str(p["_id"])
#         return jsonify(pedidos)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@pedido_bp.route('/pedido/<pedido_id>', methods=['GET'])
def ver_pedido(pedido_id):
    pedido = obtener_pedido_por_id(pedido_id)
    if pedido:
        pedido["_id"] = str(pedido["_id"])
        return jsonify(pedido)
    return jsonify({"error": "Pedido no encontrado"}), 404

@pedido_bp.route('/pedido/<pedido_id>', methods=['PUT'])
def editar_pedido(pedido_id):
    data = request.json
    actualizados = actualizar_pedido(pedido_id, data)
    if actualizados:
        return jsonify({"mensaje": "Pedido actualizado"})
    return jsonify({"error": "No se actualizó ningún pedido"}), 404

@pedido_bp.route('/pedido/<pedido_id>', methods=['DELETE'])
def borrar_pedido(pedido_id):
    eliminados = eliminar_pedido(pedido_id)
    if eliminados:
        return jsonify({"mensaje": "Pedido eliminado"})
    return jsonify({"error": "No se eliminó ningún pedido"}), 404


@pedido_bp.route('/pedidos', methods=['GET'])
def obtener_pedidos_usuario():
    id_usuario = request.args.get("usuario")
    query = {}
    if id_usuario:
        query["IdUsuario"] = id_usuario

    pedidos = pedidos_collection.find(query)
    resultado = []
    for p in pedidos:
        p["_id"] = str(p["_id"])
        resultado.append(p)
    return jsonify(resultado)
