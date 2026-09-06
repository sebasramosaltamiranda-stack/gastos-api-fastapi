# Gastos API

API REST para gestión de gastos personales, construida con FastAPI y SQLite, con operaciones completas de crear, leer, actualizar y eliminar gastos (CRUD), además de un sistema de autenticación con usuarios, contraseñas hasheadas y tokens JWT.

Este proyecto es el segundo de una serie donde fui subiendo de nivel paso a paso: el primero (to-do list) cubrió la lógica de un CRUD básico; este segundo agrega seguridad real — nada de contraseñas en texto plano, y endpoints protegidos que exigen un token válido para poder usarse.

## Tecnologías usadas

- **Python** — lenguaje
- **FastAPI** — framework para construir la API
- **Uvicorn** — servidor que ejecuta la aplicación
- **SQLite** — base de datos
- **Pydantic** — validación de los datos que llegan a la API
- **Passlib (bcrypt)** — hasheo seguro de contraseñas
- **python-jose** — creación y verificación de tokens JWT

## Instalación y uso

1. Instalar las librerías necesarias:
   ```
   pip install fastapi uvicorn passlib[bcrypt] python-jose[cryptography]
   ```

2. Correr el servidor:
   ```
   python -m uvicorn api:app --reload
   ```

3. Abrir en el navegador para ver y probar los endpoints:
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

Los endpoints de `/gastos` exigen enviar el token obtenido en el login, en el header `Authorization: Bearer <token>`. Sin un token válido, devuelven un error 401.

## Qué aprendí

Este proyecto fue mi primera vez implementando autenticación real en un backend. Aprendí:

- Por qué nunca se debe guardar una contraseña en texto plano, y cómo hashearla con bcrypt.
- Qué es un token JWT, para qué sirve (evitar reenviar la contraseña en cada petición, y no exponer datos sensibles en la red) y cómo generarlo y verificarlo.
- A usar `Depends` de FastAPI para proteger endpoints, exigiendo un token válido antes de ejecutarlos.
- A probar una API con Postman: armar peticiones POST con body en JSON, y enviar tokens en el header `Authorization`.
- Que la sintaxis de librerías nuevas (passlib, jose) se siente menos intuitiva que el CRUD con SQL al principio, porque no hay una intuición previa a la que conectarla — pero se vuelve familiar con la repetición, igual que pasó con SQL en el proyecto anterior.

Como en el proyecto anterior, hubo debugging real en el camino: un bug de compatibilidad entre versiones de bcrypt y passlib, errores de sintaxis en SQL, imports faltantes (`JWTError`), y confusiones de tipo `Bearer <token>` mal copiado.

## Posibles mejoras futuras

- Endpoint para sumar los gastos y compararlos contra un presupuesto mensual.
- Relacionar cada gasto con su usuario (para que cada quien vea solo sus propios gastos).
- Migrar de SQLite a una base de datos más robusta como PostgreSQL.
