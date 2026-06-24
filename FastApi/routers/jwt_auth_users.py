from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt  # Solución definitiva: usamos bcrypt puro sin pasar por passlib
import jwt   # Reemplazo moderno de python-jose (proviene de pip install PyJWT)
# CORRECCIÓN DE IMPORTACIÓN: Traemos los errores nativos y modernos de PyJWT
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone

# las "constantes" esto esta en la documentaicon de jwt
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 # que solo dure 1 mn 
# 1. EL SELLO MAESTRO (Nadie fuera de su laptop lo puede saber)
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b" 
# est secret se gnera ppniendo en la temrinal "openssl rand - hex 32" alg al azar 



router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="logine")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# El modelo de base de datos incluye la contraseña oculta
class UserDB(User):
    password: str

# Base de datos simulada con contraseñas hasheadas en Bcrypt
users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "$2a$12$B2Gq.Dps1WYf2t57eiIKjO4DXC3IUMUXISJF62bSRiFfqMdOI2Xa6"# estos nuemroslos saco de https://bcrypt-generator.com/
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "$2a$12$SduE7dE.i3/ygwd0Kol8bOFvEABaoOOlC8JsCSr6wpwB4zl5STU4S" # y esto se guarda en la base de datos yyy solo sabe si esat bien si la contraseña esat bien
    }
}


# busqeuda usuarios
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

####################################################################
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except PyJWTError:
        raise exception
    # no ah susedido ninguan excepcion y ay retorna el usuario con search user
    return search_user(username)

# aca toca obtener el usaurio con el token 
# esto se metio depsue deee lo de "autenticaicon " junto con al ultima parte de get
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user
#####################################################################

# autenticacion
@router.post("/logine")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    # REEMPLAZO DE PASSLIB: Bcrypt nativo exige convertir los textos a bytes (.encode)
    # CORRECCIÓN: Primero buscamos al usuario para poder usar la variable 'user' abajo
    user = search_user_db(form.username)
    user = search_user_db(form.username)

  # .checkpw compara la clave plana contra el hash de forma segura y moderna reemplazo de jose o paslib nos e

    # Verificación segura usando bcrypt nativo en bytes
    if not bcrypt.checkpw(form.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña no es correcta"
        )
    

    # ¿general el token? bn aca tmabein se claucla appra saber si ya expiro el token
  
    # 🔄 Estructuración del Payload del Token JWT:
    # "sub" guarda la identidad del usuario y "exp" define el tiempo de expiración
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {"sub": user.username, "exp": expire_time}
    
    # Se encripta el token usando la clave secreta y el algoritmo configurado
    token_jwt = jwt.encode(access_token, SECRET, algorithm=ALGORITHM)
    
    return {"access_token": token_jwt, "token_type": "bearer"}



@router.get("/users/mio")
async def me(user: User = Depends(current_user)):
    return user



# 1. Encriptar vs. Hashear (La gran diferencia de una sola vía)
# 
# Encriptar (Dos vías): Es meter un papel en una caja con candado. Si tiene la llave, abre
# la caja y vuelve a leer el mensaje original (como los chats de WhatsApp).
# 
# Hashear (Una vía): Es como meter una fruta en una licuadora. Si mete una fresa, sale jugo.
# Matemáticamente es imposible reconstruir la fresa desde el jugo. Ningún algoritmo en el
# mundo puede revertir el hash de Bcrypt para devolverle el "123456" original.
# 
# 2. ¿Entonces cómo sabe el sistema si mi contraseña es correcta?
# 
# El sistema no guarda claves reales; solo compara el resultado de la licuadora:
# 
#     - Registro: Usted pone "123456", Bcrypt genera el hash y eso se guarda en la base de datos.
#     - Login: Usted escribe "123456", FastAPI pasa ese texto de nuevo por Bcrypt.
#     - Verificación: Se compara el nuevo hash con el guardado (if hash_nuevo == hash_guardado).
# 
# 3. ¿Y qué pasa si un hacker usa "fuerza bruta"?
# 
# Bcrypt incluye un parámetro llamado "Rounds" (rondas), que por defecto suele ser 12.
# Esto significa que el algoritmo procesa la contraseña 4.096 veces antes de dar el resultado.
# 
# Al ralentizar el proceso unos milisegundos, para un usuario normal el inicio de sesión es
# instantáneo. Sin embargo, para un hacker que intente probar millones de claves por segundo,
# esa demora hace que requiera siglos para adivinar la palabra original.





# # 🎨 La analogía: La máquina de estampar sellos con relieve
# # 
# # El token JWT es un pase VIP. Para evitar que la gente falsifique pases en su casa, el dueño
# # de la discoteca usa un sello metálico con un relieve único (SECRET) que guarda en su bolsillo.
# # 
# #     - /login: Al validar la clave, FastAPI toma los datos y ¡PUM!, les estampa la firma con el
# #       sello (SECRET). Ese resultado final firmado es el chorretón de letras raras (eyJhbGci...).
# #     - /users/me: Al presentar el pase, FastAPI contrasta la firma con su sello (SECRET). Si el
# #       sello encaja, el pase es real. Si un hacker altera el texto, la firma se rompe de una.
# # 
# # 🔍 Destripando la lógica de su código actual:

# # 1. EL SELLO MAESTRO (Nadie fuera de su servidor lo puede saber)
# SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

# # 2. Verificación de contraseñas (/login)
# # Convierte el texto plano a bytes y lo compara con el hash guardado ($2a$12$...) de la BD.
# bcrypt.checkpw(form.password.encode("utf-8"), user.password.encode("utf-8"))

# # 3. Generación del Token (/login)
# # Firma el usuario y la expiración con el algoritmo HS256 y su clave secreta.
# token_jwt = jwt.encode(access_token, SECRET, algorithm=ALGORITHM)

# # 4. El guardaespaldas (current_user)
# # Usa el SECRET para descifrar y validar si la firma es real o si el token ya expiró.
# username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")

# # 🎯 En resumen, socio:
# # El SECRET nunca sale a la luz pública, pero es el cerebro de la seguridad. Sin ese SECRET,
# # es matemáticamente imposible falsificar un token para hackear su sistema o su bot.
