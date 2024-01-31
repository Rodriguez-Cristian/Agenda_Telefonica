import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import json


class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda")

        # Inicializar variables
        self.telefono_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.ubicacion_var = tk.StringVar()
        self.otros_var = tk.StringVar()

        # Crear la interfaz gráfica
        ttk.Label(root, text="Teléfono:").grid(row=0, column=0,padx=15,pady=10)
        ttk.Entry(root, textvariable=self.telefono_var).grid(row=0, column=1)
        ttk.Label(root, text="Nombre:").grid(row=1, column=0,padx=15,pady=10)
        ttk.Entry(root, textvariable=self.nombre_var).grid(row=1, column=1)
        ttk.Label(root, text="Ubicación:").grid(row=2, column=0,padx=15,pady=10)
        ttk.Entry(root, textvariable=self.ubicacion_var).grid(row=2, column=1)
        ttk.Label(root, text="Otros:").grid(row=3, column=0,padx=15,pady=10)
        ttk.Entry(root, textvariable=self.otros_var).grid(row=3, column=1)

        # Botones
        ttk.Button(root, text="Guardar",bootstyle="success", command=self.guardar_contacto).grid(row=4, column=0,padx=3,pady=3)
        ttk.Button(root, text="Eliminar por Nombre", bootstyle="danger", command=self.eliminar_por_nombre).grid(row=4, column=1, padx=3, pady=3)
        ttk.Button(root, text="Buscar por Nombre",bootstyle="info", command=self.buscar_por_nombre).grid(row=5, column=0,padx=3,pady=3)
        ttk.Button(root, text="Buscar por Ubicación",bootstyle="info", command=self.buscar_por_ubicacion).grid(row=5, column=1,padx=3,pady=3)

        # Cargar datos existentes
        self.cargar_datos()
        # Centrar la ventana en la pantalla
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)

        # Establecer el tamaño de la ventana (por ejemplo, 600x400)
        self.root.geometry("340x270+{}+{}".format(x, y))
        
        # Hacer que la ventana no sea redimensionable
        self.root.resizable(width=False, height=False)
        # Cambiar el icono de la ventana
        self.root.iconbitmap('agenda.ico') 
    def guardar_contacto(self):
        contacto = {
            "telefono": self.telefono_var.get(),
            "nombre": self.nombre_var.get(),
            "ubicacion": self.ubicacion_var.get(),
            "otros": self.otros_var.get()
        }

        # Cargar datos existentes
        datos = self.cargar_datos()

        # Agregar el nuevo contacto
        datos.append(contacto)

        # Guardar los datos en el archivo
        with open("agenda_data.json", "w") as file:
            json.dump(datos, file, indent=4)

        messagebox.showinfo("Guardado", "Contacto guardado exitosamente.")

        # Limpiar los campos después de guardar
        self.limpiar_campos()

    def buscar_por_nombre(self):
        nombre_buscado = self.nombre_var.get()

        # Cargar datos existentes
        datos = self.cargar_datos()

        # Buscar el contacto por nombre (si el nombre buscado está contenido en el nombre del contacto)
        resultados = [contacto for contacto in datos if nombre_buscado.lower() in contacto["nombre"].lower()]

        if resultados:
            mensaje_resultados = "\n\n".join([f"Nombre: {c['nombre']}, Teléfono: {c['telefono']}, Ubicación: {c['ubicacion']}, Otros: {c['otros']}" for c in resultados])
            messagebox.showinfo("\nResultados", f"Contacto(s) encontrado(s):\n{mensaje_resultados}")
            return resultados
        else:
            messagebox.showinfo("\nResultados", "No se encontraron contactos con ese nombre.")


    def buscar_por_ubicacion(self):
        ubicacion_buscada = self.ubicacion_var.get().lower()
      
        # Cargar datos existentes
        datos = self.cargar_datos()

        # Buscar el contacto por ubicación
        resultados = [contacto for contacto in datos if contacto["ubicacion"].lower() == ubicacion_buscada.lower()]

        if resultados:
            mensaje_resultados = "\n\n".join([f"Nombre: {c['nombre']}, Teléfono: {c['telefono']}, Ubicación: {c['ubicacion']}, Otros: {c['otros']}" for c in resultados])
            messagebox.showinfo("\nResultados", f"Contacto(s) encontrado(s):\n{mensaje_resultados}")
            return resultados
        else:
            messagebox.showinfo("\nResultados", "No se encontraron contactos en esa ubicación.")


    def cargar_datos(self):
        try:
            with open("agenda_data.json", "r") as file:
                datos = json.load(file)
        except FileNotFoundError:
            datos = []

        return datos

    def limpiar_campos(self):
        self.telefono_var.set("")
        self.nombre_var.set("")
        self.ubicacion_var.set("")
        self.otros_var.set("")
    def eliminar_por_nombre(self):
        resultados = self.buscar_por_nombre()

        if resultados:
            mensaje_resultados = "\n\n".join([f"Nombre: {c['nombre']}, Teléfono: {c['telefono']}, Ubicación: {c['ubicacion']}, Otros: {c['otros']}" for c in resultados])
            respuesta = messagebox.askyesno("Eliminar", f"¿Deseas eliminar el siguiente contacto?\n\n{mensaje_resultados}")

            if respuesta:
                # Cargar datos existentes
                datos = self.cargar_datos()

                # Filtrar contactos que no coincidan con el nombre buscado
                nuevos_datos = [contacto for contacto in datos if contacto["nombre"].lower() != self.nombre_var.get().lower()]

                # Guardar los datos actualizados en el archivo
                with open("agenda_data.json", "w") as file:
                    json.dump(nuevos_datos, file, indent=4)

                messagebox.showinfo("Eliminado", "Contacto eliminado exitosamente.")

                # Limpiar los campos después de eliminar
                self.limpiar_campos()
        else:
            messagebox.showinfo("Eliminar", "No se encontraron contactos con ese nombre.")


if __name__ == "__main__":
    root = ttk.Window()
    style = ttk.Style("flatly")
    app = AgendaApp(root)
    root.mainloop()
