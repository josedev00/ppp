### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from models import User
from schemas import user_schema, users_schema
from client import db_client
from bson import ObjectId

router = APIRouter(
    prefix="/userdb",
    tags=["userdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# que me de todos so usuairosque ahy
@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


@router.get("/{id}")  # Path
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/")  # Query
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    # Si el email ya existe en la base de datos, frena todo y bota error
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    # Convierte el objeto de FastAPI en un diccionario normal de Python
    user_dict = dict(user)
    
    # Borra el "id: None" vacío para que Mongo pueda meter su propio '_id' sin chocar
    del user_dict["id"]
    
    # Guarda en Docker y le pide a Mongo que le devuelva SOLAMENTE el ID que se inventó
    id = db_client.users.insert_one(user_dict).inserted_id
#NOTA ESE _id simpere o cre ahci con ese ______
    # Busca el nuevo usuario en Mongo y el Schema traduce el '_id' a un "id" de texto normal
    new_user = user_schema(db_client.users.find_one({"_id": id}))# peus da el id que se envinto albase de datos 

    # Empaca los datos traducidos en el modelo 'User' (ya con su ID real) y lo manda a la pantalla
    return User(**new_user)# es un json y pues ya se vuelv eun objeto de tipo user


@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}

# Helper

# haber si existe ne la base de datos en linea 33 se usa esto
def search_user(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
    

# 1. ¿Se le cayó la jaula sola?

# A veces, si hay un error en la configuración o si la laptop se satura de memoria, el contenedor se apaga solo a los pocos segundos de prenderlo.

# Haga esta prueba rápida en la terminal para quitarse la duda:
# Bash

# sudo docker ps

#     Si le sale la lista vacía, es porque se apagó solo.

#     Si le sale en la lista, mire debajo de la columna STATUS: debe decir algo como Up X minutes.

# 3. El comodín: Reiniciar el servicio completo

# Si Docker se quedó tonto (pasa a veces cuando uno suspende la laptop), lo mejor es revivir el servicio desde la raíz. Tire estos dos comandos en orden:
# Bash

# sudo systemctl restart docker
# sudo docker start mi-mongo





# bn esto es por siiii pues no da osea se cierr ay cierra esa mrd 

# Debajo de CONTAINER ID y de NAMES no sale absolutamente nada, está en blanco.
#
# Eso significa que la jaula se apagó del todo (o nunca llegó a prenderse). Por eso a
# Python y a la extensión de VS Code les rebota la conexión con el error "Connection
# refused", porque están intentando timbrar en una casa que está vacía y con la luz
# apagada.
#
# Hagamos el tiro definitivo para dejar esto solucionado de una vez por todas y que no
# lo vuelva a joder más. Vamos a borrar ese contenedor que se quedó tonto y a crear uno
# nuevo con el truco para que se quede prendido siempre.
#
# Copie y pegue estos dos comandos en su terminal (uno por uno):
# Bash
#
# 1. Borramos la jaula vieja que está apagada y dando lidia
# sudo docker rm -f mi-mongo
#
# 2. Creamos la jaula nueva y limpia con reinicio automático obligatorio
# sudo docker run --name mi-mongo -p 27017:27017 --restart always -d mongo:latest
#
# 🏁 La prueba de oro:
#
# Apenas corra el segundo comando, vuelva a tirar el que me acaba de mandar:
# Bash
#
# sudo docker ps


# ¡Exacto, socio! Esa es la mrd de la magia. El comando --restart always es el verdadero
# truco de los profesionales.
#
# Pille cómo funciona ese salvavidas por dentro para que sepa qué acaba de hacer:
#
# * Antes (Sin el comando): Si su laptop se quedaba sin memoria ram (que con 8GB a veces
#   el sistema se pone pesado con VS Code y FastAPI), o si Docker se colgaba al
#   suspender la computadora, la jaula se apagaba y se quedaba muerta en el piso hasta
#   que usted se diera cuenta.
# * Ahora (Con el comando): Docker se vuelve el guardaespaldas de su base de datos. Si
#   la jaula de Mongo se intenta cerrar por cualquier error pendejo o falta de memoria,
#   Docker la agarra en el aire y la vuelve a prender de una en milisegundos, de forma
#   automática y en segundo plano.
#
# Usted ya no se tiene que volver a preocupar por si está viva o muerta. Mientras el
# servicio de Docker general esté corriendo en su Vivobook, esa jaula de Mongo va a
# estar ahí firme y escuchando en la ventanilla 27017.
