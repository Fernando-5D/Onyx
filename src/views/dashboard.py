import flet as ft
from controllers.UsuarioCtrl import UsuarioCtrl

def dashboard(page: ft.Page):
    panel_control_desk = ft.Container(
        ft.Column(
            [
                ft.Text("Paginas", size=20, weight=ft.FontWeight.W_600),
                ft.Divider(),
                ft.TextButton(
                    ft.Text("esto es una nota de prueba", size=20, weight=ft.FontWeight.W_500),
                    style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10))
                )
            ],
        ),
        col=3,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        expand=True,
        padding=15,
        visible=True
    )
    
    editor = ft.Column(
        [
            ft.Row(
                [
                    ft.PopupMenuButton(
                        icon=ft.Icons.ARROW_BACK,
                        items=[
                            ft.PopupMenuItem("Guardar y salir", ft.Icons.SAVE),
                            ft.PopupMenuItem("Descartar cambios", ft.Icon(ft.Icons.CLOSE, color=ft.Colors.ERROR))
                        ],
                        bgcolor=ft.Colors.SURFACE_CONTAINER,
                        tooltip=""
                    ),
                    ft.IconButton(ft.Icons.ARTICLE_OUTLINED, bgcolor=ft.Colors.SURFACE_CONTAINER),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.ERROR, bgcolor=ft.Colors.SURFACE_CONTAINER)
                ]
            ),
            ft.Container(
                ft.TextField(hint_text="Sin Titulo", multiline=True, border=ft.InputBorder.NONE, expand=True),
                padding=ft.Padding(10, right=10)
            ),
            ft.Divider(),
            ft.Container(
                ft.TextField(multiline=True, height=250, border=ft.InputBorder.NONE, expand=True),
                padding=ft.Padding(10, right=10)
            ),
            ft.Row(
                [
                    ft.PopupMenuButton(
                        ft.Text("H", font_family="Roboto Slab", size=25, weight=ft.FontWeight.W_500),
                        [
                            ft.PopupMenuItem("Encabezado 6", ft.Image("assets/icons/format_h6.svg", width=25)),
                            ft.PopupMenuItem("Encabezado 5", ft.Image("assets/icons/format_h5.svg", width=25)),
                            ft.PopupMenuItem("Encabezado 4", ft.Image("assets/icons/format_h4.svg", width=25)),
                            ft.PopupMenuItem("Encabezado 3", ft.Image("assets/icons/format_h3.svg", width=25)),
                            ft.PopupMenuItem("Encabezado 2", ft.Image("assets/icons/format_h2.svg", width=25)),
                            ft.PopupMenuItem("Encabezado 1", ft.Image("assets/icons/format_h1.svg", width=25))
                        ],
                        tooltip=""
                    ),
                    ft.IconButton(ft.Image("assets/icons/match_case.svg", width=25)),
                    ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED),
                    ft.IconButton(ft.Icons.FORMAT_LIST_NUMBERED),
                    ft.IconButton(ft.Icons.IMAGE_OUTLINED)
                ]
            )
        ],
        col=9,
        expand=True
    )
    
    page.on_resize = lambda _: ui()
    def ui():
        if page.window.maximized:
            panel_control_desk.visible = True
            editor.col = 9
        else:
            panel_control_desk.visible = False
            editor.col = 12
    
    ui()
    user = UsuarioCtrl().obtener_data(page.session.store.get("user"), "nombre")
    nombre_usuario = "Usuario" if not user else user["nombre"] # type: ignore
    nombre_usuario = nombre_usuario if len(nombre_usuario) <= 10 else nombre_usuario[:7] + "..."
    
    return ft.View(
        route="/dashboard",
        controls=[
            ft.AppBar(
                title=ft.Row(
                    [
                        ft.Image("assets/images/onyx_logo.png", width=30, color=ft.Colors.ON_SURFACE),
                        ft.Text("Onyx", weight=ft.FontWeight.W_600, margin=ft.Margin(1, bottom=3))
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                actions=[
                    ft.Row(
                        [
                            ft.Text(nombre_usuario, size=15, weight=ft.FontWeight.W_500, margin=ft.Margin(bottom=1)),
                            ft.IconButton(
                                ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE_70),
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                                margin=ft.Margin(10, 2, 15),
                                on_click=lambda _: page.go("/usuario")
                            )
                        ],
                        spacing=0
                    )
                ],
                bgcolor=ft.Colors.SURFACE_CONTAINER
            ),
            ft.ResponsiveRow(
                [
                    panel_control_desk,
                    editor
                ]
            )
        ],
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST
    )