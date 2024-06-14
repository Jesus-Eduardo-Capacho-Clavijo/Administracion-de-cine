class Pelicula:
    def __init__(self, titulo, genero, descripcion, duracion, precio_entrada):
        self.titulo = titulo
        self.genero = genero
        self.descripcion = descripcion
        self.duracion = duracion
        self.precio_entrada = precio_entrada
        self.salas = []

class Sala:
    def __init__(self, numero):
        self.numero = numero
        self.horarios = []
        self.mapa_asientos = [["-" for _ in range(10)] for _ in range(5)]  # Mapa de asientos inicial

class ProductoComida:
    def __init__(self, nombre, tamanos):
        self.nombre = nombre
        self.tamanos = tamanos  # Diccionario de tamaños y precios

class Comida:
    def __init__(self, tipo):
        self.tipo = tipo
        self.productos = []

def mostrar_peliculas_catalogo(catalogo):
    if not catalogo:
        print("Aún no hay películas en el catálogo.")
        return False
    else:
        print("Películas en el catálogo:")
        for i, pelicula in enumerate(catalogo, 1):
            print(f"{i}. Título: {pelicula.titulo}, Género: {pelicula.genero}, Descripción: {pelicula.descripcion}, Duración: {pelicula.duracion}, Precio: ${pelicula.precio_entrada} COP")
        return True

def mostrar_mapa_asientos(sala):
    print("Mapa de asientos:")
    print("   ", end="")
    for i in range(1, 11):
        print(f"{i}", end=" ")
    print()
    for i, fila in enumerate(sala.mapa_asientos, 1):
        print(f"{i}: ", end="")
        for asiento in fila:
            print(asiento, end=" ")
        print()

def mostrar_inventario_comida(inventario):
    if not inventario:
        print("Aún no hay items en el inventario de comida.")
        return False
    else:
        print("Inventario de comida:")
        for i, item in enumerate(inventario, 1):
            print(f"{i}. Tipo: {item.tipo}")
            for producto in item.productos:
                print(f"  - Producto: {producto.nombre}")
                for tamano, precio in producto.tamanos.items():
                    print(f"    - {tamano}: ${precio} COP")
        return True

def agregar_item_inventario(inventario):
    print("Tipos de items:")
    tipos = ["Gaseosa", "Dulces", "Comida rápida", "Palomitas", "Nachos", "Helado", "Jugos", "Papitas"]
    for i, tipo in enumerate(tipos, 1):
        print(f"{i}. {tipo}")
    tipo_seleccionado = int(input("Seleccione el tipo de item: "))
    tipo_item = tipos[tipo_seleccionado - 1]

    nombre_producto = input(f"Ingrese el nombre del producto de {tipo_item}: ")

    num_tamanos = int(input("Ingrese el número de tamaños disponibles para este producto: "))
    tamanos = {}
    for _ in range(num_tamanos):
        tamano = input("Ingrese el tamaño: ")
        precio = float(input(f"Ingrese el precio para {tamano}: "))
        tamanos[tamano] = precio

    producto = ProductoComida(nombre_producto, tamanos)

    # Buscar si ya existe este tipo de comida en el inventario
    for item in inventario:
        if item.tipo == tipo_item:
            item.productos.append(producto)
            break
    else:
        # Si no existe, agregar uno nuevo
        item = Comida(tipo_item)
        item.productos.append(producto)
        inventario.append(item)

    print("Producto agregado correctamente al inventario de comida.")

def reservar_asientos(sala):
    mostrar_mapa_asientos(sala)
    fila = int(input("Ingrese el número de fila (1-5): "))
    columna = int(input("Ingrese el número de columna (1-10): "))

    if sala.mapa_asientos[fila - 1][columna - 1] == "x":
        print("Este asiento ya está ocupado. Elija otro.")
        return False, None, None
    else:
        sala.mapa_asientos[fila - 1][columna - 1] = "x"
        print("Asiento reservado correctamente.")
        return True, fila, columna

def seleccionar_comida(inventario):
    pedido = []
    total_precio = 0

    while True:
        if mostrar_inventario_comida(inventario):
            tipo_seleccionado = int(input("Seleccione el tipo de comida que desea: "))
            if 1 <= tipo_seleccionado <= len(inventario):
                item_seleccionado = inventario[tipo_seleccionado - 1]
                print(f"Ha seleccionado {item_seleccionado.tipo}. Productos disponibles:")
                for i, producto in enumerate(item_seleccionado.productos, 1):
                    print(f"{i}. {producto.nombre}")
                producto_seleccionado = int(input("Seleccione el producto que desea: "))
                if 1 <= producto_seleccionado <= len(item_seleccionado.productos):
                    producto = item_seleccionado.productos[producto_seleccionado - 1]
                    print(f"Ha seleccionado {producto.nombre}. Tamaños disponibles:")
                    for i, (tamano, precio) in enumerate(producto.tamanos.items(), 1):
                        print(f"{i}. {tamano} - ${precio} COP")
                    tamano_seleccionado = int(input("Seleccione el tamaño que desea: "))
                    tamanos = list(producto.tamanos.items())
                    if 1 <= tamano_seleccionado <= len(tamanos):
                        tamano, precio = tamanos[tamano_seleccionado - 1]
                        cantidad = int(input(f"Ingrese la cantidad de {tamano} {producto.nombre} que desea: "))
                        total_precio += precio * cantidad
                        pedido.append((item_seleccionado.tipo, producto.nombre, tamano, precio, cantidad))
                        continuar = input("¿Desea agregar otra comida? (s/n): ")
                        if continuar.lower() != "s":
                            break
                    else:
                        print("Opción de tamaño no válida.")
                else:
                    print("Opción de producto no válida.")
            else:
                print("Opción de comida no válida.")
        else:
            break

    return pedido, total_precio

def generar_informe_ventas(ventas):
    total_ganancias = 0

    print("\n--- Informe de Ventas ---")

    # Ventas de entradas
    print("Ventas de entradas:")
    for venta in ventas['entradas']:
        pelicula, sala, horario, asientos, precio_total = venta
        print(f"Película: {pelicula.titulo}")
        print(f"Sala: {sala.numero}")
        print(f"Horario: {horario}")
        print(f"Asientos:")
        for fila, columna in asientos:
            print(f"  - Fila {fila}, Asiento {columna}")
        print(f"Precio total: ${precio_total} COP")
        total_ganancias += precio_total

    # Ventas de comida
    print("\nVentas de comida:")
    for tipo, nombre, tamano, precio, cantidad in ventas['comidas']:
        print(f"{cantidad}x {tamano} {nombre} ({tipo}) - ${precio * cantidad} COP")
        total_ganancias += precio * cantidad

    print(f"\nGanancias totales: ${total_ganancias} COP")
    print("--- Fin del Informe ---")

def main():
    catalogo_peliculas = []
    inventario_comida = []
    ventas = {'entradas': [], 'comidas': []}

    while True:
        print("\n¿Qué desea hacer?")
        print("1. Agregar película al catálogo")
        print("2. Ver películas en el catálogo")
        print("3. Reservar asientos")
        print("4. Agregar item al inventario de comida")
        print("5. Ver inventario de comida")
        print("6. Ver informe de ventas del día")
        print("7. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            titulo = input("Ingrese el título de la película: ")
            genero = input("Ingrese el género de la película: ")
            descripcion = input("Ingrese la descripción de la película: ")
            duracion = input("Ingrese la duración de la película: ")
            precio_entrada = float(input("Ingrese el precio de la entrada: "))
            num_salas = int(input("Ingrese el número de salas disponibles para proyectar la película: "))
            salas = []

            for _ in range(num_salas):
                numero_sala = input("Ingrese el número de la sala: ")
                sala = Sala(numero_sala)
                num_horarios = int(input("Ingrese el número de horarios de proyección de la película en esta sala: "))
                for _ in range(num_horarios):
                    horario = input("Ingrese el horario de proyección de la película (ej. 2:00pm a 3:00pm): ")
                    sala.horarios.append(horario)
                salas.append(sala)

            pelicula = Pelicula(titulo, genero, descripcion, duracion, precio_entrada)
            pelicula.salas = salas
            catalogo_peliculas.append(pelicula)
            print("Película agregada correctamente al catálogo.")

        elif opcion == "2":
            if not mostrar_peliculas_catalogo(catalogo_peliculas):
                opcion_agregar = input("¿Desea agregar una película al catálogo? (1: sí / 2: no): ")
                if opcion_agregar == "1":
                    continue
                elif opcion_agregar == "2":
                    print("Regresando al menú principal...")
                else:
                    print("Opción no válida. Intente nuevamente.")

        elif opcion == "3":
            if not mostrar_peliculas_catalogo(catalogo_peliculas):
                opcion_agregar = input("¿Desea agregar una película al catálogo? (1: sí / 2: no): ")
                if opcion_agregar == "1":
                    continue
                elif opcion_agregar == "2":
                    print("Regresando al menú principal...")
                else:
                    print("Opción no válida. Intente nuevamente.")
            else:
                seleccion = int(input("Seleccione el número de la película: "))
                if 1 <= seleccion <= len(catalogo_peliculas):
                    pelicula_seleccionada = catalogo_peliculas[seleccion - 1]
                    print("Salas disponibles:")
                    for i, sala in enumerate(pelicula_seleccionada.salas, 1):
                        print(f"{i}. Sala {sala.numero}")
                    seleccion_sala = int(input("Seleccione el número de la sala: "))
                    if 1 <= seleccion_sala <= len(pelicula_seleccionada.salas):
                        sala_seleccionada = pelicula_seleccionada.salas[seleccion_sala - 1]
                        print("Horarios disponibles:")
                        for i, horario in enumerate(sala_seleccionada.horarios, 1):
                            print(f"{i}: {horario}")
                        seleccion_horario = int(input("Seleccione el número del horario: "))
                        if 1 <= seleccion_horario <= len(sala_seleccionada.horarios):
                            horario_seleccionado = sala_seleccionada.horarios[seleccion_horario - 1]
                            num_entradas = int(input("¿Cuántas entradas desea comprar? "))
                            asientos_reservados = []
                            total_precio_entradas = 0
                            for _ in range(num_entradas):
                                while True:
                                    exito, fila, columna = reservar_asientos(sala_seleccionada)
                                    if exito:
                                        asientos_reservados.append((fila, columna))
                                        total_precio_entradas += pelicula_seleccionada.precio_entrada
                                        break

                            ventas['entradas'].append((pelicula_seleccionada, sala_seleccionada, horario_seleccionado, asientos_reservados, total_precio_entradas))

                            desea_comprar_comida = input("¿Desea comprar comida? (s/n): ")
                            total_precio_comida = 0
                            pedido_comida = []
                            if desea_comprar_comida.lower() == 's':
                                pedido_comida, total_precio_comida = seleccionar_comida(inventario_comida)
                                ventas['comidas'].extend(pedido_comida)

                            print("\n--- Ticket de Compra ---")
                            print(f"Película: {pelicula_seleccionada.titulo}")
                            print(f"Sala: {sala_seleccionada.numero}")
                            print(f"Horario: {horario_seleccionado}")
                            print(f"Entradas: {num_entradas} x ${pelicula_seleccionada.precio_entrada} COP")
                            print("Asientos:")
                            for fila, columna in asientos_reservados:
                                print(f" - Fila {fila}, Asiento {columna}")
                            print(f"Total entradas: ${total_precio_entradas} COP")
                            if pedido_comida:
                                print("Comida:")
                                for tipo, nombre, tamano, precio, cantidad in pedido_comida:
                                    print(f" - {cantidad}x {tamano} {nombre} ({tipo}) - ${precio * cantidad} COP")
                                print(f"Total comida: ${total_precio_comida} COP")
                            print(f"Total a pagar: ${total_precio_entradas + total_precio_comida} COP")
                        else:
                            print("Opción de horario no válida.")
                    else:
                        print("Opción de sala no válida.")
                else:
                    print("Opción de película no válida.")

        elif opcion == "4":
            agregar_item_inventario(inventario_comida)

        elif opcion == "5":
            mostrar_inventario_comida(inventario_comida)

        elif opcion == "6":
            generar_informe_ventas(ventas)

        elif opcion == "7":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
