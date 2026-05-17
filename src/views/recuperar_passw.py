import flet as ft
from controllers.usuarioCtrl import UsuarioCtrl

def recuperar_passw(page: ft.Page):
    email = ft.TextField(label="Correo Electronico", suffix=".com", keyboard_type=ft.KeyboardType.EMAIL)
    alert_email = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
        
    def recuperar_passwClick():
        alert_email.visible = False
        
        if not email.value:
            alert_email.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_email.visible = True
        
        if email.value:
            email_format = f"{email.value}.com"
            is_valid, mensaje = UsuarioCtrl().recuperar_passw(email_format) # type: ignore
            if not is_valid:
                alert_email.controls[1].value = mensaje # type: ignore
                alert_email.visible = True
            else:
                page.go("/sesion")
            
        page.update()
    
    return ft.View(
        route="/recuperar_passw",
        controls=[
            ft.Text("Recuperar Contraseña", size=20, weight=ft.FontWeight.W_600),
            ft.Text(
                "Escribe tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.",
                text_align=ft.TextAlign.LEFT
            ),
            email,
            alert_email,
            ft.Button("Enviar Enlace", on_click=lambda _: recuperar_passwClick())
        ],
        margin=ft.Margin(2),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        spacing=0
    )