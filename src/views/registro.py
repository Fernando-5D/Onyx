import flet as ft
from controllers.UsuarioCtrl import UsuarioCtrl

def registro(page: ft.Page):
    nombre = ft.TextField(label="Nombre de Usuario")
    alert_nombre = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR, margin=ft.Margin(top=2)),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
    
    email = ft.TextField(label="Correo Electrónico", keyboard_type=ft.KeyboardType.EMAIL, margin=ft.Margin(top=10))
    alert_email = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR, margin=ft.Margin(top=2)),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
    
    passw = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, margin=ft.Margin(top=10))
    alert_passw = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR, margin=ft.Margin(top=2)),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
    
    def registrateClick():
        alert_nombre.visible = alert_email.visible = alert_passw.visible = False
        
        if not nombre.value:
            alert_nombre.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_nombre.visible = True
            
        if not email.value:
            alert_email.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_email.visible = True
        
        if not passw.value:
            alert_passw.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_passw.visible = True
        
        if nombre.value and email.value and passw.value:
            is_valid, mensaje = UsuarioCtrl().registrar(nombre.value, email.value, passw.value) # type: ignore
            if not is_valid:
                if "nombre" in mensaje:
                    alert_nombre.controls[1].value = mensaje # type: ignore
                    alert_nombre.visible = True
                elif "correo" in mensaje:
                    alert_email.controls[1].value = mensaje # type: ignore
                    alert_email.visible = True
                elif "contraseña" in mensaje:
                    alert_passw.controls[1].value = mensaje # type: ignore
                    alert_passw.visible = True
                else:
                    alert_nombre.controls[1].value = alert_email.controls[1].value = alert_passw.controls[1].value = mensaje # type: ignore
                    alert_nombre.visible = alert_email.visible = alert_passw.visible = True
            else:
                page.go("/sesion")
            
        page.update()
    
    return ft.View(
        route="/registro",
        controls=[
            ft.Text("Registrate", size=20, weight=ft.FontWeight.W_600, margin=ft.Margin(top=30, bottom=20)),
            nombre,
            alert_nombre,
            email,
            alert_email,
            passw,
            alert_passw,
            ft.Button(
                ft.Text("Registrarme", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                bgcolor="#5c71eb",
                width=300,
                style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10)),
                margin=ft.Margin(top=28),
                on_click=lambda _: registrateClick()
            ),
            ft.TextButton(
                ft.Text("Ya tengo una cuenta", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE),
                width=300,
                style=ft.ButtonStyle(bgcolor=ft.Colors.SURFACE_CONTAINER, padding=15, shape=ft.RoundedRectangleBorder(radius=10)),
                margin=ft.Margin(top=5),
                on_click=lambda _: page.go("/sesion")
            )
        ],
        margin=ft.Margin(2),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        spacing=0
    )