from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from flask import flash
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import Partida, db_session, Time



def select_todas_partidas():
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)



    partidas_sql = (
        select(Partida, TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante,Partida.time_visitante_id == TimeVisitante.id)
    )

    #executar o select
    partidas_casa = db_session.execute(partidas_sql).all()
    return partidas_casa

def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    quantidade_total = db_session.execute(partidas_sql).scalar()
    return quantidade_total
print(select_quantidade_total())

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