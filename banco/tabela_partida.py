from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from flask import flash
from database import Partida, db_session



def select_todas_partidas():
    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()
    return partidas

def salvar(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida ):
    try:
        nova_partida = Partida(time_casa_id=time_casa_id,time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
        db_session.add(nova_partida)
        db_session.commit()
        flash("Partida salva com sucesso!", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Houve um erro. Tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Houve um erro. Tente novamente", "error")
        print(f"{e}")