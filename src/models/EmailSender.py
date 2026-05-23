import os
import yagmail
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    @staticmethod
    def enviar_codigo(email, codigo):
        try:
            yag = yagmail.SMTP(
                user = os.getenv("EMAIL_USER"),
                password = os.getenv("EMAIL_PASSWORD")
            )

            yag.send(
                to = email,
                subject = "Recuperación de contraseña",
                contents = f"Tu código es: {codigo}"
            )

            return True, "Enviado!"

        except Exception as err:
            print(f"Error: {err}")
            return False, "Hubo un error al enviar el código, intente nuevamente"