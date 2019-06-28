import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange
#from wtforms.fields.html5 import IntegerField
from wtforms.widgets.html5 import NumberInput
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

# https://devcenter.heroku.com/articles/heroku-postgresql
# https://devcenter.heroku.com/articles/heroku-cli

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.environ.get('DYNO'):
    # Produção no heroku
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SECRET_KEY'] = 'hard to guess string'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Classe(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    turma = db.Column(db.String(128), index=True)
    serie = db.Column(db.String(128), index=True)
    
    def __repr__(self):
        return '%s %s' % (self.serie, self.turma)

    @staticmethod
    def inserir_classes():
        db.session.add(Classe(serie= "1°", turma="Meio Ambiente"))
        db.session.add(Classe(serie= "1°", turma="Informatica"))
        db.session.add(Classe(serie= "2°", turma="Meio Ambiente"))
        db.session.add(Classe(serie= "2°", turma="Informatica"))
        db.session.add(Classe(serie= "3°", turma="Meio Ambiente"))
        db.session.add(Classe(serie= "3°", turma="Informatica"))
        db.session.commit()


@app.route("/", methods = ['GET'])
def exibir ():
    return render_template('index.html', classes=Classe.query.all())
    
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
    
@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
    # Insere valores iniciais
    Classe.inserir_classes()
    
class Report(FlaskForm):
    classes = Classe.query.all()
    classe = SelectField("Classe", choices = [(classe, classe) for classe in classes], validators=[DataRequired()])
    disc = StringField("Discente",  validators=[DataRequired()])
    prof = StringField("Docente",  validators=[DataRequired()])
    disciplina = StringField("Disciplina",  validators=[DataRequired()])
    coment = StringField("Comentário",  validators=[DataRequired()])
    
    submit = SubmitField('Comentar')
    
class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    classeT = db.Column(db.String(128), index=True)
    discente = db.Column(db.String(128), index=True)
    docente = db.Column(db.String(128), index=True)
    disciplina = db.Column(db.String(128), index=True)
    comentario = db.Column(db.String(128), index=True)
    
    def __repr__(self):
        return '<Comentario: %s, %s, %s>' % (self.comentario, self.discente, self.classeT)
    
    
@app.route("/comentar", methods = ['GET', 'POST'])
def comentario ():
    form = Report()
    if request.form:
        p = Comentario(classeT=form.classe.data, discente=form.disc.data, docente=form.prof.data, disciplina=form.disciplina.data, comentario=form.coment.data)
        db.session.add(p)
        db.session.commit()
    else:
        print("Erro")
    return render_template('comentar.html', classes=Classe.query.all(), form=form)
    
    
@app.route("/listar", methods = ['GET', 'POST'])
def listar():
    return render_template('list.html', coments=Comentario.query.all())