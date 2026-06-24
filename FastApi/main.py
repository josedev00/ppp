from fastapi import FastAPI
from routers import products, users , basic_auth_users , jwt_auth_users,users_db
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.include_router(users_db.router)

# Url local: http://127.0.0.1:8000
@app.get("/")
async def root():
    return "Hola FastAPI!"

# Url local: http://127.0.0.1:8000/url
@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}


######### static imagnes ########

from fastapi.staticfiles import StaticFiles 
app.mount("/static",StaticFiles(directory="static"),name = "static")
#navegador:
#http://127.0.0.1:8000/static/images/python.jpg


# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C
#aca en el de "docs" le doy try out para probar y eller lo qeu tiene
# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
#solo por tener en cuant aue si descargo la documentaicon eprooooo modifico 
#los nomrbes de pro eejmplo la ln 16 pues esa documaentqaicon no sirve




# 🍔 El Mundo Síncrono (Tradicional / Lento)
#
# Usted llega a la caja a pedir su hamburguesa. El cajero toma su orden, va a la cocina, se queda
# esperando a que la carne se cocine, arma la hamburguesa, se la entrega a usted y, solo cuando
# usted se retira con su comida, el cajero atiende a la siguiente persona en la fila.
#
#     Mientras la carne se cocinaba, la fila se quedó congelada. Nadie más pudo pedir.
#
#     Así es como funcionan frameworks viejos o tradicionales como Flask. Si una petición se
#     demora (por ejemplo, esperando a que una base de datos responda), todo el servidor se frena.

# ⚡ El Mundo Asíncrono (FastAPI / Ultra Veloz)
#
# Usted llega a la caja. El cajero toma su orden, le da un recibo con un número y le dice:
# "Socio, hágase a un lado, cuando esté lista lo llamo". En el segundo en que usted se mueve, el
# cajero inmediatamente atiende al siguiente de la fila, toma su orden y hace lo mismo.
#
#     La cocina (el procesador) va haciendo las hamburguesas a su ritmo, pero la caja nunca deja
#     de recibir clientes.
#
#     Cuando su hamburguesa está lista, la cocina grita su número, usted va y la recoge.

# 🎯 ¿Para qué le sirve esto a su bot de trading?
#
# Esto es el superpoder de FastAPI. Imagine que su bot está corriendo y tiene que hacer dos cosas:
#
#     Ir a internet a pedir el historial de precios de los últimos 10 años (eso se demora unos
#     segundos porque es mucha info).
#
#     Estar pendiente de si usted le hunde el "Botón de Pánico" desde el celular para apagarlo.
#
#     Si fuera síncrono: Mientras el bot descarga los 10 años de precios, el código se congela.
#     Si usted le hunde "Apagar" en ese momento, el bot no lo escucha porque está ocupado
#     descargando el archivo.
#
#     Como es ASÍNCRONO: El bot pide los precios a internet y dice: "Esto se va a demorar, voy a
#     dejar la tarea en el fondo (background)". Mientras los datos viajan por el cable, el bot
#     queda libre para seguir escuchando si usted le manda un mensaje, si el mercado cambia o si
#     tiene que hacer otra operación. No pierde el tiempo esperando sentado.


# 1. El Combo de los 4 Métodos Principales
#
# Método    ¿Qué significa en cristiano?    ¿Para qué sirve en general?
# GET       👁️ Leer / Traer                  Pedirle información al servidor. No cambia nada, solo mira.
# POST      ✍️ Crear / Enviar                Mandar datos nuevos para que el servidor haga algo con ellos o los guarde.
# PUT       🔄 Actualizar / Modificar        Cambiar los datos de algo que ya existe por completo.
# DELETE    ❌ Borrar                        Eliminar un dato del sistema o de la base de datos.
#
# 🎯 ¿Cuáles va a usar usted en su Bot y en qué momento?
#
# Socio, guarde esto en su Obsidian porque este es el plano de cómo va a interactuar su código de
# Python con Tradovate, con Telegram y con su base de datos SQLite.
#
# 1. GET (Traer información)
#
# Lo va a usar muchísimo para revisar el estado de las cosas.
#
#     En Tradovate: Su bot va a hacer un GET a la API de Tradovate para preguntar: ¿Cuál es el
#     saldo actual de mi cuenta? o ¿Cuáles son las posiciones que tengo abiertas ahorita?.
#
#     En su FastAPI (FUTURO): Si crea una ruta para usted mirar desde la calle, haría un GET
#     /estado-bot para que su laptop le devuelva si el script sigue prendido o apagado.
#
# 2. POST (Ejecutar acciones / Mandar datos)
#
# Este es el método de la acción pesada. Cada vez que usted va a crear algo nuevo o disparar un
# evento, usa POST.
#
#     En Tradovate (Cuenta Demo/Real): Cuando su lógica de Pandas diga "¡COMPRAR YA!", su código
#     va a mandar una petición POST a Tradovate llevando un JSON con la orden de compra. Tradovate
#     recibe ese POST y crea la orden en el mercado.
#
#     En Telegram: Para que a su celular le llegue la alerta, su script de Python le hace un POST
#     a los servidores de Telegram diciendo: «Mándele este texto ("🚨 Señal de Compra") al ChatID
#     de este socio». Telegram recibe el paquete y dispara la notificación a su teléfono.
#
# 3. PUT / PATCH (Modificar órdenes)
#
# Lo va a usar cuando necesite cambiar las reglas del juego sobre la marcha.
#
#     En el mercado: Imagine que el bot metió una operación con un Stop Loss en un precio "X",
#     pero el precio empieza a subir y usted quiere hacer Trailing Stop para asegurar ganancias.
#     Su bot va a mandar un PUT o un PATCH a Tradovate diciendo: "Oiga, la orden que metí hace 10
#     minutos, modifíquele el Stop Loss y póngaselo en este nuevo precio "Y"".
#
# 4. DELETE (Cancelar / Apagar)
#
# Este es para limpiar la mesa.
#
#     En el mercado: Si tiene una orden pendiente (un Limit Order) esperando a que el precio caiga
#     a cierto punto para comprar, pero el mercado cambia de dirección y la estrategia se invalida,
#     su bot manda un DELETE a la API de Tradovate diciendo: "Cancele y borre esa orden pendiente
#     que tenía allá, ya no quiero comprar nada".
#
# 🛠️ ¿Qué procede en su curso?
#
# Los ejemplos que escribió con @app.get("/") y @app.get("/url") están melos para entender las
# rutas. Lo que va a ver a continuación en el curso de MoureDev es cómo usar @app.post().
#
# Cuando llegue a esa parte, pille que el video le va a enseñar a mandar un JSON dentro de la
# petición POST (el famoso Request Body). Preste atención a cómo el profe usa Thunder Client o
# Postman para escribir un JSON y enviárselo a FastAPI, porque ese es exactamente el mismo
# ejercicio que usted hará después para enviarle las órdenes a Tradovate.
