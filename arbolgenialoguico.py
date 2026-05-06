lass Persona:
    def __init__(self, nombre, nacimiento):
        self.nombre = nombre
        # Se asegura de que el nacimiento sea un número entero para las comparaciones
        self.nacimiento = int(nacimiento)
        self.hijos = []

    def __str__(self):
        return f"{self.nombre} (Nacido en: {self.nacimiento})"

class ArbolGenealogico:
    def __init__(self, raiz_nombre, raiz_nacimiento):
        # El árbol comienza con un ancestro raíz
        self.raiz = Persona(raiz_nombre, raiz_nacimiento)

    def buscar_persona(self, actual, nombre):
        """Algoritmo de búsqueda recursiva"""
        if actual.nombre.lower() == nombre.lower():
            return actual
        for hijo in actual.hijos:
            resultado = self.buscar_persona(hijo, nombre)
            if resultado:
                return resultado
        return None

    def agregar_hijo(self, nombre_padre, nombre_hijo, nacimiento_hijo):
        """Inserta un nodo validando la jerarquía cronológica"""
        padre = self.buscar_persona(self.raiz, nombre_padre)
        
        if padre:
            try:
                nacimiento_hijo_int = int(nacimiento_hijo)
                # Restricción lógica
                if nacimiento_hijo_int <= padre.nacimiento:
                    print(f"\n ERROR CRONOLÓGICO: El hijo ({nacimiento_hijo_int}) no puede ser mayor o igual que su padre ({padre.nacimiento}).")
                else:
                    nuevo_hijo = Persona(nombre_hijo, nacimiento_hijo_int)
                    padre.hijos.append(nuevo_hijo)
                    print(f"\n EXITOSO: {nombre_hijo} ha sido registrado como descendiente de {nombre_padre}.")
            except ValueError:
                print("\n ERROR: El año debe ser un número válido.")
        else:
            print(f"\n ERROR: No se encontró a '{nombre_padre}' en el árbol.")

    def mostrar_arbol(self, actual, nivel=0):
        """Recorrido preorden para representar la jerarquía visualmente"""
        print("  " * nivel + "|--" + str(actual))
        for hijo in actual.hijos:
            self.mostrar_arbol(hijo, nivel + 1)

def menu_interactivo():
    """Interfaz de consola para la demostración funcional"""
    print("--- SISTEMA DE GESTIÓN GENEALÓGICA ---")
    print("configuracion de la cabeza")
    
    try:
        nombre_raiz = input("Nombre del ancestro principal: ")
        anio_raiz = input("Año de nacimiento: ")
        familia = ArbolGenealogico(nombre_raiz, anio_raiz)

        while True:
            print("\n-------------------------------------------")
            print("MENÚ DE OPERACIONES:")
            print("[1] Agregar Descendiente")
            print("[2] Visualizar Estructura Familiar")
            print("[3] Buscar un Integrante")
            print("[4] Finalizar Programa")
            
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                p = input("Nombre del padre/madre: ")
                h = input("Nombre del hijo/hija: ")
                a = input("Año de nacimiento del hijo: ")
                familia.agregar_hijo(p, h, a)

            elif opcion == "2":
                print("\n--- DIAGRAMA DEL ÁRBOL FAMILIAR ---")
                familia.mostrar_arbol(familia.raiz)

            elif opcion == "3":
                nombre = input("Ingrese el nombre a buscar: ")
                res = familia.buscar_persona(familia.raiz, nombre)
                if res:
                    print(f"\n RESULTADO: Se localizó a {res}")
                else:
                    print(f"\n AVISO: '{nombre}' no se encuentra en la base de datos.")

            elif opcion == "4":
                print("Cerrando sesión de usuario...")
                break
            else:
                print(" Opción inválida. Intente de nuevo.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# Ejecución del programa principal
if __name__ == "__main__":
    menu_interactivo()
