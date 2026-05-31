import flet as ft

class Pagina(ft.ResponsiveRow):
    def __init__(self, titulo, data, paginaClick, eliminarClick):
        super().__init__(
            [
                ft.TextButton(
                    ft.Text(
                        titulo if len(titulo) <= 30 else titulo[:7] + "...",
                        size=20,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.ON_SURFACE,
                        align=ft.Alignment.CENTER_LEFT
                    ),
                    col=10,
                    style=ft.ButtonStyle(
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(10, 0, 10, 0)),
                        overlay_color=ft.Colors.with_opacity(.1, ft.Colors.WHITE),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW
                    ),
                    width=300,
                    height=50,
                    data=data,
                    on_click=paginaClick
                ),
                ft.PopupMenuButton(
                    icon=ft.Icon(ft.Icons.MORE_HORIZ_OUTLINED, size=30, color=ft.Colors.ON_SURFACE),
                    tooltip="",
                    items=[
                        ft.PopupMenuItem(
                            ft.Text("Eliminar", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                            ft.Icon(ft.Icons.DELETE_OUTLINE, color=ft.Colors.RED),
                            data=data,
                            on_click=eliminarClick
                        )
                    ],
                    col=2,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(0, 10, 0, 10))
                    )
                )
            ]
        )
        
        self.spacing = 0