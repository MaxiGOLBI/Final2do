import mysql.connector
from tkinter import *
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox, END

# Conectar a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bdfinal2"
)
# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# Crear las tablas si no existen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock (
        ID TEXT PRIMARY KEY,
        cantidad INTEGER,
        precio_costo REAL,
        precio_final REAL,
        detalle TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS proveedores (
        ID TEXT PRIMARY KEY,
        nombre TEXT,
        costo REAL,
        detalle TEXT,
        fecha TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        ID TEXT PRIMARY KEY,
        nombre_y_apellido TEXT,
        detalle TEXT,
        fecha TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        ID TEXT PRIMARY KEY,  
        cantidad INTEGER,
        detalle TEXT,
        fecha TEXT,
        total REAL
    )
''')

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
    for frame in [frame_inicio, frame_stock, frame_ventas, frame_proveedores, frame_clientes, frame_carrito, frame_tickets]:
        frame.pack_forget()

# Frames
frame_inicio = Frame(ventana, bg="gray0")
frame_stock = Frame(ventana, bg="gray0")
frame_ventas = Frame(ventana, bg="gray0")
frame_proveedores = Frame(ventana, bg="gray0")
frame_clientes = Frame(ventana, bg="gray0")
frame_carrito = Frame(ventana, bg="gray0")
frame_tickets = Frame(ventana, bg="gray0")

# Frame de botones
frame_botones = Frame(ventana, bg="gray2")
frame_botones.pack(side=TOP, fill=X)

# Crear un frame interno para centrar los botones
frame_botones_interno = Frame(frame_botones, bg="spring green")
frame_botones_interno.pack(side=TOP)

# Frame inicio - Contenido de la página de inicio
try:
    logo = PhotoImage(file="celupng.png") 
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

def verProveedores():
    sacarFrames()
    frame_proveedores.pack(fill=BOTH, expand=True)

def verClientes():
    sacarFrames()
    frame_clientes.pack(fill=BOTH, expand=True)

def verCarrito():
    sacarFrames()
    frame_carrito.pack(fill=BOTH, expand=True)

def vertickets():
    sacarFrames()
    frame_tickets.pack(fill=BOTH, expand=True)

# Función para cerrar la aplicación
def cerrar():
    ventana.destroy()

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

botonCarrito = Button(frame_botones_interno, text="Ventas", command=verVentas, bg="spring green", fg="black")
botonCarrito.pack(side=LEFT, padx=5, pady=5)

botonTickets = Button(frame_botones_interno, text="Tickets", command=vertickets, bg="spring green", fg="black")
botonTickets.pack(side=LEFT, padx=5, pady=5)

# Ventana de stock
label_buscador =  Label(frame_stock, text="Busca un Articulo:", font=("Impact", 13), fg="spring green", bg="gray0")
label_buscador.pack(anchor=W, padx=20, pady=(21, 0))
entry_buscador = Entry(frame_stock, font=("Impact", 13), width=23, fg="snow", bg="gray0")
entry_buscador.pack(anchor=W, padx=20, pady=(21, 0))

# Inicialización de `articulos` como una lista vacía
articulos = []

#id
label_id = Label(frame_stock, text="ID:", font=("Impact", 13), fg="spring green", bg="gray0")
label_id.pack(anchor=W, padx=20, pady=(21, 0))
entry_id = Entry(frame_stock, font=("Impact", 13), width=23, fg="snow", bg="gray0")
entry_id.pack(anchor=W, padx=20, pady=(21, 0))

#cantidad
label_cantidad = Label(frame_stock, text="Cantidad:", font=("Impact", 13), fg="spring green", bg="gray0")
label_cantidad.pack(anchor=W, padx=20, pady=(21, 0))
entry_cantidad = Entry(frame_stock, font=("Impact", 13), width=23, fg="snow", bg="gray0")
entry_cantidad.pack(anchor=W, padx=20, pady=(21, 0))

#precio_costo
label_precio_costo = Label(frame_stock, text="Costo:", font=("Impact", 13), fg="spring green", bg="gray0")
label_precio_costo.pack(anchor=W, padx=20, pady=(21, 0))
entry_precio_costo = Entry(frame_stock, font=("Impact", 13), width=23, fg="snow", bg="gray0")
entry_precio_costo.pack(anchor=W, padx=20, pady=(21, 0))

#precio_final
label_precio_final = Label(frame_stock, text="Final:", font=("Impact", 13), fg="spring green", bg="gray0")
label_precio_final.pack(anchor=W, padx=20, pady=(21, 0))
entry_precio_final = Entry(frame_stock, font=("Impact", 13), width=23, fg="snow", bg="gray0")
entry_precio_final.pack(anchor=W, padx=20, pady=(21, 0))

#detalle
label_detalle = Label(frame_stock, text="Detalle:", font=("Impact", 13), fg="spring green", bg="gray0")
label_detalle.pack(anchor=W, padx=20, pady=(21, 0))
entry_detalle = Entry(frame_stock, font=("Impact", 13), width=33, fg="snow", bg="gray0")
entry_detalle.pack(anchor=W, padx=20, pady=(21, 0))

#####botones y funciones#####
def buscarProducto():
    if entry_buscador.get() == "":
        messagebox.showwarning("Mensaje por parte de FE!n", "Ingrese algo para buscar")
    else:
        conexion = None
        cursor = None
        try:
            # Conexión a la base de datos MySQL
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bdfinal2"  
            )
            if conexion.is_connected():
                cursor = conexion.cursor()

                
                cursor.execute("SHOW TABLES LIKE 'stock'")
                if cursor.fetchone() is None:
                    messagebox.showerror("Error", "La tabla 'stock' no existe en la base de datos.")
                    return

                
                buscar = (entry_buscador.get(),)  # Solo utiliza el valor ingresado para 'detalle'
                cursor.execute("SELECT * FROM stock WHERE detalle=%s", buscar)
                datos = cursor.fetchall()



                # Limpiar las entradas antes de mostrar los resultados
                entry_id.config(state="normal")
                entry_id.delete(0, END)
                entry_cantidad.config(state="normal")
                entry_cantidad.delete(0, 100)
                entry_precio_costo.delete(0, END)
                entry_precio_final.delete(0, END)
                entry_detalle.delete(0, END)

                # Mostrar los datos encontrados en los campos correspondientes
                if datos:
                    for dato in datos:
                        entry_id.insert(0, dato[0])
                        entry_cantidad.insert(0, dato[1])
                        entry_precio_costo.insert(0, dato[2])
                        entry_precio_final.insert(0, dato[3])
                        entry_detalle.insert(0, dato[4])
                else:
                    messagebox.showwarning("Mensaje por parte de FE!n", "Todavía no hay artículos :(")

        except mysql.connector.Error as err:
            # Muestra el error específico de MySQL
            messagebox.showerror("Error de MySQL", f"Se produjo un error: {err}")
        except Exception as e:
            # Muestra cualquier otro error de Python
            messagebox.showerror("Error", f"Se produjo un error: {str(e)}")
        finally:
            # Cerrar cursor y conexión si están abiertos
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

boton_buscar = Button(frame_stock, text="Buscar un Producto por Detalle", command=buscarProducto, bg="spring green", fg="black")
boton_buscar.pack(anchor=W, padx=20, pady=(21, 0))

#validar todos los campos#
def validar_campos_vacios():
    if not entry_id.get() or not entry_cantidad.get() or not entry_precio_costo.get() or not entry_precio_final.get() or not entry_detalle.get():
        messagebox.showerror("Error", "Todos los campos son obligatorios")

# Inicialización de `articulos` como una lista vacía
articulos = []

# Función `ver_stock` corregida
def ver_stock():
    ventana_stock = Toplevel()
    ventana_stock.title("Stock disponible")
    listbox = Listbox(ventana_stock, width=600, height=400)
    listbox.pack(pady=10)
    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Verificar que la tabla 'stock' existe
        cursor.execute("SHOW TABLES LIKE 'stock'")
        if cursor.fetchone() is None:
            messagebox.showerror("Error", "La tabla 'stock' no existe en la base de datos.")
            return

        # Realizar la consulta para obtener todos los artículos
        cursor.execute("SELECT * FROM stock")
        articulos = cursor.fetchall()

        # Insertar los artículos en el Listbox
        if articulos:
            for articulo in articulos:
                listbox.insert(tk.END, f"ID: {articulo[0]}, Cantidad: {articulo[1]}, Costo: {articulo[2]}, Final: {articulo[3]}, Detalle: {articulo[4]}")
        else:
            listbox.insert(tk.END, "No hay artículos en stock.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error de MySQL", f"Se produjo un error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error: {str(e)}")
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

boton_ver_stock = Button(frame_stock, text="Ver Stock", command=ver_stock, bg="spring green", fg="black")
boton_ver_stock.pack(side=LEFT, padx=20, pady=(21, 0))

# Función `agregar_articulo`
def agregar_articulo():
    id_artagregar = entry_id.get()
    cantidad = entry_cantidad.get()
    precio_costo = entry_precio_costo.get()
    precio_final = entry_precio_final.get()
    detalle = entry_detalle.get()

    if not id_artagregar or not cantidad or not precio_costo or not precio_final or not detalle:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    articulo = {
        'id': id_artagregar,
        'cantidad': cantidad,
        'costo': precio_costo,
        'final': precio_final,
        'detalle': detalle
    }

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO stock (id, cantidad, precio_costo, precio_final, detalle)
            VALUES (%s, %s, %s, %s, %s)
        """, (articulo['id'], articulo['cantidad'], articulo['costo'], articulo['final'], articulo['detalle']))
        conexion.commit()
        messagebox.showinfo("Información", "Artículo agregado correctamente")
        
        # Limpiar campos después de agregar
        entry_id.delete(0, END)
        entry_cantidad.delete(0, 100)
        entry_precio_costo.delete(0, END)
        entry_precio_final.delete(0, END)
        entry_detalle.delete(0, END)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar el artículo: {err}")
    finally:
        cursor.close()
        conexion.close()

boton_agregar = Button(frame_stock, text="Agregar", command=agregar_articulo, bg="spring green", fg="black")
boton_agregar.pack(side=LEFT, padx=20, pady=(21, 0))

def actualizar_articulo():
    id = entry_id.get()
    cantidad = entry_cantidad.get()
    precio_costo = entry_precio_costo.get()
    precio_final = entry_precio_final.get()
    detalle = entry_detalle.get()
    if not id or not cantidad or not precio_costo or not precio_final or not detalle:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    for item in articulos:
        if item['id'] == id:
            item['cantidad'] = cantidad
            item['costo'] = precio_costo
            item['final'] = precio_final
            item['detalle'] = detalle
            messagebox.showinfo("Informacion", "Articulo actualizado correctamente")
            return
    messagebox.showerror("Error", "Articulo no encontrado")
boton_actualizar = Button(frame_stock, text="Actualizar", command=actualizar_articulo, bg="spring green", fg="black")
boton_actualizar.pack(side=LEFT, padx=20, pady=(21, 0))

def eliminar_articulo():
    id = entry_id.get()
    for item in articulos:
        if item['id'] == id:
            articulos.remove(item)
            messagebox.showinfo("Informacion", "Articulo eliminado correctamente")
            return
    messagebox.showerror("Error", "Articulo no encontrado")
boton_eliminar = Button(frame_stock, text="Eliminar", command=eliminar_articulo, bg="spring green", fg="black")
boton_eliminar.pack(side=LEFT, padx=20, pady=(21, 0))

def limpiar_campos():
    entry_buscador.delete(0, END)
    entry_id.delete(0, END)
    entry_cantidad.delete(0, 100)
    entry_precio_costo.delete(0, END)
    entry_precio_final.delete(0, END)
    entry_detalle.delete(0, END)
boton_limpiar = Button(frame_stock, text="Limpiar", command=limpiar_campos, bg="spring green", fg="black")
boton_limpiar.pack(side=LEFT, padx=20, pady=(21, 0))

def ver_stock():
    ventana_stock = Toplevel()
    ventana_stock.title("Stock disponible")
    listbox = Listbox(ventana_stock, width=600, height=400)
    listbox.pack(pady=10)

    # Llenado del Listbox con los datos
    for item in articulos:
        listbox.insert(END, f"ID: {item['id']}, Cantidad: {item['cantidad']}")

    btn_cerrar = Button(ventana_stock, text="Cerrar", command=ventana_stock.destroy)
    btn_cerrar.pack(pady=10)

# Corrección del botón para `ver_stock`
boton_ver_stock = Button(frame_stock, text="Ver Stock", command=ver_stock, bg="spring green", fg="black")
boton_ver_stock.pack(side=LEFT , padx=20, pady=(21, 0))


# Ventana de ventas

# Ventana de proveedor

# Ventana de clientes


# Mostrar el frame de inicio al iniciar la aplicación
verInicio()
# Iniciar ventana

ventana.mainloop()

# Cerrar cursor y conexión
cursor.close()
conexion.close()