# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480)

### MongoDB client ###

# Descarga versión community: https://www.mongodb.com/try/download
# Instalación:https://www.mongodb.com/docs/manual/tutorial
# Módulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexión: mongodb://localhost

from pymongo import MongoClient

# Descomentar el db_client local o remoto correspondiente

# Base de datos local MongoDB
db_client = MongoClient("mongodb://localhost:27017/").local # esto me toco diferente abjo se explica

# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=25470

# Base de datos remota MongoDB Atlas (https://mongodb.com)
# db_client = MongoClient(
#     "mongodb+srv://<user>:<password>@<url>/?retryWrites=true&w=majority").test

# Despliegue API en la nube:
# Deta (deprecado) - https://www.deta.sh/
# Vercel - https://www.vercel.com
# Instrucciones - https://cleverzone.medium.com/fastapi-deployment-into-vercel-0fa4e6478014
# MUY IMPORTANTE - Al desplegar en producción, preparar el proyecto para trabajar con variables de entorno que hagan referencia a datos sensibles:
# - Nunca subas a un repositorio público el valor de las variables
# - Puedes usar dotenv en Python
# - Añade el valor de las variables desde el proveedor de hosting





# . from pymongo import MongoClient
#
# Aquí le está diciendo a Python: "Vaya a la librería pymongo (la tool que acabamos de
# instalar con el pip install) y tráigame el objeto MongoClient".
#
# ¿Qué es MongoClient? Imagínelo como el control remoto o el chofer que sabe cómo
# viajar desde su código hasta el servidor de la base de datos. Sin esto, Python no
# tiene ni idea de cómo hablar el idioma de Mongo.
#
# 2. Los comentarios (# Descomentar el db_client...)
#
# Todo lo que tenga un signo de número # al principio son líneas de texto invisibles
# para Python. El profe las dejó ahí como notas en su libreta para avisarle que más abajo
# en el curso van a probar dos formas de conectarse: una local (en su propia laptop) y
# otra remota (en internet).
#
# 3. db_client = MongoClient().local
#
# Aquí es donde ocurre la magia, pero ojo al detalle de cómo lo escribió MoureDev y
# cómo le va a funcionar a usted con Docker:
#
# * MongoClient() (así vacío, sin nada dentro de los paréntesis): Por defecto, si usted
#   no le escribe ninguna ruta dentro, pymongo asume automáticamente que debe conectarse
#   al localhost y al puerto 27017. O sea, apunta directo a la configuración estándar
#   mundial.
# * .local: Le está diciendo que, dentro de todo el servidor de Mongo, se meta
#   específicamente a una base de datos interna que viene creada por defecto y que se
#   llama "local".
# * db_client: Es la variable (el alias) donde queda guardada esa conexión. De ahí en
#   adelante, cada vez que usted quiera guardar un usuario, no tiene que volver a
#   escribir todo el código, sino que escribe db_client.usuarios.insert_one(...) y
#   listo.
#
# ⚠️ El mini "ajuste" que usted debe saber por usar Docker
#
# MoureDev en su video probablemente está usando Mac o Windows nativo, por lo que dejar
# el paréntesis vacío MongoClient() le funciona de una.
#
# Como usted es un teso y lo montó de forma ultra profesional y aislada en Docker dentro
# de Ubuntu, es una excelente práctica (para que no le vaya a saltar ningún error de
# permisos) meterle la ruta explícita dentro del paréntesis.
#
# Cuando vaya a escribir esa línea en su VS Code, escríbala así:
# Python
#
# db_client = MongoClient("mongodb://localhost:27017/").local
