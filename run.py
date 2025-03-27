from celery import Celery, Task
from flask_mail import Mail

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
    celery_app.config_from_object("celery_config")
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    # Flask-Mail configuration for MailHog
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_PORT'] = 1025  # MailHog SMTP port
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@serviceapp.com'

    # Initialize Flask-Mail
    mail = Mail(app)
    app.extensions["mail"] = mail

    return celery_app