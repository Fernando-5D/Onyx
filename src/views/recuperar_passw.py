import flet as ft
import random
from controllers.usuarioCtrl import UsuarioCtrl
from models.emailRe import EmailSender

codigo_generado = ""

def recuperar_passw(page: ft.Page):
    email = ft.TextField(label="Correo Electronico",keyboard_type=ft.KeyboardType.EMAIL)

    codigo = ft.TextField(label="Código")
    nueva_passw = ft.TextField(label="Nueva contraseña",password=True)
    alert_email = ft.Text(color=ft.Colors.RED)

    def enviar_codigo():
        global codigo_generado

        if not email.value:
            alert_email.value = "Escribe un correo"
            page.update()
            return

        codigo_generado = str(random.randint(100000, 999999))
        enviado = EmailSender.enviar_codigo(email.value,codigo_generado)

        if enviado:
            alert_email.color = ft.Colors.GREEN
            alert_email.value = "Código enviado"

        else:
            alert_email.color = ft.Colors.RED
            alert_email.value = "Error enviando código"

        page.update()

    def cambiar_passw():
        global codigo_generado
        if not codigo_generado:
            alert_email.color = ft.Colors.RED
            alert_email.value = "Primero envía un código"
            page.update()
            return
        if codigo.value != codigo_generado:
            alert_email.color = ft.Colors.RED
            alert_email.value = "Código incorrecto"
            page.update()
            return

        is_valid, mensaje = UsuarioCtrl().cambiar_passw(email.value,nueva_passw.value)

        if is_valid:
            alert_email.color = ft.Colors.GREEN
            alert_email.value = mensaje

        else:
            alert_email.color = ft.Colors.RED
            alert_email.value = mensaje

        page.update()

    return ft.View(
        route="/recuperar_passw",

        controls=[

            ft.Text(
                "Recuperar Contraseña",
                size=20,
                weight=ft.FontWeight.W_600
            ),
            
            ft.TextButton(
                "Volver a iniciar sesión",
                on_click=lambda _: page.go("/sesion")
                ),

            email,
            ft.Button("Enviar codigo",on_click=lambda _: enviar_codigo()
            ),

            codigo,
            nueva_passw,
            alert_email,
            ft.Button(
                "Cambiar contraseña",
                on_click=lambda _: cambiar_passw()
            )
        ]
    )