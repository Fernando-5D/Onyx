import flet as ft
import random
import asyncio
from controllers.UsuarioCtrl import UsuarioCtrl

def recuperar_passw(page: ft.Page):
    email = ft.TextField(label="Correo Electronico", keyboard_type=ft.KeyboardType.EMAIL)
    alert_email = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
    
    boton_enviar = ft.FilledButton(
        ft.Text("Enviar Codigo", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
        bgcolor="#5c71eb",
        style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10)),
        width=300,
        on_click=lambda _: page.run_task(enviar_codigo)
    )
    
    alertSht_enviar = ft.BottomSheet(
        ft.Column(
            [
                ft.Text("Enviando...", size=20, weight=ft.FontWeight.W_600, color="#5c71eb"),
                ft.FilledButton(
                    ft.Text("Cancelar", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                    bgcolor="#5c71eb",
                    style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10)),
                    visible=False,
                    on_click=lambda _: cerrar_alertSht()
                )
            ]
        ),
        shape=ft.RoundedRectangleBorder(radius=15),
        dismissible=False
    )
    
    codigo = ft.TextField(label="Código", keyboard_type=ft.KeyboardType.NUMBER, disabled=True)
    alert_codigo = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
    
    nuevaPassw = ft.TextField(label="Nueva contraseña", password=True, can_reveal_password=True, disabled=True)
    alert_nuevaPassw = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(15, 2, bottom=5),
        visible=False
    )
    
    boton_cambiarPassw = ft.FilledButton(
        ft.Text("Cambiar contraseña", size=15, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
        bgcolor="#5c71eb",
        style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10)),
        width=300,
        disabled=True,
        on_click=lambda _: cambiar_passw()
    )
    
    def cerrar_alertSht():
        alertSht_enviar.open = False
        page.update()
        
    page.overlay.append(alertSht_enviar)
    async def enviar_codigo():
        alert_email.visible = False
        alertSht_enviar.content.controls[0].value = "Enviando..." # type: ignore
        alertSht_enviar.content.controls[0].color = "#5c71eb" # type: ignore
        alertSht_enviar.content.controls[1].visible = False # type: ignore
        
        if not email.value:
            alert_email.controls[1].value = "Este campo es obligatorio" # type: ignore
            alert_email.visible = True
        
        if email.value:
            email.disabled = True
            alertSht_enviar.open = True
            page.update()
            
            page.session.store.set("code", random.randint(100000, 999999))
            is_valid, mensaje = await asyncio.to_thread(
                UsuarioCtrl().enviar_codigo, email.value, page.session.store.get("code")
            )
            
            email.disabled = True
            alertSht_enviar.content.controls[0].value = mensaje # type: ignore
            if not is_valid:
                alertSht_enviar.content.controls[0].color = ft.Colors.ERROR # type: ignore
                email.disabled = False

            else:
                alertSht_enviar.content.controls[0].color = ft.Colors.LIGHT_GREEN # type: ignore
                boton_enviar.disabled = True
                codigo.disabled = False
                nuevaPassw.disabled = False
                boton_cambiarPassw.disabled = False
                
        
        alertSht_enviar.content.controls[1].visible = True # type: ignore
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
                    ft.Text("Ingresa tu correo para recibir un código de verificación", size=15),
                    email,
                    alert_email,
                    boton_enviar,
                    codigo,
                    alert_codigo,
                    nuevaPassw,
                    alert_nuevaPassw,
                    boton_cambiarPassw
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                expand=True
            )
        ],
        margin=ft.Margin(2),
        expand=True
    )