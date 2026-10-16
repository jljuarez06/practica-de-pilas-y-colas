cola_pendientes = []
pila_historial = []
siguiente_id = 1

def registrar_solicitud(cliente, asunto):
    global siguiente_id
    if not cliente.strip() or not asunto.strip():
        return None
    # Control de duplicados
    for s in cola_pendientes:
        if s["cliente"].lower() == cliente.strip().lower() and s["asunto"].lower() == asunto.strip().lower():
            return "duplicado"
            
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

def consultar_siguiente():
    if not cola_pendientes:
        return None
    return cola_pendientes[0]

def buscar_por_id(id_buscado):
    for s in cola_pendientes:
        if s["id"] == id_buscado:
            return s
    for s in pila_historial:
        if s["id"] == id_buscado:
            return s
    return None

def cancelar_solicitud(id_buscado):
    for i, s in enumerate(cola_pendientes):
        if s["id"] == id_buscado:
            return cola_pendientes.pop(i)
    return None

def deshacer_varias_atenciones(n):
    contador = 0
    for _ in range(n):
        res = deshacer_ultima_atencion()
        if res is not None:
            contador += 1
        else:
            break
    return contador