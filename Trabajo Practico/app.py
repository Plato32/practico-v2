from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from string import hexdigits
import hashlib

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db 
from models import Usuario, Receta, Ingrediente
		
@app.route('/')
def inicio():
	return render_template('ingreso_usuario.html')
    

@app.route('/pagina_inicio', methods = ['GET','POST'])
def pagina_inicio():   
    
    if request.method == 'POST':
        if  not request.form['email'] or not request.form['password']:
            return render_template('error.html', error="Por favor ingrese los datos requeridos")
        else:
            Usuario_actual = Usuario.query.filter_by(correo= request.form['email']).first()
            if Usuario_actual is None:
                return render_template('error.html', error="El correo no está registrado")
            else:
                password=(hashlib.md5(bytes(request.form['password'], encoding='utf-8'))).hexdigest()
                if (password == Usuario_actual.clave): 
                    session['nombre']=Usuario_actual.nombre
                    session['id']=Usuario_actual.id
                    recetasrecientes=Receta.query.all()
                    recetasrecientes.reverse()
                    return render_template('opciones_registrado.html', tipo_busqueda="Recetas Recientes", usuario_actual=Usuario_actual, recetas=recetasrecientes, usuarios=Usuario.query.all(), ingrediente=Ingrediente.query.all()) #Redirecciona al usuario al template de Bienvenido.html
                else:
                    return render_template('error.html', error="La contraseña no es válida")
    else:
        return render_template('ingreso_usuario.html')
	
@app.route('/compartir_receta', methods = ['GET','POST'])
def compartir_receta():
    if 'nombre' in session:
        if request.method == 'POST':
            if not request.form['nombre']:
                return render_template('error_receta.html', error="Nombre no ingresado...")
            else: 
                    if not request.form['tiempo']:
                        return render_template('error_receta.html', error=" Debe ingresar el tiempo estimado de elaboracion de la receta.")
                    else:
                        if not request.form['elaboracion']:
                            return render_template('error_receta.html', error="Debe ingresar la elaboración de la receta.")
                        else:                     
                            return render_template("Ingresar_ingredientes.html", nombre_receta=request.form['nombre'], tiempo=request.form['tiempo'], elaboracion=request.form['elaboracion'], usuario_actual=session, ingredientes="", cantidadingredientes=0) 
        else:
            return render_template("compartir_receta.html", usuario_actual=session)
    else:
        return render_template('ingreso_usuario.html') 

@app.route('/ingresar_ingredientes', methods = ['GET','POST'])
def ingresar_ingredientes():
    if 'nombre' in session:
        if request.method == 'POST':
            if not request.form['ingrediente']:
                return render_template('error_receta.html', error="Ingrediente no ingresado...")
            else: 
                    if not request.form['cantidad']:
                        return render_template('error_receta.html', error=" Debe ingresar la cantidad del ingrediente.")
                    else:
                        if not request.form['unidad']:
                            return render_template('error_receta.html', error="Debe ingresar la unidad del ingrediente.")
                        else:                     
                            return render_template("publicar_receta.html", nombre_receta=request.form['nombre_receta'], tiempo=request.form['tiempo'], elaboracion=request.form['elaboracion'], usuario_actual=session, ingredientes=request.form['ingrediente'], cantidadingredientes=request.form['cantidad'], unidad=request.form['unidad']) 
        else:
            return render_template("ingresar_ingredientes.html", usuario_actual=session)
    else:
        return render_template('ingreso_usuario.html')

@app.route('/ranking', methods = ['GET','POST'])
def ranking():
    pass
'''if 'nombre' in session:   
        if request.method=='POST':
            if not request.form['nombre']:
                return render_template("Error_Receta.html", error="Debe ingresar nombre de la receta.", usuario_actual=session)
            else: 
                if not request.form['tiempo']:
                    return render_template("Error_Receta.html", error="Debe ingresar el tiempo de la receta.", usuario_actual=session)
                else:
                    if not request.form['descripcion']:
                        return render_template("Error_Receta.html", error="Debe ingresar la elaboración de la receta.", usuario_actual=session)
                    else:                     
                        
                        return render_template("Ingresar_Ingrediente.html", nombre_receta=request.form['nombre'], tiempo=request.form['tiempo'], descripcion=request.form['descripcion'], usuario_actual=session, ingredientes="", cantidadingredientes=0)
        else:
            return render_template("Ingresar_Receta.html", usuario_actual=session)
    else:
        return render_template('index.html') #El caso base lo redirecciona al Ingreso.html''' 

@app.route('/consultar_receta', methods = ['GET','POST'])
def consultar_recetas():
    pass
#    return render_template('listar_comentario.html', comentarios = Comentario.query.all())

@app.route('/me_gusta', methods = ['GET', 'POST'])
def me_gusta():
    pass
# def listar_comentarios_usuario():  
#     if request.method == 'POST':
#         if not request.form['usuarios']:
# 			#Pasa como parámetro todos los usuarios
#             return render_template('listar_comentario_usuario.html', usuarios = Usuario.query.all(), usuario_seleccionado = None )
#         else:
#             return render_template('listar_comentario_usuario.html', usuarios= None, usuario_selec = Usuario.query.get(request.form['usuarios'])) 
#     else:
#         return render_template('listar_comentario_usuario.html', usuarios = Usuario.query.all(), usuario_selec = None )   
        

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)	