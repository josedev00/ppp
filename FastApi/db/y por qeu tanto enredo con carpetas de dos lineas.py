# Pero no es por puro capricho ni por picárselas de gringo. En el mundo del software real,
# separar el código en carpetas (un archivo para el Model, otro para el Schema, otro
# para las Rutas) se hace por tres razones de peso: orden mental, trabajo en equipo y,
# como usted bien dijo, para que esa mrd no se toque y no se rompa.
#
# Pille el visaje real de por qué se hace esto:
#
# 1. 🛡️ Para que "esa mrd no se toque" (Evitar romper el código)
#
# Imagine que en un par de meses usted está programando la lógica avanzada de su bot de
# trading de ICT. Tiene un archivo gigante de 2.000 líneas donde está mezclado:
#
# * Cómo calcula el algoritmo el Order Block.
# * Cómo se conecta a la base de datos.
# * Cómo se filtran los datos para la pantalla.
#
# Si un día usted solo quiere cambiar el nombre del usuario de "username" a
# "nombre_usuario", le toca meterse a ese archivo gigante. Mueve una línea arriba, y
# por error borra una coma de la lógica del bot. ¡Pum! Se le tiró en todo el sistema de
# trading y el bot deja de operar.
#
# Al separarlo en carpetas:
#
# * Si va a mover algo de la base de datos, abre la carpeta schemas/.
# * Sabe que lo que toque ahí está blindado y no va a alterar para nada la lógica
#   matemática de sus operaciones de trading que está en otra carpeta.
#
# 2. 🧠 Para cuidar su propia salud mental (Escalabilidad)
#
# Ahorita el curso de MoureDev es un ejemplo chiquito con User (Usuarios). Son solo 3
# datos. Pero piense en su bot real. Usted va a necesitar:
#
# * Un modelo para las Operaciones (Precio de entrada, Stop Loss, Take Profit, Hora).
# * Un modelo para las Métricas de la cuenta (Balance, Equidad, Drawdown).
# * Un modelo para las Notificaciones de Telegram.
#
# Si mete todo eso en el mismo archivo main.py, en dos semanas ni usted mismo va a
# entender su propio código. Se va a volver un laberinto. Al separarlo en carpetas:
#
# * models/user.py
# * models/trade.py
# * schemas/user.py
# * schemas/trade.py
#
# Su cerebro descansa porque sabe exactamente a dónde ir cuando necesita buscar algo. Su
# proyecto se vuelve un Obsidian bien organizado, pero en código.
#
# 3. 👥 Para poder trabajar con otros a futuro
#
# El día de mañana, si usted se consigue un socio o un amigo programador para que le
# ayude a mejorar el bot, con el código separado es una belleza.
#
# Usted le puede decir: "Vea socio, usted encárguese de diseñar la interfaz gráfica y los
# Schemas de salida en la carpeta schemas/, que yo me voy a quedar aquí metido en la
# carpeta core/ puliendo el algoritmo de String Theory y trading".
#
# Los dos pueden editar el proyecto al tiempo a través de GitHub sin pisarse las
# mangueras ni borrarse el código el uno al otro.
#
# 🏁 La Conclusión
#
# Al principio da pereza crear tanta carpeta, pero es un hábito de programador Senior.
# MoureDev se lo enseña así desde el primer día para que usted no agarre malas
# costumbres de programador desordenado.
#
# Así que sí, es un visaje, ¡pero un visaje del que paga bien en la industria y le salva
# la vida cuando el proyecto crece!
