from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Catálogo base (simulado)
productos = {
    1: {'nombre': 'Mouse Logitech', 'precio': 80, 'imagen': 'mouse.png'},
    2: {'nombre': 'Teclado Mecánico Redragon', 'precio': 220, 'imagen': 'teclado.png'},
    3: {'nombre': 'Monitor LG 24"', 'precio': 750, 'imagen': 'monitor.png'},
    4: {'nombre': 'Tarjeta Gráfica RTX 3060', 'precio': 1800, 'imagen': 'gpu.png'},
    5: {'nombre': 'Micrófono USB Blue Yeti', 'precio': 350, 'imagen': 'microfono.png'},
    6: {'nombre': 'Auriculares Gamer HyperX', 'precio': 270, 'imagen': 'auriculares.png'},
    7: {'nombre': 'Webcam Logitech HD', 'precio': 150, 'imagen': 'webcam.png'},
}

@app.route('/')
def catalogo():
    return render_template('catalogo.html', productos=productos)

@app.route('/agregar/<int:id>')
def agregar(id):
    carrito = session.get('carrito', {})
    if str(id) in carrito:
        carrito[str(id)]['cantidad'] += 1
    else:
        producto = productos[id]
        carrito[str(id)] = {
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'imagen': producto['imagen'],
            'cantidad': 1
        }
    session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))

@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render_template('carrito.html', carrito=carrito, total=total)


@app.route('/vaciar')
def vaciar():
    session.pop('carrito', None)
    return redirect(url_for('catalogo'))

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    carrito = session.get('carrito', {})
    id_str = str(id)
    if id_str in carrito:
        del carrito[id_str]
        session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')


if __name__ == '__main__':
    app.run(debug=True)
