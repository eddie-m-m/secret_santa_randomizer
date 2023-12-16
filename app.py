from flask import Flask, render_template, session, url_for, redirect, request, Response
from models import SecretSanta, db
from random import shuffle
from collections import deque


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
        self.app.add_url_rule(
            '/clear_list', 'clear_list', self.clear_list)

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
        if len(all_santas) == 0:
            error_message = f'Add participants to create a Secret Santa list!'
            return render_template('home.html', display_message=error_message)

        santas = [(santa.name, santa.recipient) for santa in all_santas]

        self.hybrid_sort(santas)

        return render_template('view_list.html', participants=santas)

    def clear_list(self) -> str:
        db.session.query(SecretSanta).delete()
        db.session.commit()

        return redirect(url_for('home'))

    def randomize_list(self) -> str | Response:
        all_santas = SecretSanta.query.all()

        if len(all_santas) == 1:
            error_message = f"Add at least one more participant to create a Secret Santa list."
            return render_template('home.html',  display_message=error_message)

        santa_list = [santa.name for santa in all_santas]
        shuffle(santa_list)
        shuffle(all_santas)
        recipient_deque = deque(santa_list)

        for santa in all_santas:
            recipient = recipient_deque.pop()
            while recipient == santa.name:
                recipient_deque.appendleft(recipient)
                recipient = recipient_deque.pop()

            santa.recipient = recipient
        db.session.commit()

        return redirect(url_for('view_list'))

    def hybrid_sort(self, santas: list) -> None:
        self.quick_sort(santas) if len(
            santas) > 15 else self.insertion_sort(santas)

    def insertion_sort(self, santas: list) -> list:
        for i in range(1, len(santas)):
            key = santas[i]
            j = i - 1
            while santas[j] > key and j >= 0:
                santas[j + 1] = santas[j]
                j -= 1
            santas[j + 1] = key
        return santas

    def quick_sort(self, santas: list) -> list:
        if len(santas) < 2:
            return santas

        pivot = santas.pop()[0]
        left, middle, right = [], [pivot], []

        right = [santa for santa in santas if santa[0] > pivot]
        middle = [
            santa for santa in santas if santa[0] == pivot]
        left = [santa for santa in santas if santa[0] < pivot]

        return self.quick_sort(left) + middle + self.quick_sort(right)


if __name__ == "__main__":
    secret_santa_app = SecretSantaApp()
    with secret_santa_app.app.app_context():
        db.create_all()
    secret_santa_app.app.run(debug=False)
