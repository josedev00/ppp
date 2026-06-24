
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router = APIRouter()

#inciiar con  uvicorn 1_users:app --reload
#otra cosaese def lo emjro o bn lo OBLIGATORIO es que todos se llamem diisnto

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="Brais", surname="Moure", url="https://moure.dev", age=35),
              User(id=2, name="Moure", surname="Dev",url="https://mouredev.com", age=35),
              User(id=3, name="Brais", surname="Dahlberg", url="https://haakon.com", age=33)]


# --- RESPUESTAS GENERALES ---

@router.get("/usersjson")
async def usersjson():  # Creamos un JSON a mano
    return [{"name": "Brais", "surname": "Moure", "url": "https://moure.dev", "age": 35},
            {"name": "Moure", "surname": "Dev","url": "https://mouredev.com", "age": 35},
            {"name": "Haakon", "surname": "Dahlberg", "url": "https://haakon.com", "age": 33}]

@router.get("/usere")
async def users():
    return usersjson

#bueno hasta aca era simple SIN EL ID

# Crea el molde con el BaseModel (la clase).
# Crea una lista vacía en Python (por ejemplo, lista_operaciones = []) global,
# que hace las veces de base de datos temporal en la memoria RAM.

######3 PATH Y QUERY #######

#bn solloo como recuerdo y es cada def colocarle un nomrbe el cual se qeu va ahcer osea de acruedo a laoperaicon

@router.get("/users")
async def get_all_users():
    return users_list

# --- PATH Y QUERY (Nombres de funciones cambiados) ---

# Por Path: http://127.0.0
@router.get("/user/{id}")  
async def get_user_by_path(id: int):
    return search_user(id)

# Por Query: http://127.0.0.1:8000/user/?id=1
@router.get("/user/")  
async def get_user_by_query(id: int):
    return search_user(id)

# --- FUNCIÓN DE BÚSQUEDA ---

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except :
        return {"error": "No se ha encontrado el usuario"}
    
# 🛣️ 1. Parámetros por PATH (Ruta)
# 
# Mire la estructura de la URL: http://127.0.0.1:8000/user/1
# 
#     ¿Qué es?: El dato (id) forma parte fija de la dirección de la página. Está metido dentro de los slashes (/).
# 
#     ¿Cuándo se usa?: Cuando el dato que va a buscar es obligatorio e identificable. Es decir, cuando apunta a un recurso único y específico que usted sabe que existe o debería existir.
# 
#     Ejemplo en su mundo: Si usted quiere ver el historial exacto de la operación número 45 que guardó en su base de datos. La ruta lógica sería /operacion/45. Sin ese "45", la ruta /operacion/ no tiene sentido porque usted va por un elemento único.
# 
# 🔍 2. Parámetros por QUERY (Consulta)
# 
# Mire la estructura de la URL: http://127.0.0.1:8000/user/?id=1 (lleva el signo de interrogación ?).
# 
#     ¿Qué es?: El dato no es parte de la dirección fija. La ruta real es /user/, y lo que va después del ? son "filtros" o opciones extras que usted le añade a la búsqueda.
# 
#     ¿Cuándo se usa?: Se usa para filtrar, ordenar, paginar o buscar elementos dentro de una lista, o cuando el parámetro es opcional.
# 
#     Ejemplo en su mundo: Imagine que quiere ver sus operaciones en el mercado, pero solo las del par EURUSD y que hayan sido ganadoras. En lugar de crear una ruta fija rara, usted usa Query Parameters:
#     /operaciones/?par=EURUSD&resultado=win
#     Si usted quita los filtros y deja solo /operaciones/, la página sigue funcionando (le traería todas las operaciones del mundo). El Query solo refina la búsqueda.
# 
# 📊 Tabla Comparativa (Para su Obsidian)
# Característica    PATH (/user/{id})   QUERY (/user/?id=1)
# Obligatorio   Sí. Si no pone el id, da error 404 (No encontrado). No necesariamente. Puede ser opcional.
# En la URL se ve   Como parte del camino limpio (/user/5). Después de un signo de pregunta (/user/?id=5).
# Objetivo principal    Identificar un recurso único.   Filtrar o clasificar una lista de recursos.
# 🎯 En conclusión: ¿Cuál debería usar en su código de ejemplo?
# 
# Para el ejemplo que escribió, donde está buscando un solo usuario específico por su ID, la regla internacional de las APIs (REST) dice que debería usar PATH (/user/{id}). Es más limpio, directo y semánticamente correcto porque el ID identifica a ese usuario único.
# 
# Deje el Query para cuando haga funciones como: "Tráigame las operaciones, pero ?limit=10 (solo las últimas 10)".


# 🎯 La lección de oro:
# 
# Usted ya piensa como programador de Backend. Cuando tenga dudas de cómo estructurar una URL en su bot o en su API, mire cómo lo hacen los grandes como Google.
# 
#     ¿Va a buscar algo que cambia todo el tiempo o que es un filtro opcional? Use ?query=algo (Como Google).
# 
#     ¿Va a ir por un usuario o una operación fija que tiene un número único? Use /path/123.



############# POST PUT Y DELETE ############


#1.uqweeo agregar un usuraio entocnes toca 'user' y no users
@router.post("/user/")
async def user(user: User):# la clase
    if type(search_user(user.id)) == User:
        return{"no se ha encontrado el usuario"}
    else:
        users_list.append(user)

#ahroa actualizar datos
#mmm segun si es actualizar tod tod pues un PUT y si es una cosilla toca con PTH epor aca no lo muestra

@router.put("/user/")
async def user(user: User):

    found = False # variabel apra saber si se actualizado o no el usuario

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}

    return user

@router.delete("/user/{id}")
async def user(id: int):

    found = False # variabel apra saber si se actualizado o no el usuario

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] 
            found = True

    if not found:
        return {"error": "No se ha eliminado el usuario"}





############## HTPP estatus code ####################


from fastapi import APIRouter, HTTPException  # <-- Importa esto

@router.delete("/userr/{id}")

async def delete_user(id: int):
    # ... su lógica de buscar el usuario ...
    
    # Si no lo encuentra o no lo puede borrar, dispara esto:
    raise HTTPException(status_code=404, detail="No se ha encontrado o eliminado el usuario")


# 1. ¿Por qué el código de estado (el número) es vital para SU código?
# 
# Imagine que en el futuro su script de Python (el que procesa los datos de Tradovate) necesita
# borrar una orden vieja, y para eso toca su propia API de FastAPI.
# 
#     Si usted solo devuelve texto (return {"error": "..."}): A su script de Python le va a
#     tocar leer ese JSON, extraer el texto y ponerse a hacer un condicional hpta tipo:
#     if respuesta["error"] == "No se ha eliminado el usuario":. Si mañana usted cambia una sola
#     letra de ese mensaje (por ejemplo, escribe "eliminado" con mayúscula), su propio script
#     se va a romper porque ya no coincide el texto.
# 
#     Si usa el Status Code (e.g., 404 o 400): En Python usted solo valida el número:
#     if respuesta.status_code == 404:. Es un estándar absoluto. No importa si usted cambia el
#     mensaje en español, en inglés o lo que sea, el número siempre va a ser 404. Es blindado.
# 
# 2. La combinación perfecta (El estándar profesional)
# 
# La forma en la que trabajan los duros del backend (y como debería acostumbrar a su API desde
# ya) es mandar el Status Code en la cabecera para que los programas lo entiendan rápido, y un
# JSON con un mensaje claro adentro para que usted, cuando esté mirando el Thunder Client, sepa
# exactamente qué pasó en cristiano.
# 
# FastAPI tiene una herramienta nativa para hacer esto en una sola línea sin enredarse. Se llama
# HTTPException.






# 🟢 1. Los 2xx: "¡Todo melo, socio!" (Éxito)
# 
# Significa que la petición llegó bien, el servidor la entendió y todo salió a pedir de boca.
# 
#     200 OK: Es el rey de internet. Significa "Todo perfecto, aquí tiene sus datos". Es lo que
#     le sale cuando hace un GET y le devuelve la lista de usuarios limpia.
# 
#     201 Created: Este lo va a usar usted mucho. Significa "¡Listo, socio! Recibí los datos y
#     ya creé el registro con éxito". Es el código ideal para responder después de un POST
#     (por ejemplo, cuando crea un usuario nuevo o cuando su bot mete una orden de compra).
# 
# 🟡 2. Los 3xx: "Por ahí no es, muévase" (Redirección)
# 
# El servidor le dice que lo que busca cambió de lugar y lo va a mandar a otra URL. En su bot
# casi no los va a programar, pero internet los usa un montón por debajo.
# 
#     301 Moved Permanently: La página se mudó de link para siempre.
# 
#     304 Not Modified: Sirve para ahorrar internet. El servidor le dice al navegador: "Socio,
#     esa página no ha cambiado desde la última vez que la vio, use la copia que tiene guardada".
# 
# 🔴 3. Los 4xx: "La cagó usted, socio" (Error del Cliente)
# 
# Aquí el servidor se lava las manos. Significa que usted mandó algo mal en la petición (escribió
# la URL como no era, no mandó el JSON con el molde correcto o no tiene permiso).
# 
#     400 Bad Request: "Socio, me mandó un viaje de datos horrible". Es lo que Pydantic dispara
#     automáticamente si usted en el BaseModel pide un número y le mandan un texto.
# 
#     401 Unauthorized: "Usted no está bautizado aquí". Significa que no ha iniciado sesión o no
#     mandó la llave de seguridad (token). Fijo le va a salir con Tradovate si escribe mal la clave.
# 
#     404 Not Found: El más famoso del mundo. El servidor le dice: "Caminé por toda la base de
#     datos y esa ruta o ese ID que me pidió no existe". Es lo que debería devolver su función.
# 
# 💥 4. Los 5xx: "La cagué yo, pailas" (Error del Servidor)
# 
# Esto es cuando su código de Python se rompió por completo en el fondo. El cliente mandó todo
# bien, pero el backend estalló.
# 
#     500 Internal Server Error: El terror de los programadores. Significa que su código tiró una
#     excepción que usted no controló con un try/except y el servidor se congeló. Si ve este
#     número en Thunder Client, le toca ir corriendo a mirar la terminal de VS Code.
# 
# 🎯 ¿Cómo se usan en FastAPI?
# 
# MoureDev le va a mostrar que usted puede elegir qué código devolver. Por defecto, FastAPI
# devuelve 200 para todo lo que salga bien, pero usted puede ser más pro.
# 
# Por ejemplo, para su error de "No se ha encontrado el usuario", en vez de devolver un texto
# que simule un error, uno le dice a FastAPI que dispare un status_code=404. Así, el Thunder Client
# se pinta de rojo y cualquier otra aplicación sabe que no existe con leer el número.





# 📋 Los únicos que se tiene que aprender (El "Top 8")
# 
#     200 (OK): Todo salió perfecto (GET exitoso).
# 
#     201 (Created): El registro se guardó con éxito (POST exitoso).
# 
#     400 (Bad Request): El cliente mandó datos inválidos o con errores de formato.
# 
#     401 (Unauthorized): No ha iniciado sesión o el token/llave está malo.
# 
#     403 (Forbidden): Sabe quién es, pero usted no tiene permisos para esa zona.
# 
#     404 (Not Found): Lo que busca (ruta o ID) no existe.
# 
#     500 (Internal Server Error): Su código de Python estalló y tiró un error.
# 
#     503 (Service Unavailable): El servidor externo (Tradovate/Telegram) está caído.
# 
# 🧐 ¿Y qué pasa con los otros 50 códigos?
# 
# Están ahí para casos muy específicos de la arquitectura de internet. Si el día de mañana una
# API rara le devuelve un número que usted nunca en su vida ha visto (por ejemplo, un 429), usted
# no se estresa: va a la documentación, lo busca, entiende qué significa y soluciona.
# 
#     💡 Dato curioso: Existe literalmente el código 418 I'm a teapot (Soy una tetera). Fue una
#     broma que crearon los ingenieros en 1998 para el día de los inocentes, parodiando que si
#     usted le pide a una tetera un café, ella debería responderle con ese código.
# 
# Con que sepa qué significa cada familia (2xx es éxito, 4xx es error suyo, 5xx es error del
# servidor) y domine el Top 8 de arriba, está más que listo para cualquier desarrollo Backend.






##### para temrinar ####

# 1. El status_code personalizado (Éxito específico)
# 
# FastAPI devuelve 200 OK por defecto si la función no se rompe. Sin embargo, para crear
# recursos (como un POST de usuario o de orden de compra), el estándar exige usar 201 Created.
# Se configura directamente en el decorador para que FastAPI se encargue del sello HTTP:

@router.post("/user/", status_code=201)
async def create_user(user: User):
    users_list.append(user)
    return user

# 2. El response_model (El filtro de seguridad de salida)
# 
# Pydantic valida los datos al entrar, pero response_model filtra y limpia los datos antes de
# que salgan a internet. Sirve para ocultar datos privados (como contraseñas encriptadas).
# 
# Si su base de datos tiene un modelo completo con contraseña hashed:

class UserDB(BaseModel):
    id: int
    name: str
    password_hashed: str

# Usted crea un molde de salida limpio, sin el campo de la contraseña:

class UserResponse(BaseModel):
    id: int
    name: str

# Al asignarlo en el decorador, FastAPI extirpa la contraseña automáticamente antes de enviar:

@router.get("/user/{id}", response_model=UserResponse) # <-- ¡Le clava el molde de salida! ooooo el normal
async def get_user(id: int):
    # Supongamos que aquí busca en la base de datos y trae el usuario completo (con todo y contraseña)
    usuario_de_bd = search_user_in_db(id) #type:ignore
    
    return usuario_de_bd  # <-- Usted devuelve el objeto completo sin miedo

# 🕵️‍♂️ ¿Qué pasa por debajo de la mesa?
# 
# FastAPI recibe el objeto completo (con contraseña), pero al ver response_model=UserResponse,
# le extirpa los campos ocultos, lo amolda al formato limpio y escupe un JSON seguro.
# También valida que no falten datos obligatorios del molde de salida antes de enviarlo.

# 🎯 El resumen de una línea pro:

# @app.post("/user/", response_model=UserResponse, status_code=201)
# async def create_user(user: User):
    # 1. Filtro de entrada: Pydantic valida los tipos de datos que envía el cliente.
    # 2. Acción: Se ejecuta su lógica interna (guardar en base de datos o listas).
    # 3. Filtro de salida: El response_model limpia el resultado antes de mandarlo a internet.
    # 4. Cabecera: El status_code pone el sello 201 para avisar que se creó con éxito.

