from datetime import datetime, timedelta
import sqlite3


class Pessoa:
    def __init__(self, nome, telefone, nacionalidade):
        self.nome = nome
        self.telefone = telefone
        self.nacionalidade = nacionalidade

class Autor(Pessoa):
    def __init__(self, nome, telefone, nacionalidade):
        super().__init__(nome, telefone, nacionalidade)

class Usuario(Pessoa):
    def __init__(self, nome, telefone, nacionalidade):
        super().__init__(nome, telefone, nacionalidade)

class Livro:
    def __init__(self, titulo, editora, generos, renovacoes_maximas=3):
        self.titulo = titulo
        self.editora = editora
        self.generos = generos
        self.renovacoes_maximas = renovacoes_maximas

class Livro_Disponivel:
    def __init__(self, livro, estado="Disponível"):
        self.livro = livro
        self.estado = estado

class Emprestar:
    def __init__(self, livro_disponivel, usuario):
        self.livro_disponivel = livro_disponivel
        self.usuario = usuario
        self.data_emprestimo = datetime.now()
        self.data_devolucao = self.data_emprestimo + timedelta(days=14)
        self.estado = "Emprestado"

    def devolver(self):
        self.livro_disponivel.estado = "Disponível"
        self.estado = "Devolvido"


conn = sqlite3.connect('biblioteca.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Livro (
        LivroID INTEGER PRIMARY KEY,
        Titulo TEXT,
        Editora TEXT,
        Generos TEXT,
        RenovacoesMaximas INTEGER
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Exemplar (
        ExemplarID INTEGER PRIMARY KEY,
        LivroID INTEGER,
        Estado TEXT,
        FOREIGN KEY (LivroID) REFERENCES Livro(LivroID)
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        UsuarioID INTEGER PRIMARY KEY,
        Nome TEXT,
        Telefone TEXT,
        Nacionalidade TEXT
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Emprestar (
        EmprestimoID INTEGER PRIMARY KEY,
        ExemplarID INTEGER,
        UsuarioID INTEGER,
        DataEmprestimo DATETIME,
        DataDevolucao DATETIME,
        Estado TEXT,
        FOREIGN KEY (ExemplarID) REFERENCES Exemplar(ExemplarID),
        FOREIGN KEY (UsuarioID) REFERENCES Usuario(UsuarioID)
    )
''')


cursor.execute('INSERT INTO Livro (Titulo, Editora, Generos, RenovacoesMaximas) VALUES (?, ?, ?, ?)',
               ('Livro 1', 'Editora A', 'Ação, Aventura', 3))
cursor.execute('INSERT INTO Livro (Titulo, Editora, Generos, RenovacoesMaximas) VALUES (?, ?, ?, ?)',
               ('Livro 2', 'Editora B', 'Romance', 3))
cursor.execute('INSERT INTO Usuario (Nome, Telefone, Nacionalidade) VALUES (?, ?, ?)',
               ('Usuario 1', '111222333', 'Brasileiro'))
cursor.execute('INSERT INTO Usuario (Nome, Telefone, Nacionalidade) VALUES (?, ?, ?)',
               ('Usuario 2', '444555666', 'Estrangeiro'))

# Commit para salvar as alterações no banco de dados
conn.commit()

# Criando livro com exemplares
livro1 = Livro("Livro 1", "Editora A", ["Ação"])
livro2 = Livro("Livro 2", "Editora B", ["Romance"])

# Inserindo livros na tabela Livro
cursor.execute('INSERT INTO Livro (Titulo, Editora, Generos, RenovacoesMaximas) VALUES (?, ?, ?, ?)',
               (livro1.titulo, livro1.editora, ', '.join(livro1.generos), livro1.renovacoes_maximas))
cursor.execute('INSERT INTO Livro (Titulo, Editora, Generos, RenovacoesMaximas) VALUES (?, ?, ?, ?)',
               (livro2.titulo, livro2.editora, ', '.join(livro2.generos), livro2.renovacoes_maximas))

# Inserindo exemplares na tabela Exemplar
for i in range(2):  # Criando 2 exemplares para cada livro
    cursor.execute('INSERT INTO Exemplar (LivroID, Estado) VALUES (?, ?)', (i + 1, 'Disponível'))

# Realizando empréstimos
emprestimo1 = Emprestar(Livro_Disponivel(livro1), Usuario("Usuario 1", "111222333", "Brasileiro"))
emprestimo2 = Emprestar(Livro_Disponivel(livro2), Usuario("Usuario 2", "444555666", "Estrangeiro"))

# Inserindo empréstimos na tabela Emprestimo
cursor.execute('INSERT INTO Emprestar (ExemplarID, UsuarioID, DataEmprestimo, DataDevolucao, Estado) VALUES (?, ?, ?, ?, ?)',
               (1, 1, emprestimo1.data_emprestimo, emprestimo1.data_devolucao, 'Emprestado'))
cursor.execute('INSERT INTO Emprestar (ExemplarID, UsuarioID, DataEmprestimo, DataDevolucao, Estado) VALUES (?, ?, ?, ?, ?)',
               (2, 2, emprestimo2.data_emprestimo, emprestimo2.data_devolucao, 'Emprestado'))


# Devolução
emprestimo1.devolver()


# Commit para salvar as alterações no banco de dados
conn.commit()

# Consulta SQL para verificar o estado dos exemplares
cursor.execute('SELECT * FROM Exemplar')
print("Estado dos Livros após devolução:")
for row in cursor.fetchall():
    print(row)



# Fechando a conexão com o banco de dados
conn.close()