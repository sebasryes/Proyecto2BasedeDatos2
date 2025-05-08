from flask import Blueprint, request, jsonify
from app.db import db
from bson import ObjectId

menu_bp = Blueprint('menu', __name__)
menu_collection = db["articulos_menu"]

# Funciones de lógica
def insertar_articulo(data):
    resultado = menu_collection.insert_one(data)
    return str(resultado.inserted_id)

def obtener_articulos():
    return list(menu_collection.find())

def obtener_articulo_por_id(articulo_id):
    return menu_collection.find_one({"_id": ObjectId(articulo_id)})

def actualizar_articulo(articulo_id, nuevos_datos):
    resultado = menu_collection.update_one(
        {"_id": ObjectId(articulo_id)},
        {"$set": nuevos_datos}
    )
    return resultado.modified_count

def eliminar_articulo(articulo_id):
    resultado = menu_collection.delete_one({"_id": ObjectId(articulo_id)})
    return resultado.deleted_count

# Rutas
@menu_bp.route('/menu', methods=['POST'])
def crear_articulo():
    data = request.json
    try:
        id_insertado = insertar_articulo(data)
        return jsonify({"mensaje": "Artículo insertado", "id": id_insertado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/menu', methods=['GET'])
def listar_articulos():
    id_restaurante = request.args.get('restaurante')
    query = {}
    if id_restaurante:
        query["idRestaurante"] = id_restaurante

    try:
        articulos = menu_collection.find(query)
        resultado = []
        for a in articulos:
            a["_id"] = str(a["_id"])
            resultado.append(a)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@menu_bp.route('/menu/<articulo_id>', methods=['GET'])
def ver_articulo(articulo_id):
    articulo = obtener_articulo_por_id(articulo_id)
    if articulo:
        articulo["_id"] = str(articulo["_id"])
        return jsonify(articulo)
    return jsonify({"error": "Artículo no encontrado"}), 404

@menu_bp.route('/menu/<articulo_id>', methods=['PUT'])
def editar_articulo(articulo_id):
    data = request.json
    actualizados = actualizar_articulo(articulo_id, data)
    if actualizados:
        return jsonify({"mensaje": "Artículo actualizado"})
    return jsonify({"error": "No se actualizó ningún artículo"}), 404

@menu_bp.route('/menu/<articulo_id>', methods=['DELETE'])
def borrar_articulo(articulo_id):
    eliminados = eliminar_articulo(articulo_id)
    if eliminados:
        return jsonify({"mensaje": "Artículo eliminado"})
    return jsonify({"error": "No se eliminó ningún artículo"}), 404
