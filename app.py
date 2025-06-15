import datetime
from datetime import datetime, timedelta



from flask import Flask, redirect, render_template, request

import models
import database

app = Flask(__name__)

# приклад
# user = database.db_session.query(models.User).filter_by(login=username,pasword=pasword).first()
# smth = database.db_session.execute(select(models.Client).where(client_name=name).first()

def calculate_end_time(start_time_str):
    # Припустимо, тривалість 1 година
    from datetime import datetime, timedelta
    t = datetime.strptime(start_time_str, "%H:%M")
    end = t + timedelta(hours=1)
    return end.strftime("%H:%M")

@app.get('/')
def index():
    return render_template('invitation.html')
    #return redirect('/')


@app.get('/services/')  # відображає форму для заповнення
def service_form():
    return render_template('services.html')


@app.post('/services/')# заповняю форму з одним сервісом
def fill_services_form():
    # беру форму з services і заповнюю її
    # form_data = request.form
    # database.init_db()
    #
    # перевіряю чи є вже такий сервіс у базі!!!!!!!! думаю,що це не вірно
    # service = database.db_session.query(models.Service.type_of_service,
    #                                     models.Service.price.filter_by(
    #                                         service=type_of_service
    #                                     )
    # if service is None:
    #     service = models.Service(type_of_service=form_data["type_of_service"],
    #                              price=form_data["price"])
    #     database.db_session.add(service)
    #     database.db_session.commit()
    # else:
    #     return f"you have already written this service"
    #     redirect('/services/')
    #return render_template('services.html')
    #
    # можливо просто пододавати сервіси ось так і все

    form_data = request.form
    database.init_db()
    service = models.Service(name=form_data['type_of_service'],# name-це в моделях
                             price=int(form_data['price']))# type_of_service-в темплейті
    database.db_session.add(service)
    database.db_session.commit()
    return redirect('/')


@app.get('/services/delete/')
def delete_service_form():
    services = database.db_session.query(models.Service).all()
    return render_template('services_delete.html', services=services)


@app.post('/services/delete/')
def delete_service():
    form_data = request.form
    service_name = form_data.get('type_of_service')

    service = database.db_session.query(models.Service).filter_by(name=service_name).first()
    if service:
        database.db_session.delete(service)
        database.db_session.commit()
        return redirect('/')
    else:
        return "Service not found"

    #return redirect('/services/')  #name - in template, data-here
    #return render_template('services_delete.html', services=services)
    #database.db_session.delete()


@app.get('/clients/form/')  # відображає форму для заповнення
def client_form():
    return render_template('client_registration.html')


@app.post('/clients/form/') # заповняю форму з одним клієнтом
def fill_client_form():#перероблю потім,щоб перевіряло чи є вже такий клієнт
    form_data = request.form
    database.init_db()

    client = models.Client(name=form_data['name'],
                           birth_date=form_data['birth_date'],
                            # birth_date=datetime.datetime.strptime(form_date['birth_date'],"%y-%m-%d"),
                           #birth_date=datetime.datetime.fromisoformat(birth_date_str),
                            racket_tension=form_data['racket_tension'],
                            phone=form_data['phone'],
                            email=form_data['email'])
    database.db_session.add(client)
    database.db_session.commit()
    return render_template('client_registration.html')
    # return redirect('/clients/form/') не можна тут редірект!!!!



@app.get('/clients/')  # відображає список усіх клієнтів
def show_all_clients():
    database.init_db()
    clients = database.db_session.query(models.Client).all()
    return render_template('clients_list.html',clients=clients)


@app.get('/clients/info/') #  здається не працює інф про конкретного клієнта з кнопкою по id
def redirect_to_client_info():
    client_id = request.args.get('client_id')
    return redirect(f'/clients/{client_id}/')# f` - це щоб {client_id} побачити


@app.get('/clients/<int:client_id>/') # інф про конкретного клієнта
def get_client_info(client_id):
    database.init_db()
    data = (database.db_session.query(models.Client.name, models.Client.birth_date,
    models.Client.racket_tension, models.Client.phone, models.Client.email)
            .filter_by(id=client_id).first())
    return render_template('client_info.html', client=data)


@app.post('/clients/update/') #дороблю потім
def update_client(client_id):
    pass


@app.get('/clients/delete/')
def delete_client_form():
    clients = database.db_session.query(models.Client).all()
    return render_template('client_delete.html', clients=clients)#, services=services)


@app.post('/clients/delete/')
def delete_client():
    database.init_db()
    form_data = request.form
    client_name = form_data.get('name')
    client_for_delete = (database.db_session.query(models.Client).
                         filter_by(name=client_name).first())
    if client_for_delete:
        database.db_session.delete(client_for_delete)
        database.db_session.commit()
    #return render_template('clients_list.html')# чим відрізняються??????????????
    return redirect('/clients/')# чим відрізняються??????????????


# корти - все працює
@app.get('/courts/')# інф про всі корти
def show_all_courts():
    database.init_db()
    list_of_courts = database.db_session.query(models.Court).all()
    return render_template('courts_list.html', courts=list_of_courts)


@app.get('/courts/form/')#форма для заповнення
def courts_form():
    return render_template('court_form.html')

@app.post('/courts/form/')#заповнити форму
def fill_courts_form():
    form_data = request.form
    database.init_db()
    court = models.Court(name=form_data['name'],  # name-це в моделях, 'name' -in template
                         coach_payment=int(form_data['coach_payment']),
                         business_time_cost=int(form_data['business_time_cost']),
                         regular_time_cost=int(form_data['regular_time_cost']),
                         weekend_time_cost=int(form_data['weekend_time_cost']),
                         phone=form_data['phone'],
                         type_of_courts=form_data['type_of_courts'])
    database.db_session.add(court)
    database.db_session.commit()
    return redirect('/courts/form/')


@app.get('/courts/delete/')
def delete_court_form():
    courts = database.db_session.query(models.Court).all()
    return render_template('courts_delete.html', courts=courts)


@app.post('/courts/delete/')
def delete_court():
    form_data = request.form
    court_name = form_data.get('name')

    court= database.db_session.query(models.Court).filter_by(name=court_name).first()
    if court:
        database.db_session.delete(court)
        database.db_session.commit()
        return redirect('/courts/')
    else:
        return "courts not found"


@app.get('/reservation/')# резервейшн це частина скедул
def reservation_form():
    database.init_db()
    courts = database.db_session.query(models.Court).all()
    services = database.db_session.query(models.Service).all()
    clients = database.db_session.query(models.Client).all()

    return render_template('reservation.html', courts=courts, services=services, clients=clients)


@app.post('/reservation/')# заповнити форму
def add_reservation():
    form_data = request.form
    database.init_db()
    reservation = models.Reservation(court_id=int(form_data['court_id']),
                                     client_id=int(form_data['client_id']),
                                     service_id=int(form_data['service_id']),
                                     date=form_data['date'],
                                     time=form_data['time'])
                                     # datetime.datetime.fromisoformat(form_data['date'])
    database.db_session.add(reservation)
    database.db_session.commit()

    # Дістати додаткову інформацію (можна, щоб вона була в шаблоні одразу)
    service_id = int(form_data['service_id'])
    service = database.db_session.query(models.Service).filter_by(id=service_id).first()

    # Створення відповідного запису у Schedule
    start_time_str = form_data['time']
    start_time = datetime.strptime(start_time_str, '%H:%M')
    end_time = (start_time + timedelta(hours=1)).strftime('%H:%M')

    # schedule = models.Schedule(
    #     date=form_data['date'],
    #     service_id=int(form_data['service_id']),
    #     start_time=start_time_str,
    #     end_time=end_time
    #     #start_time=form_data['time'],
    #     #end_time=''  # Можна додати окреме поле для end_time у формі
    # )




    schedule = models.Schedule(
        date=form_data['date'],
        service_id=service_id,
        start_time=form_data['time'],
        end_time=calculate_end_time(form_data['time'])  # функція на початку
    )


    database.db_session.add(schedule)
    database.db_session.commit()

    return render_template('reservation.html')





@app.post('/reservation/update/')#потім зроблю
def update_reservation(reservation_id):
    pass

# не працює
# @app.post('/reservation/delete/<int:reservation_id>/')# всі резервації з номерами можна в скедул подивитись
# def delete_reservation():# (reservation_id) можливо так в дужках треба
#     form_data = request.form
#     reservation_id = form_data.get('id')
#     reservation_delete = (database.db_session.query(models.Schedule).
#                           filter_by(id=reservation_id).first())
#     database.db_session.delete(reservation_delete)
#     database.db_session.commit()
#     #return redirect('/reservation/')
#     return redirect('/schedule/schedule_by_day/') #id=reservation_delete)


# в темплейті зробити випадайку з датами і по датах показати ліст з резерваціями на
# цю дату в ('/schedule/schedule_by_day/')

@app.post('/reservation/delete/')
def delete_reservation():
    database.init_db()
    form_data = request.form
    reservation_id = form_data.get('id')


    reservation_delete = (database.db_session.query(models.Reservation)
                          .filter_by(id=reservation_id).first())

    if reservation_delete:
        database.db_session.delete(reservation_delete)
        database.db_session.commit()

    return redirect('/schedule/')


@app.get('/schedule/')
def show_schedule_form():
    return render_template('schedule.html')


@app.get('/schedule/schedule_by_day/')
def show_schedule_by_day():
    # selected_date = request.args.get('date')# my working variant
    # database.init_db()
    #
    # # якщо фільтрувати за місяцем
    # reservations = (database.db_session.query(models.Schedule)
    #                 .filter(models.Schedule.date.like(f'{selected_date}%'))
    #                 .all())
    # return render_template('schedule_by_day.html', reservations=reservations)#,selected_date=selected_date)

    # selected_date = request.args.get('date') # my best working variant
    # database.init_db()
    # reservations = (database.db_session.query(
    #     models.Schedule.date.like(f'{selected_date}%'),
    #     models.Schedule.id,
    #     models.Schedule.start_time,
    #     models.Schedule.end_time,
    #     models.Service.name.label("service_name")
    # )
    # .join(models.Service, models.Schedule.service_id == models.Service.id)
    # .all())
    #
    # return render_template('schedule_by_day.html', reservations=reservations)

    selected_date = request.args.get('date')
    database.init_db()
    reservations = (database.db_session.query(
        models.Reservation.date,
        models.Reservation.id,# не знаю як ай ді правильно
        models.Reservation.time.label("start_time"),
        models.Service.name.label("service_name"),
        models.Client.name.label("client_name"),
        models.Court.name.label("court_name")
    )
                    .join(models.Service, models.Reservation.service_id == models.Service.id)
                    .join(models.Client, models.Reservation.client_id == models.Client.id)
                    .join(models.Court, models.Reservation.court_id == models.Court.id)
                    .filter(models.Reservation.date == selected_date)
                    .order_by(models.Reservation.time)# models.Reservation.date,
                    .all())

    return render_template('schedule_by_day.html', reservations=reservations,
                           selected_date=selected_date)

    # if not selected_date:
    #     return render_template('schedule_by_day.html', reservations=[], message="Choose date!")
    # тут запит до бази даних by_day, але як красиво це зобразити???
    # database.init_db()
    # list_of_reservations = database.db_session.query(models.Schedule).all()
    # return render_template('schedule_by_day.html', reservations=list_of_reservations)


# @app.post('/schedule/schedule_by_day/')# можливо краще пост зробити
# def show_schedule_by_day():
#     selected_date = request.form.get('date')
#     database.init_db()
#     list_of_reservations = (database.db_session.query(models.Schedule)
#                             .filter(models.Schedule.date == selected_date)
#                             .all())
#     return render_template('schedule_by_day.html', reservations=list_of_reservations)
#


@app.get('/money/')
def money_form():
    return render_template('money_form.html')

# dont count((((((((((
@app.get('/money/money_by_month/')
def show_money_by_month():
    month = request.args.get('month')
    database.init_db()

    reservations = (database.db_session.query(models.Schedule)
                    .filter_by(date=month).all())

# не спрацює, якщо date — повна дата. Треба змінити на щось типу
    # спробуй .filter(models.Schedule.date.like(f'{month}-%'))
                    #date['як взяти місяць з дати']).all()
    sum = 20500
    for reservation in reservations:

        service_obj = database.db_session.query(
            models.Service).filter_by(id=reservation.service_id).first()
        sum = sum + service_obj.price

    return render_template('money_by_month.html',# amount = sum)
                           money={"month": month, "amount": sum})#  amount=sum),# amount-in template,sum-here


# money_by_month = database.db_session.query(models.зі Schedule взяти усі id(це резервації),потім з них
# взяти servise_id, а з нього взяти price. і кожну id зі  Schedule  додати )

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000 # 8080- postgres?
    app.run(host=host, port=port, debug=True)
