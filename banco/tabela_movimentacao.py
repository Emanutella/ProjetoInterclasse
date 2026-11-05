from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from database import Partida, db_session, Time, Jogador, Movimentacao
from datetime import datetime

def select_todos():
    TimeOrigem = aliased(Time)
    TimeDestino = aliased(Time)

    movimentacoes_sql = (
        select(Movimentacao, Jogador, TimeOrigem, TimeDestino)
        .join(Jogador, Movimentacao.jogador_id == Jogador.id)
        .outerjoin(TimeOrigem, Movimentacao.time_origem_id == TimeOrigem.id)
        .outerjoin(TimeDestino, Movimentacao.time_destino_id == TimeDestino.id)
    )
    movimentacoes = db_session.execute(movimentacoes_sql).all()
    return movimentacoes


def select_quantidade_total():
    movimentacoes_sql = select(func.count(Movimentacao.id))
    qtd_total = db_session.execute(movimentacoes_sql).scalar()
    return qtd_total

def salvar(jogador, time_destino):
    try:
        jogador_sql = select(Jogador).where(Jogador.id == jogador)
        jogador_resultado = db_session.execute(jogador_sql).scalar_one_or_none()

        if not jogador_resultado:
            flash("jogador não encontrado!", "error")
            return
        time_origem_id = jogador_resultado.time_id

        #Validar se o jogador já pertence ao time destino
        if time_origem_id == time_destino:
            flash("O jogador já pertence a este time!", "error")
            return

        #Obter data e hora atual
        data_atual = datetime.now()

        #Atualizar o time do jogador
        jogador_resultado.time_id = time_destino

        movimentacao_nova = Movimentacao(
            jogador_id = int(jogador),
            time_origem_id = time_origem_id,
            time_destino_id = int(time_destino),
            data_movimentacao = data_atual
        )
        db_session.add(movimentacao_nova)
        db_session.commit()
        flash("Movimentação realizada com sucesso!", "success")
    except SQLAlchemyError as e:
        print(e)
        db_session.rollback()
        flash("Ocorreu um erro. Tente novamente", "error")
    except Exception as e:
        print(e)
        db_session.rollback()
        flash("Ocorreu um erro. Tente novamente", "error")