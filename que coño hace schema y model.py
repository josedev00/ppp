# 🏗️ 1. El User Model (La aduana o el molde de entrada)
#
# Este bloque que usa Pydantic es el molde estricto que define cómo debe ser un usuario
# en su aplicación de FastAPI.
# Python
#
# class User(BaseModel):
#     id: Optional[str] = None
#     username: str
#     email: str
#
# ¿Para qué sirve?
#
# Es como el vigilante de la entrada. Cuando un usuario se vaya a registrar en su app,
# FastAPI usa este modelo para revisar que los datos estén completos antes de hacer
# cualquier otra cosa.
#
# * Si alguien intenta registrarse mandando solo el username pero se le olvida el
#   email, FastAPI frena la petición en seco y bota un error automático en rojo.
# * El id: Optional[str] = None significa: "Al principio no tenemos un ID porque el
#   usuario apenas se va a registrar, así que puede ser vacío".
#
# 🎨 2. El User Schema (El traductor o el filtro de salida)
#
# Aquí es donde entra el choque con MongoDB y por eso la gente se confunde.
# Python
#
# def user_schema(user) -> dict:
#     return {"id": str(user["_id"]),
#             "username": user["username"],
#             "email": user["email"]}
#
# ¿Para qué carajos sirve este traductor?
#
# Cuando usted guarda ese usuario en la jaula de MongoDB, Mongo (que es un bicho raro)
# le clava automáticamente un ID alfanumérico extraño en una clave llamada _id (con un
# guion bajo al principio) y envuelto en un formato especial de Mongo llamado
# ObjectId.
#
# Si usted intenta mandarle ese _id de Mongo directo a una aplicación de celular o a su
# frontend de Python, la app va a romperse porque no entiende qué es un ObjectId de
# Mongo. Solo entiende texto plano (string).
#
# Entonces, el Schema es una función traductora. Pille lo que hace línea por línea:
#
# 1. Toma el usuario tal cual sale de la base de datos de Mongo.
# 2. Agarra el horrible user["_id"], lo convierte en un texto normal con str() y lo
#    mete en una palabra limpia: "id" (sin el guion bajo).
# 3. Mapea el username y el email.
# 4. Le devuelve a FastAPI un diccionario limpio y purificado, listo para mostrar en
#    pantalla sin romper nada.
#
# 💡 ¿Y el users_schema con la "s" al final? Hace exactamente lo mismo, pero usando un
# bucle corto de Python (list comprehension) para traducir una lista entera de 20 o 100
# usuarios al mismo tiempo cuando usted pida ver a todos los registrados.
#
# 🔄 ¿Cómo trabajan en equipo dentro de su proyecto?
#
# Mírelo como una línea de ensamblaje en una fábrica:
#
# [Cliente manda datos] -> Con forma de MODELO (User) -> Procesa y guarda en Mongo
#                                                                     |
# [Cliente pide datos]  <- Filtrado por el SCHEMA (user_schema) <- Mongo devuelve (_id)
#
# * Entrada: Alguien se registra -> FastAPI revisa que cumpla el Model -> Se guarda en
#   la jaula de Docker.
# * Salida: Usted pide ver el perfil -> Mongo saca el usuario con su feo _id -> El
#   Schema lo traduce a "id" de texto plano -> Usted lo ve melo en su pantalla.
