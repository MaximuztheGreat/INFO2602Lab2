import click, sys
from models import db, User
from app import app


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('database initialized')


@app.cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob)


@app.cli.command('get-users')
def get_users():
  # gets all objects of a model
  users = User.query.all()
  print(users)


@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  bob.email = email
  db.session.add(bob)
  db.session.commit()
  print(bob)


@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    #let's the database undo any previous steps of a transaction
    db.session.rollback()
    # print(e.orig) #optionally print the error raised by the database
    print("Username or email already taken!")  #give the user a useful message
  else:
    print(newuser)  # print the newly created user
