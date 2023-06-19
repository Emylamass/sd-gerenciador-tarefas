import os
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect

# cria a conexao com o BD
def get_db_connection():
    # load_dotenv()
    conn = psycopg2.connect(
        host="localhost",
        database="sd",
        user=os.getenv('DB_USERNAME'),
        password=os.environ['DB_PASSWORD']
    )
    return conn

# query todos os tarefas no banco
def get_tarefa(tarefa_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tarefas WHERE id = %s', (tarefa_id,))
    tarefa = cur.fetchone()
    cur.close()
    conn.close()
    return tarefa

# cria o serviço
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET_KEY_DEV')

# definicao das rotas
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tarefas')
    tarefas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tarefas=tarefas)

@app.route('/<int:tarefa_id>')
def post(tarefa_id):
    tarefa = get_tarefa(tarefa_id)
    if tarefa is None:
        return render_template('404.html')
    return render_template('tarefa.html', tarefa=tarefa)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        tarefa = request.form['tarefa']
        descricao = request.form['descricao']

        if not tarefa:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO tarefas (tarefa, descricao) VALUES (%s, %s)',
                         (tarefa, descricao))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    tarefa = get_tarefa(id)

    if tarefa is None:
        return render_template('404.html')

    if request.method == 'POST':
        tarefa = request.form['tarefa']
        descricao = request.form['descricao']

        if not tarefa:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('UPDATE tarefas SET tarefa = %s, descricao = %s'
                         ' WHERE id = %s',
                         (tarefa, descricao, id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', tarefa=tarefa)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    tarefa = get_tarefa(id)
    if tarefa is None:
        return render_template('404.html')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tarefas WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('"{}" was successfully deleted!'.format(tarefa[2]))
    return redirect(url_for('index'))

# inicia servico
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)