# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=12475

### Products API ###

from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"message": "No encontrado"}}
)

products_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]


@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def products(id: int):
    return products_list[id]



# # 📦 El concepto: Los Routers son "Bolsas Temáticas"
# # 
# # En lugar de meter todas las rutas en el archivo principal (un desorden total), APIRouter 
# # permite crear archivos independientes y especializados para cada sección de la aplicación:
# # 
# #     - users.py    ➡️ Lógica exclusiva de usuarios (crear, buscar, eliminar).
# #     - products.py ➡️ Lógica exclusiva de stock o productos.
# #     - trading.py  ➡️ Lógica de órdenes de compra/venta y conexión a Tradovate.
# # 
# # 🔌 La magia: El include_router (La Unión)
# # 
# # El archivo main.py funciona como el conector central. Usted importa los módulos de sus 
# # respectivas carpetas y los acopla a la aplicación principal usando .include_router().

# from fastapi import FastAPI
# from routers import users, products

# app = FastAPI()

# # Aquí está la magia: Conecta los cables
# app.include_router(users.router)
# app.include_router(products.router)

# @app.get("/")
# async def root():
#     return {"message": "¡Hola, socio! Esta es la entrada principal del centro comercial"}

# # 🚀 Una ventaja pro de los Routers: Los Prefijos (prefix)
# # 
# # Al configurar un router, se le puede poner una "etiqueta" en el main.py para no tener que
# # escribir /user/ o /product/ en cada ruta del archivo separado.
# # 
# # El parámetro tags=["Usuarios"] agrupa y organiza visualmente las rutas por colores en la
# # página de pruebas (/docs).

# app.include_router(users.router, prefix="/users", tags=["Usuarios"])

# # 🎯 En conclusión, socio:
# # 
# # El APIRouter mantiene el código limpio y escalable. Cuando su proyecto de trading crezca,
# # usted no toca nada de usuarios ni de productos; simplemente crea un archivo trading.py,
# # programa su lógica ahí, y lo conecta en el main.py.
