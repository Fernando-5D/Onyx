import flet as ft
from controllers.UsuarioCtrl import UsuarioCtrl

def usuario(page: ft.Page):
    alert_eliminar = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR, margin=ft.Margin(top=2)),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(25, 2, bottom=5),
        visible=False
    )
    
    sheet_eliminar = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("¿Estas seguro de que quieres eliminar tu cuenta?", size=15, text_align=ft.TextAlign.CENTER),
                    ft.FilledButton(
                        ft.Text("Cancelar", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            bgcolor="#5c71eb",
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15
                        ),
                        width=300,
                        margin=ft.Margin(top=25, bottom=5),
                        on_click=lambda _: cerrar_alertD()
                    ),
                    ft.TextButton(
                        ft.Text("Eliminar mi cuenta", size=20, color=ft.Colors.RED, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15
                        ),
                        width=300,
                        on_click=lambda _: eliminar_cuenta(page.session.store.get("user"))
                    ),
                    alert_eliminar
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True
            ), 
            width=300,
            padding=15
        ),
        bgcolor=ft.Colors.SURFACE,
        shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(15, 15, 0, 0))
    )
    
    page.overlay.append(sheet_eliminar)
    def abrir_alertD():
        sheet_eliminar.open = True
        page.update()
    
    def cerrar_alertD():
        sheet_eliminar.open = False
        page.update()
    
    def cerrar_sesionClick():
        page.session.store.clear()
        page.go("/sesion")
    
    def eliminar_cuenta(email):
        alert_eliminar.visible = False
        
        is_valid, mensaje = UsuarioCtrl().eliminar_cuenta(email)
        if not is_valid:
            alert_eliminar.controls[1].value = mensaje # type: ignore
            alert_eliminar.visible = True
        else:
            page.go("/sesion")
        
        page.update()
    
    user = UsuarioCtrl().obtener_data(page.session.store.get("user"), "nombre")
    nombre_usuario = "Usuario" if not user else user["nombre"] # type: ignore
    
    return ft.View(
        route="/usuario",
        controls=[
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.ARROW_BACK,
                                align=ft.Alignment.CENTER_LEFT,
                                margin=ft.Margin(top=2),
                                on_click=lambda _: page.go("/dashboard")
                            ),
                            ft.Text(
                                "Perfil",
                                size=20,
                                weight=ft.FontWeight.W_600,
                                align=ft.Alignment.CENTER,
                                expand=True,
                                margin=ft.Margin(right=50)
                            )
                        ],
                        expand=True
                    ),
                    ft.Divider(),
                    ft.Container(
                        ft.Icon(ft.Icons.PERSON, size=125, color=ft.Colors.WHITE_70),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                        shape=ft.BoxShape.CIRCLE,
                        margin=ft.Margin(top=25),
                        padding=20
                    ),
                    ft.Text(nombre_usuario, size=25, weight=ft.FontWeight.W_600, margin=ft.Margin(top=5), expand=True),
                    ft.TextButton(
                        ft.Text("Cerrar sesion", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15
                        ),
                        width=300,
                        margin=ft.Margin(top=35, bottom=2),
                        on_click=lambda _: cerrar_sesionClick()
                    ),
                    ft.TextButton(
                        ft.Text("Eliminar cuenta", size=20, color=ft.Colors.RED, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15
                        ),
                        width=300,
                        on_click=lambda _: abrir_alertD()
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        margin=ft.Margin(2)
    )