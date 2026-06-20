import sqlite3

conn = sqlite3.connect("banco.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS professores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    especialidade TEXT,
    email TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS salas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    capacidade INTEGER NOT NULL
)
""")

professores = [
    ("Profª Ana Clara", "(51) 99999-9999", "ana.clara@email.com", "Ballet Clássico"),
    ("Profª Marina Lopes", "(51) 98888-8888", "marina.lopes@email.com", "Baby Class"),
    ("Profª Helena Duarte", "(51) 97777-7777", "helena.duarte@email.com", "Jazz e Alongamento"),
]

salas = [
    ("Sala Rosa", 12),
    ("Sala Clássica", 18),
    ("Sala Espelho", 10),
]

conn.executemany("""
INSERT INTO professores (nome, telefone, email, especialidade)
VALUES (?, ?, ?, ?)
""", professores)

conn.executemany("""
INSERT INTO salas (nome, capacidade)
VALUES (?, ?)
""", salas)

conn.commit()
conn.close()

print("Dados inseridos com sucesso!")
