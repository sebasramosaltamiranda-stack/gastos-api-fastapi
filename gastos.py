import sqlite3


conexion = sqlite3.connect("gastos.db")
cursor = conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS GASTOS(ID INTEGER PRIMARY KEY AUTOINCREMENT, DESCRIPCION TEXT, VALOR INTEGER,FECHA TEXT, CATEGORIA TEXT)")

conexion = sqlite3.connect("gastos.db")
cursor = conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS USUARIOS(ID INTEGER PRIMARY KEY AUTOINCREMENT, USUARIO TEXT UNIQUE, CONTRASEÑA_HASH TEXT)")