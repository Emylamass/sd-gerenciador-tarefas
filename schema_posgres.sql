/* cria a tabela */
DROP TABLE IF EXISTS tarefas;

CREATE TABLE sd (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title CHAR(50) NOT NULL,
    content CHAR(100) NOT NULL
);

/* insere dados iniciais */
INSERT INTO tarefas(tarefa, descricao) VALUES 
('First Tarefa', 'Content for the first tarefa');

INSERT INTO tarefas(tarefa, descricao) VALUES 
('Seg Tarefa', 'Content for the Seg tarefa');
