import flet as ft
from views.sesion import sesion
from views.recuperar_passw import recuperar_passw
from views.registro import registro
from views.dashboard import dashboard
from views.usuario import usuario

def start(page: ft.Page):
    page.title = "Onyx"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    
    def route_change():
        page.views.clear()
        if page.route == "/sesion" or page.route == "/":
            page.views.append(sesion(page))
        
        elif page.route == "/recuperar_passw":
            page.views.append(recuperar_passw(page))
        
        elif page.route == "/registro":
            page.views.append(registro(page))
        
        elif page.route == "/dashboard":
            page.views.append(dashboard(page))
        
        elif page.route == "/usuario":
            page.views.append(usuario(page))
            
        page.update()

    page.on_route_change = lambda _: route_change()
    page.go("/sesion")

def main():
    ft.app(target=start)

if __name__ == "__main__":
    main()
