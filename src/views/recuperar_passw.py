import flet as ft
import random
import asyncio
from controllers.UsuarioCtrl import UsuarioCtrl

def recuperar_passw(page: ft.Page):
    email = ft.TextField(label="Correo Electronico", keyboard_type=ft.KeyboardType.EMAIL)
    alert_email = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR, margin=ft.Margin(top=2)),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
    
    button_enviar = ft.FilledButton(
        ft.Text("Enviar Codigo", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
        bgcolor="#5c71eb",
        style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10)),
        width=300,
        margin=ft.Margin(top=10, bottom=35),
        on_click=lambda e: page.run_task(enviar_codigo)
    )
    
    status = ft.Text("Enviando...", size=20, color="#5c71eb", weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)
    sheet_enviar = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    status
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True
            ), 
            width=300,
            padding=15
        ),
        shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(15, 15, 0, 0))
    )
    
    codigo = ft.TextField(label="Codigo", keyboard_type=ft.KeyboardType.NUMBER, disabled=True)
    alert_codigo = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR, margin=ft.Margin(top=2)),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
    
    nuevaPassw = ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True, disabled=True, margin=ft.Margin(top=10))
    alert_nuevaPassw = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR, margin=ft.Margin(top=2)),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
    
    button_cambiarPassw = ft.FilledButton(
        ft.Text("Cambiar Contraseña", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.SURFACE_CONTAINER_HIGHEST),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10)),
        width=300,
        disabled=True,
        margin=ft.Margin(top=10),
        on_click=lambda _: cambiar_passw()
    )
        
    page.overlay.append(sheet_enviar)
    async def enviar_codigo():
        alert_email.visible = False
        status.value = "Enviando..."
        status.color = "#5c71eb"
        
        if not email.value:
            alert_email.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_email.visible = True
        
        if email.value:
            email.disabled = True
            sheet_enviar.open = True
            page.update()
            
            page.session.store.set("code", random.randint(100000, 999999))
            is_valid, mensaje = await asyncio.to_thread(
                UsuarioCtrl().enviar_codigo, email.value, page.session.store.get("code")
            )
            
            status.value = mensaje
            if not is_valid:
                status.color = ft.Colors.WHITE
                email.disabled = False
                
            else:
                status.color = ft.Colors.LIGHT_GREEN
                
                button_enviar.content.color = ft.Colors.SURFACE_CONTAINER_HIGHEST # type: ignore
                button_enviar.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW
                button_enviar.disabled = True
                
                codigo.disabled = False
                nuevaPassw.disabled = False
                
                button_cambiarPassw.content.color = ft.Colors.WHITE # type: ignore
                button_cambiarPassw.bgcolor = "#5c71eb"
                button_cambiarPassw.disabled = False
        
        page.update()

    def cambiar_passw():
        alert_codigo.visible = False
        alert_nuevaPassw.visible = False
        
        if not codigo.value:
            alert_codigo.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_codigo.visible = True
        
        elif not nuevaPassw.value:
            alert_nuevaPassw.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_nuevaPassw.visible = True
        
        else:
            is_valid, mensaje = UsuarioCtrl().cambiar_passw(email.value, codigo.value, page.session.store.get("code"), nuevaPassw.value) # type: ignore
            if not is_valid:
                if "código" in mensaje:
                    alert_codigo.controls[1].value = mensaje # type: ignore
                    alert_codigo.visible = True
                    
                elif "contraseña" in mensaje:
                    alert_nuevaPassw.controls[1].value = mensaje # type: ignore
                    alert_nuevaPassw.visible = True
                    
                else:
                    alert_codigo.controls[1].value = alert_nuevaPassw.controls[1].value = mensaje # type: ignore
                    alert_codigo.visible = alert_nuevaPassw.visible = True

            else:
                page.go("/sesion")

        page.update()
    
    def volver():
        page.session.store.clear()
        page.go("/sesion")
    
    return ft.View(
        route="/recuperar_passw",
        controls=[
            ft.IconButton(ft.Icons.ARROW_BACK, align=ft.Alignment.TOP_LEFT, on_click=lambda _: volver()),
            ft.Column(
                [
                    ft.Text("Recuperar Contraseña", size=20, weight=ft.FontWeight.W_600),
                    ft.Text(
                        "Ingresa tu correo para recibir un código de verificación",
                        size=15,
                        text_align=ft.TextAlign.CENTER,
                        margin=ft.Margin(top=10, bottom=20)
                    ),
                    email,
                    alert_email,
                    button_enviar,
                    codigo,
                    alert_codigo,
                    nuevaPassw,
                    alert_nuevaPassw,
                    button_cambiarPassw
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                expand=True
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        margin=ft.Margin(2),
        expand=True
    )