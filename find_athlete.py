import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы,
    если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    Session = sessionmaker(engine)
    session = Session()
    return session


def list_atheletes():
    session = connect_db()
    atheletes = session.query(Atheletes).all()
    return atheletes


def list_users():
    session = connect_db()
    users = session.query(User).all()
    return users


class Atheletes(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)


def get_id():
    num_id = int(input("Введи номер id: "))
    return num_id


def find(num_id, session):
    """
    Производит поиск пользователя в таблице user по заданному id
    """
    query = session.query(User).filter(User.id == num_id).first()
    return query


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    num_id = get_id()
    user = find(num_id, session)
    if user:
        print("Найден пользователь: %s %s; рост: %s." % (user.first_name, user.last_name, user.height))
    else:
        print("Такого пользователя нет!")
    atheletes = list_atheletes()
    for athelete in atheletes:
        if athelete.height == user.height:
            print("Близок по росту %s из %s." % (athelete.name, athelete.country))
            break

if __name__ == "__main__":
    main()
