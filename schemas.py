### User schema ###

def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]}


def users_schema(users) -> list:
    return [user_schema(user) for user in users]

# 1. Toma el usuario tal cual sale de la base de datos de Mongo.
# 2. Agarra el horrible user["_id"], lo convierte en un texto normal con str() y lo
#    mete en una palabra limpia: "id" (sin el guion bajo).
# 3. Mapea el username y el email.
# 4. Le devuelve a FastAPI un diccionario limpio y purificado, listo para mostrar en
#    pantalla sin romper nada.

# 💡 ¿Y el users_schema con la "s" al final? Hace exactamente lo mismo, pero usando un
# bucle corto de Python (list comprehension) para traducir una lista entera de 20 o 100
# usuarios al mismo tiempo cuando usted pida ver a todos los registrados.


# Su único trabajo en la vida es agarrar el formato raro de MongoDB (con el _id) 
# y transformarlo en un diccionario limpio con "id" normal para que Python
# y el cliente lo entiendan sin problemas.

