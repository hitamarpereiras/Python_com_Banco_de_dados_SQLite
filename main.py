import flet as ft
import threading
import time
from datetime import datetime
from time import sleep
from Models import inserts

data = datetime.now()
day = data.day
month = data.month
year = data.year

def fade_in(page: ft.Page):
    for opacity in range(0, 101, 4):  # De 0 a 100 com incrementos de 5
        page.window.opacity = opacity / 100
        page.update()
        time.sleep(0.03)  # Intervalo entre os ajustes de opacidade

def main(page: ft.Page):
    # Inicia o efeito de fade-in em uma thread separada
    threading.Thread(target=fade_in, args=(page,)).start()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment= ft.CrossAxisAlignment.CENTER
    page.vertical_alignment= ft.MainAxisAlignment.CENTER
    page.window.width = 360
    page.window.height = 720
    page.padding = 0

    """ Funcao de cadastro """
    def cadastrar(e):
        if cpf.value == '' or name.value == '':
            alert_app('Preencha os campos')
        elif email.value == '' or nascimento_input.value == '':
            alert_app('Preencha os campos')
        else:
            cliente = inserts.Client(cpf.value, name.value, email.value, nascimento_input.value)
            v, f = cliente.is_valid()
            if not v:
                alert_app(f)
            else:    
                alert.visible = True
                insert = inserts.insert_values(cliente)
                text_alert.color = ft.colors.GREEN_300
                text_alert.value = f"{insert}"
                img_up = inserts.save_image_profile(file_input.value)
                alert.update()

    def get_file_picker(e):
        if e.files:
            file_input.value = f"{e.files[0].path}"
            file_input.update()

    # Update em alerta
    def alert_app(value):
        alert.visible = True
        text_alert.color = ft.colors.RED_500
        text_alert.value = value
        alert.update()
        sleep(3)
        alert.visible = False
        text_alert.value = ''
        text_alert.color = ft.colors.RED_500
        alert.update()

    # Limpar inputs
    def clear_all(e):
        cpf.value = ''
        name.value = ''
        email.value = ''
        nascimento_input.value = ''
        page.update()

    # Pegar a data de nascimento
    def handle_change(e):
        nascimento_input.value = f"{e.control.value.strftime('%d/%m/%Y')}"
        nascimento_input.update()

    def handle_dismissal(e):
        nascimento_input.value = "Obrigatorio!"
        nascimento_input.update()

    date_picker = ft.DatePicker(
        first_date= datetime(day=1, month=1, year=1970),
        last_date= datetime(day=day, month=month, year=year),
        on_change= handle_change,
        on_dismiss= handle_dismissal
    )
    text_alert = ft.Text(
            value= '',
            size= 15,
            weight= ft.FontWeight.W_500,
            color= ft.colors.RED_500
        )
    alert = ft.Row(
        visible= False,
        controls=[
        ft.Image(src='./assets/alert.png', width=20,),
        text_alert
    ],alignment=ft.MainAxisAlignment.CENTER
    )

    cpf = ft.TextField(
        label= 'CPF:',
        width= 200,
        border_radius= 16,
        border_width= 2,
        color= ft.colors.WHITE,
        bgcolor= ft.colors.BLACK38,
        border_color= ft.colors.BLACK,
        cursor_color= '#000000',
        max_length= 11
    )

    name = ft.TextField(
        label= 'Nome:',
        width= 200,
        border_radius= 16,
        border_width= 2,
        color= ft.colors.WHITE,
        bgcolor= ft.colors.BLACK38,
        border_color= ft.colors.BLACK,
        cursor_color= '#000000',
        capitalization= ft.TextCapitalization.WORDS,
    )

    email = ft.TextField(
        label= 'Email:',
        width= 200,
        border_radius= 16,
        border_width= 2,
        color= ft.colors.WHITE,
        bgcolor= ft.colors.BLACK38,
        border_color= ft.colors.BLACK,
        cursor_color= '#000000',
        prefix_icon=(ft.icons.EMAIL)
    )

    pick_file = ft.FilePicker(
        on_result= get_file_picker
    )
    page.overlay.append(pick_file)

    file_input = ft.TextField(
        width= 140,
        border_radius= 16,
        border_width= 2,
        color= ft.colors.WHITE,
        bgcolor= ft.colors.BLACK38,
        border_color= ft.colors.BLACK,
        cursor_color= '#000000'
    )

    btn_getFile = ft.IconButton(
        bgcolor= ft.colors.BLACK45,
        icon= ft.icons.FILE_OPEN,
        icon_color= ft.colors.BLACK,
        on_click= lambda _:pick_file.pick_files()
    )

    nascimento_input = ft.TextField(
        width= 140,
        border_radius= 16,
        border_width= 2,
        color= ft.colors.WHITE,
        bgcolor= ft.colors.BLACK38,
        border_color= ft.colors.BLACK,
        cursor_color= '#000000'
    )

    btn_nascimento = ft.IconButton(
        bgcolor= ft.colors.BLACK45,
        icon= ft.icons.DATE_RANGE,
        icon_color= ft.colors.BLACK,
        on_click= lambda e: page.open(date_picker)
    )

    btn_cadastro = ft.ElevatedButton(
        width= 200,
        height= 40,
        icon= ft.icons.SEND,
        text= 'CADASTRAR',
        bgcolor= ft.colors.BLACK,
        color= ft.colors.WHITE,
        on_click= cadastrar
    )

    btn_clear = ft.ElevatedButton(
        width= 200,
        height= 40,
        icon= ft.icons.CLEAR_ALL,
        text= 'LIMPAR',
        bgcolor= ft.colors.WHITE60,
        color= ft.colors.BLACK,
        on_click= clear_all
    )

    container_main = ft.Stack(
        controls=[
            # Background de fundo
            ft.Image(src='./assets/backg.jpg', width=474, height=780, fit=ft.ImageFit.COVER),

            # Conteudo acima
            ft.Container(
                bgcolor= ft.colors.WHITE24,
                padding= 20,
                expand= True,
                width= 300,
                height= 620,
                border_radius= 24,
                blur= 4,
                content=ft.Column(
                    scroll= ft.ScrollMode.AUTO,
                    spacing= 10,
                    controls=[
                        ft.Text('CADASTRE-SE', size=22, color= ft.colors.RED_800, weight=ft.FontWeight.W_500),
                        alert,
                        #ft.Text('CPF', color= ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                        cpf,
                        #ft.Text('Nome Completo', color= ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                        name,
                        #ft.Text('Email', color= ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                        email,
                        ft.Text('Data de nascimento:', color= ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                        ft.Row([btn_nascimento, nascimento_input],alignment= ft.MainAxisAlignment.CENTER),
                        ft.Text('Foto de Perfil:', color= ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                        ft.Row([btn_getFile, file_input],alignment= ft.MainAxisAlignment.CENTER),
                        btn_cadastro, btn_clear
                    ],alignment= ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ],
        alignment= ft.alignment.center,
        width= 360,
        height= 780,
        expand= True,
    )

    page.add(
        container_main
    )

if __name__ == "__main__":
    ft.app(target=main)