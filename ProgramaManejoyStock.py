import mysql.connector
from tkinter import *
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import time

# Conexión a la base de datos MySQL
try:
    conexion = mysql.connector.connect(
        user='root', password='',  # Cambia estos valores según tu configuración
        host='localhost',
        database='bdfinal2',
        port='3306'
    )
    print("Conexión exitosa")
except mysql.connector.Error as err:
    messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
    exit()  # Termina el programa si la conexión falla

# Ventana principal
ventana = Tk()
ventana.geometry("1680x1050")
ventana.title("Celu PRO")

# Manejo de error en el icono
try:
    ventana.iconbitmap("celu.ico")
except Exception as e:
    messagebox.showwarning("Advertencia", f"No se encontró el ícono: {e}")

# Función para ocultar todos los frames
def sacarFrames():
    for frame in [frame_inicio, frame_stock, frame_ventas, frame_proveedores, frame_clientes]:
        frame.pack_forget()

# Frames
frame_inicio = Frame(ventana, bg="gray0")
frame_stock = Frame(ventana, bg="gray0")
frame_ventas = Frame(ventana, bg="gray0")
frame_proveedores = Frame(ventana, bg="gray0")
frame_clientes = Frame(ventana, bg="gray0")

# Frame de botones
frame_botones = Frame(ventana, bg="gray2")
frame_botones.pack(side=TOP, fill=X)

# Crear un frame interno para centrar los botones
frame_botones_interno = Frame(frame_botones, bg="spring green")
frame_botones_interno.pack(side=TOP)

# Frame inicio - Contenido de la página de inicio
try:
    logo = PhotoImage(file="celupng.png")  # Cambia esto por la ruta correcta de tu logo
    label_image_logo = Label(frame_inicio, image=logo, relief=FLAT, bd=0)
    label_image_logo.pack(pady=50)
except Exception as e:
    messagebox.showwarning("Advertencia", f"No se encontró la imagen: {e}")

# Funciones para mostrar los diferentes frames
def verInicio():
    sacarFrames()
    frame_inicio.pack(fill=BOTH, expand=True)

def verStock():
    sacarFrames()
    frame_stock.pack(fill=BOTH, expand=True)

def verVentas():
    sacarFrames()
    frame_ventas.pack(fill=BOTH, expand=True)
    cargar_articulos()

def verProveedores():
    sacarFrames()
    frame_proveedores.pack(fill=BOTH, expand=True)

def verClientes():
    sacarFrames()
    frame_clientes.pack(fill=BOTH, expand=True)

# Función para cerrar la aplicación
def cerrar():
    ventana.destroy()

# Función para regresar al frame de inicio
def regresar():
    sacarFrames()
    frame_inicio.pack(fill=BOTH, expand=True)

# Boton de regresar
botonRegresar = Button(frame_botones_interno, text="Regresar", command=regresar, bg="spring green", fg="black")
botonRegresar.pack(side=LEFT, padx=5, pady=5)

# Boton de cerrar
botonCerrar = Button(frame_botones_interno, text="Cerrar", command=cerrar, bg="spring green", fg="black")
botonCerrar.pack(side=RIGHT, padx=5, pady=5)

# Botones en el frame interno
botonInicio = Button(frame_botones_interno, text="Inicio", command=verInicio, bg="spring green", fg="black")
botonInicio.pack(side=LEFT, padx=5, pady=5)

botonStock = Button(frame_botones_interno, text="Stock", command=verStock, bg="spring green", fg="black")
botonStock.pack(side=LEFT, padx=5, pady=5)

botonVentas = Button(frame_botones_interno, text="Ventas", command=verVentas, bg="spring green", fg="black")
botonVentas.pack(side=LEFT, padx=5, pady=5)

botonProveedores = Button(frame_botones_interno, text="Proveedores", command=verProveedores, bg="spring green", fg="black")
botonProveedores.pack(side=LEFT, padx=5, pady=5)

botonClientes = Button(frame_botones_interno, text="Clientes", command=verClientes, bg="spring green", fg="black")
botonClientes.pack(side=LEFT, padx=5, pady=5)

################################CARRITO DE COMPRAS y TICKET################################
# Carrito de compras como una lista de diccionarios
carrito = []

# Función para agregar un artículo al carrito
def agregar_al_carrito():
    seleccion = lista_articulos.curselection()
    cantidad = entry_cantidad.get()

    if seleccion and cantidad.isdigit():
        id_articulo = articulos[seleccion[0]][0]  # ID del artículo
        cantidad = int(cantidad)
        # Buscar el artículo en la base de datos
        cursor = conexion.cursor()
        cursor.execute("SELECT ID, detalle, precio_final FROM stock WHERE ID = %s", (id_articulo,))
        articulo = cursor.fetchone()
        cursor.close()

        if articulo:
            id_articulo, detalle, precio = articulo
            carrito.append({
                'ID': id_articulo,
                'detalle': detalle,
                'cantidad': cantidad,
                'precio': precio,
                'subtotal': cantidad * precio
            })
            entry_cantidad.delete(0, END)  # Limpiar la entrada de cantidad
            actualizar_carrito()
        else:
            messagebox.showwarning("Advertencia", "Artículo no encontrado")
    else:
        messagebox.showwarning("Advertencia", "Selecciona un artículo y especifica una cantidad válida.")

# Función para actualizar el área del carrito en la interfaz
def actualizar_carrito():
    lista_carrito.delete(0, END)
    for item in carrito:
        lista_carrito.insert(END, f"{item['detalle']} - Cantidad: {item['cantidad']} - Subtotal: ${item['subtotal']:.2f}")
    calcular_total()

# Función para calcular el total de la compra
def calcular_total():
    total = sum(item['subtotal'] for item in carrito)
    etiqueta_total.config(text=f"Total: ${total:.2f}")

# Funcion para eliminar un elemento del carrito
def eliminar_del_carrito(indice):
    del carrito[indice]
    actualizar_carrito()

# Función para vaciar el carrito
def vaciar_carrito():
    carrito.clear()
    actualizar_carrito()

# Función para obtener los artículos de la base de datos MySQL
def obtener_articulos():
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT ID, cantidad, precio_final, detalle FROM stock")
        articulos = cursor.fetchall()
        cursor.close()
        return articulos
    except mysql.connector.Error as err:
        messagebox.showerror("Error de base de datos", f"No se pudieron obtener los artículos: {err}")
        return []

# Función para cargar los artículos en el Listbox
def cargar_articulos():
    global articulos
    articulos = obtener_articulos()
    lista_articulos.delete(0, END)
    for articulo in articulos:
        lista_articulos.insert(END, f"{articulo[3]} - Precio: ${articulo[2]:.2f}")  # Detalle y precio

# Crear interfaz para el carrito de compras en el frame de ventas
Label(frame_ventas, text="Artículos disponibles:", bg="gray0", fg="white").pack(pady=10)

lista_articulos = Listbox(frame_ventas, bg="white", width=50, height=10)
lista_articulos.pack(pady=10)

Label(frame_ventas, text="Cantidad:", bg="gray0", fg="white").pack(pady=5)
entry_cantidad = Entry(frame_ventas)
entry_cantidad.pack(pady=5)

botonAgregarCarrito = Button(frame_ventas, text="Agregar al Carrito", command=agregar_al_carrito, bg="lightblue", fg="black")
botonAgregarCarrito.pack(pady=5)

Label(frame_ventas, text="Carrito:", bg="gray0", fg="white").pack(pady=10)

lista_carrito = Listbox(frame_ventas, bg="white", width=50, height=10)
lista_carrito.pack(pady=10)

etiqueta_total = Label(frame_ventas, text="Total: $0.00", bg="gray0", fg="white")
etiqueta_total.pack(pady=10)

botonVaciarCarrito = Button(frame_ventas, text="Vaciar Carrito", command=vaciar_carrito, bg="lightcoral", fg="black")
botonVaciarCarrito.pack(pady=5)

# Obtener fecha y hora actuales para el nombre del archivo y formato de fecha
horaActual = time.strftime("%H%M%S")
fechaActual = time.strftime("%d%m%Y")
fechaHoy = time.strftime("%d/%m/%Y")
nombreArchivo = f"ticket{fechaActual}{horaActual}.pdf"

# Crear el PDF (esta función debe ser llamada en el momento adecuado)
def crear_ticket():
    # Crear el PDF
    nuevoPdf = canvas.Canvas(nombreArchivo, pagesize=A4)

    # Líneas horizontales (X)
    nuevoPdf.line(20, 820, 570, 820)  # Línea superior
    nuevoPdf.line(20, 20, 570, 20)    # Línea inferior
    nuevoPdf.line(20, 720, 570, 720)  # Línea de encabezado

    # Líneas verticales (Y)
    nuevoPdf.line(20, 20, 20, 820)    # Borde izquierdo
    nuevoPdf.line(570, 20, 570, 820)  # Borde derecho
    nuevoPdf.line(480, 720, 480, 820) # Separador entre título y fecha

    # Texto de encabezado
    nuevoPdf.setFont("Times-Roman", 20)
    nuevoPdf.drawString(50, 780, "Ticket de Compra")
    nuevoPdf.setFont("Times-Roman", 12)
    nuevoPdf.drawString(490, 780, fechaHoy)  # Fecha actual en la esquina superior derecha

    # Encabezados de la tabla de productos
    nuevoPdf.drawString(50, 700, "Artículo")
    nuevoPdf.drawString(300, 700, "Cantidad")
    nuevoPdf.drawString(400, 700, "Precio")
    nuevoPdf.drawString(500, 700, "Subtotal")

    # Variables para controlar la posición vertical en la tabla y el total
    y_position = 680
    total = sum(item['subtotal'] for item in carrito)

    # Agregar artículos del carrito al ticket
    for item in carrito:
        nuevoPdf.drawString(50, y_position, f"{item['ID']} - {item['detalle']}")
        nuevoPdf.drawString(300, y_position, str(item['cantidad']))
        nuevoPdf.drawString(400, y_position, f"${item['precio']:.2f}")
        nuevoPdf.drawString(500, y_position, f"${item['subtotal']:.2f}")
        y_position -= 20  # Mover la posición hacia abajo para la siguiente fila

    # Mostrar el total
    nuevoPdf.drawString(400, y_position - 20, "Total:")
    nuevoPdf.drawString(500, y_position - 20, f"${total:.2f}")

    # Guardar el PDF
    nuevoPdf.save()
    print(f"Ticket guardado como {nombreArchivo}")

# Mostrar el frame de inicio al iniciar la aplicación
verInicio()
# Iniciar ventana
ventana.mainloop()
