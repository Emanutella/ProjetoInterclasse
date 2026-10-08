from sqlalchemy import select,func
from sqlalchemy.exc import SQLAlchemyError
from flask import flash
from database import Time, db_session, Jogador


def select_todos_times():
    times_sql = (
        select(Time, func.count(Jogador.id).label("jogadores"))
        .outerjoin(Jogador, Jogador.time_id == Time.id)
        .group_by(Time.id)
    )
    times = db_session.execute(times_sql).all()
    return times

def select_quantidade_total():
    times_sql = select(func.count(Time.id))
    quantidade_total = db_session.execute(times_sql).scalar()
    return quantidade_total
print(select_quantidade_total())

def salvar(nome, turma, responsavel):
    try:
        novo_time = Time(nome=nome, responsavel=responsavel, turma=turma)
        db_session.add(novo_time)
        db_session.commit()
        flash("Time criado com sucesso!", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Houve um erro. Tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Houve um erro. Tente novamente", "error")
        print(f"{e}")