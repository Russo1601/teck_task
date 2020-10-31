from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    adress = Column(String)

class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    status = Column(String)
    date_visit = Column(String)


class UserObject:
    def __init__(self, name, phone, adress, services):
        self.name = name
        self.phone = phone
        self.adress = adress
        self.services = services

    def __str__(self):
        return f"name = {self.name}, phone = {self.phone}, adress = {self.adress},"\
            f"services = {[str(service) for service in self.services]}"


class ServiceObject:
    def __init__(self, id,  user_id, status, date_visit):
        self.id = id
        self.user_id = user_id
        self.status = status
        self.date_visit = date_visit

    def __str__(self):
        return f"id = {self.id}, user_id = {self.user_id}, status = {self.status}, date_visit = {self.date_visit}"


def get_users(session):
    users_objects = {}
    result = session.query(User, Service).filter(User.id == Service.user_id).all()
    for user, service in result:
        service_object = ServiceObject(service.id, service.user_id, service.status, service.date_visit)
        if user.id in users_objects:
            users_objects[user.id].services.append(service_object)
        else:
            users_objects[user.id] = UserObject(user.name, user.phone, user.adress, [service_object])
    return users_objects.values()



if __name__ == "__main__":
    engine = create_engine('sqlite:///services.db', echo = True)
    Session = sessionmaker(bind = engine)
    session = Session()
    # Base.metadata.create_all(engine)
    # session.add_all([
    #     User(name = 'Geralt', phone = '+124235981623', adress = 'Kaer Morhen'),
    #     User(name = 'Yennefer', phone = '+124235943123', adress = 'Vengerberg'),
    #     User(name = 'Ciri', phone = '+124235356853', adress = 'Cintra'),
    #     Service(user_id = 1, status = 'Success', date_visit = '12.12.1260'),
    #     Service(user_id = 2, status = 'Success', date_visit = '17.06.1260'),
    #     Service(user_id = 3, status = 'Failure', date_visit = '24.09.1260'),
    #     Service(user_id = 3, status = 'Success', date_visit = '26.09.1260'),
    #     ]
    # )
    # session.commit()

    for user in get_users(session):
        print(str(user))

    # I`ve tried to implemet additional task, but after setuping AWS user, Acces Token 
    # and docker I`ve got some nasty problem. Execution of 'serverless deploy' command gave me
    # Invalid requirement: '\ "x00'" Error. That was happening because during deploy for some 
    # reason characters in .serverless\requirements.txt file transormed into chinese ieroglifs :/
    # I found that not only me faced with this issue, but not any solution worked for me.