class Nodo:
    def __init__(self, codigo, nota):
        self.codigo = codigo
        self.nota = nota
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None

    # ---------------- UTILIDADES ----------------

    def altura(self, nodo):
        return nodo.height if nodo else 0

    def balance(self, nodo):
        return self.altura(nodo.left) - self.altura(nodo.right)

    def min_nodo(self, nodo):
        while nodo.left:
            nodo = nodo.left
        return nodo

    # ---------------- ROTACIONES ----------------

    def rotar_derecha(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.altura(y.left), self.altura(y.right))
        x.height = 1 + max(self.altura(x.left), self.altura(x.right))

        return x

    def rotar_izquierda(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.altura(x.left), self.altura(x.right))
        y.height = 1 + max(self.altura(y.left), self.altura(y.right))

        return y

    # ---------------- INSERTAR ----------------

    def insertar(self, codigo, nota):
        self.root = self._insertar(self.root, codigo, nota)

    def _insertar(self, nodo, codigo, nota):
        if not nodo:
            return Nodo(codigo, nota)

        if codigo < nodo.codigo:
            nodo.left = self._insertar(nodo.left, codigo, nota)
        elif codigo > nodo.codigo:
            nodo.right = self._insertar(nodo.right, codigo, nota)
        else:
            nodo.nota = nota  # actualización

        nodo.height = 1 + max(self.altura(nodo.left), self.altura(nodo.right))
        balance = self.balance(nodo)

        # LL
        if balance > 1 and codigo < nodo.left.codigo:
            return self.rotar_derecha(nodo)

        # RR
        if balance < -1 and codigo > nodo.right.codigo:
            return self.rotar_izquierda(nodo)

        # LR
        if balance > 1 and codigo > nodo.left.codigo:
            nodo.left = self.rotar_izquierda(nodo.left)
            return self.rotar_derecha(nodo)

        # RL
        if balance < -1 and codigo < nodo.right.codigo:
            nodo.right = self.rotar_derecha(nodo.right)
            return self.rotar_izquierda(nodo)

        return nodo

    # ---------------- BUSCAR ----------------

    def buscar(self, nodo, codigo):
        if not nodo:
            return None
        if nodo.codigo == codigo:
            return nodo
        if codigo < nodo.codigo:
            return self.buscar(nodo.left, codigo)
        return self.buscar(nodo.right, codigo)

    # ---------------- ELIMINAR ----------------

    def eliminar(self, codigo):
        self.root = self._eliminar(self.root, codigo)

    def _eliminar(self, nodo, codigo):
        if not nodo:
            return nodo

        if codigo < nodo.codigo:
            nodo. left = self._eliminar(nodo.left, codigo)
        elif codigo > nodo.codigo:
            nodo.right = self._eliminar(nodo.right, codigo)
        else:
            if not nodo.left:
                return nodo.right
            elif not nodo.right:
                return nodo.left

            temp = self.min_nodo(nodo.right)
            nodo.codigo = temp.codigo
            nodo.nota = temp.nota
            nodo.right = self._eliminar(nodo.right, temp.codigo)

        nodo.height = 1 + max(self.altura(nodo.left), self.altura(nodo.right))
        balance = self.balance(nodo)

        # rebalanceo
        if balance > 1 and self.balance(nodo.left) >= 0:
            return self.rotar_derecha(nodo)

        if balance > 1 and self.balance(nodo.left) < 0:
            nodo.left = self.rotar_izquierda(nodo.left)
            return self.rotar_derecha(nodo)

        if balance < -1 and self.balance(nodo.right) <= 0:
            return self.rotar_izquierda(nodo)

        if balance < -1 and self.balance(nodo.right) > 0:
            nodo.right = self.rotar_derecha(nodo.right)
            return self.rotar_izquierda(nodo)

        return nodo

    # ---------------- RANKING (INORDEN) ----------------

    def ranking(self, nodo):
        if nodo:
            self.ranking(nodo.left)
            print(f"Código: {nodo.codigo} | Nota: {nodo.nota}")
            self.ranking(nodo.right)

    # ---------------- RANGO DE NOTAS ----------------

    def rango_notas(self, nodo, min_nota, max_nota):
        if not nodo:
            return

        self.rango_notas(nodo.left, min_nota, max_nota)

        if min_nota <= nodo.nota <= max_nota:
            print(f"Código: {nodo.codigo} | Nota: {nodo.nota}")

        self.rango_notas(nodo.right, min_nota, max_nota)


def menu():
    arbol = AVL()

    while True:
        print("\n====== SISTEMA ACADÉMICO AVL ======")
        print("1. Insertar estudiante")
        print("2. Buscar estudiante")
        print("3. Eliminar estudiante")
        print("4. Mostrar ranking")
        print("5. Buscar por rango de notas")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                codigo = int(input("Código: "))
                nota = float(input("Nota: "))
                arbol.insertar(codigo, nota)
                print("✔ Estudiante insertado")

            case "2":
                codigo = int(input("Código a buscar: "))
                nodo = arbol.buscar(arbol.root, codigo)
                if nodo:
                    print(f"✔ Encontrado -> Código: {nodo.codigo}, Nota: {nodo.nota}")
                else:
                    print("❌ No encontrado")

            case "3":
                codigo = int(input("Código a eliminar: "))
                arbol.eliminar(codigo)
                print("✔ Eliminado (si existía)")

            case "4":
                print("\n📊 RANKING ACADÉMICO:")
                arbol.ranking(arbol.root)

            case "5":
                min_n = float(input("Nota mínima: "))
                max_n = float(input("Nota máxima: "))
                print("\n📈 RESULTADOS:")
                arbol.rango_notas(arbol.root, min_n, max_n)

            case "6":
                print("👋 Saliendo del sistema...")
                break

            case _:
                print("❌ Opción inválida")


menu()