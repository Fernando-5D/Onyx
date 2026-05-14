import flet as ft
from controllers.paginaCtrl import PaginaCtrl
from views.components.ClassButton import ClassButton

def dashboard(page: ft.Page):
    def cambiar_tema(e):
        if page.theme_mode == ft.ThemeMode.SYSTEM:
            page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.Icons.LIGHT_MODE
            
        elif page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.Icons.DARK_MODE
            
        else:
            page.theme_mode = ft.ThemeMode.SYSTEM
            e.control.icon = ft.Icons.CONTRAST
        
        page.update()
    
    def obtener_data(email, campo = "*"):
        return PaginaCtrl().obtener_data(email, campo)
    
    nombre_usuario = "Usuario"
    if obtener_data(page.session.store.get("user"), "nombre"):
        nombre_usuario = obtener_data(page.session.store.get("user"), "nombre")["nombre"] # type: ignore
        
        if len(nombre_usuario) > 10:
            nombre_usuario.replace(nombre_usuario[-3], "...")
    
    return ft.View(
        route="/dashboard",
        controls=[
            ft.AppBar(
                title=ft.Text(
                    "Onyx",
                    weight=ft.FontWeight.W_700
                ),
                actions=[
                    ft.Row(
                        [
                            ft.Text(nombre_usuario, size=15, weight=ft.FontWeight.W_500),
                            ft.IconButton(
                                ft.Icons.PERSON,
                                margin=ft.Margin(right=6),
                                on_click=lambda _: page.go("/usuario")
                            )
                        ],
                        spacing=0
                    )
                ],
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH
            ),
            ft.Column(
                [
                    
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            )
        ]
    )