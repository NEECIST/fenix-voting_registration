from flask import request
from datetime import datetime
import fenixedu

from app import app, db
from app.models import *

config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')
client = fenixedu.FenixEduClient(config)

@app.route('/')
def index():
    CODE = request.args.get('code')
    user = client.get_user_by_code(CODE)
    person = client.get_person(user)
    
    birthday = datetime.strptime(person["birthday"], "%d/%m/%Y")
    
    p = Person(campus=person["campus"], name=person["name"], gender=person["gender"], username=person["username"], email=person["email"], displayName=person["displayName"], institutionalEmail=person["institutionalEmail"], birthday=birthday)

    photo = Photo(type=person["photo"]["type"], data=person["photo"]["data"])
    p.photo = photo

    personalEmails = []
    for email in person["personalEmails"]:
        personalEmails.append(PersonalEmail(email=email))

    p.personalEmails = personalEmails

    workEmails = []
    for email in person["workEmails"]:
        workEmails.append(WorkEmail(email=email))

    p.workEmails = workEmails

    webAddresses = []
    for url in person["webAddresses"]:
        webAddresses.append(WebAddress(url=url))

    p.webAddresses = webAddresses

    workWebAddresses = []
    for url in person["workWebAddresses"]:
        workWebAddresses.append(WorkWebAddress(url=url))

    p.workWebAddresses = workWebAddresses

    roles = []
    for role in person["roles"]:
        r = Role(type=role["type"])
        
        registrations = []
        for registration in role["registrations"]:
            reg = Registration(registration_id=registration["id"], name=registration["name"], acronym=registration["acronym"])

            terms = []
            for term in registration["academicTerms"]:
                t = AcademicTerm(term=term)
                terms.append(t)

            reg.academicTerms = terms
            registrations.append(reg)
        
        r.registrations = registrations
        roles.append(r)

    p.roles = roles

    db.session.add(p)
    db.session.commit()

    return "Obrigado pelo registo!"
