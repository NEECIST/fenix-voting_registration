from app import db
from sqlalchemy.orm import relationship

class AcademicTerm(db.Model):
    __tablename__ = "academicTerms"
    id = db.Column(db.Integer, primary_key=True)
    
    registration_id = db.Column(db.Integer, db.ForeignKey('registrations.id'))

    term = db.Column(db.String)

class Registration(db.Model):
    __tablename__ = "registrations"
    id = db.Column(db.Integer, primary_key=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    registration_id = db.Column(db.String)
    name = db.Column(db.String)
    acronym = db.Column(db.String)
    academicTerms = relationship("AcademicTerm") 

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

    type = db.Column(db.String)
    registrations = relationship("Registration")

    def __str__(self):
        string = f"{self.type}\n"
        return string

class Photo(db.Model):
    __tablename__ = "photos"
    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = relationship("Person", back_populates="photo")

    type = db.Column(db.String)
    data = db.Column(db.Text)

class PersonalEmail(db.Model):
    __tablename__ = "personalEmails"
    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

    email = db.Column(db.String)

class WorkEmail(db.Model):
    __tablename__ = "workEmails"
    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

    email = db.Column(db.String)

class WebAddress(db.Model):
    __tablename__ = "webAddresses"
    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

    url = db.Column(db.String)

class WorkWebAddress(db.Model):
    __tablename__ = "workWebAddresses"
    id = db.Column(db.Integer, primary_key=True)
    
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

    url = db.Column(db.String)

class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)

    campus = db.Column(db.String)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    birthday = db.Column(db.Date)
    username = db.Column(db.String)
    email = db.Column(db.String)
    displayName = db.Column(db.String)
    institutionalEmail = db.Column(db.String)

    roles = relationship("Role")
    photo = relationship("Photo", uselist=False, back_populates="person")
    personalEmails = relationship("PersonalEmail")
    workEmails = relationship("WorkEmail")
    webAddresses = relationship("WebAddress")
    workWebAddresses = relationship("WorkWebAddress")

    def __str__(self):
        string = f"password,{self.username},{self.email},{self.name}\n"
        return string
    
    def __repr__(self):
        return self.__str__()
