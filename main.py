from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()



# Modelo de usuario
class User(BaseModel):
    id: int
    name: str
    email: str

# Base de datos simulada
users_db: List[User] = []

# Ruta de inicio
@app.get("/")
def read_root():
    return {"status": "success", "message": "¡Bienvenido a la API de usuarios!"}

# Obtener todos los usuarios
@app.get("/users/", response_model=dict)
def get_users():
    if not users_db:
        return {
            "status": "success",
            "message": "No hay usuarios registrados.",
            "data": []
        }
    return {
        "status": "success",
        "message": "Lista de usuarios obtenida con éxito.",
        "data": users_db
    }

# Obtener un usuario por ID
@app.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return {
                "status": "success",
                "message": "Usuario encontrado.",
                "data": user
            }
    raise HTTPException(status_code=404, detail={
        "status": "error",
        "message": "Usuario no encontrado."
    })

# Crear un usuario
@app.post("/users/", response_model=dict)
def create_user(user: User):
    # Verificar si ya existe un usuario con el mismo ID
    for existing_user in users_db:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "message": "El usuario con este ID ya existe."
            })
    users_db.append(user)
    return {
        "status": "success",
        "message": "Usuario creado con éxito.",
        "data": user
    }

# Actualizar un usuario
@app.put("/users/{user_id}", response_model=dict)
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db[index] = updated_user
            return {
                "status": "success",
                "message": "Usuario actualizado con éxito.",
                "data": updated_user
            }
    raise HTTPException(status_code=404, detail={
        "status": "error",
        "message": "Usuario no encontrado."
    })

# Eliminar un usuario
@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(index)
            return {
                "status": "success",
                "message": f"Usuario con ID {user_id} eliminado con éxito."
            }
    raise HTTPException(status_code=404, detail={
        "status": "error",
        "message": "Usuario no encontrado."
    })

# Buscar usuarios por nombre
@app.get("/users/search/{name}", response_model=dict)
def search_users_by_name(name: str):
    matching_users = [user for user in users_db if name.lower() in user.name.lower()]
    if not matching_users:
        return {
            "status": "success",
            "message": "No se encontraron usuarios con ese nombre.",
            "data": []
        }
    return {
        "status": "success",
        "message": "Usuarios encontrados.",
        "data": matching_users
    }
