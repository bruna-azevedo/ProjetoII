from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from dotenv import load_dotenv
import smtplib
import sqlite3
from datetime import datetime, timedelta
from email.message import EmailMessage
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = "troque-essa-chave-secreta"

ADMIN_SENHA = "ballet123"

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "danceacademyproject@gmail.com")
EMAIL_SENHA = os.getenv("EMAIL_SENHA", "dgldxnumbuothlzy")
EMAIL_SMTP = os.getenv("EMAIL_SMTP", "smtp.gmail.com")
EMAIL_PORTA = int(os.getenv("EMAIL_PORTA", "465"))

@app.context_processor
def contexto_admin():
    return {"admin_autenticado": bool(session.get("admin_logado"))}

@app.after_request
def desativar_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def conectar():
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row
    return conn


def coluna_existe(conn, tabela, coluna):
    colunas = conn.execute(f"PRAGMA table_info({tabela})").fetchall()
    return any(c["name"] == coluna for c in colunas)


def calcular_horario_fim(horario_inicio, duracao_minutos):
    inicio = datetime.strptime(horario_inicio, "%H:%M")
    fim = inicio + timedelta(minutes=int(duracao_minutos))
    return fim.strftime("%H:%M")


def existe_conflito_reserva(conn, sala_id, data, horario_inicio, horario_fim, reserva_id=None):
    """
    Verifica conflito por intervalo:
    existe conflito quando a nova reserva começa antes do fim de outra
    e termina depois do início de outra.
    """
    parametros = [sala_id, data, horario_fim, horario_inicio]

    filtro_id = ""
    if reserva_id is not None:
        filtro_id = " AND id != ?"
        parametros.append(reserva_id)

    return conn.execute(f"""
    SELECT * FROM reservas
    WHERE sala_id = ?
      AND data = ?
      AND horario < ?
      AND horario_fim > ?
      {filtro_id}
    """, parametros).fetchone()


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
        horario_fim TEXT,
        duracao_minutos INTEGER,
        observacao TEXT,
        FOREIGN KEY(professor_id) REFERENCES professores(id),
        FOREIGN KEY(sala_id) REFERENCES salas(id)
    )
    """)

    # Atualiza bancos antigos que ainda não tinham duração e horário final
    if not coluna_existe(conn, "reservas", "horario_fim"):
        conn.execute("ALTER TABLE reservas ADD COLUMN horario_fim TEXT")

    if not coluna_existe(conn, "reservas", "duracao_minutos"):
        conn.execute("ALTER TABLE reservas ADD COLUMN duracao_minutos INTEGER")

    # Preenche dados antigos para manter compatibilidade
    reservas_sem_fim = conn.execute("""
    SELECT id, horario FROM reservas
    WHERE horario_fim IS NULL OR horario_fim = ''
    """).fetchall()

    for reserva in reservas_sem_fim:
        horario_fim = calcular_horario_fim(reserva["horario"], 60)
        conn.execute("""
        UPDATE reservas
        SET horario_fim = ?, duracao_minutos = ?
        WHERE id = ?
        """, (horario_fim, 60, reserva["id"]))

    conn.commit()
    conn.close()


def enviar_email(destinatario, assunto, mensagem, mensagem_html=None):
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

    if mensagem_html:
        email.add_alternative(mensagem_html, subtype="html")

    try:
        with smtplib.SMTP_SSL(EMAIL_SMTP, EMAIL_PORTA) as smtp:
            smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
            smtp.send_message(email)
        return True
    except Exception as erro:
        print("Erro ao enviar e-mail:", erro)
        return False


def formatar_data_br(data_iso):
    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return data_iso


def campo_html(rotulo, valor):
    return f"""
        <tr>
            <td style="padding: 10px 12px; border-bottom: 1px solid #f1d8e3; color: #8a4b68; font-weight: 700; width: 38%;">{rotulo}</td>
            <td style="padding: 10px 12px; border-bottom: 1px solid #f1d8e3; color: #333333;">{valor}</td>
        </tr>
    """


def template_email_reserva(titulo, saudacao, mensagem_principal, reserva, cor="#c76d95"):
    observacao = reserva["observacao"] or "Sem observação."
    data_formatada = formatar_data_br(reserva["data"])
    horario = f"{reserva['horario']} às {reserva['horario_fim']}"

    return f"""\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{titulo}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8f1f5; font-family: Arial, Helvetica, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f1f5; padding: 28px 0;">
        <tr>
            <td align="center">
                <table width="620" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 18px; overflow: hidden; box-shadow: 0 8px 24px rgba(120, 60, 90, 0.16);">
                    <tr>
                        <td style="background: linear-gradient(135deg, #f4c7dc, #c76d95); padding: 28px 32px; text-align: center;">
                            <div style="font-size: 38px; line-height: 1;">🩰</div>
                            <h1 style="margin: 10px 0 4px; color: #ffffff; font-size: 26px;">Dance Academy</h1>
                            <p style="margin: 0; color: #fff5fa; font-size: 15px;">Sistema de Reserva de Salas</p>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 32px;">
                            <span style="display: inline-block; background-color: #fde8f1; color: {cor}; padding: 8px 14px; border-radius: 999px; font-size: 13px; font-weight: 700;">
                                {titulo}
                            </span>

                            <h2 style="color: #4b2f3b; margin: 18px 0 8px; font-size: 24px;">{saudacao}</h2>
                            <p style="color: #5f5f5f; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
                                {mensagem_principal}
                            </p>

                            <table width="100%" cellpadding="0" cellspacing="0" style="border: 1px solid #f1d8e3; border-radius: 14px; overflow: hidden; background-color: #fffafd;">
                                {campo_html("Professor(a)", reserva["professor"])}
                                {campo_html("Sala", reserva["sala"])}
                                {campo_html("Data", data_formatada)}
                                {campo_html("Horário", horario)}
                                {campo_html("Observação", observacao)}
                            </table>

                            <p style="color: #777777; font-size: 14px; line-height: 1.6; margin: 24px 0 0;">
                                Esta é uma mensagem automática enviada pelo sistema Dance Academy.
                            </p>
                        </td>
                    </tr>

                    <tr>
                        <td style="background-color: #fff3f8; padding: 18px 32px; text-align: center; color: #9b5876; font-size: 13px;">
                            Atenciosamente,<br>
                            <strong>Equipe Dance Academy</strong>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def texto_para_linhas(texto):
    return "".join(f"<p style='margin: 8px 0; color: #555555; line-height: 1.5;'>{linha}</p>" for linha in texto.splitlines() if linha.strip())


def template_email_alteracao(antiga, nova):
    return f"""\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Reserva Alterada</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8f1f5; font-family: Arial, Helvetica, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f1f5; padding: 28px 0;">
        <tr>
            <td align="center">
                <table width="620" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 18px; overflow: hidden; box-shadow: 0 8px 24px rgba(120, 60, 90, 0.16);">
                    <tr>
                        <td style="background: linear-gradient(135deg, #f4c7dc, #c76d95); padding: 28px 32px; text-align: center;">
                            <div style="font-size: 38px; line-height: 1;">🩰</div>
                            <h1 style="margin: 10px 0 4px; color: #ffffff; font-size: 26px;">Dance Academy</h1>
                            <p style="margin: 0; color: #fff5fa; font-size: 15px;">Sistema de Reserva de Salas</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 32px;">
                            <span style="display: inline-block; background-color: #fde8f1; color: #c76d95; padding: 8px 14px; border-radius: 999px; font-size: 13px; font-weight: 700;">
                                Reserva Alterada
                            </span>

                            <h2 style="color: #4b2f3b; margin: 18px 0 8px; font-size: 24px;">Olá, {nova['professor']}.</h2>
                            <p style="color: #5f5f5f; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
                                Sua reserva foi alterada pelo administrador. Confira abaixo os dados anteriores e os novos dados.
                            </p>

                            <h3 style="color: #8a4b68; margin: 0 0 10px;">Antes</h3>
                            <table width="100%" cellpadding="0" cellspacing="0" style="border: 1px solid #f1d8e3; border-radius: 14px; overflow: hidden; background-color: #fffafd; margin-bottom: 22px;">
                                {campo_html("Sala", antiga["sala"])}
                                {campo_html("Data", formatar_data_br(antiga["data"]))}
                                {campo_html("Horário", f"{antiga['horario']} às {antiga['horario_fim']}")}
                                {campo_html("Observação", antiga["observacao"] or "Sem observação.")}
                            </table>

                            <h3 style="color: #8a4b68; margin: 0 0 10px;">Agora</h3>
                            <table width="100%" cellpadding="0" cellspacing="0" style="border: 1px solid #f1d8e3; border-radius: 14px; overflow: hidden; background-color: #fffafd;">
                                {campo_html("Sala", nova["sala"])}
                                {campo_html("Data", formatar_data_br(nova["data"]))}
                                {campo_html("Horário", f"{nova['horario']} às {nova['horario_fim']}")}
                                {campo_html("Observação", nova["observacao"] or "Sem observação.")}
                            </table>

                            <p style="color: #777777; font-size: 14px; line-height: 1.6; margin: 24px 0 0;">
                                Esta é uma mensagem automática enviada pelo sistema Dance Academy.
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #fff3f8; padding: 18px 32px; text-align: center; color: #9b5876; font-size: 13px;">
                            Atenciosamente,<br>
                            <strong>Equipe Dance Academy</strong>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def html_comprovante_reserva(reserva):
    return template_email_reserva(
        "Reserva Confirmada",
        f"Olá, {reserva['professor']}!",
        "Sua reserva foi confirmada com sucesso. Confira abaixo os dados da reserva:",
        reserva,
        "#2f8f5b"
    )


def html_cancelamento_reserva(reserva):
    return template_email_reserva(
        "Reserva Cancelada",
        f"Olá, {reserva['professor']}.",
        "Sua reserva foi cancelada pelo administrador. Confira abaixo os dados da reserva cancelada:",
        reserva,
        "#b94a48"
    )


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
        reservas.horario_fim,
        reservas.duracao_minutos,
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
Horário: {reserva['horario']} às {reserva['horario_fim']}
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
Horário: {reserva['horario']} às {reserva['horario_fim']}
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
Horário: {antiga['horario']} às {antiga['horario_fim']}
Observação: {antiga['observacao'] or 'Sem observação.'}

Agora:
Sala: {nova['sala']}
Data: {nova['data']}
Horário: {nova['horario']} às {nova['horario_fim']}
Observação: {nova['observacao'] or 'Sem observação.'}

Atenciosamente,
Dance Academy
"""


def admin_logado(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if not session.get("admin_logado"):
            flash("Apenas o administrador logado pode editar ou excluir reservas.")
            return redirect(url_for("login_admin", next=request.path))
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
            proxima_pagina = request.args.get("next")
            if proxima_pagina:
                return redirect(proxima_pagina)
            return redirect(url_for("admin"))

        flash("Senha incorreta. Tente novamente.")

    return render_template("login_admin.html", next_url=request.args.get("next", ""))


@app.route("/sair-admin")
def sair_admin():
    session.pop("admin_logado", None)
    flash("Você saiu da área administrativa.")
    return redirect(url_for("reservas"))


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
    duracao_minutos = request.form.get("duracao_minutos", "60")
    observacao = request.form.get("observacao")
    horario_fim = calcular_horario_fim(horario, duracao_minutos)

    conn = conectar()

    reserva_existente = existe_conflito_reserva(conn, sala_id, data, horario, horario_fim)

    if reserva_existente:
        conn.close()
        flash("Esta sala já está reservada em um horário que entra em conflito com a duração escolhida.")
        return redirect(url_for("index"))

    cursor = conn.execute("""
    INSERT INTO reservas (professor_id, sala_id, data, horario, horario_fim, duracao_minutos, observacao)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (professor_id, sala_id, data, horario, horario_fim, duracao_minutos, observacao))

    reserva_id = cursor.lastrowid
    conn.commit()

    reserva = buscar_reserva(conn, reserva_id)
    conn.close()

    enviar_email(
        reserva["professor_email"],
        "Comprovante de Reserva - Dance Academy",
        texto_comprovante_reserva(reserva),
        html_comprovante_reserva(reserva)
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
        reservas.horario_fim,
        reservas.duracao_minutos,
        reservas.observacao
    FROM reservas
    JOIN professores ON reservas.professor_id = professores.id
    JOIN salas ON reservas.sala_id = salas.id
    ORDER BY reservas.data, reservas.horario
    """).fetchall()

    conn.close()

    return render_template(
        "reservas.html",
        reservas=reservas,
        admin_autenticado=bool(session.get("admin_logado"))
    )


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
        duracao_minutos = request.form.get("duracao_minutos", "60")
        observacao = request.form.get("observacao")
        horario_fim = calcular_horario_fim(horario, duracao_minutos)

        conflito = existe_conflito_reserva(conn, sala_id, data, horario, horario_fim, id)

        if conflito:
            professores = conn.execute("SELECT * FROM professores ORDER BY nome").fetchall()
            salas = conn.execute("SELECT * FROM salas ORDER BY nome").fetchall()
            conn.close()
            flash("Não foi possível alterar: esta sala já está reservada em um horário que entra em conflito com a duração escolhida.")
            return render_template("editar_reserva.html", reserva=reserva_antiga, professores=professores, salas=salas)

        conn.execute("""
        UPDATE reservas
        SET professor_id = ?, sala_id = ?, data = ?, horario = ?, horario_fim = ?, duracao_minutos = ?, observacao = ?
        WHERE id = ?
        """, (professor_id, sala_id, data, horario, horario_fim, duracao_minutos, observacao, id))

        conn.commit()

        reserva_nova = buscar_reserva(conn, id)
        conn.close()

        enviar_email(
            reserva_nova["professor_email"],
            "Reserva Alterada - Dance Academy",
            texto_alteracao_reserva(reserva_antiga, reserva_nova),
            template_email_alteracao(reserva_antiga, reserva_nova)
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
        texto_cancelamento_reserva(reserva),
        html_cancelamento_reserva(reserva)
    )

    flash("Reserva excluída com sucesso.")
    return redirect(url_for("reservas"))


if __name__ == "__main__":
    app.run(debug=True)
