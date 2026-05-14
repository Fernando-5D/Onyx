import flet as ft

class ClassButton(ft.Container):
    def __init__(self, page: ft.Page, titulo: str, desc: str, background_color: ft.ColorValue, route: str):
        super().__init__()
        
        self.content = ft.ElevatedButton(
            ft.Column(
                [
                    ft.Text(
                        titulo,
                        size=20,
                        weight=ft.FontWeight.NORMAL,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        desc,
                        weight=ft.FontWeight.NORMAL,
                        color=ft.Colors.WHITE
                    )
                ]
            ),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                shadow_color=ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.TRANSPARENT,
                padding=0
            ),
            expand=True,
            on_click=lambda _: page.go(route)
        )
        
        self.padding = 10
        self.bgcolor = background_color
        self.border_radius = 10