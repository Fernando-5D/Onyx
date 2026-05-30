import flet as ft

class Pagina(ft.ResponsiveRow):
    def __init__(self, titulo, data, paginaClick, eliminarClick):
        super().__init__(
            [
                ft.TextButton(
                    ft.Text(titulo, size=20, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                    col=10,
                    style=ft.ButtonStyle(padding=10, shape=ft.RoundedRectangleBorder(radius=15)),
                    width=300,
                    height=50,
                    data=data,
                    on_click=paginaClick
                ),
                ft.PopupMenuButton(
                    icon=ft.Icons.MORE_HORIZ_OUTLINED,
                    items=[
                        ft.PopupMenuItem(
                            ft.Text("Eliminar", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                            ft.Icon(ft.Icons.DELETE_OUTLINE),
                            data=data,
                            on_click=eliminarClick
                        )
                    ],
                    col=2,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                )
            ]
        )