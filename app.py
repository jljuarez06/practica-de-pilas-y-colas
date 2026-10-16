from flask import (Flask, render_template, request, redirect, url_for, flash)
import logica

app = Flask(__name__)
app.secret_key = "clave_secreta_flask"

@app.get("/")
def inicio():
    id_buscado = request.args.get("id", type=int)
    resultado_busqueda = logica.buscar_por_id(id_buscado) if id_buscado is not None else None
    
    total_pendientes = len(logica.cola_pendientes)
    total_atendidas = len(logica.pila_historial)
    
    return render_template(
        "index.html",
        pendientes=logica.cola_pendientes,
        historial=logica.pila_historial,
        siguiente=logica.consultar_siguiente(),
        resultado_busqueda=resultado_busqueda,
        id_buscado=id_buscado,
        total_pendientes=total_pendientes,
        total_atendidas=total_atendidas
    )

@app.post("/registrar")
def registrar():
    cliente = request.form.get("cliente", "")
    asunto = request.form.get("asunto", "")
    res = logica.registrar_solicitud(cliente, asunto)
    if res == "duplicado":
        flash("La solicitud ya se encuentra registrada como pendiente.", "warning")
    elif not res:
        flash("Datos de cliente o asunto inválidos.", "danger")
    return redirect(url_for("inicio"))

@app.post("/atender")
def atender():
    logica.atender_siguiente()
    return redirect(url_for("inicio"))

@app.post("/deshacer")
def deshacer():
    logica.deshacer_ultima_atencion()
    return redirect(url_for("inicio"))

@app.post("/cancelar/<int:id>")
def cancelar(id):
    logica.cancelar_solicitud(id)
    return redirect(url_for("inicio"))

@app.post("/deshacer-varias")
def deshacer_varias():
    try:
        cantidad = int(request.form.get("cantidad", 0))
        restauradas = logica.deshacer_varias_atenciones(cantidad)
        flash(f"Se restauraron exitosamente {restauradas} solicitudes.", "success")
    except ValueError:
        flash("Ingrese un número válido.", "danger")
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)