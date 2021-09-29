from flask_mail import Message
import os
from .. import mail


class Messages:
    ConfirmationEmail = {'m': 'El email {} ha sido confirmado correctamente. <br>Ya puede acceder con su nueva contraseña',
                         's': 'Adamo - Email confirmado'}
    SendUrl = {'m': 'Para poder validar su correo y crear su contraseña entre en este <a href="{}">enlace</a>',
               's':  'Adamo - Validar email'}
    ChangePassword = {'m': 'Para poder cambiar su contraseña entre en este <a href="{}">enlace</a>',
                      's':  'Adamo - Cambiar contraseña'}

    @staticmethod
    def send_email(message, recipient, *params):
        message = Message(subject=message['s'], html=message['m'].format(*list(params)),
                          sender=os.environ.get('MAIL_USERNAME', 'adamo@gmail.com'),
                          recipients=[recipient])
        mail.send(message)
        return 'sent'
