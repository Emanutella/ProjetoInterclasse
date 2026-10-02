from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from flask import flash
from database import Jogador, db_session



def select_todos_jogadores():
    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return jogadores

def salvar(nome, time_id, numero_camisa, posicao):
    try:
        novo_jogador = Jogador(nome=nome,time_id=time_id , numero_camisa=numero_camisa, posicao=posicao)
        db_session.add(novo_jogador)
        db_session.commit()
        flash("Jogador salvo com sucesso!", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Houve um erro. Tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Houve um erro. Tente novamente", "error")
        print(f"{e}")