from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

def cargar_diccionario():
    try:
        with open('diccionario.json', 'r') as file:
            content = file.read()
            if content:
                return json.loads(content)
            else:
                return []
    except FileNotFoundError:
        return []

def guardar_diccionario(diccionario):
    with open('diccionario.json', 'w') as file:
        json.dump(diccionario, file)

def obtener_palabras_ordenadas():
    palabras = cargar_diccionario()
    palabras.sort(key=lambda x: x['palabra'])
    return palabras

next_id = 1  # Inicializa un contador para IDs únicos

@app.route('/')
def index():
    palabras_microeconomia = obtener_palabras_ordenadas()
    palabras_con_indice = [{"indice": idx+1, **palabra} for idx, palabra in enumerate(palabras_microeconomia)]
    return render_template('index.html', palabras=palabras_con_indice)

@app.route('/agregar', methods=['POST'])
def agregar_palabra():
    global next_id  # Utiliza la variable global

    palabra = request.form.get('palabra')
    significado = request.form.get('significado')

    if palabra and significado:
        palabras_microeconomia = cargar_diccionario()
        palabras_microeconomia.append({'id': next_id, 'palabra': palabra, 'significado': significado})
        next_id += 1  # Incrementa el contador de IDs
        guardar_diccionario(palabras_microeconomia)

    return redirect(url_for('index'))

@app.route('/eliminar', methods=['POST'])
def eliminar_palabra():
    palabra = request.form.get('palabra')
    palabras_microeconomia = cargar_diccionario()

    for idx, palabra_dict in enumerate(palabras_microeconomia):
        if palabra_dict['palabra'] == palabra:
            del palabras_microeconomia[idx]
            guardar_diccionario(palabras_microeconomia)
            break

    return redirect(url_for('index'))

@app.route('/modificar', methods=['POST'])
def modificar_palabra():
    palabra = request.form.get('palabra')
    nuevo_significado = request.form.get('nuevo_significado')
    palabras_microeconomia = cargar_diccionario()

    for idx, palabra_dict in enumerate(palabras_microeconomia):
        if palabra_dict['palabra'] == palabra:
            palabras_microeconomia[idx]['significado'] = nuevo_significado
            guardar_diccionario(palabras_microeconomia)
            break

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
