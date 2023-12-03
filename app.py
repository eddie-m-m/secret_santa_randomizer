from flask import Flask, render_template, session, url_for, redirect, request
from models import SecretSanta, db


class SecretSantaApp:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secret_santa.db'
        db.init_app(self.app)
        self.register_routes()

    def register_routes(self):
        # home (/GET ?)
        self.app.add_url_rule('/', 'home', self.home)
        # view_list (/GET ?)
        self.app.add_url_rule('/view_list', 'view_list',
                              self.view_list)
        # add_santa: /POST
        self.app.add_url_rule('/add_santa/<int: santa_id> ', 'add_santa',
                              self.add_santa, methods=['POST'])
        # randomize_list: /GET /POST
        self.app.add_url_rule('/randomize_list',
                              'randomize_list', self.randomize_list, methods=['GET', 'POST'])

    def home(self):
        # enables dynamic updating of participant list from user inputs
        all_santas = SecretSanta.query.all()
        return render_template('home.html', participants=all_santas)

    def add_santa(self):
        participant = request.form.get('participant')
        santa = SecretSanta(participant)

        db.session.add(santa)
        db.session.commit()

        return redirect(url_for('home'))

    def view_list(self):
        # retrieves all db info for display
        all_santas = SecretSanta.query.all()
        # return db results ordered by name in ascending order
        return render_template('view_list.html', participants=all_santas)

    def randomize_list(self):
        pass
        # all_santas = SecretSanta.query.all()
        # initalize santa_list, recipient_list from all_santas

        # sort santa_list by name (santa) in ascending order with hybrid insertion/quicksort (threshold == 14)
        # randomly assign recipient to santa:
        # after matching a recipient to a santa, pop santa from santa_list and pop recipient from recipient_list
        # repeat until lists are empty

        # return redirect(url_for('view_list'))

        # EDGE CASES:
        # odd number of santas input to db
        # duplicate names (santa, recipient)
        # validate for alphabetic input
        # strip whitespace from input


if __name__ == "__main__":
    with SecretSantaApp().app.app_context():
        db.create_all()
    SecretSantaApp().app.run(debug=True)
