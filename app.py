from flask import Flask, render_template, session, url_for, redirect, request, Response
from models import SecretSanta, db
from random import shuffle


class SecretSantaApp:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secret_santa.db'
        db.init_app(self.app)
        self.register_routes()

    def register_routes(self) -> None:
        self.app.add_url_rule('/', 'home', self.home)
        self.app.add_url_rule('/view_list', 'view_list',
                              self.view_list)
        self.app.add_url_rule('/add_participant', 'add_participant',
                              self.add_participant, methods=['POST'])
        self.app.add_url_rule('/randomize_list',
                              'randomize_list', self.randomize_list, methods=['GET', 'POST'])

    def home(self) -> str:
        all_santas = SecretSanta.query.all()
        return render_template('home.html', participants=all_santas)

    def add_participant(self) -> Response:
        participant = request.form.get('participant')
        santa = SecretSanta(participant, None)

        db.session.add(santa)
        db.session.commit()

        return redirect(url_for('home'))

    def view_list(self) -> str:
        all_santas = SecretSanta.query.all()
        self.hybrid_sort(all_santas)

        return render_template('view_list.html', participants=all_santas)

    def randomize_list(self) -> str | Response:

        all_santas = SecretSanta.query.filter(
            SecretSanta.recipient == None).all()

        if len(all_santas) < 2:
            error_message = 'There are not enough participants added to create a Secret Santa list. Please add more participants.'
            return render_template('home.html',  display_error=error_message)

        if len(all_santas) % 2 != 0:
            error_message = f"Add one more participant to create a Secret Santa list. Otherwise, someone won't get a present!"
            return render_template('home.html',  display_error=error_message)

        santa_list = [santa.name for santa in all_santas]
        shuffle(santa_list)
        recipient_list = [santa.name for santa in all_santas]

        for santa in all_santas:
            recipient = recipient_list.pop()
            santa.recipient = recipient

            db.session.commit()

        return redirect(url_for('view_list'))

    def hybrid_sort(self, all_santas_list: list) -> None:
        if len(all_santas_list) < 15:
            self.insertion_sort(all_santas_list)
        else:
            self.quick_sort(all_santas_list)

    def insertion_sort(self, all_santas_list: list) -> list:
        for i in range(1, len(all_santas_list)):
            key = all_santas_list[i].name
            j = i - 1
            while all_santas_list[j].name > key and j >= 0:
                all_santas_list[j+1].name = all_santas_list[j].name
                j -= 1
            all_santas_list[j+1].name = key
        return all_santas_list

    def quick_sort(self, all_santas_list: list) -> list:
        pivot = all_santas_list.pop()
        grtr_lst, equal_lst, smlr_lst = [], [pivot], []
        for item in all_santas_list:
            if item == pivot:
                equal_lst.append(item)
            elif item > pivot:
                grtr_lst.append(item)
            else:
                smlr_lst.append(item)
        return self.quick_sort(smlr_lst) + equal_lst + self.quick_sort(grtr_lst)


if __name__ == "__main__":
    secret_santa_app = SecretSantaApp()
    with secret_santa_app.app.app_context():
        db.create_all()
    secret_santa_app.app.run(debug=False)
