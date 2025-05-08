from flask import Blueprint, request, jsonify
from app.db import db
from bson import ObjectId

usuario_bp = Blueprint('usuarios', __name__)
usuarios_collection = db["usuarios"]

# Funciones CRUD
def insertar_usuario(usuario):
    resultado = usuarios_collection.insert_one(usuario)
    return str(resultado.inserted_id)

def obtener_usuarios():
    return list(usuarios_collection.find())

def obtener_usuario_por_id(usuario_id):
    return usuarios_collection.find_one({"_id": ObjectId(usuario_id)})

def actualizar_usuario(usuario_id, nuevos_datos):
    resultado = usuarios_collection.update_one(
        {"_id": ObjectId(usuario_id)},
        {"$set": nuevos_datos}
    )
    return resultado.modified_count

def eliminar_usuario(usuario_id):
    resultado = usuarios_collection.delete_one({"_id": ObjectId(usuario_id)})
    return resultado.deleted_count

def validar_credenciales(nombre_de_usuario, contrasena):
    return usuarios_collection.find_one({
        "nombre_de_usuario": nombre_de_usuario,
        "contrasena": contrasena
    })

# Rutas (endpoints)
@usuario_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    try:
        id_insertado = insertar_usuario(data)
        return jsonify({"mensaje": "Usuario insertado", "id": id_insertado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = obtener_usuarios()
        for u in usuarios:
            u["_id"] = str(u["_id"])
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario_bp.route('/usuarios/<usuario_id>', methods=['GET'])
def ver_usuario(usuario_id):
    usuario = obtener_usuario_por_id(usuario_id)
    if usuario:
        usuario["_id"] = str(usuario["_id"])
        return jsonify(usuario)
    return jsonify({"error": "Usuario no encontrado"}), 404

@usuario_bp.route('/usuarios/<usuario_id>', methods=['PUT'])
def editar_usuario(usuario_id):
    data = request.json
    actualizados = actualizar_usuario(usuario_id, data)
    if actualizados:
        return jsonify({"mensaje": "Usuario actualizado"})
    return jsonify({"error": "No se actualizó ningún usuario"}), 404

@usuario_bp.route('/usuarios/<usuario_id>', methods=['DELETE'])
def borrar_usuario(usuario_id):
    eliminados = eliminar_usuario(usuario_id)
    if eliminados:
        return jsonify({"mensaje": "Usuario eliminado"})
    return jsonify({"error": "No se eliminó ningún usuario"}), 404

@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    nombre = data.get("nombre_de_usuario")
    contra = data.get("contrasena")

    usuario = usuarios_collection.find_one({
        "nombre_de_usuario": nombre,
        "contrasena": contra
    })

    if usuario:
        return jsonify({
            "id": str(usuario["_id"]),
            "nombre": usuario["nombre"],
            "mensaje": "Login exitoso"
        })
    else:
        return jsonify({ "error": "Credenciales inválidas" }), 401