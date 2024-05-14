from flask import request, make_response
from datetime import datetime
import fenixedu

from app import app, db
from app.models import *


config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')
client = fenixedu.FenixEduClient(config)

def create_person(person_data):
    birthday = datetime.strptime(person_data["birthday"], "%d/%m/%Y")

    p = Person(campus=person_data["campus"], name=person_data["name"], gender=person_data["gender"], username=person_data["username"], email=person_data["email"], displayName=person_data["displayName"], institutionalEmail=person_data["institutionalEmail"], birthday=birthday)

    photo = Photo(type=person_data["photo"]["type"], data=person_data["photo"]["data"])
    p.photo = photo

    personal_emails = []
    for email in person_data["personalEmails"]:
        personal_emails.append(PersonalEmail(email=email))

    p.personal_emails = personal_emails

    work_mails = []
    for email in person_data["workEmails"]:
        work_mails.append(WorkEmail(email=email))

    p.workEmails = work_mails

    web_addresses = []
    for url in person_data["webAddresses"]:
        web_addresses.append(WebAddress(url=url))

    p.webAddresses = web_addresses

    work_web_addresses = []
    for url in person_data["workWebAddresses"]:
        work_web_addresses.append(WorkWebAddress(url=url))

    p.workWebAddresses = work_web_addresses

    roles = []
    for role in person_data["roles"]:
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

@app.route('/')
def index():
    CODE = request.args.get('code')
    if CODE is None:
        
        return """
               <!DOCTYPE html>
               <html lang="en">
               <head>
                   <meta charset="UTF-8">
                   <meta http-equiv="X-UA-Compatible" content="IE=edge">
                   <meta name="viewport" content="width=device-width, initial-scale=1.0">
                   <title>Confirmação de Registo de Voto</title>
                   <style>
                       body {
                           font-family: Arial, sans-serif;
                           background-color: #f9f9f9;
                           text-align: center;
                           padding: 20px;
                       }
                       .container {
                           max-width: 600px;
                           margin: 0 auto;
                           background-color: #fff;
                           padding: 20px;
                           border-radius: 8px;
                           box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                       }
                       h1 {
                           color: #333;
                       }
                       p {
                           color: #666;
                           font-size: 1.1em;
                       }
                   </style>
               </head>
               <body>
                   <div class="container">
                       <h1>Para fazeres o registo como votante para as eleições do NEECIST acede a:</h1>
                       <p>
                            <a href="https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=2821814988308503&redirect_uri=https://voting-test.midas-cloud.xyz/">Registo e Autorização</a>
                       </p>
                       <p>
                           Obrigado!
                       </p>
                   </div>
               </body>
               </html>
               """

    user = client.get_user_by_code(CODE)
    person = client.get_person(user)

    if Person.query.filter(Person.username == person["username"]).first() is None:
        print(person)
        create_person(person)

    return  """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Confirmação de Registo de Voto</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    text-align: center;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333;
                }
                p {
                    color: #666;
                    font-size: 1.1em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Obrigado por te registares para as eleições do NEECIST</h1>
                <p>
                    As eleições vão ocorrer durante o dia xx de xxxx.
                </p>
                <p>
                    No dia anterior ao das eleições será enviado um email que conterá o teu link pessoal para a plataforma <a href="https://vote.heliosvoting.org/">Helios</a>.
                </p>
                <p>
                    Obrigado e até lá!
                </p>
            </div>
        </body>
        </html>
        """


@app.route('/temporary-path')
def records():
    people = Person.query.join(Role).filter(Role.type == "STUDENT").join(Registration).all()

    csv = ""
    for entry in people:
        for reg in entry.roles[0].registrations:
            academic_terms = AcademicTerm.query.filter(AcademicTerm.registration_id == reg.id).all()
            for term in academic_terms:
                if term.term == ("1º semestre 2023/2024"):
                    csv += str(entry) + "\n"
                    break
    
    response = make_response(csv, 200)
    response.mimetype = "application/json"

    return response