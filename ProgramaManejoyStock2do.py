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
ventana.state("zoomed")
ventana.title("Celu PRO")

# Manejo de error en el icono
try:
    ventana.iconbitmap("celu.ico")
except Exception as e:
    messagebox.showwarning("Advertencia", f"No se encontró el ícono: {e}")

def sacarFrames():
    for frame in [frame_inicio, frame_stock, frame_ventas, frame_proveedores, frame_clientes]:
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
frame_botones = Frame(ventana, bg="spring green")
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
    ver_ventas()
def verProveedores():
    sacarFrames()
    frame_proveedores.pack(fill=BOTH, expand=True)
    ver_proveedores()
def verClientes():
    sacarFrames()
    frame_clientes.pack(fill=BOTH, expand=True)
    ver_clientes()

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

botonCarrito = Button(frame_botones_interno, text="Carrito  ", command=verVentas, bg="spring green", fg="black")
botonCarrito.pack(side=LEFT, padx=5, pady=5)

botonTickets = Button(frame_botones_interno, text="Tickets", command=vertickets, bg="spring green", fg="black")
botonTickets.pack(side=LEFT, padx=5, pady=5)

# Ventana de stock
label_buscador =  Label(frame_stock, text="Busca un Articulo:", font=("Impact", 13), fg="spring green", bg="gray0")
label_buscador.pack(anchor=W, padx=20, pady=(21, 0))
entry_buscador = Entry(frame_stock, font=("Impact", 13), width=23, fg="gray0", bg="snow")
entry_buscador.pack(anchor=W, padx=20, pady=(21, 0))

# ID label and entry (which will show the next available code)
label_id = Label(frame_stock, text="ID:", font=("Impact", 13), fg="spring green", bg="gray0")
label_id.pack(anchor="w", padx=20, pady=(21, 0))
entry_id = Entry(frame_stock, font=("Impact", 13), width=23, fg="gray0", bg="snow", state="readonly")
entry_id.pack(anchor="w", padx=20, pady=(21, 0))

def obtener_id_nuevo():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Obtener el código más alto actual
        cursor.execute("SELECT MAX(id) FROM stock")  # Cambia 'productos' a 'stock' si es necesario
        max_codigo = cursor.fetchone()[0]

        # Asignar el nuevo código (siguiente disponible)
        nuevo_codigo = int(max_codigo) + 1 if max_codigo is not None else 1

        # Asignar el nuevo código al Entry
        entry_id.config(state="normal")
        entry_id.delete(0, END)
        entry_id.insert(0, str(nuevo_codigo))
        entry_id.config(state="readonly")

    except mysql.connector.Error as err:
        messagebox.showerror("Error de MySQL", f"Error al obtener el código: {err}")
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

# Asegúrate de llamar a esta función en el inicio de tu aplicación
obtener_id_nuevo()

#cantidad
label_cantidad = Label(frame_stock, text="Cantidad:", font=("Impact", 13), fg="spring green", bg="gray0")
label_cantidad.pack(anchor=W, padx=20, pady=(21, 0))
entry_cantidad = Entry(frame_stock, font=("Impact", 13), width=23, fg="gray0", bg="snow")
entry_cantidad.pack(anchor=W, padx=20, pady=(21, 0))

#precio_costo
label_precio_costo = Label(frame_stock, text="Costo:", font=("Impact", 13), fg="spring green", bg="gray0")
label_precio_costo.pack(anchor=W, padx=20, pady=(21, 0))
entry_precio_costo = Entry(frame_stock, font=("Impact", 13), width=23, fg="gray0", bg="snow")
entry_precio_costo.pack(anchor=W, padx=20, pady=(21, 0))

#precio_final
label_precio_final = Label(frame_stock, text="Final:", font=("Impact", 13), fg="spring green", bg="gray0")
label_precio_final.pack(anchor=W, padx=20, pady=(21, 0))
entry_precio_final = Entry(frame_stock, font=("Impact", 13), width=23, fg="gray0", bg="snow")
entry_precio_final.pack(anchor=W, padx=20, pady=(21, 0))

#detalle
label_detalle = Label(frame_stock, text="Detalle:", font=("Impact", 13), fg="spring green", bg="gray0")
label_detalle.pack(anchor=W, padx=20, pady=(21, 0))
entry_detalle = Entry(frame_stock, font=("Impact", 13), width=33, fg="gray0", bg="snow")
entry_detalle.pack(anchor=W, padx=20, pady=(21, 0))

#####botones y funciones#####
def buscarProducto():
    if entry_buscador.get() == "":
        messagebox.showwarning("Mensaje por parte de FE!N", "Ingrese algo para buscar")
        return

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
            entry_cantidad.delete(0, END)
            entry_precio_costo.delete(0, END)
            entry_precio_final.delete(0, END)
            entry_detalle.delete(0, END)

            # Mostrar los datos encontrados en los campos correspondientes
            if datos:
                for dato in datos:
                    entry_id.delete(0, END)  # Limpiar el campo ID antes de insertar
                    entry_id.insert(0, dato[0])  # Asignar el ID encontrado
                    entry_cantidad.insert(0, dato[1])
                    entry_precio_costo.insert(0, dato[2])
                    entry_precio_final.insert(0, dato[3])
                    entry_detalle.insert(0, dato[4])
            else:
                messagebox.showwarning("Mensaje por parte de FE!N", "Todavía no hay artículos :(")

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

# Función `ver_stock`
def ver_stock():
    ventana_stock = Toplevel()
    ventana_stock.title("Stock disponible")
    listbox = Listbox(ventana_stock, width=100, height=40)
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

        obtener_id_nuevo()  # Obtener el nuevo ID


    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar el artículo: {err}")
    finally:
        cursor.close()
        conexion.close()

boton_agregar = Button(frame_stock, text="Agregar", command=agregar_articulo, bg="spring green", fg="black")
boton_agregar.pack(side=LEFT, padx=20, pady=(21, 0))

def actualizar_articulo():
    id_articulo = entry_id.get()
    cantidad = entry_cantidad.get()
    precio_costo = entry_precio_costo.get()
    precio_final = entry_precio_final.get()
    detalle = entry_detalle.get()

    # Verificar si todos los campos están llenos
    if not id_articulo or not cantidad or not precio_costo or not precio_final or not detalle:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Verificar si el artículo con el ID especificado existe en la base de datos
        cursor.execute("SELECT * FROM stock WHERE id = %s", (id_articulo,))
        articulo_existente = cursor.fetchone()

        if articulo_existente:
            # Si el artículo existe, actualizar sus valores en la base de datos
            cursor.execute("""
                UPDATE stock SET cantidad = %s, precio_costo = %s, precio_final = %s, detalle = %s WHERE id = %s
            """, (cantidad, precio_costo, precio_final, detalle, id_articulo))
            conexion.commit()
            messagebox.showinfo("Información", "Artículo actualizado correctamente")
            # Limpiar los campos después de agregar
            entry_id.delete(0, END) 
            entry_cantidad.delete(0, END)
            entry_precio_costo.delete(0, END)
            entry_precio_final.delete(0, END)
            entry_detalle.delete(0, END)

         # Llamar a obtener_codigo_nuevo() si es necesario (esto depende de tu implementación)
            obtener_id_nuevo()  # Puedes ajustar esta llamada si necesitas mostrar el nuevo ID

        else:
            # Si el artículo no existe, mostrar un mensaje de error
            messagebox.showerror("Error", "Artículo no encontrado")

    except mysql.connector.Error as err:
        # Muestra el error específico de MySQL
        messagebox.showerror("Error de MySQL", f"Se produjo un error: {err}")
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

boton_actualizar = Button(frame_stock, text="Actualizar", command=actualizar_articulo, bg="spring green", fg="black")
boton_actualizar.pack(side=LEFT, padx=20, pady=(21, 0))

def eliminar_articulo():
    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Verificar si el artículo con el ID especificado existe en la base de datos
        cursor.execute("SELECT * FROM stock WHERE id = %s", (entry_id.get(),))
        articulo_existente = cursor.fetchone()

        # Preguntar al usuario si está seguro de eliminar el artículo
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este artículo?")
    
        if not respuesta:  # Si el usuario elige "No", salimos de la función
            return

        if articulo_existente:
            # Si el artículo existe, eliminarlo de la base de datos
            cursor.execute("DELETE FROM stock WHERE id = %s", (entry_id.get(),))
            conexion.commit()  # Confirmar la eliminación
            messagebox.showinfo("Información", "Artículo eliminado correctamente")
            # Limpiar los campos después de agregar
            entry_cantidad.delete(0, END)
            entry_precio_costo.delete(0, END)
            entry_precio_final.delete(0, END)
            entry_detalle.delete(0, END)
            
            # Llamar a obtener_codigo_nuevo() si es necesario (esto depende de tu implementación)
            obtener_id_nuevo()  # Puedes ajustar esta llamada si necesitas mostrar el nuevo ID
        else:
            # Si el artículo no existe, mostrar un mensaje de error
            messagebox.showerror("Error", "Artículo no encontrado")

    except mysql.connector.Error as err:
        # Muestra el error específico de MySQL
        messagebox.showerror("Error de MySQL", f"Se produjo un error: {err}")
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

    # Limpiar los campos de entrada
    entry_id.delete(0, END)
    entry_cantidad.delete(0, END)
    entry_precio_costo.delete(0, END)
    entry_precio_final.delete(0, END)
    entry_detalle.delete(0, END)

boton_eliminar = Button(frame_stock, text="Eliminar", command=eliminar_articulo, bg="spring green", fg="black")
boton_eliminar.pack(side=LEFT, padx=20, pady=(21, 0))

def limpiar_campos():
    entry_buscador.delete(0, END)
    entry_id.delete(0, END)
    entry_cantidad.delete(0, 100)
    entry_precio_costo.delete(0, END)
    entry_precio_final.delete(0, END)
    entry_detalle.delete(0, END)

    # Obtener el nuevo ID máximo
    obtener_id_nuevo()  # Llama a la función que actualiza el ID

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

# Frame de Proveedores
# Función para mostrar los proveedores en el Treeview dentro de frame_proveedores
def ver_proveedores():
    # Limpiar cualquier widget anterior en el frame_proveedores
    for widget in frame_proveedores.winfo_children():
        widget.destroy()

    # Crear el Treeview dentro de frame_proveedores
    global tree  # Definir tree como global para que sea accesible en otras funciones
    tree = ttk.Treeview(frame_proveedores, columns=("ID", "Nombre", "Costo", "Fecha", "Detalle"), show="headings", height=15)
    
    # Configurar el estilo de la tabla
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 10))

    # Definir encabezados de columna
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Costo", text="Costo")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Detalle", text="Detalle")

    # Ajustar el ancho de las columnas
    tree.column("ID", width=50)
    tree.column("Nombre", width=150)
    tree.column("Costo", width=100)
    tree.column("Fecha", width=100)
    tree.column("Detalle", width=200)

    # Crear las barras de desplazamiento dentro de frame_proveedores
    scrollbar_y = ttk.Scrollbar(frame_proveedores, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame_proveedores, orient="horizontal", command=tree.xview)

    # Asignar las barras de desplazamiento al Treeview
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Colocar el Treeview y las barras de desplazamiento en el Grid
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    # Crear un botón para agregar un nuevo proveedor, debajo de la tabla
    btn_agregar = tk.Button(frame_proveedores, text="Agregar Proveedor", command=abrir_ventana_agregar)
    btn_agregar.grid(row=2, column=0, pady=10, sticky="ew")  # Ubicar el botón debajo de la tabla

    # Asegurar que el frame_proveedores expanda el Treeview al redimensionarse
    frame_proveedores.grid_rowconfigure(0, weight=1)
    frame_proveedores.grid_columnconfigure(0, weight=1)

    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Verificar que la tabla 'proveedores' existe
        cursor.execute("SHOW TABLES LIKE 'proveedores'")
        if cursor.fetchone() is None:
            messagebox.showerror("Error", "La tabla 'proveedores' no existe en la base de datos.")
            return

        # Realizar la consulta para obtener todos los proveedores
        cursor.execute("SELECT * FROM proveedores")
        proveedores = cursor.fetchall()

        # Insertar los proveedores en el Treeview
        if proveedores:
            for proveedor in proveedores:
                tree.insert("", tk.END, values=(proveedor[0], proveedor[1], proveedor[2], proveedor[3], proveedor[4]))
        else:
            messagebox.showinfo("Información", "No hay Proveedores.")

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

def abrir_ventana_agregar():
    # Crear la ventana emergente
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Proveedor")
    # Etiquetas y campos de entrada para cada campo de proveedor
    def obtener_id_nuevo2():
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Obtener el código más alto actual
        cursor.execute("SELECT MAX(id) FROM proveedores")  # Cambia 'productos' a 'stock' si es necesario
        max_codigo2 = cursor.fetchone()[0]

        # Asignar el nuevo código (siguiente disponible)
        nuevo_codigo2 = int(max_codigo2) + 1 if max_codigo2 is not None else 1
        return nuevo_codigo2
    
    
    tk.Label(ventana_agregar, text="ID:").grid(row=0, column=0, padx=10, pady=5)
    entry_id = tk.Entry(ventana_agregar)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    entry_id.delete(0,END)
    max_id_proveedor=obtener_id_nuevo2()
    entry_id.insert(END,max_id_proveedor)
    entry_id.config(state="readonly")

    tk.Label(ventana_agregar, text="Nombre:").grid(row=1, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(ventana_agregar)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar, text="Costo:").grid(row=2, column=0, padx=10, pady=5)
    entry_costo = tk.Entry(ventana_agregar)
    entry_costo.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar, text="Fecha:").grid(row=3, column=0, padx=10, pady=5)
    entry_fecha = tk.Entry(ventana_agregar)
    entry_fecha.grid(row=3, column=1, padx=10, pady=5)
    entry_fecha.delete(0,END)
    #obtener fecha y hora actual
    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y")
    entry_fecha.insert(END,fecha)
    entry_fecha.config(state="readonly")

    entry_fecha.config(state="readonly")

    tk.Label(ventana_agregar, text="Detalle:").grid(row=4, column=0, padx=10, pady=5)
    entry_detalle = tk.Entry(ventana_agregar)
    entry_detalle.grid(row=4, column=1, padx=10, pady=5)

    # Botón para guardar el proveedor
    btn_guardar = tk.Button(
        ventana_agregar,
        text="Guardar",
        command=lambda: guardar_proveedor(entry_id.get(), entry_nombre.get(), entry_costo.get(), entry_fecha.get(), entry_detalle.get(), ventana_agregar)
    )
    btn_guardar.grid(row=5, column=0, columnspan=2, pady=10)

# Función para guardar un nuevo proveedor en la base de datos
def guardar_proveedor(id, nombre, costo, fecha, detalle, ventana_agregar):
    # Validación básica
    if not id or not nombre or not costo or not fecha or not detalle:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return

    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Insertar el nuevo proveedor en la tabla 'proveedores'
        cursor.execute("INSERT INTO proveedores (ID, nombre, costo, fecha, detalle) VALUES (%s, %s, %s, %s, %s)", (id, nombre, costo, fecha, detalle))
        conexion.commit()

        messagebox.showinfo("Éxito", "Proveedor agregado exitosamente.")
        ventana_agregar.destroy()  # Cerrar la ventana de agregar

        # Actualizar la lista de proveedores después de agregar uno nuevo
        ver_proveedores()  # Asegúrate de que esta función esté definida para actualizar la tabla

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

# Ventana de clientes
# Función para mostrar los proveedores en el Treeview dentro de frame_clientes
def ver_clientes():
    # Limpiar cualquier widget anterior en el frame_clientes
    for widget in frame_clientes.winfo_children():
        widget.destroy()

    # Crear el Treeview dentro de frame_clientes
    global tree  # Definir tree como global para que sea accesible en otras funciones
    tree = ttk.Treeview(frame_clientes, columns=("ID", "nombre_y_apellido", "Fecha", "Detalle"), show="headings", height=15)
    
    # Configurar el estilo de la tabla
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 10))

    # Definir encabezados de columna
    tree.heading("ID", text="ID")
    tree.heading("nombre_y_apellido", text="nombre_y_apellido")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Detalle", text="Detalle")

    # Ajustar el ancho de las columnas
    tree.column("ID", width=50)
    tree.column("nombre_y_apellido", width=150)
    tree.column("Fecha", width=100)
    tree.column("Detalle", width=200)

    # Crear las barras de desplazamiento dentro de frame_clientes
    scrollbar_y = ttk.Scrollbar(frame_clientes, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame_clientes, orient="horizontal", command=tree.xview)

    # Asignar las barras de desplazamiento al Treeview
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Colocar el Treeview y las barras de desplazamiento en el Grid
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    # Crear un botón para agregar un nuevo proveedor, debajo de la tabla
    btn_agregar = tk.Button(frame_clientes, text="Agregar cliente", command=abrir_ventana_agregar2)
    btn_agregar.grid(row=2, column=0, pady=10, sticky="ew")  # Ubicar el botón debajo de la tabla

    # Asegurar que el frame_clientes expanda el Treeview al redimensionarse
    frame_clientes.grid_rowconfigure(0, weight=1)
    frame_clientes.grid_columnconfigure(0, weight=1)

    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Verificar que la tabla 'clientes' existe
        cursor.execute("SHOW TABLES LIKE 'clientes'")
        if cursor.fetchone() is None:
            messagebox.showerror("Error", "La tabla 'clientes' no existe en la base de datos.")
            return

        # Realizar la consulta para obtener todos los clientes
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

        # Insertar los clientes en el Treeview
        if clientes:
            for cliente in clientes:
                tree.insert("", tk.END, values=(cliente[0], cliente[1], cliente[2], cliente[3]))
        else:
            messagebox.showinfo("Información", "No hay Clientes.")

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

def abrir_ventana_agregar2():
    # Crear la ventana emergente
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Clientes")
    # Etiquetas y campos de entrada para cada campo de proveedor
    def obtener_id_nuevo3():
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Obtener el código más alto actual
        cursor.execute("SELECT MAX(id) FROM clientes")
        max_codigo3 = cursor.fetchone()[0]

        # Asignar el nuevo código (siguiente disponible)
        nuevo_codigo3 = int(max_codigo3) + 1 if max_codigo3 is not None else 1
        return nuevo_codigo3
    
    
    tk.Label(ventana_agregar, text="ID:").grid(row=0, column=0, padx=10, pady=5)
    entry_id = tk.Entry(ventana_agregar)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    entry_id.delete(0,END)
    max_id_cliente=obtener_id_nuevo3()
    entry_id.insert(END,max_id_cliente)
    entry_id.config(state="readonly")

    tk.Label(ventana_agregar, text="Nombre:").grid(row=1, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(ventana_agregar)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar, text="Fecha:").grid(row=2, column=0, padx=10, pady=5)
    entry_fecha = tk.Entry(ventana_agregar)
    entry_fecha.grid(row=2, column=1, padx=10, pady=5)
    entry_fecha.delete(0,END)
    #obtener fecha y hora actual
    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y")
    entry_fecha.insert(END,fecha)
    entry_fecha.config(state="readonly")

    entry_fecha.config(state="readonly")

    tk.Label(ventana_agregar, text="Detalle:").grid(row=3, column=0, padx=10, pady=5)
    entry_detalle = tk.Entry(ventana_agregar)
    entry_detalle.grid(row=3, column=1, padx=10, pady=5)

    # Botón para guardar el proveedor
    btn_guardar = tk.Button(
        ventana_agregar,
        text="Guardar",
        command=lambda: guardar_cliente(entry_id.get(), entry_nombre.get(), entry_fecha.get(), entry_detalle.get(), ventana_agregar)
    )
    btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)

# Función para guardar un nuevo proveedor en la base de datos
def guardar_cliente(id, nombre, fecha, detalle, ventana_agregar):
    # Validación básica
    if not id or not nombre or not fecha or not detalle:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return

    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Insertar el nuevo proveedor en la tabla 'clientes'
        cursor.execute("INSERT INTO clientes (ID, nombre, fecha, detalle) VALUES (%s, %s, %s, %s)", (id, nombre, fecha, detalle))
        conexion.commit()

        messagebox.showinfo("Éxito", "Cliente agregado exitosamente.")
        ventana_agregar.destroy()  # Cerrar la ventana de agregar

        # Actualizar la lista de proveedores después de agregar uno nuevo
        ver_clientes()  # Asegúrate de que esta función esté definida para actualizar la tabla

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

# Ventana de ventas
# Función para mostrar los proveedores en el Treeview dentro de frame_ventas
def ver_ventas():
    # Limpiar cualquier widget anterior en el frame_ventas
    for widget in frame_ventas.winfo_children():
        widget.destroy()

    # Crear el Treeview dentro de frame_ventas
    global tree  # Definir tree como global para que sea accesible en otras funciones
    tree = ttk.Treeview(frame_ventas, columns=("ID","tof", "Fecha", "detalle o ST", "cantidad", "total"), show="headings", height=15)
    
    # Configurar el estilo de la tabla
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 10))

    # Definir encabezados de columna
    tree.heading("ID", text="ID")
    tree.heading("tof", text="Tarjeta o Efectivo")
    tree.heading("Fecha", text="Fecha")
    tree.heading("detalle o ST", text="detalle o ST")
    tree.heading("cantidad", text="cantidad")
    tree.heading("total", text="total")
    # Ajustar el ancho de las columnas
    tree.column("ID", width=50)
    tree.column("tof", width=150)
    tree.column("Fecha", width=100)
    tree.column("detalle o ST", width=200)
    tree.column("cantidad", width=100)
    tree.column("total", width=100)

    # Crear las barras de desplazamiento dentro de frame_ventas
    scrollbar_y = ttk.Scrollbar(frame_ventas, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame_ventas, orient="horizontal", command=tree.xview)

    # Asignar las barras de desplazamiento al Treeview
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Colocar el Treeview y las barras de desplazamiento en el Grid
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    # Crear un botón para agregar un nuevo proveedor, debajo de la tabla
    btn_agregar2 = tk.Button(frame_ventas, text="Agregar venta", command=abrir_ventana_agregar3)
    btn_agregar2.grid(row=2, column=0, pady=10, sticky="ew")  # Ubicar el botón debajo de la tabla

    # Asegurar que el frame_clientes expanda el Treeview al redimensionarse
    frame_ventas.grid_rowconfigure(0, weight=1)
    frame_ventas.grid_columnconfigure(0, weight=1)

    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Verificar que la tabla 'ventas' existe
        cursor.execute("SHOW TABLES LIKE 'ventas'")
        if cursor.fetchone() is None:
            messagebox.showerror("Error", "La tabla 'ventas' no existe en la base de datos.")
            return

        # Realizar la consulta para obtener todos los ventas
        cursor.execute("SELECT * FROM ventas")
        ventas = cursor.fetchall()

        # Insertar las ventas en el Treeview
        if ventas:
            for venta in ventas:
                tree.insert("", tk.END, values=(venta[0], venta[1], venta[2], venta[3], venta[4], venta[5]))
        else:
            messagebox.showinfo("Información", "No hay Ventas.")

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

def abrir_ventana_agregar3():
    # Crear la ventana emergente
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Ventas")
    # Etiquetas y campos de entrada para cada campo de proveedor
    def obtener_id_nuevo4():
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Obtener el código más alto actual
        cursor.execute("SELECT MAX(id) FROM ventas")
        max_codigo4 = cursor.fetchone()[0]

        # Asignar el nuevo código (siguiente disponible)
        nuevo_codigo4 = int(max_codigo4) + 1 if max_codigo4 is not None else 1
        return nuevo_codigo4
    
    
    tk.Label(ventana_agregar, text="ID:").grid(row=0, column=0, padx=10, pady=5)
    entry_id = tk.Entry(ventana_agregar)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    entry_id.delete(0,END)
    max_id_venta=obtener_id_nuevo4()
    entry_id.insert(END,max_id_venta)
    entry_id.config(state="readonly")

    tk.Label(ventana_agregar, text="toe:").grid(row=1, column=0, padx=10, pady=5)
    entry_toe = tk.Entry(ventana_agregar)
    entry_toe.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar, text="Fecha:").grid(row=2, column=0, padx=10, pady=5)
    entry_fecha = tk.Entry(ventana_agregar)
    entry_fecha.grid(row=2, column=1, padx=10, pady=5)
    entry_fecha.delete(0,END)
    #obtener fecha y hora actual
    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y")
    entry_fecha.insert(END,fecha)
    entry_fecha.config(state="readonly")

    entry_fecha.config(state="readonly")

    tk.Label(ventana_agregar, text="Detalle o ST:").grid(row=3, column=0, padx=10, pady=5)
    entry_detalle = tk.Entry(ventana_agregar)
    entry_detalle.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar, text="cantidad:").grid(row=4, column=0, padx=10, pady=5)
    entry_cantidad = tk.Entry(ventana_agregar)
    entry_cantidad.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar, text="total:").grid(row=5, column=0, padx=10, pady=5)
    entry_total = tk.Entry(ventana_agregar)
    entry_total.grid(row=5, column=1, padx=10, pady=5)

    # Botón para guardar venta
    btn_guardar = tk.Button(
        ventana_agregar,
        text="Guardar",
        command=lambda: guardar_venta(entry_id.get(), entry_toe.get(), entry_fecha.get(), entry_detalle.get(), entry_cantidad.get(), entry_total.get(), ventana_agregar)
    )
    btn_guardar.grid(row=6, column=0, columnspan=2, pady=10)

# Función para guardar un nuevo venta en la base de datos
def guardar_venta(id, toe, fecha, detalle, cantidad, total, ventana_agregar):
    # Validación básica
    if not id or not cantidad or not total or not detalle:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return

    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bdfinal2"
        )
        cursor = conexion.cursor()

        # Insertar la nueva venta en la tabla 'ventas'
        cursor.execute("INSERT INTO ventas (id, toe, Fecha, detalle o ST, cantidad, total) VALUES (%s, %s, %s, %s, %s, %s)", (id, toe, fecha, detalle, cantidad, total))
        conexion.commit()

        messagebox.showinfo("Éxito", "  venta agregada exitosamente.")
        ventana_agregar.destroy()  # Cerrar la ventana de agregar

        # Actualizar la lista de proveedores después de agregar uno nuevo
        ver_ventas()  # Asegúrate de que esta función esté definida para actualizar la tabla

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
# Ventana de carrito

# Ventana de tickets

# Mostrar el frame de inicio al iniciar la aplicación
verInicio()
# Iniciar ventana

ventana.mainloop()

# Cerrar cursor y conexión
cursor.close()
conexion.close()
