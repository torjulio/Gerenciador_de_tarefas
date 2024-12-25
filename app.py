from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Configurações do Flask e SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Modelo da Tabela Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


# Criação das tabelas no banco de dados
def create_tables():
    db.create_all()
    # Não adiciona tarefas de exemplo se não houver tarefas no banco de dados
    # Nenhuma tarefa é inserida quando o banco está vazio
    if not Task.query.first():
        pass  # Nenhuma ação, apenas garantindo que o banco esteja vazio


@app.before_request
def initialize():
    create_tables()

# Rota principal para listar as tarefas
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Rota para adicionar uma nova tarefa
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    
    # Cria uma nova tarefa e a adiciona ao banco de dados
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

# Rota para excluir uma tarefa
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # Busca a tarefa pelo id no banco de dados
    task_to_delete = Task.query.get_or_404(task_id)
    db.session.delete(task_to_delete)  # Deleta a tarefa
    db.session.commit()  # Confirma a exclusão no banco de dados

    return redirect(url_for('index'))

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
