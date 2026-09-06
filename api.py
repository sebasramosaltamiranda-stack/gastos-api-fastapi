
import sqlite3
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
load_dotenv()

conexion = sqlite3.connect("gastos.db")
cursor = conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS GASTOS(ID INTEGER PRIMARY KEY AUTOINCREMENT, DESCRIPCION TEXT, VALOR INTEGER,FECHA TEXT, CATEGORIA TEXT)")

conexion = sqlite3.connect("gastos.db")
cursor = conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS USUARIOS(ID INTEGER PRIMARY KEY AUTOINCREMENT, USUARIO TEXT UNIQUE, CONTRASEÑA_HASH TEXT)")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()


CLAVE_SECRETA = os.getenv("CLAVE_SECRETA")
ALGORITMO = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



class Gasto(BaseModel):
    descripcion: str
    valor: int
    fecha: str 
    categoria: str

class Usuario (BaseModel):
    usuario: str
    contrasena: str
    
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        usuario= payload.get("sub") 
        return usuario
    except JWTError:
        raise  HTTPException(status_code=401, detail="Token inválido o expirado")
        
def crear_token_acceso(usuario: str):
    expiracion = datetime.utcnow() + timedelta(hours=1)
    datos ={"sub": usuario, "exp": expiracion}
    token = jwt.encode(datos, CLAVE_SECRETA, algorithm=ALGORITMO)
    return token
    
    
@app.post("/registro")
def registrar_usuario(usuario: Usuario):
    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()
    hash_contrasena = pwd_context.hash(usuario.contrasena)
    cursor.execute("INSERT INTO USUARIOS(USUARIO, CONTRASEÑA_HASH) VALUES (?,?)",(usuario.usuario, hash_contrasena))
    conexion.commit()
    return{"mensaje": "TE HAS REGISTRADO CORRECTAMENTE"}

@app.post("/login")
def login(usuario: Usuario):
    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM USUARIOS WHERE USUARIO = ?", (usuario.usuario,))
    resultado = cursor.fetchone()
    if resultado is None:
        return {"mensaje": "usuario no encontrado"}
    contrasena_correcta = pwd_context.verify(usuario.contrasena, resultado[2])
    if not contrasena_correcta :
        return {"mensaje": "contraseña incorrecta"}
    token_creado = crear_token_acceso(usuario.usuario)
    return{"mensaje": "inicio de sesión exitoso", "token": token_creado}
    
    
    
@app.get("/gastos")
def mostrar_gastos(token: str = Depends(verificar_token)):
    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM GASTOS")
    resultados = cursor.fetchall()
    return {"gastos": resultados}

@app.post("/gastos")
def agregar_gasto(gasto: Gasto, token: str = Depends(verificar_token)):
    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO GASTOS(DESCRIPCION, VALOR, FECHA, CATEGORIA) VALUES (?,?,?,?)",(gasto.descripcion, gasto.valor, gasto.fecha, gasto.categoria,))
    conexion.commit()
    return {"mensaje": "Gasto agregado correctamente"}
@app.put("/gastos/{id}")
def Actualizar_gasto(id: int, gasto: Gasto, token: str = Depends(verificar_token)   ):
    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE GASTOS SET DESCRIPCION = ?, VALOR= ?, FECHA= ?, CATEGORIA= ? WHERE ID= ?", (gasto.descripcion, gasto.valor, gasto.fecha, gasto.categoria, id ))
    conexion.commit()
    return {"mensaje": "Gasto actualizado correctamente"}
@app.delete("/gastos/{id}")
def eliminar_gasto(id: int, token: str = Depends(verificar_token)):
    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM GASTOS WHERE ID = ?", (id,))
    conexion.commit()
    return {"mensaje": "Gasto eliminado correctamente"}