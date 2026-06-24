from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

# 1. Configura el portero. Le dice a FastAPI que cuando alguien pida un Token,
# la ventanilla para ir a comprarlo es la ruta "/login".
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
# Acá no le metemos contraseña para que eso de la contraseña se guarde es adentro
# en la base y no salga en las respuestas JSON. ¡Excelente lógica, socio!

class UserDB(User):
    password: str
 
users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "123456" # La contraseña así como tal en la base no se puede dejar,
    },                       # es mejor hashearla/encriptarla con una semilla (salt) o algo. ¡Tal cual!
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "654321"
    }   
}

# Acá toca ver si el usuario existe primero y devolver exactamente el usuario de la base de datos.
def search_user(username: str):
    if username in users_db:
        # ¿Qué mrd son estos punticos? Abajo en la explicación le desgloso la magia del kwargs unpacking (**)
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


# --- EL MISTERIO DEL CURRENT_USER ---

# Esta función es el "filtro de seguridad" para las rutas privadas.
# Pide el token que viaja en la cabecera (Bearer) usando Depends(oauth2).
async def current_user(token: str = Depends(oauth2)):
    # En este ejemplo básico, el 'token' es literalmente el string del username (ej: "mouredev").
    # Por eso lo busca directo en la base de datos. Con JWT, aquí tocaría primero desencriptarlo.
    user = search_user(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, # El módulo status tiene todos los códigos limpios (evita escribir 401 a mano)
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"}) # Le avisa al navegador/cliente qué tipo de token exige (Bearer)
            
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


# --- LA RUTA DE LOGIN ---

# Acá toca login ya que ahí es donde va a colocar los datos el usuario.
# OAuth2PasswordRequestForm crea un formulario estándar en el Swagger (/docs) para mandar username y password.
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Buscar en la base a ver si está el usuario
    user_db = users_db.get(form.username)
    
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    # Ahora toca ver si la contraseña está bien
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    # Esto también es estándar en la red.
    # ¿Puedo poner "pip" en vez de user.username? ¡SÍ! Usted ahí puede retornar el string que le dé la gana,
    # por ejemplo: return {"access_token": "pip", "token_type": "bearer"}. 
    # El problema es que si pone "pip", cuando la ruta de abajo reciba el token, va a buscar el usuario "pip" 
    # en la base de datos, no lo va a encontrar y va a sacar error 401. 
    # En este ejemplo básico se usa el username como token para que la función de arriba lo pueda buscar de una.
    return {"access_token": user.username, "token_type": "bearer"}


# --- RUTA PRIVADA ---

@router.get("/users/me")
# ¿Qué carajos hace el Depends aquí? Pille la explicación abajo, socio.
async def me(user: User = Depends(current_user)):
    return user


# 🧐 Explicación de los dos dolores de cabeza del código:
# 
# 1. ¿Qué significan los dos asteriscos (**)? (Diccionario a Argumentos)
# 
# En Python, los dos asteriscos se conocen como Dictionary Unpacking (desempaquetado).
# Sirven para transformar un diccionario directamente en los argumentos de una clase.
# 
# En lugar de mapear cada campo a mano de forma aburrida:
# data = users_db["mouredev"]
# return User(username=data["username"], full_name=data["full_name"], email=data["email"])
# 
# Los dos asteriscos rompen el diccionario y asocian las llaves automáticamente:
# return User(**users_db[username])
# 
# 2. ¿Para qué sirve el Depends()? (Inyección de Dependencias)
# 
# El Depends actúa como un interceptor o un guardaespaldas para sus funciones de ruta.
# 
# async def me(user: User = Depends(current_user)):
# 
# Cuando usted llama a /users/me, FastAPI detiene el proceso y ejecuta primero current_user:
# 
#     - La petición se desvía a la función current_user.
#     - Se verifica si el token viene en la cabecera y si el usuario existe.
#     - Si las credenciales fallan, se dispara un HTTPException y el proceso muere ahí.
#     - Si todo está correcto, current_user retorna el objeto de usuario verificado.
# 
# FastAPI toma ese retorno y se lo inyecta a la variable user. Dentro de la función me(),
# usted ya no tiene que validar nada porque el usuario llega completamente limpio y filtrado.
