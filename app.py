from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import smtplib
import sqlite3
from email.message import EmailMessage
from functools import wraps

app = Flask(__name__)
app.secret_key = "troque-essa-chave-secreta"

ADMIN_SENHA = "ballet123"

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "")
EMAIL_SENHA = os.getenv("EMAIL_SENHA", "")
EMAIL_SMTP = os.getenv("EMAIL_SMTP", "smtp.gmail.com")
EMAIL_PORTA = int(os.getenv("EMAIL_PORTA", "465"))


def conectar():
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row
    return conn


def coluna_existe(conn, tabela, coluna):
    colunas = conn.execute(f"PRAGMA table_info({tabela})").fetchall()
    return any(c["name"] == coluna for c in colunas)


def criar_tabelas():
    conn = conectar()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        especialidade TEXT,
        email TEXT
    )
    """)

    # Atualiza bancos antigos que ainda não tinham o campo email
    if not coluna_existe(conn, "professores", "email"):
        conn.execute("ALTER TABLE professores ADD COLUMN email TEXT")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS salas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        capacidade INTEGER NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        professor_id INTEGER NOT NULL,
        sala_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        horario TEXT NOT NULL,
        observacao TEXT,
        FOREIGN KEY(professor_id) REFERENCES professores(id),
        FOREIGN KEY(sala_id) REFERENCES salas(id)
    )
    """)

    conn.commit()
    conn.close()


def enviar_email(destinatario, assunto, mensagem):
    if not destinatario:
        print("E-mail não enviado: professor sem e-mail cadastrado.")
        return False

    if not EMAIL_REMETENTE or not EMAIL_SENHA:
        print("E-mail não enviado: configure EMAIL_REMETENTE e EMAIL_SENHA_APP.")
        print("Destinatário:", destinatario)
        print("Assunto:", assunto)
        print(mensagem)
        return False

    email = EmailMessage()
    email["From"] = EMAIL_REMETENTE
    email["To"] = destinatario
    email["Subject"] = assunto
    email.set_content(mensagem)

    try:
        with smtplib.SMTP_SSL(EMAIL_SMTP, EMAIL_PORTA) as smtp:
            smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
            smtp.send_message(email)
        return True
    except Exception as erro:
        print("Erro ao enviar e-mail:", erro)
        return False


def buscar_reserva(conn, reserva_id):
    return conn.execute("""
    SELECT
        reservas.id,
        reservas.professor_id,
        reservas.sala_id,
        professores.nome AS professor,
        professores.email AS professor_email,
        salas.nome AS sala,
        reservas.data,
        reservas.horario,
        reservas.observacao
    FROM reservas
    JOIN professores ON reservas.professor_id = professores.id
    JOIN salas ON reservas.sala_id = salas.id
    WHERE reservas.id = ?
    """, (reserva_id,)).fetchone()


def texto_comprovante_reserva(reserva):
    observacao = reserva["observacao"] or "Sem observação."

    return f"""Olá, {reserva['professor']}!

Sua reserva foi confirmada com sucesso.

Comprovante da reserva:
Professor(a): {reserva['professor']}
Sala: {reserva['sala']}
Data: {reserva['data']}
Horário: {reserva['horario']}
Observação: {observacao}

Atenciosamente,
Dance Academy
"""


def texto_cancelamento_reserva(reserva):
    observacao = reserva["observacao"] or "Sem observação."

    return f"""Olá, {reserva['professor']}.

Sua reserva foi cancelada pelo administrador.

Dados da reserva cancelada:
Professor(a): {reserva['professor']}
Sala: {reserva['sala']}
Data: {reserva['data']}
Horário: {reserva['horario']}
Observação: {observacao}

Atenciosamente,
Dance Academy
"""


def texto_alteracao_reserva(antiga, nova):
    return f"""Olá, {nova['professor']}.

Sua reserva foi alterada pelo administrador.

Antes:
Sala: {antiga['sala']}
Data: {antiga['data']}
Horário: {antiga['horario']}
Observação: {antiga['observacao'] or 'Sem observação.'}

Agora:
Sala: {nova['sala']}
Data: {nova['data']}
Horário: {nova['horario']}
Observação: {nova['observacao'] or 'Sem observação.'}

Atenciosamente,
Dance Academy
"""


def admin_logado(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if not session.get("admin_logado"):
            return redirect(url_for("login_admin"))
        return f(*args, **kwargs)
    return decorada


criar_tabelas()


@app.route("/")
def index():
    conn = conectar()
    professores = conn.execute("SELECT * FROM professores ORDER BY nome").fetchall()
    salas = conn.execute("SELECT * FROM salas ORDER BY nome").fetchall()

    total_professores = conn.execute("SELECT COUNT(*) FROM professores").fetchone()[0]
    total_salas = conn.execute("SELECT COUNT(*) FROM salas").fetchone()[0]
    total_reservas = conn.execute("SELECT COUNT(*) FROM reservas").fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        professores=professores,
        salas=salas,
        total_professores=total_professores,
        total_salas=total_salas,
        total_reservas=total_reservas
    )


@app.route("/login-admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        senha = request.form.get("senha", "")

        if senha == ADMIN_SENHA:
            session["admin_logado"] = True
            return redirect(url_for("admin"))

        flash("Senha incorreta. Tente novamente.")

    return render_template("login_admin.html")


@app.route("/sair-admin")
def sair_admin():
    session.pop("admin_logado", None)
    return redirect(url_for("index"))


@app.route("/admin")
@admin_logado
def admin():
    return render_template("admin.html")


@app.route("/cadastrar_professor", methods=["POST"])
@admin_logado
def cadastrar_professor():
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    especialidade = request.form.get("especialidade")
    email = request.form.get("email")

    conn = conectar()
    conn.execute("""
    INSERT INTO professores (nome, telefone, especialidade, email)
    VALUES (?, ?, ?, ?)
    """, (nome, telefone, especialidade, email))
    conn.commit()
    conn.close()

    flash("Professor cadastrado com sucesso.")
    return redirect(url_for("admin"))


@app.route("/cadastrar_sala", methods=["POST"])
@admin_logado
def cadastrar_sala():
    nome = request.form.get("nome")
    capacidade = request.form.get("capacidade")

    conn = conectar()
    conn.execute("""
    INSERT INTO salas (nome, capacidade)
    VALUES (?, ?)
    """, (nome, capacidade))
    conn.commit()
    conn.close()

    flash("Sala cadastrada com sucesso.")
    return redirect(url_for("admin"))


@app.route("/reservar", methods=["POST"])
def reservar():
    professor_id = request.form.get("professor_id")
    sala_id = request.form.get("sala_id")
    data = request.form.get("data")
    horario = request.form.get("horario")
    observacao = request.form.get("observacao")

    conn = conectar()

    reserva_existente = conn.execute("""
    SELECT * FROM reservas
    WHERE sala_id = ? AND data = ? AND horario = ?
    """, (sala_id, data, horario)).fetchone()

    if reserva_existente:
        conn.close()
        flash("Esta sala já está reservada neste horário.")
        return redirect(url_for("index"))

    cursor = conn.execute("""
    INSERT INTO reservas (professor_id, sala_id, data, horario, observacao)
    VALUES (?, ?, ?, ?, ?)
    """, (professor_id, sala_id, data, horario, observacao))

    reserva_id = cursor.lastrowid
    conn.commit()

    reserva = buscar_reserva(conn, reserva_id)
    conn.close()

    enviar_email(
        reserva["professor_email"],
        "Comprovante de Reserva - Dance Academy",
        texto_comprovante_reserva(reserva)
    )

    flash("Reserva realizada com sucesso.")
    return redirect(url_for("reservas"))


@app.route("/reservas")
def reservas():
    conn = conectar()

    reservas = conn.execute("""
    SELECT 
        reservas.id,
        professores.nome AS professor,
        professores.email AS professor_email,
        salas.nome AS sala,
        reservas.data,
        reservas.horario,
        reservas.observacao
    FROM reservas
    JOIN professores ON reservas.professor_id = professores.id
    JOIN salas ON reservas.sala_id = salas.id
    ORDER BY reservas.data, reservas.horario
    """).fetchall()

    conn.close()

    return render_template("reservas.html", reservas=reservas)


@app.route("/editar_reserva/<int:id>", methods=["GET", "POST"])
@admin_logado
def editar_reserva(id):
    conn = conectar()

    reserva_antiga = buscar_reserva(conn, id)

    if not reserva_antiga:
        conn.close()
        flash("Reserva não encontrada.")
        return redirect(url_for("reservas"))

    if request.method == "POST":
        professor_id = request.form.get("professor_id")
        sala_id = request.form.get("sala_id")
        data = request.form.get("data")
        horario = request.form.get("horario")
        observacao = request.form.get("observacao")

        conflito = conn.execute("""
        SELECT * FROM reservas
        WHERE sala_id = ? AND data = ? AND horario = ? AND id != ?
        """, (sala_id, data, horario, id)).fetchone()

        if conflito:
            professores = conn.execute("SELECT * FROM professores ORDER BY nome").fetchall()
            salas = conn.execute("SELECT * FROM salas ORDER BY nome").fetchall()
            conn.close()
            flash("Não foi possível alterar: esta sala já está reservada neste horário.")
            return render_template("editar_reserva.html", reserva=reserva_antiga, professores=professores, salas=salas)

        conn.execute("""
        UPDATE reservas
        SET professor_id = ?, sala_id = ?, data = ?, horario = ?, observacao = ?
        WHERE id = ?
        """, (professor_id, sala_id, data, horario, observacao, id))

        conn.commit()

        reserva_nova = buscar_reserva(conn, id)
        conn.close()

        enviar_email(
            reserva_nova["professor_email"],
            "Reserva Alterada - Dance Academy",
            texto_alteracao_reserva(reserva_antiga, reserva_nova)
        )

        flash("Reserva alterada com sucesso.")
        return redirect(url_for("reservas"))

    professores = conn.execute("SELECT * FROM professores ORDER BY nome").fetchall()
    salas = conn.execute("SELECT * FROM salas ORDER BY nome").fetchall()
    conn.close()

    return render_template("editar_reserva.html", reserva=reserva_antiga, professores=professores, salas=salas)


@app.route("/excluir_reserva/<int:id>")
@admin_logado
def excluir_reserva(id):
    conn = conectar()

    reserva = buscar_reserva(conn, id)

    if not reserva:
        conn.close()
        flash("Reserva não encontrada.")
        return redirect(url_for("reservas"))

    conn.execute("DELETE FROM reservas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    enviar_email(
        reserva["professor_email"],
        "Reserva Cancelada - Dance Academy",
        texto_cancelamento_reserva(reserva)
    )

    flash("Reserva excluída com sucesso.")
    return redirect(url_for("reservas"))


if __name__ == "__main__":
    app.run(debug=True)
