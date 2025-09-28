from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/livros")
def listar():
    livros = Livro.query.all()
    return render_template("listar.html", livros=livros)

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        ano = int(request.form["ano"])
        categoria = request.form["categoria"]

        novo_livro = Livro(titulo=titulo, autor=autor, ano=ano, categoria=categoria)
        db.session.add(novo_livro)
        db.session.commit()
        return redirect(url_for("listar"))

    return render_template("adicionar.html")

if __name__ == "__main__":
    app.run(debug=True)
