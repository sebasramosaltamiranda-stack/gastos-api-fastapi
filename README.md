# Gastos API

API REST para gestión de gastos personales, construida con FastAPI y SQLite, con operaciones completas de crear, leer, actualizar y eliminar gastos (CRUD), además de un sistema de autenticación con usuarios, contraseñas hasheadas y tokens JWT.

Este proyecto es el segundo de una serie donde fui subiendo de nivel paso a paso: el primero (to-do list) cubrió la lógica de un CRUD básico; este segundo agrega seguridad real — nada de contraseñas en texto plano, endpoints protegidos que exigen un token válido, y además está desplegado en internet, accesible desde cualquier lugar.

## 🌐 Proyecto en vivo

La API está desplegada en Render y accesible públicamente:

**https://gastos-api-3wyj.onrender.com/docs**

Desde ahí se puede ver la documentación interactiva y probar los endpoints de registro y login directamente en el navegador, sin instalar nada. Los endpoints de `/gastos` requieren un token (ver sección de Autenticación más abajo), así que para probarlos completos se recomienda una herramienta como Postman.

## Tecnologías usadas

- **Python** — lenguaje
- **FastAPI** — framework para construir la API
- **Uvicorn** — servidor que ejecuta la aplicación
- **SQLite** — base de datos
- **Pydantic** — validación de los datos que llegan a la API
- **Passlib (bcrypt)** — hasheo seguro de contraseñas
- **python-jose** — creación y verificación de tokens JWT
- **python-dotenv** — manejo de variables de entorno (la clave secreta nunca queda escrita en el código)
- **Render** — plataforma de despliegue

## Instalación y uso local

1. Instalar las librerías necesarias:
   ```
   pip install -r requirements.txt
   ```

2. Crear un archivo `.env` en la raíz del proyecto con:
   ```
   CLAVE_SECRETA=tu-clave-secreta-aqui
   ```

3. Correr el servidor:
   ```
   python -m uvicorn api:app --reload
   ```

4. Abrir en el navegador para ver y probar los endpoints:
   ```
   http://127.0.0.1:8000/docs
   ```

## Endpoints disponibles

- `POST /registro` — Crea un usuario nuevo (la contraseña se guarda hasheada, nunca en texto plano)
- `POST /login` — Verifica usuario y contraseña, y devuelve un token JWT si son correctos
- `GET /gastos` — Muestra todos los gastos (requiere token)
- `POST /gastos` — Agrega un gasto nuevo (requiere token)
- `PUT /gastos/{id}` — Actualiza un gasto existente (requiere token)
- `DELETE /gastos/{id}` — Elimina un gasto (requiere token)

### Cómo probar los endpoints protegidos

1. Hacer `POST /registro` con un usuario y contraseña.
2. Hacer `POST /login` con esas mismas credenciales. La respuesta incluye un token.
3. En Postman (u otra herramienta similar), agregar un header:
   ```
   Authorization: Bearer <el token que devolvió el login>
   ```
4. Con ese header, cualquier petición a `/gastos` funciona normalmente. Sin él, devuelve un error 401.

## Qué aprendí

Este proyecto fue mi primera vez implementando autenticación real en un backend, y también mi primera vez desplegando algo en un servidor real. Aprendí:

- Por qué nunca se debe guardar una contraseña en texto plano, y cómo hashearla con bcrypt.
- Qué es un token JWT, para qué sirve y cómo generarlo y verificarlo.
- A usar `Depends` de FastAPI para proteger endpoints, exigiendo un token válido antes de ejecutarlos.
- A probar una API con Postman: peticiones POST con body en JSON, y tokens en el header `Authorization`.
- Por qué una clave secreta nunca debe quedar escrita directamente en el código, y cómo sacarla a variables de entorno con `python-dotenv`.
- A desplegar una API en Render: `requirements.txt`, comandos de build y de inicio, variables de entorno configuradas en el propio servidor (separadas de mi `.env` local), y por qué un servidor recién desplegado arranca con una base de datos vacía si no se sube (con `CREATE TABLE IF NOT EXISTS` ejecutado al iniciar la aplicación).

Hubo debugging real en cada etapa: un bug de compatibilidad entre versiones de bcrypt y passlib, imports faltantes (`JWTError`), un despliegue que fallaba porque las tablas nunca se creaban en el servidor, y el clásico error de editar un archivo y olvidar guardarlo antes de correr o hacer commit.

## Posibles mejoras futuras

- Endpoint para sumar los gastos y compararlos contra un presupuesto mensual.
- Relacionar cada gasto con su usuario (para que cada quien vea solo sus propios gastos).
- Migrar de SQLite a una base de datos más robusta como PostgreSQL.
- Empaquetar el proyecto con Docker.
