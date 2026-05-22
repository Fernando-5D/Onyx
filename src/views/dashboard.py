import flet as ft
from controllers.UsuarioCtrl import UsuarioCtrl
from views.components.ClassButton import ClassButton

def dashboard(page: ft.Page):
    def obtener_data(email, campo = "*"):
        return UsuarioCtrl().obtener_data(email, campo)
    
    nombre_usuario = "Usuario"
    if obtener_data(page.session.store.get("user"), "nombre"):
        nombre_usuario = obtener_data(page.session.store.get("user"), "nombre")["nombre"] # type: ignore
        
        if len(nombre_usuario) > 10:
            nombre_usuario.replace(nombre_usuario[-3], "...")
    
    return ft.View(
        route="/dashboard",
        controls=[
            ft.AppBar(
                title=ft.Row(
                    [
                        ft.Image(
                            "assets/images/onyx_dark.png" if page.platform_brightness == ft.Brightness.DARK else "assets/images/onyx_light.png",
                            width=30,
                            color=ft.Colors.ON_SURFACE
                        ),
                        ft.Text("Onyx", weight=ft.FontWeight.W_600, margin=ft.Margin(bottom=0))
                    ]
                ),
                actions=[
                    ft.Row(
                        [
                            ft.Text(nombre_usuario, size=15, weight=ft.FontWeight.W_500, margin=ft.Margin(bottom=1)),
                            ft.IconButton(
                                ft.Icons.PERSON,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                                margin=ft.Margin(10, 1, 15),
                                on_click=lambda _: page.go("/usuario")
                            )
                        ],
                        spacing=0
                    )
                ],
                bgcolor=ft.Colors.SURFACE_CONTAINER
            ),
            ft.Column(
                [
                    
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            )
        ]
    )