
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="semana8"
    )

# Funciones CRUD
def agregar_objeto():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        query = "INSERT INTO fauna_flora (nombre_cientifico, habitat, estado_conservacion, region_geografica) VALUES (%s, %s, %s, %s)"
        values = (entry_nombre_cientifico.get(), entry_habitat.get(), entry_estado_conservacion.get(), entry_region_geografica.get())
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        mostrar_lista()
        messagebox.showinfo("Éxito", "Objeto agregado correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar objeto: {err}")

def mostrar_lista():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fauna_flora")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        for row in tree.get_children():
            tree.delete(row)
        
        for row in rows:
            tree.insert("", "end", values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al mostrar lista: {err}")

def borrar_objeto():
    selected_item = tree.selection()[0]
    id = tree.item(selected_item)['values'][0]
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fauna_flora WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        tree.delete(selected_item)
        messagebox.showinfo("Éxito", "Objeto eliminado correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al borrar objeto: {err}")

def actualizar_objeto():
    selected_item = tree.selection()[0]
    id = tree.item(selected_item)['values'][0]
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        query = """UPDATE fauna_flora 
                   SET nombre_cientifico = %s, habitat = %s, estado_conservacion = %s, region_geografica = %s 
                   WHERE id = %s"""
        values = (entry_nombre_cientifico.get(), entry_habitat.get(), entry_estado_conservacion.get(), entry_region_geografica.get(), id)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        mostrar_lista()
        messagebox.showinfo("Éxito", "Objeto actualizado correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al actualizar objeto: {err}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Fauna/Flora")

# Etiquetas y campos de entrada
tk.Label(root, text="Nombre Científico").grid(row=0, column=0)
entry_nombre_cientifico = tk.Entry(root)
entry_nombre_cientifico.grid(row=0, column=1)

tk.Label(root, text="Hábitat").grid(row=1, column=0)
entry_habitat = tk.Entry(root)
entry_habitat.grid(row=1, column=1)

tk.Label(root, text="Estado de Conservación").grid(row=2, column=0)
entry_estado_conservacion = tk.Entry(root)
entry_estado_conservacion.grid(row=2, column=1)

tk.Label(root, text="Región Geográfica").grid(row=3, column=0)
entry_region_geografica = tk.Entry(root)
entry_region_geografica.grid(row=3, column=1)

tk.Button(root, text="Agregar", command=agregar_objeto).grid(row=4, column=0)
tk.Button(root, text="Actualizar", command=actualizar_objeto).grid(row=4, column=1)
tk.Button(root, text="Eliminar", command=borrar_objeto).grid(row=4, column=2)

# Tabla para mostrar objetos
columns = ("ID", "Nombre Científico", "Hábitat", "Estado de Conservación", "Región Geográfica")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=3)

mostrar_lista()

root.mainloop()
