import flet as ft
import asyncio
from controllers.UsuarioCtrl import UsuarioCtrl
from controllers.PaginaCtrl import PaginaCtrl
from views.components.Pagina import Pagina

def dashboard(page: ft.Page):
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
                    ft.Text("¿Estas seguro de que quieres eliminar esta pagina?", size=15, text_align=ft.TextAlign.CENTER),
                    ft.FilledButton(
                        ft.Text("Cancelar", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            bgcolor="#5c71eb",
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15
                        ),
                        width=300,
                        margin=ft.Margin(top=25, bottom=5),
                        on_click=lambda _: cerrar_sheet()
                    ),
                    ft.TextButton(
                        ft.Text("Eliminar pagina", size=20, color=ft.Colors.RED, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15
                        ),
                        width=300,
                        on_click=lambda e: eliminar(e)
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
    
    panel_control_desk = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Paginas", size=20, weight=ft.FontWeight.W_600, align=ft.Alignment.CENTER_LEFT),
                        ft.FilledButton(
                            ft.Text("Vaciar", size=15, weight=ft.FontWeight.W_600),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW
                        )
                    ]
                ),
                ft.Divider(),
                ft.Column(
                    [
                        Pagina(
                            pagina["titulo"],
                            pagina["id"],
                            lambda e: page.run_task(obtener, e),
                            lambda e: abrir_sheet(e)
                        ) for pagina in PaginaCtrl().obtener_data(page.session.store.get("user")) # type: ignore
                    ]
                )
            ],
        ),
        col=3,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        expand=True,
        padding=15,
        visible=True
    )
    
    titulo = ft.TextField(
        hint_text="Sin Titulo",
        hint_style=ft.TextStyle(color=ft.Colors.SURFACE_CONTAINER_HIGH),
        border_color=ft.Colors.SURFACE_CONTAINER_HIGH
    )
    
    contenido_modo = ft.IconButton(
        ft.Icons.DESCRIPTION_OUTLINED,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        data="editor",
        on_click=lambda e: cambiar_modo(e)
    )
    
    contenido_preview = ft.Markdown(
        "",
        True,
        ft.MarkdownExtensionSet.GITHUB_WEB,
        ft.MarkdownCodeTheme.VS,
        md_style_sheet=ft.MarkdownStyleSheet(
            blockquote_decoration=ft.BoxDecoration(
                bgcolor=ft.Colors.with_opacity(.5, ft.Colors.WHITE),
                border=ft.Border.only(left=ft.BorderSide(10))
            ),
            horizontal_rule_decoration=ft.BoxDecoration(border=ft.Border.all(1))
        ),
        soft_line_break=True,
        height=475,
        expand=True,
        visible=False
    )
    
    contenido_editor = ft.TextField(
        multiline=True,
        border=ft.InputBorder.NONE,
        height=475,
        expand=True
    )
    
    editor = ft.Column(
        [
            ft.Row(
                [
                    ft.PopupMenuButton(
                        icon=ft.Icons.ARROW_BACK,
                        items=[
                            ft.PopupMenuItem("Guardar cambios", ft.Icons.SAVE_OUTLINED),
                            ft.PopupMenuItem("Descartar cambios", ft.Icon(ft.Icons.CLOSE, color=ft.Colors.ERROR))
                        ],
                        style=ft.ButtonStyle(bgcolor=ft.Colors.SURFACE_CONTAINER),
                        tooltip=""
                    ),
                    titulo,
                    contenido_modo,
                    ft.IconButton(ft.Icons.SAVE_OUTLINED, bgcolor=ft.Colors.SURFACE_CONTAINER, on_click=lambda _: guardar())
                ]
            ),
            ft.Divider(),
            ft.Container(
                ft.Column(
                    [contenido_editor, contenido_preview]
                ),
                padding=ft.Padding(10, right=10)
            ),
            ft.Container(
                ft.Row(
                    [
                        ft.PopupMenuButton(
                            icon=ft.Image("assets/icons/format_h1.svg", width=25),
                            tooltip="Encabezados",
                            items=[
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 4", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h4.svg", width=25),
                                    data="h4",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 3", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h3.svg", width=25),
                                    data="h3",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 2", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h2.svg", width=25),
                                    data="h2",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 1", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h1.svg", width=25),
                                    data="h1",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                )
                            ]
                        ),
                        ft.PopupMenuButton(
                            icon=ft.Image("assets/icons/match_case.svg", width=25),
                            tooltip="Estilos",
                            items=[
                                ft.PopupMenuItem(
                                    ft.Text("Tachado", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Icon(ft.Icons.STRIKETHROUGH_S_OUTLINED),
                                    data="strike",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Cursiva", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Icon(ft.Icons.FORMAT_ITALIC_OUTLINED),
                                    data="italic",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Negrita", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Icon(ft.Icons.FORMAT_BOLD_OUTLINED),
                                    data="bold",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                )
                            ]
                        ),
                        ft.IconButton(
                            ft.Icons.STICKY_NOTE_2_OUTLINED,
                            tooltip="Nota",
                            data="quote",
                            on_click=lambda e: page.run_task(button_markdown, e.control.data)
                        ),
                        ft.IconButton(
                            ft.Icons.FORMAT_LIST_NUMBERED,
                            tooltip="Lista Ordenada",
                            data="list_or",
                            on_click=lambda e: page.run_task(button_markdown, e.control.data)
                        ),
                        ft.IconButton(
                            ft.Icons.FORMAT_LIST_BULLETED,
                            tooltip="Lista",
                            data="list_un",
                            on_click=lambda e: page.run_task(button_markdown, e.control.data)
                        ),
                        ft.IconButton(
                            ft.Icons.CODE_OUTLINED,
                            tooltip="Bloque de Codigo",
                            data="code",
                            on_click=lambda e: page.run_task(button_markdown, e.control.data)
                        ),
                        ft.IconButton(
                            ft.Icons.HORIZONTAL_RULE,
                            tooltip="Separador",
                            data="divider",
                            on_click=lambda e: page.run_task(button_markdown, e.control.data)
                        ),
                        ft.PopupMenuButton(
                            icon=ft.Image("assets/icons/link_2.svg", width=25),
                            tooltip="Enlace",
                            items=[
                                ft.PopupMenuItem(
                                    ft.Text("Link Rapido", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Icon(ft.Icons.ADD_LINK_OUTLINED),
                                    data="quick_link",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("URL", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/link_2.svg", width=25),
                                    data="link",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                )
                            ]
                        ),
                        ft.IconButton(
                            ft.Icons.IMAGE_OUTLINED,
                            tooltip="Imagen",
                            data="image",
                            on_click=lambda e: page.run_task(button_markdown, e.control.data)
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                border=ft.Border.all(1, ft.Colors.SURFACE_CONTAINER_HIGH),
                border_radius=50
            )
        ],
        col=9,
        expand=True
    )
    
    page.overlay.append(sheet_eliminar)
    def abrir_sheet(e):
        sheet_eliminar.open = True
        sheet_eliminar.data = e.control.data
        page.update()
    
    def cerrar_sheet():
        sheet_eliminar.open = False
        sheet_eliminar.data = None
        page.update()
    
    def update_panel():
        panel_control_desk.content.controls[2].controls = [ # type: ignore
            Pagina(
                pagina["titulo"],
                pagina["id"],
                lambda e: page.run_task(obtener, e),
                lambda e: abrir_sheet(e)
            ) for pagina in PaginaCtrl().obtener_data(page.session.store.get("user")) # type: ignore
        ]
        
        page.update()
    
    async def obtener(e):
        page.session.store.set("pagina", e.control.data)
        pagina = PaginaCtrl().obtener_data(id = e.control.data)
        
        titulo.value = pagina["titulo"] # type: ignore
        contenido_preview.value = contenido_editor.value = pagina["contenido"] # type: ignore
        await contenido_modo.focus()
    
    def guardar():
        id_pagina = page.session.store.get("pagina")
        if id_pagina:
            PaginaCtrl().editar_pagina(id_pagina, titulo.value, contenido_editor.value)
            page.update()
            
        else:
            PaginaCtrl().crear_pagina(page.session.store.get("user"), titulo.value, contenido_editor.value)
            update_panel()
    
    def eliminar(e):
        PaginaCtrl().eliminar_pagina(id=e.control.data)
        update_panel()
        
    def cambiar_modo(e):
        if e.control.data == "preview":
            e.control.data = "editor"
            e.control.icon = ft.Icons.DESCRIPTION_OUTLINED

            contenido_preview.visible = False
            contenido_editor.visible = True
        
        elif e.control.data == "editor":
            e.control.data = "preview"
            e.control.icon = ft.Icons.EDIT_OUTLINED

            contenido_editor.visible = False
            contenido_preview.value = contenido_editor.value
            contenido_preview.visible = True
        
        page.update()
    
    async def button_markdown(tipo: str):
        tipos = {
            "h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ", "bold": "****", "italic": "**",
            "strike": "~~~~", "list_or": "1. ", "list_un": "- ", "quote": "> ", "code": "````",
            "divider": "---", "link": "[]()", "quick_link": "<>", "image": "![]()"
        }
        
        contenido_editor.value += tipos[tipo]
        
        pos = len(contenido_editor.value)
        if tipo == "image": pos -= 4
        elif tipo == "link": pos -= 3
        elif tipo in ["bold", "strike", "code"]: pos -= 2
        elif tipo in ["italic", "quick_link"]: pos -= 1
        
        contenido_editor.selection = ft.TextSelection(pos, pos)
        
        await contenido_editor.focus()
        page.update()
    
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
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
        padding=0
    )