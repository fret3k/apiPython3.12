from fastapi import FastAPI
from pydantic import BaseModel

# Crear la aplicación FastAPI
app = FastAPI()

# Modelo de datos para un usuario
class User(BaseModel):
    id: int
    name: str
    email: str

# Ruta de inicio
@app.get("/")
def read_root():
    return {"message": "¡Hola,34 FastAPI!"}

# Ruta para obtener un saludo
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"¡Hola, {name}!"}

# Ruta para crear un usuario
@app.post("/users/")
def create_user(user: User):
    return {"message": "Usuario creado con éxito", "user": user}
