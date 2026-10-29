from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_partida, tabela_jogador
from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times = tabela_time.select_quantidade_total()
    jogadores = tabela_jogador.select_quantidade_total()
    partidas = tabela_partida.select_quantidade_total()

    return render_template(
        "dashboard.html",
        total_jogadores= jogadores,
        total_times= times,
        total_partidas= partidas

    )


@app.route("/jogadores")
def listar_jogadores():

    jogadores = tabela_jogador.select_todos_jogadores()

    return render_template("jogadores.html", jogadores=jogadores)


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

@app.route("/jogadores/<id_jogador>", methods=["GET", "POST"])
def editar_jogador(id_jogador):
    # Buscar o jogador no banco
    jogador = tabela_jogador.select_um(id_jogador)
    # Salvar as alterações
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None
        if not nome:
            flash("Preencha este campo!", "error")
        if not numero_camisa:
            flash("Preencha este campo!", "error")
        if not posicao:
            flash("Preencha este campo!", "error")
        if not time_id:
            flash("Preencha este campo!", "error")
        else:
            jogador.nome = nome
            jogador.numero_camisa = numero_camisa
            jogador.posicao = posicao
            jogador.time_id = int(time_id)
            db_session.commit()

            flash("Jogador editado com sucesso!", "success")
        return redirect(url_for("listar_jogadores"))
    # Carregar as informações
    jogadores = tabela_jogador.select_todos_jogadores()
    times = tabela_time.select_todos_times()
    return render_template("jogadores.html", jogadores=jogadores, editar=jogador, times=times)

@app.route("/times")
def listar_times():
    times = tabela_time.select_todos_times()
    return render_template("times.html", times=times)

@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":
        #1-Pegar os valores digitados no Form
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel","").strip()
        turma = request.form.get("turma","").strip()
        jogadores_ids = request.form.getlist("jogadores")
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
        time = tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

        if jogadores_ids:
            for jogador_id in jogadores_ids:
                jogador = tabela_jogador.select_um(jogador_id)
                jogador.time_id = time.id
                db_session.add(jogador)
                db_session.commit()

    times = tabela_time.select_todos_times()
    jogadores = tabela_jogador.select_todos_jogadores()
    return render_template("times.html", times=times, jogadores=jogadores)


@app.route("/times/<id_time>", methods=["GET", "POST"])
def detalhes_time(id_time):
    time = tabela_time.select_um(int(id_time))
    jogadores= tabela_jogador.select_jogadores_por_time(int(id_time)) # Fazer uma função que traga todos os jogadores do time
    partidas= tabela_partida.select_partidas_por_time(int(id_time))
    return render_template(
        "time_detalhes.html",
        time=time,
        jogadores=jogadores,
        partidas=partidas,
        qtd_jogadores=len(jogadores),
        qtd_partidas=len(partidas))


@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todas_partidas()
    return render_template("partidas.html", partidas=partidas)


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
            return render_template("partida.html")

        # 3-Salvar no banco
        tabela_partida.salvar(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = tabela_partida.select_todas_partidas()
    times = tabela_time.select_todos_times()
    return render_template("partidas.html", partidas=partidas,times=times)
if __name__ == "__main__":
    app.run(debug=True)
