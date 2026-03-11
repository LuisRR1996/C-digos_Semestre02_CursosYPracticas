import json
import os
from datetime import datetime

# ==========================================
# 1. CLASE TAREA (Programación Orientada a Objetos)
# ==========================================
class Tarea:
    def __init__(self, id_tarea, titulo, descripcion, estado, prioridad, fecha_vencimiento):
        self.id_tarea = id_tarea
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.prioridad = prioridad
        self.fecha_vencimiento = fecha_vencimiento

    # Método para convertir el objeto a diccionario (necesario para el JSON)
    def to_dict(self):
        return {
            "id": self.id_tarea,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "prioridad": self.prioridad,
            "fecha_vencimiento": self.fecha_vencimiento
        }

# ==========================================
# 2. CLASE GESTOR DE TAREAS (Lógica y Archivos)
# ==========================================
class GestorTareas:
    def __init__(self, archivo="tareas.json"):
        self.archivo = archivo
        self.tareas = []
        self.cargar_tareas() # Carga las tareas al iniciar el programa

    def cargar_tareas(self):
        """Lee el archivo JSON y carga las tareas en la lista."""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r') as file:
                    datos = json.load(file)
                    # Convertimos los diccionarios del JSON en objetos Tarea
                    self.tareas = [Tarea(d['id'], d['titulo'], d['descripcion'], d['estado'], d['prioridad'], d['fecha_vencimiento']) for d in datos]
            except Exception as e:
                print(f"Error al cargar el archivo: {e}")
        else:
            self.tareas = []

    def guardar_tareas(self):
        """Guarda la lista de tareas en el archivo JSON."""
        try:
            with open(self.archivo, 'w') as file:
                # Convertimos los objetos Tarea a diccionarios antes de guardar
                datos = [tarea.to_dict() for tarea in self.tareas]
                json.dump(datos, file, indent=4)
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def crear_tarea(self):
        """Operación C del CRUD: Crear"""
        print("\n--- NUEVA TAREA ---")
        try:
            # Generar un ID automático basado en el ID más alto existente
            if self.tareas:
                id_tarea = max(t.id_tarea for t in self.tareas) + 1
            else:
                id_tarea = 1
                
            titulo = input("Título de la tarea: ")
            descripcion = input("Descripción: ")
            print("Prioridades: Alta, Media, Baja")
            prioridad = input("Prioridad: ").capitalize()
            
            # Uso del módulo datetime para registrar la fecha actual
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            
            nueva_tarea = Tarea(id_tarea, titulo, descripcion, "Pendiente", prioridad, fecha_actual)
            self.tareas.append(nueva_tarea)
            self.guardar_tareas()
            print("¡Tarea creada y guardada con éxito!")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def leer_tareas(self):
        """Operación R del CRUD: Leer"""
        print("\n--- LISTA DE TAREAS ---")
        if not self.tareas:
            print("No hay tareas registradas.")
            return
        
        for t in self.tareas:
            print(f"ID: {t.id_tarea} | Título: {t.titulo} | Estado: {t.estado} | Prioridad: {t.prioridad} | Fecha: {t.fecha_vencimiento}")

    def actualizar_tarea(self):
        """Operación U del CRUD: Actualizar"""
        print("\n--- ACTUALIZAR TAREA ---")
        if not self.tareas:
            print("No hay tareas para actualizar.")
            return

        try:
            id_buscar = int(input("Ingrese el ID de la tarea a actualizar: "))
            tarea_encontrada = False

            for t in self.tareas:
                if t.id_tarea == id_buscar:
                    print(f"Tarea actual: {t.titulo} | Estado actual: {t.estado}")
                    print("Opciones: 1. Pendiente | 2. En Progreso | 3. Completada")
                    nuevo_estado = input("Seleccione el nuevo estado (1/2/3): ")

                    if nuevo_estado == '1':
                        t.estado = "Pendiente"
                    elif nuevo_estado == '2':
                        t.estado = "En Progreso"
                    elif nuevo_estado == '3':
                        t.estado = "Completada"
                    else:
                        print("Opción inválida. Se mantuvo el estado actual.")
                        return

                    self.guardar_tareas() # Guardamos los cambios en el JSON
                    print("¡Tarea actualizada con éxito!")
                    tarea_encontrada = True
                    break

            if not tarea_encontrada:
                print("No se encontró ninguna tarea con ese ID.")
        except ValueError:
            print("Error: Por favor ingrese un número de ID válido.")

    def eliminar_tarea(self):
        """Operación D del CRUD: Eliminar"""
        print("\n--- ELIMINAR TAREA ---")
        if not self.tareas:
            print("No hay tareas para eliminar.")
            return

        try:
            id_buscar = int(input("Ingrese el ID de la tarea a eliminar: "))
            tarea_encontrada = False

            for t in self.tareas:
                if t.id_tarea == id_buscar:
                    self.tareas.remove(t)
                    self.guardar_tareas() # Guardamos los cambios en el JSON
                    print(f"¡La tarea '{t.titulo}' ha sido eliminada de la base de datos!")
                    tarea_encontrada = True
                    break

            if not tarea_encontrada:
                print("No se encontró ninguna tarea con ese ID.")
        except ValueError:
            print("Error: Por favor ingrese un número de ID válido.")

# ==========================================
# 3. MENÚ PRINCIPAL (Interfaz de usuario)
# ==========================================
def menu_principal():
    gestor = GestorTareas()
    
    while True:
        print("\n" + "="*30)
        print("  SISTEMA DE GESTIÓN DE TAREAS  ")
        print("="*30)
        print("1. Crear nueva tarea")
        print("2. Ver todas las tareas")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            gestor.crear_tarea()
        elif opcion == '2':
            gestor.leer_tareas()
        elif opcion == '3':
            gestor.actualizar_tarea()
        elif opcion == '4':
            gestor.eliminar_tarea()
        elif opcion == '5':
            print("¡Saliendo del programa! Tus datos han sido guardados de forma segura.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Punto de entrada del programa
if __name__ == "__main__":
    menu_principal()