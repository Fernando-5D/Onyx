import flet as ft
from controllers.usuarioCtrl import UsuarioCtrl

def sesion(page: ft.Page):
    email = ft.TextField(label="Correo Electronico", suffix=".com", keyboard_type=ft.KeyboardType.EMAIL)
    alert_email = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        margin=ft.Margin(5, 2, bottom=5),
        visible=False
    )
    
    passw = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, margin=ft.Margin(top=10))
    alert_passw = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        margin=ft.Margin(5, 2, bottom=5),
        visible=False
    )
    
    alertD_passw = ft.AlertDialog()
    
    def entrarClick():
        alert_email.visible = alert_passw.visible = False
        
        if not email.value:
            alert_email.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_email.visible = True
        
        if not passw.value:
            alert_passw.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_passw.visible = True
        
        if email.value and passw.value:
            is_valid, mensaje = UsuarioCtrl().iniciar_sesion(email.value, passw.value) # type: ignore
            if not is_valid:
                if "correo" in mensaje:
                    alert_email.controls[1].value = mensaje # type: ignore
                    alert_email.visible = True
                elif "contraseña" in mensaje:
                    alert_passw.controls[1].value = mensaje # type: ignore
                    alert_passw.visible = True
                else:
                    alert_email.controls[1].value = alert_passw.controls[1].value = mensaje # type: ignore
                    alert_email.visible = alert_passw.visible = True
            else:
                page.session.store.set("user", email.value)
                page.go("/dashboard")
            
        page.update()
    
    def recuperar_passw():
        return
    
    return ft.View(
        route="/sesion",
        controls=[
            ft.Column(
                [
                    ft.Image(
                        "assets/images/onyx_dark.png" if page.platform_brightness == ft.Brightness.DARK else "assets/images/onyx_light.png",
                        width=150
                    ),
                    ft.Text("Iniciar Sesión", size=20, weight=ft.FontWeight.W_600, margin=ft.Margin(top=35, bottom=20)),
                    email,
                    alert_email,
                    passw,
                    alert_passw,
                    ft.Button(
                        ft.Text("Entrar", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                        bgcolor="#5c71eb",
                        width=300,
                        style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=5)),
                        margin=ft.Margin(top=25),
                        on_click=lambda _: entrarClick()
                    ),
                    ft.TextButton(
                        ft.Text("No tengo una cuenta", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE),
                        width=300,
                        style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=5)),
                        margin=ft.Margin(top=5),
                        on_click=lambda _: page.go("/registro")
                    ),
                    ft.TextButton(
                        ft.Text(
                            "¿Olvidaste tu contraseña?",
                            size=15,
                            weight=ft.FontWeight.W_400,
                            color=ft.Colors.ON_SURFACE
                        ),
                        width=300,
                        style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=5)),
                        margin=ft.Margin(top=30),
                        on_click=lambda _: recuperar_passw()
                    )
                ],
                margin=ft.Margin(1),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )