from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from flask import flash
from database import Time, db_session



def select_todos_times():
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()
    return times

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