
cola_pendientes = []
pila_historial = []
siguiente_id = 1

def mostrar_estado():
    print("\nPendientes:", cola_pendientes)
    print("Historial:", pila_historial)

def registrar_solicitud(cliente, asunto):
    global siguiente_id
    if not cliente.strip() or not asunto.strip():
        return None
    
    # Reto 5: Control de duplicados (evitar que un mismo cliente registre exactamente el mismo asunto pendiente)
    for s in cola_pendientes:
        if s["cliente"].lower() == cliente.strip().lower() and s["asunto"].lower() == asunto.strip().lower():
            print("Aviso: Esta solicitud ya se encuentra pendiente.")
            return None

    solicitud = {
        "id": siguiente_id,
        "cliente": cliente.strip(),
        "asunto": asunto.strip(),
        "estado": "pendiente"
    }
    cola_pendientes.append(solicitud)
    siguiente_id += 1
    return solicitud

def atender_siguiente():
    if not cola_pendientes:
        return None
    solicitud = cola_pendientes.pop(0)
    solicitud["estado"] = "atendida"
    pila_historial.append(solicitud)
    return solicitud

def deshacer_ultima_atencion():
    if not pila_historial:
        return None
    solicitud = pila_historial.pop()
    solicitud["estado"] = "pendiente"
    cola_pendientes.insert(0, solicitud)
    return solicitud

# ==========================================
# DESARROLLO DE LOS 5 RETOS INTERMEDIOS
# ==========================================

# Reto 1: Consultar el siguiente turno sin extraerlo
def consultar_siguiente():
    if not cola_pendientes:
        return None
    return cola_pendientes[0]

# Reto 2: Buscar una solicitud por ID (en pendientes o historial)
def buscar_solicitud(id_buscado):
    for s in cola_pendientes:
        if s["id"] == id_buscado:
            return s
    for s in pila_historial:
        if s["id"] == id_buscado:
            return s
    return None

# Reto 3: Cancelar una solicitud pendiente por ID
def cancelar_solicitud(id_buscado):
    for i, s in enumerate(cola_pendientes):
        if s["id"] == id_buscado:
            return cola_pendientes.pop(i)
    return None

# Reto 4: Deshacer varias atenciones
def deshacer_varias(n):
    restauradas = []
    for _ in range(n):
        res = deshacer_ultima_atencion()
        if res is not None:
            restauradas.append(res)
        else:
            break
    return restauradas

# Reto 5: Estadísticas y control de duplicados
def mostrar_estadisticas():
    total_pendientes = len(cola_pendientes)
    total_atendidas = len(pila_historial)
    total_general = total_pendientes + total_atendidas
    print("\n--- ESTADÍSTICAS ---")
    print(f"Total de solicitudes registradas: {total_general}")
    print(f"Pendientes de atención: {total_pendientes}")
    print(f"Atendidas (en historial): {total_atendidas}")
    print("--------------------")

def ejecutar_menu():
    while True:
        print("\n1. Registrar solicitud")
        print("2. Atender siguiente")
        print("3. Deshacer última atención")
        print("4. Mostrar estado")
        print("5. Consultar siguiente turno (Reto 1)")
        print("6. Buscar solicitud por ID (Reto 2)")
        print("7. Cancelar solicitud pendiente (Reto 3)")
        print("8. Deshacer varias atenciones (Reto 4)")
        print("9. Ver estadísticas (Reto 5)")
        print("10. Salir")
        
        opcion = input("Opción: ").strip()
        
        if opcion == "1":
            cliente = input("Cliente: ")
            asunto = input("Asunto: ")
            resultado = registrar_solicitud(cliente, asunto)
            print("Registrada:", resultado if resultado else "Datos inválidos o duplicados")
        elif opcion == "2":
            print("Atendida:", atender_siguiente())
        elif opcion == "3":
            print("Restaurada:", deshacer_ultima_atencion())
        elif opcion == "4":
            mostrar_estado()
        elif opcion == "5":
            print("Siguiente turno:", consultar_siguiente())
        elif opcion == "6":
            try:
                id_b = int(input("Ingrese ID a buscar: "))
                print("Resultado de búsqueda:", buscar_solicitud(id_b))
            except ValueError:
                print("ID inválido.")
        elif opcion == "7":
            try:
                id_c = int(input("Ingrese ID de la solicitud a cancelar: "))
                print("Cancelada:", cancelar_solicitud(id_c))
            except ValueError:
                print("ID inválido.")
        elif opcion == "8":
            try:
                cantidad = int(input("¿Cuántas atenciones desea deshacer?: "))
                restauradas = deshacer_varias(cantidad)
                print(f"Se restauraron {len(restauradas)} solicitudes.")
            except ValueError:
                print("Cantidad inválida.")
        elif opcion == "9":
            mostrar_estadisticas()
        elif opcion == "10":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    ejecutar_menu()
