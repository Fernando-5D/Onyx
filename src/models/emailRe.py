import os
import yagmail
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    @staticmethod
    def enviar_codigo(email, codigo):
        try:
            yag = yagmail.SMTP(user=os.getenv("EMAIL_USER"),
                password=os.getenv("EMAIL_PASSWORD")
            )

            yag.send(
                to=email,
                subject="Recuperación de contraseña",
                contents=f"Tu código es: {codigo}"
            )

            return True

        except Exception as e:
            print("Error:", e)
            return False

