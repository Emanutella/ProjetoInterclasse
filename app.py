from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_partida, tabela_jogador
from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()

    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()

    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()
    return render_template(
        "dashboard.html",
        total_jogadores=len(jogadores),
        total_times=len(times),
        total_partidas=len(partidas),

    )


@app.route("/jogadores")
def listar_jogadores():
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()

    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()

    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None
        if not nome:
            flash("Preencha este campo!", "error")
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash("Preencha este campo!", "error")
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash("Preencha este campo!", "error")
            return redirect(url_for("novo_jogador"))
        if not time_id:
            flash("Preencha este campo!", "error")
            return redirect(url_for("novo_jogador"))
            # 3-Salvar no banco
        tabela_jogador.salvar(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)

    jogadores = tabela_jogador.select_todos_jogadores()
    times = tabela_time.select_todos_times()
    return render_template("jogadores.html", jogadores=jogadores, times=times)



@app.route("/times")
def listar_times():
    # Buscar todos os times no banco
    # 1-Montar o select
    times_sql = select(Time)
    # 2-Executar o select
    times = db_session.execute(times_sql).scalars().all()
    return render_template("times.html", times=times)

@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":
        #1-Pegar os valores digitados no Form
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel","").strip()
        turma = request.form.get("turma","").strip()
        #2-Verificar se foi digitado
        if not nome:
            flash("Preencha este campo!", "error")
            return redirect(url_for("novo_time"))
        if not responsavel:
            flash("Preencha este campo!", "error")
            return redirect(url_for("novo_time"))
        if not turma:
            flash("Preencha este campo!", "error")
            return redirect(url_for("novo_time"))
        #3-Salvar no banco
        tabela_time.salvar(nome=nome, responsavel=responsavel, turma=turma)

    times = tabela_time.select_todos_times()
    return render_template("times.html", times=times)



@app.route("/partidas")
def listar_partidas():
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()

    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()
    return render_template("partidas.html", partidas=partidas, times=times)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        if not time_casa_id:
            flash("Preencha este campo!", "error")
            return redirect(url_for("nova_partida"))
        if not time_visitante_id:
            flash("Preencha este campo!", "error")
            return redirect(url_for("nova_partida"))
        if not gols_casa:
            flash("Preencha este campo!", "error")
            return redirect(url_for("nova_partida"))
        if not gols_visitante:
            flash("Preencha este campo!", "error")
            return redirect(url_for("nova_partida"))
        if not data_partida:
            flash("Preencha este campo!", "error")
            return redirect(url_for("nova_partida"))
        if time_visitante_id == time_casa_id:
            flash("Selecione outro time!", "error")
            return redirect(url_for("nova_partida"))

        # 3-Salvar no banco
        tabela_partida.salvar(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = tabela_partida.select_todas_partidas()
    times = tabela_time.select_todos_times()
    return render_template("partidas.html", partidas=partidas,times=times)
if __name__ == "__main__":
    app.run(debug=True)
