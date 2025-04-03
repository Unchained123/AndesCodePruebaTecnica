from flask import Flask, request, render_template, url_for, redirect,session
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db=SQLAlchemy(app)
api = Api(app)


class ProfesionalModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(80), unique=True, nullable=False)
	rubro = db.Column(db.String(80), nullable=False)
	descripcion = db.Column(db.String(200), nullable=False)
	ubicacion = db.Column(db.String(200), nullable=False)
	def __repr__(self):
		return f"Profesional: id = {self.id}, nombre = {self.name}, rubro = {self.rubro}, descripcion = {self.descripcion}"

profesional_args = reqparse.RequestParser()
profesional_args.add_argument('nombre', type=str, required=True, help="nombre no puede estar vacio")
profesional_args.add_argument('rubro', type=str, required=True, help="Rubro no puede estar vacio")
profesional_args.add_argument('descripcion', type=str, required=True, help="Descripcion no puede estar vacio")
profesional_args.add_argument('ubicacion', type=str, required=True, help="Ubicacion no puede estar vacio")

profesional_args_filter = reqparse.RequestParser()
profesional_args_filter.add_argument('rubro', type=str,required=False, location='args')
profesional_args_filter.add_argument('ubicacion', type=str,required=False, location='args')

profesionalFields = {
	'id':fields.Integer,
	'nombre':fields.String,
	'rubro':fields.String,
	'ubicacion':fields.String,
	'descripcion':fields.String,
}

class profesionales(Resource):
	@marshal_with(profesionalFields)
	def get(self):
		args = profesional_args_filter.parse_args()		
		if args['ubicacion']:
			if args['rubro']:
				profesionals = ProfesionalModel.query.filter_by(ubicacion=args['ubicacion'],rubro=args['rubro']).all()
			else:
				profesionals = ProfesionalModel.query.filter_by(ubicacion=args['ubicacion']).all()
		elif args['rubro']:
			profesionals = ProfesionalModel.query.filter_by(rubro=args['rubro']).all()
		else:
			profesionals = ProfesionalModel.query.all()
		return profesionals
	
	@marshal_with(profesionalFields)
	def post(self):
		args = profesional_args.parse_args()
		profesional = ProfesionalModel(nombre=args["nombre"],rubro=args["rubro"], ubicacion=args["ubicacion"], descripcion=args["descripcion"])
		db.session.add(profesional)
		db.session.commit()
		profesionals= ProfesionalModel.query.all()
		return profesionals, 201
	
class profesional(Resource):
	@marshal_with(profesionalFields)
	def get(self, id):
		profesional= ProfesionalModel.query.filter_by(id=id).first()
		if not profesional:
			abort(404, "Profesional no encontrado")
		return profesional
	
	@marshal_with(profesionalFields)
	def patch(self, id):
		args = profesional_args.parse_args()
		profesional= ProfesionalModel.query.filter_by(id=id).first()
		if not profesional:
			abort(404)
		profesional.nombre=args["nombre"]
		profesional.ubicacion=args["ubicacion"]
		profesional.descripcion=args["descripcion"]
		profesional.rubro=args["rubro"]
		db.session.commit()
		return profesional

	@marshal_with(profesionalFields)
	def delete(self, id):
		profesional= ProfesionalModel.query.filter_by(id=id).first()
		if not profesional:
			abort(404, "Profesional no encontrado")
		db.session.delete(profesional)
		db.session.commit()
		profesionales=ProfesionalModel.query.all()
		return profesionales, 204
	
api.add_resource(profesionales, '/api/profesionales')
api.add_resource(profesional, '/api/profesionales/<int:id>')

@app.route('/')
def inicio():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug = True,port=8000)	