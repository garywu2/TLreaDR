from user_service.models import db
from user_service.app import create_app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates the models tables"""
    db.create_all()


@manager.command
def drop_db():
    """Drops all models tables"""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
