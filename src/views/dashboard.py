import flet as ft
from controllers.UsuarioCtrl import UsuarioCtrl
from controllers.PaginaCtrl import PaginaCtrl

def dashboard(page: ft.Page):
    notas = [
        ft.TextButton(
            ft.Text(nota["titulo"], size=20, weight=ft.FontWeight.W_500),
            style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10)),
            data=nota["id"]
        ) for nota in PaginaCtrl().obtener_pajina(page.session.store.get("user")) # type: ignore
    ]
    
    panel_control_desk = ft.Container(
        ft.Column(
            [
                ft.Text("Paginas", size=20, weight=ft.FontWeight.W_600),
                ft.Divider(),
                ft.Column(
                    notas # type: ignore
                )
            ],
        ),
        col=3,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        height=500,
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
        ft.MarkdownExtensionSet.GITHUB_FLAVORED,
        ft.MarkdownCodeTheme.VS,
        soft_line_break=False,
        height=475,
        visible=False
    )
    
    contenido_editor = ft.TextField(multiline=True, height=475, border=ft.InputBorder.NONE, expand=True)
    
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
                    ft.IconButton(ft.Icons.SAVE_OUTLINED, bgcolor=ft.Colors.SURFACE_CONTAINER, on_click=lambda _: uardar()),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.ERROR, bgcolor=ft.Colors.SURFACE_CONTAINER)
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
                            items=[
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 6", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h6.svg", width=25),
                                    data="h6",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 5", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h5.svg", width=25),
                                    data="h5",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
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
                            ],
                            tooltip="Encabezados"
                        ),
                        ft.PopupMenuButton(
                            icon=ft.Image("assets/icons/match_case.svg", width=25),
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
                            ],
                            tooltip="Estilos"
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
                            items=[
                                ft.PopupMenuItem(
                                    ft.Text("Link Rapido", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Icon(ft.Icons.ADD_LINK_OUTLINED)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("URL", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/link_2.svg", width=25)
                                )
                            ],
                            tooltip=""
                        ),
                        ft.IconButton(ft.Icons.IMAGE_OUTLINED)
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER
            )
        ],
        col=9,
        expand=True
    )
    
    def uardar():
        PaginaCtrl().crear_pagina(page.session.store.get("user"), titulo.value, contenido_editor.value)
        notas = [
            ft.TextButton(
                ft.Text(nota["titulo"], size=20, weight=ft.FontWeight.W_500),
                style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10)),
                data=nota["id"]
            ) for nota in PaginaCtrl().obtener_pajina(page.session.store.get("user")) # type: ignore
        ]
        
        page.update()
    
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
            "h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ", "h5": "##### ", "h6": "###### ",
            "bold": "****", "italic": "**", "strike": "~~~~", "quote": "> ",
            "list_or": "1. ", "list_un": "- ", "code": "````", "divider": "---"
        }
        
        contenido_editor.value += tipos[tipo]
        
        pos = len(contenido_editor.value)
        if tipo in ["bold", "strike", "code"]: pos -= 2    
        elif tipo == "italic": pos -= 1
        
        contenido_editor.selection = ft.TextSelection(pos, pos)
        
        await contenido_editor.focus()
        page.update()
    
    page.on_resize = lambda _: ui()
    def ui():
        if page.window.maximized:
            panel_control_desk.visible = True
            editor.col = 9
            titulo.width = None
            contenido_editor.height = 475
        else:
            panel_control_desk.visible = False
            editor.col = 12
            titulo.width = 105
            contenido_editor.height = 395
    
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