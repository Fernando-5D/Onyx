import flet as ft
from controllers.UsuarioCtrl import UsuarioCtrl
from controllers.PaginaCtrl import PaginaCtrl
from views.components.Pagina import Pagina

def dashboard(page: ft.Page):
    alert_vaciar = ft.Row(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=12, color=ft.Colors.ERROR, margin=ft.Margin(top=2)),
            ft.Text("", size=12, color=ft.Colors.ERROR, expand=True)
        ],
        width=300,
        margin=ft.Margin(25, 2, bottom=5),
        visible=False
    )
        
    sheet_vaciar = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("¿Estas seguro de que quieres vaciar todas las paginas?", size=15, text_align=ft.TextAlign.CENTER),
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
                        ft.Text("Vaciar paginas", size=20, color=ft.Colors.RED, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15
                        ),
                        width=300,
                        on_click=lambda _: eliminar()
                    ),
                    alert_vaciar
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
                            ft.Text("Vaciar", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.RED),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                                padding=15,
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            align=ft.Alignment.CENTER_RIGHT,
                            on_click=lambda _: abrir_sheet()
                        )
                    ],
                    expand=True
                ),
                ft.Divider(),
                ft.Column(
                    [
                        Pagina(
                            pagina["titulo"],
                            pagina["id"],
                            lambda e: obtener(e),
                            lambda e: eliminar(e)
                        ) for pagina in PaginaCtrl().obtener_data(page.session.store.get("user")) # type: ignore
                    ]
                )
            ],
            expand=True
        ),
        col=3,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        expand=True,
        border_radius=ft.BorderRadius(0, 20, 0, 20),
        padding=15,
        visible=True
    )
    
    popbutton_cerrar = ft.PopupMenuButton(
        icon=ft.Icon(ft.Icons.ARROW_BACK, size=30, color=ft.Colors.ON_SURFACE),
        items=[
            ft.PopupMenuItem(
                ft.Text("Guardar cambios", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                ft.Icon(ft.Icons.SAVE_OUTLINED, color=ft.Colors.ON_SURFACE),
                on_click=lambda _: cerrar(True)
            ),
            ft.PopupMenuItem(
                ft.Text("Descartar cambios", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                ft.Icon(ft.Icons.CLOSE, color=ft.Colors.RED),
                on_click=lambda _: cerrar(False)
            )
        ],
        style=ft.ButtonStyle(bgcolor=ft.Colors.SURFACE_CONTAINER, side=ft.BorderSide(1, ft.Colors.SURFACE_CONTAINER_HIGHEST)),
        tooltip="Cerrar",
        visible=False
    )
    
    txt_editando = ft.Text(
        "Editando:",
        size=15,
        color="#5c71eb",
        weight=ft.FontWeight.W_400,
        margin=ft.Margin(25, bottom=3),
        visible=False
    )
    
    titulo = ft.TextField(
        hint_text="Sin Titulo",
        hint_style=ft.TextStyle(color=ft.Colors.SURFACE_CONTAINER_HIGH),
        border_color=ft.Colors.SURFACE_CONTAINER_HIGH,
        margin=ft.Margin(10),
    )
    
    contenido_preview = ft.Markdown(
        "",
        True,
        ft.MarkdownExtensionSet.GITHUB_WEB,
        ft.MarkdownCodeTheme.ATOM_ONE_DARK,
        md_style_sheet=ft.MarkdownStyleSheet(
            blockquote_decoration=ft.BoxDecoration(
                bgcolor=ft.Colors.with_opacity(.1, ft.Colors.WHITE),
                border=ft.Border.only(left=ft.BorderSide(10, ft.Colors.GREY))
            ),
            blockquote_padding=ft.Padding(30, 10, 20, 10),
            horizontal_rule_decoration=ft.BoxDecoration(border=ft.Border.all(10, ft.Colors.GREY))
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
                    popbutton_cerrar,
                    txt_editando,
                    titulo,
                    ft.IconButton(
                        ft.Icons.DESCRIPTION_OUTLINED,
                        icon_size=30,
                        bgcolor=ft.Colors.SURFACE_CONTAINER,
                        align=ft.Alignment.CENTER_RIGHT,
                        data="editor",
                        style=ft.ButtonStyle(side=ft.BorderSide(1, ft.Colors.SURFACE_CONTAINER_HIGHEST)),
                        on_click=lambda e: cambiar_modo(e)
                    ),
                    ft.IconButton(
                        ft.Icons.SAVE_OUTLINED,
                        icon_size=30,
                        bgcolor=ft.Colors.SURFACE_CONTAINER,
                        align=ft.Alignment.CENTER_RIGHT,
                        style=ft.ButtonStyle(side=ft.BorderSide(1, ft.Colors.SURFACE_CONTAINER_HIGHEST)),
                        on_click=lambda _: guardar()
                    )
                ],
                expand=True
            ),
            ft.Divider(),
            ft.Container(
                ft.Column(
                    [contenido_editor, contenido_preview],
                    scroll=ft.ScrollMode.ALWAYS
                ),
                padding=ft.Padding(10, right=10)
            ),
            ft.Container(
                ft.Row(
                    [
                        ft.PopupMenuButton(
                            icon=ft.Image("assets/icons/format_h1.svg", color=ft.Colors.ON_SURFACE, width=25),
                            tooltip="Encabezados",
                            items=[
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 4", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h4.svg", color=ft.Colors.ON_SURFACE, width=25),
                                    data="h4",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 3", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h3.svg", color=ft.Colors.ON_SURFACE, width=25),
                                    data="h3",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 2", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h2.svg", color=ft.Colors.ON_SURFACE, width=25),
                                    data="h2",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Encabezado 1", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Image("assets/icons/format_h1.svg", color=ft.Colors.ON_SURFACE, width=25),
                                    data="h1",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                )
                            ]
                        ),
                        ft.PopupMenuButton(
                            icon=ft.Image("assets/icons/match_case.svg", color=ft.Colors.ON_SURFACE, width=25),
                            tooltip="Estilos",
                            items=[
                                ft.PopupMenuItem(
                                    ft.Text("Tachado", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Icon(ft.Icons.STRIKETHROUGH_S_OUTLINED, color=ft.Colors.ON_SURFACE),
                                    data="strike",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Cursiva", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Icon(ft.Icons.FORMAT_ITALIC_OUTLINED, color=ft.Colors.ON_SURFACE),
                                    data="italic",
                                    on_click=lambda e: page.run_task(button_markdown, e.control.data)
                                ),
                                ft.PopupMenuItem(
                                    ft.Text("Negrita", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Icon(ft.Icons.FORMAT_BOLD_OUTLINED, color=ft.Colors.ON_SURFACE),
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
                            icon=ft.Image("assets/icons/link_2.svg", color=ft.Colors.ON_SURFACE, width=25),
                            tooltip="Enlace",
                            items=[
                                ft.PopupMenuItem(
                                    ft.Text("Link Rapido", weight=ft.FontWeight.W_400, margin=ft.Margin(3, bottom=3)),
                                    ft.Icon(ft.Icons.ADD_LINK_OUTLINED, color=ft.Colors.ON_SURFACE),
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
                border=ft.Border.all(1, ft.Colors.SURFACE_CONTAINER_HIGHEST),
                border_radius=50
            )
        ],
        col=9,
        margin=ft.Margin(top=10),
        expand=True
    )
    
    page.overlay.append(sheet_vaciar)
    def abrir_sheet():
        sheet_vaciar.open = True
        page.update()
    
    def cerrar_sheet():
        sheet_vaciar.open = False
        page.update()
    
    def update_panel():
        panel_control_desk.content.controls[2].controls = [ # type: ignore
            Pagina(
                pagina["titulo"],
                pagina["id"],
                lambda e: obtener(e),
                lambda e: eliminar(e)
            ) for pagina in PaginaCtrl().obtener_data(page.session.store.get("user")) # type: ignore
        ]
        
        page.update()
    
    def obtener(e):
        page.session.store.set("pagina", e.control.data)
        pagina = PaginaCtrl().obtener_data(id = e.control.data)
        
        popbutton_cerrar.visible = txt_editando.visible = True
        titulo.value = pagina["titulo"] # type: ignore
        contenido_preview.value = contenido_editor.value = pagina["contenido"] # type: ignore
        page.update()
    
    def guardar():
        id_pagina = page.session.store.get("pagina")
        if id_pagina:
            PaginaCtrl().editar_pagina(id_pagina, titulo.value, contenido_editor.value)
            
        else:
            PaginaCtrl().crear_pagina(page.session.store.get("user"), titulo.value, contenido_editor.value)
            update_panel()
            popbutton_cerrar.visible = txt_editando.visible = True
            
        page.update()
    
    def cerrar(save: bool):
        if save: guardar()
        if page.session.store.get("pagina") != None: page.session.store.remove("pagina")
        
        popbutton_cerrar.visible = txt_editando.visible = False
        titulo.value = contenido_editor.value = contenido_preview.value = ""
        page.update()
    
    def eliminar(e = None):
        if e:
            PaginaCtrl().eliminar_pagina(id=e.control.data)
        else:
            PaginaCtrl().eliminar_pagina(page.session.store.get("user"))
            cerrar_sheet()
        
        update_panel()
        
        popbutton_cerrar.visible = txt_editando.visible = False
        titulo.value = contenido_preview.value = contenido_editor.value = ""
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
            "h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ", "bold": "****", "italic": "**",
            "strike": "~~~~", "list_or": "1. ", "list_un": "- ", "quote": "> ", "code": "```lenguaje\n\n```",
            "divider": "---", "link": "[]()", "quick_link": "<>", "image": "![]()"
        }
        
        contenido_editor.value += tipos[tipo]
        
        pos = len(contenido_editor.value)
        if tipo == "code": pos -= 4
        elif tipo in ["link", "image"]: pos -= 3
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
                        ft.Image("assets/images/onyx_logo.png", width=30),
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
        padding=5
    )