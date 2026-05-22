import flet as ft
from controllers.UsuarioCtrl import UsuarioCtrl

def usuario(page: ft.Page):
    icon_tema = ft.Icons.CONTRAST
    if page.theme_mode == ft.ThemeMode.SYSTEM:
        icon_tema = ft.Icons.CONTRAST
        
    elif page.theme_mode == ft.ThemeMode.LIGHT:
        icon_tema = ft.Icons.LIGHT_MODE
         
    else:
        icon_tema = ft.Icons.DARK_MODE
    
    alertD_eliminar = ft.AlertDialog(
        ft.Column(
            [
                ft.Text("¿Estas seguro de que quieres eliminar tu cuenta?"),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR),
                        ft.Text("", size=12, color=ft.Colors.ERROR)
                    ],
                    visible=False
                )
            ],
            height=40
        ),
        actions=[
            ft.TextButton(
                ft.Text("Eliminar mi cuenta", size=20, color=ft.Colors.RED, weight=ft.FontWeight.W_600),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=15
                ),
                width=300,
                margin=ft.Margin(bottom=10),
                on_click=lambda _: eliminar_cuenta(page.session.store.get("user"))
            ),
            ft.TextButton(
                ft.Text("Cancelar", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.RED,
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=15
                ),
                width=300,
                on_click=lambda _: cerrar_alertD()
            )
        ],
        modal=True
    )
    
    def obtener_data(email, campo = "*"):
        return UsuarioCtrl().obtener_data(email, campo)
    
    nombre_usuario = "Usuario"
    if obtener_data(page.session.store.get("user"), "nombre"):
        nombre_usuario = obtener_data(page.session.store.get("user"), "nombre")["nombre"] # type: ignore
    
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
    
    def cerrarClick():
        page.session.store.clear()
        page.go("/sesion")
    
    page.overlay.append(alertD_eliminar)
    def abrir_alertD():
        alertD_eliminar.open = True
        page.update()
    
    def cerrar_alertD():
        alertD_eliminar.open = False
        page.update()
    
    def eliminar_cuenta(email):
        is_valid, mensaje = UsuarioCtrl().eliminar_cuenta(email)
        if not is_valid:
            alertD_eliminar.content.controls[1].value = mensaje # type: ignore
            alertD_eliminar.content.controls[1].visible = True # type: ignore
        else:
            page.go("/sesion")
        
        page.update()
    
    return ft.View(
        route="/usuario",
        controls=[
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.ARROW_BACK,
                                on_click=lambda _: page.go("/dashboard")
                            ),
                            ft.Text("Perfil", size=20, weight=ft.FontWeight.W_600),
                            ft.IconButton(
                                icon_tema,
                                on_click=lambda e: cambiar_tema(e)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        expand=True
                    ),
                    ft.Divider(),
                    ft.IconButton(
                        ft.Icons.PERSON,
                        icon_size=150,
                        bgcolor=ft.Colors.SURFACE_CONTAINER,
                        margin=ft.Margin(top=10),
                        disabled=True
                    ),
                    ft.Text(nombre_usuario, size=25, weight=ft.FontWeight.W_600, margin=ft.Margin(top=5)),
                    ft.TextButton(
                        ft.Text("Cerrar sesion", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15
                        ),
                        width=300,
                        margin=ft.Margin(top=30, bottom=2),
                        on_click=lambda _: cerrarClick()
                    ),
                    ft.TextButton(
                        ft.Text("Borrar cuenta", size=20, color=ft.Colors.RED, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15
                        ),
                        width=300,
                        on_click=lambda _: abrir_alertD()
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    )