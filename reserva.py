import datetime

CAPACIDAD_RESTAURANTE = 50
reservas = []
lista_espera = []

def obtener_informacion_contacto():
    nombre = input("Ingrese su nombre: ")
    numero = input("Ingrese su número de teléfono: ")
    correo = input("Ingrese su correo electrónico: ")
    return {"nombre": nombre, "numero": numero, "correo": correo}

def obtener_numero_comensales():
    return int(input("Ingrese el número de comensales: "))

def obtener_fecha_hora_reserva():
    fecha_input = input("Ingrese la fecha de la reserva (en formato dd/mm/aaaa): ")
    hora_input = input("Ingrese la hora de la reserva (en formato hh:mm): ")
    fecha = datetime.datetime.strptime(fecha_input, '%d/%m/%Y')
    hora = datetime.datetime.strptime(hora_input, '%H:%M').time()
    return {"fecha": fecha, "hora": hora}

def verificar_disponibilidad_reserva(fecha, hora, numero_comensales):
    capacidad_disponible = CAPACIDAD_RESTAURANTE - sum(r["numero_comensales"] for r in reservas if r["fecha"] == fecha and r["hora"] == hora)
    return numero_comensales <= capacidad_disponible

def mostrar_mesas_disponibles():
    print("Mesas disponibles:")
    for mesa in range(1, 11):  # Suponiendo que hay 10 mesas en el restaurante
        mesa_ocupada = any(r["mesa"] == mesa for r in reservas)
        if not mesa_ocupada:
            print(f"Mesa {mesa}")

def seleccionar_mesa():
    mesa = None
    while not mesa:
        mesa_input = input("Seleccione una mesa disponible: ")
        try:
            mesa = int(mesa_input)
            if mesa < 1 or mesa > 10:  # Suponiendo que hay 10 mesas en el restaurante
                raise ValueError
            mesa_ocupada = any(r["mesa"] == mesa for r in reservas)
            if mesa_ocupada:
                print("La mesa seleccionada ya está ocupada. Por favor, seleccione otra.")
                mesa = None
        except ValueError:
            print("Opción inválida. Por favor, seleccione una mesa disponible.")
    return mesa

def hacer_reserva():
    informacion_contacto = obtener_informacion_contacto()
    numero_comensales = obtener_numero_comensales()
    fecha_hora_reserva = obtener_fecha_hora_reserva()
    disponible = verificar_disponibilidad_reserva(fecha_hora_reserva["fecha"], fecha_hora_reserva["hora"], numero_comensales)
    if disponible:
        mostrar_mesas_disponibles()
        mesa = seleccionar_mesa()
        reserva = {
            "nombre": informacion_contacto["nombre"],
            "numero": informacion_contacto["numero"],
            "correo": informacion_contacto["correo"],
            "fecha": fecha_hora_reserva["fecha"],
            "hora": fecha_hora_reserva["hora"],
            "numero_comensales": numero_comensales,
            "mesa": mesa
        }
        reservas.append(reserva)
        guardar_reservas()
        print("Reserva realizada con éxito.")
        confirmar_reserva(informacion_contacto)
    else:
        print("Lo siento, no hay capacidad disponible para la fecha y hora solicitadas.")
        opcion = input("¿Desea quedar en lista de espera? (S/N): ")
        if opcion.lower() == 's':
            lista_espera.append(informacion_contacto)
            guardar_lista_espera()
            print("Usted ha sido añadido a la lista de espera.")
        else:
            print("La reserva ha sido cancelada.")

def confirmar_reserva(informacion_contacto):
    print("Confirmación de reserva:")
    print("Nombre:", informacion_contacto["nombre"])
    print("Número:", informacion_contacto["numero"])
    print("Correo:", informacion_contacto["correo"])
    opcion = input("¿Desea modificar la reserva? (S/N): ")
    if opcion.lower() == 's':
        editar_reserva()
    else:
        calificar_servicio()

def guardar_lista_espera():
    with open("lista_espera.txt", "w") as file:
        for contacto in lista_espera:
            linea = f"{contacto['nombre']} {contacto['numero']} {contacto['correo']}\n"
            file.write(linea)

def editar_reserva():
    fecha_input = input("Ingrese la fecha de la reserva a editar (en formato dd/mm/aaaa): ")
    hora_input = input("Ingrese la hora de la reserva a editar (en formato hh:mm): ")
    fecha = datetime.datetime.strptime(fecha_input, '%d/%m/%Y')
    hora = datetime.datetime.strptime(hora_input, '%H:%M').time()
    reserva_existente = next((r for r in reservas if r["fecha"] == fecha and r["hora"] == hora), None)
    if reserva_existente:
        print("Reserva encontrada:")
        print("Fecha:", reserva_existente["fecha"].strftime("%d/%m/%Y"))
        print("Hora:", reserva_existente["hora"].strftime("%H:%M"))
        print("Nombre:", reserva_existente["nombre"])
        print("Número:", reserva_existente["numero"])
        print("Correo:", reserva_existente["correo"])
        opcion = input("¿Desea editar la reserva? (S/N): ")
        if opcion.lower() == 's':
            nueva_fecha_hora_reserva = obtener_fecha_hora_reserva()
            disponible = verificar_disponibilidad_reserva(nueva_fecha_hora_reserva["fecha"], nueva_fecha_hora_reserva["hora"], reserva_existente["numero_comensales"])
            if disponible:
                reserva_existente["fecha"] = nueva_fecha_hora_reserva["fecha"]
                reserva_existente["hora"] = nueva_fecha_hora_reserva["hora"]
                guardar_reservas()
                print("La reserva ha sido editada exitosamente.")
                confirmar_reserva(reserva_existente)
            else:
                print("Lo siento, no hay capacidad disponible para la nueva fecha y hora solicitadas.")
                opcion_lista_espera = input("¿Desea quedar en lista de espera? (S/N): ")
                if opcion_lista_espera.lower() == 's':
                    lista_espera.append(reserva_existente)
                    reservas.remove(reserva_existente)
                    guardar_reservas()
                    guardar_lista_espera()
                    print("Usted ha sido añadido a la lista de espera.")
                else:
                    print("La reserva ha sido cancelada.")
                    reservas.remove(reserva_existente)
                    guardar_reservas()
        else:
            print("La reserva no ha sido modificada.")
    else:
        print("No se encontró ninguna reserva con la fecha y hora especificadas.")

def cancelar_reserva():
    fecha_input = input("Ingrese la fecha de la reserva a cancelar (en formato dd/mm/aaaa): ")
    hora_input = input("Ingrese la hora de la reserva a cancelar (en formato hh:mm): ")
    fecha = datetime.datetime.strptime(fecha_input, '%d/%m/%Y')
    hora = datetime.datetime.strptime(hora_input, '%H:%M').time()
    reserva_existente = next((r for r in reservas if r["fecha"] == fecha and r["hora"] == hora), None)
    if reserva_existente:
        print("Reserva encontrada:")
        print("Fecha:", reserva_existente["fecha"].strftime("%d/%m/%Y"))
        print("Hora:", reserva_existente["hora"].strftime("%H:%M"))
        print("Nombre:", reserva_existente["nombre"])
        print("Número:", reserva_existente["numero"])
        print("Correo:", reserva_existente["correo"])
        opcion = input("¿Desea cancelar la reserva? (S/N): ")
        if opcion.lower() == 's':
            reservas.remove(reserva_existente)
            guardar_reservas()
            print("La reserva ha sido cancelada.")
        else:
            print("La reserva no ha sido cancelada.")
    else:
        print("No se encontró ninguna reserva con la fecha y hora especificadas.")

def calificar_servicio():
    calificacion = input("Ingrese la calificación del servicio (1-5): ")
    opinion = input("Ingrese su opinión sobre el servicio: ")
    print("Gracias por utilizar nuestro servicio.")
    print("Su opinión y calificación son las siguientes:")
    print("Calificación:", calificacion)
    print("Opinión:", opinion)

def mostrar_menu():
    print("------- MENÚ -------")
    print("1. Hacer una reserva")
    print("2. Editar una reserva")
    print("3. Cancelar una reserva")
    print("0. Salir")

def guardar_reservas():
    with open("reservas.txt", "w") as file:
        for reserva in reservas:
            fecha_str = reserva["fecha"].strftime('%d/%m/%Y')
            hora_str = reserva["hora"].strftime('%H:%M')
            linea = f"{fecha_str} {hora_str} {reserva['nombre']} {reserva['numero']} {reserva['correo']} {reserva['numero_comensales']} {reserva['mesa']}\n"
            file.write(linea)

def cargar_reservas():
    try:
        with open("reservas.txt", "r") as file:
            for linea in file:
                campos = linea.strip().split()
                if len(campos) == 7:  # Verificar que haya suficientes valores en la línea
                    fecha_str, hora_str, nombre, numero, correo, numero_comensales, mesa = campos
                    fecha = datetime.datetime.strptime(fecha_str, '%d/%m/%Y')
                    hora = datetime.datetime.strptime(hora_str, '%H:%M').time()
                    reserva = {
                        "fecha": fecha,
                        "hora": hora,
                        "nombre": nombre,
                        "numero": numero,
                        "correo": correo,
                        "numero_comensales": int(numero_comensales),
                        "mesa": int(mesa)
                    }
                    reservas.append(reserva)
                else:
                    print("Error: la línea no contiene todos los campos necesarios.")
    except FileNotFoundError:
        pass

def cargar_lista_espera():
    try:
        with open("lista_espera.txt", "r") as file:
            for linea in file:
                nombre, numero, correo = linea.strip().split()
                contacto = {
                    "nombre": nombre,
                    "numero": numero,
                    "correo": correo
                }
                lista_espera.append(contacto)
    except FileNotFoundError:
        pass

cargar_reservas()
cargar_lista_espera()

while True:
    mostrar_menu()
    opcion = input("Ingrese el número de la opción que desea ejecutar: ")
    if opcion == '1':
        hacer_reserva()
    elif opcion == '2':
        editar_reserva()
    elif opcion == '3':
        cancelar_reserva()
    elif opcion == '0':
        break
    else:
        print("Opción no válida. Por favor, ingrese una opción válida.")