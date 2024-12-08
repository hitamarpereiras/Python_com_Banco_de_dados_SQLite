import flet as ft
from datetime import datetime
import os
from time import sleep
import asyncio
from Models import DAO

date = datetime.now()
day = date.day
month = date.month
year = date.year

def main(page: ft.Page):
    page.window.width = 780
    page.window.height = 600
    page.window.min_width = 780
    page.window.min_height = 600
    page.window.max_width = 790
    page.window.max_height = 620
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = '#23192d'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    global card_cliente

    def get_register(e):
        if name.value == '' or email.value == '':
            alert_function(False, 'Please fill in the fields!') 
        elif password.value == '' or date_value.value == '':
            alert_function(False, 'Please fill in the fields!')
        elif cursos.value == '' or comment.value == '':
            alert_function(False, 'Please fill in the fields!')
        else:
            client = DAO.UserDAO(name.value, email.value, password.value, date_value.value, picture_path.value, cursos.value, comment.value)
            v, res = client.is_valid()
            if not v:
                alert_function(v, res)
            else:
                cmd, cmd_res = DAO.add_client(client)
                if cmd:
                    alert_function(cmd, cmd_res)
                    clean_inputs(e)
                else:
                    alert_function(cmd, cmd_res)

    def update_and_search(e):
        id_c = search.value.lower()
        if 'up' in id_c:
            client_id = id_c.replace('up', '')
            res, values = DAO.search_client(client_id)
            if res:
                name.value = res[1]
                email.value = res[2]
                password.value = res[3]
                date_value.value = res[4]
                section_signup.update()
            else:
                alert_function(False, 'Not implemented!')
        else:
            clean_card_input(e)
            res, values = DAO.search_client(id_c)
            load.visible = True
            card_cliente.update()
            sleep(2)
            load.visible = False
            card_cliente.update()
            if res:
                name_card.value = res[1]
                email_card.value = res[2]
                date_card.value = res[4]
                folder = get_path_folders(e)
                img_dard.src = f"{os.path.join(folder, values)}"
                card_cliente.update()
            else:
                alert_function(False, values)

    def cliente_up(e):
        if name.value == '' or email.value == '':
            alert_function(False, 'Please fill in the fields!') 
        elif password.value == '' or date_value.value == '':
            alert_function(False, 'Please fill in the fields!')
        elif cursos.value == '' or comment.value == '':
            alert_function(False, 'Please fill in the fields!')
        else:
            client = DAO.UserDAO(name.value, email.value, password.value, date_value.value, picture_path.value, cursos.value, comment.value)
            v, res = client.is_valid()
            if not v:
                alert_function(v, res)
            else:
                if 'up' in search.value:
                    client_id = search.value.replace('up', '') 
                    cmd, cmd_res = DAO.update_client(client_id, client)
                    if cmd:
                        alert_function(cmd, cmd_res)
                        clean_inputs(e)
                    else:
                        alert_function(cmd, cmd_res)
                else:
                    alert_function(False, 'Please isert UP and ID')

    def client_delete_now(e):
        if search.value:
            client_id = search.value.replace('up', '') 
            res = DAO.delete_cliente(client_id)
            if res:
                alert_function(True, res)
                clean_inputs(e)
            else:
                alert_function(False, res)
        else:
            alert_function(False, 'Please isert ID')

    def get_path_folders(e):
        path = 'Data'
        origin = 'profiles'
        folder = os.path.join(path, origin)
        return folder
    
    def clean_card_input(e):
            name_card.value = ''
            email_card.value = ''
            date_card.value = ''
            img_dard.src = './assets/avatar.jpg'
            card_cliente.update()

    def clean_inputs(e):
        name.value = ''
        email.value = ''
        password.value = ''
        date_value.value = ''
        picture_path.value = ''
        cursos.value = ''
        comment.value = ''
        section_signup.update()

    async def animation(e=None):
            card_alert.scale = 1  
            card_alert.update() 
            await asyncio.sleep(1)
            sleep(7)
            card_alert.scale = 0  
            card_alert.update() 
            await asyncio.sleep(1)

    def alert_function(value, text):
        if value:
            icon_alert.src = './assets/ok.png'
            title_alert.value = 'Successfully!'
            card_alert.bgcolor = '#94e0b0'
            text_alert.value = f"{text}"
            text_alert.update()
            page.run_task(animation)
        else:
            icon_alert.src = './assets/danger.png'
            title_alert.value = 'Erro ao registrar!!'
            card_alert.bgcolor = '#ffe498'
            text_alert.value = f"{text}"
            text_alert.update()
            page.run_task(animation)
            
    def change_date(e):
        date_value.value = f"{e.control.value.strftime('%d/%m/%Y')}"
        date_value.update()

    def dismiss(e):
        date_value.value = 'Please Date!'
        date_value.update()

    def get_your_picture(e):
        if e.files:
            picture_path.value = f"{e.files[0].path}"
            picture_path.update()        

    h1 = ft.Text(
        value= 'Settings Box',
        size= 22,
        weight= ft.FontWeight.W_500,
        color= '#23192d'
    )

    copyrights = ft.Text(
        value= 'Desenvolvido por: Hitamar Silva®',
        size= 12,
        italic= True,
        color= '#23192d'
    )

    load = ft.Image(
        src= './assets/loading.gif',
        width= 120,
        visible= False
    )

    title_alert = ft.Text(
        value= 'Erro ao registrar!',
        size= 18,
        color= 'black',
        weight=ft.FontWeight.W_500
    )

    text_alert = ft.Text(
        value= 'Texto complementar',
        size= 14,
        color= 'black',
        weight=ft.FontWeight.W_400
    )

    icon_alert = ft.Image(
        src= './assets/danger.png',
        width= 25
    )

    ##################### Inputs e Botoes #####################
    name = ft.TextField(
        width= 200,
        height= 50,
        border_color= '#77477e',
        border_width= 2,
        border_radius= 16,
        cursor_color= '#77477e',
        prefix_icon= ft.icons.PERSON,
        capitalization= ft.TextCapitalization.WORDS
    )

    email = ft.TextField(
        width= 200,
        height= 50,
        border_color= '#77477e',
        border_width= 2,
        border_radius= 16,
        cursor_color= '#77477e',
        prefix_icon= ft.icons.EMAIL,
    )

    password = ft.TextField(
        width= 200,
        height= 50,
        border_color= '#77477e',
        border_width= 2,
        border_radius= 16,
        cursor_color= '#77477e',
        prefix_icon= ft.icons.SECURITY,
        password= True,
        can_reveal_password= True
    )

    """ Pegar data de nascimento """
    date_value = ft.TextField(
        width= 140,
        height= 50,
        border_color= '#77477e',
        border_width= 2,
        border_radius= 16,
        cursor_color= '#77477e'
    )
    date_piker = ft.DatePicker(
        first_date= datetime(day=1, month=1, year=1970),
        last_date= datetime(day=day, month=month, year=year),
        on_change= change_date,
        on_dismiss= dismiss
    )
    button_date = ft.IconButton(
        icon= ft.icons.CALENDAR_MONTH,
        icon_color= '#77477e',
        icon_size= 30,
        bgcolor= ft.colors.BLACK12,
        on_click= lambda e: page.open(date_piker)
    )

    """ Pegar foto para perfil """
    picture_path = ft.TextField(
        width= 140,
        height= 50,
        border_color= '#77477e',
        border_width= 2,
        border_radius= 16,
        cursor_color= '#77477e',
    )
    picker_picture = ft.FilePicker(
        on_result= get_your_picture
    )
    page.overlay.append(picker_picture)
    button_picture = ft.IconButton(
        icon= ft.icons.IMAGE,
        icon_color= '#77477e',
        icon_size= 30,
        bgcolor= ft.colors.BLACK12,
        on_click= lambda _:picker_picture.pick_files()
    )

    button_signup = ft.ElevatedButton(
        width= 140,
        text= 'Register Now',
        color= 'white',
        bgcolor= '#77477e',
        on_click= get_register
    )

    button_update = ft.ElevatedButton(
        width= 140,
        text= 'UPDATE',
        color= 'white',
        bgcolor= '#364461',
        icon= ft.icons.UPDATE,
        on_click= cliente_up
    )

    button_delete = ft.ElevatedButton(
        width= 140,
        text= 'DELETE',
        color= '#feedbf',
        bgcolor= '#bb375e',
        icon= ft.icons.REMOVE,
        on_click= client_delete_now
    )

    search = ft.TextField(
        hint_text= 'Search',
        width= 140,
        height= 40,
        border_color= 'transparent',
        border_width= 2,
        border_radius= 16,
        cursor_color= '#77477e',
        bgcolor= ft.colors.BLACK12,
        suffix_icon= ft.icons.SEARCH,
        on_submit= update_and_search
    )

    name_card = ft.Text(
        value= 'Exemple',
        size= 20,
        weight=ft.FontWeight.W_400,
        color= 'black'
    )
    email_card = ft.Text(
        value= 'exemple@email.com',
        size= 14,
        weight=ft.FontWeight.W_400,
        color= 'black'
    )
    date_card = ft.Text(
        value= '01/01/2000',
        size= 14,
        weight=ft.FontWeight.W_400,
        color= 'black'
    )
    img_dard = ft.Image(
        src= './assets/avatar.jpg',
        width= 60,
        border_radius= 50
    )

    cursos = ft.Dropdown(
        label= 'Cursos',
        bgcolor= '#feedbf',
        border_color= '#77477e',
        border_width= 2,
        border_radius= 16,
        width= 120,
        options=[
            ft.dropdown.Option('HTML/CSS'),
            ft.dropdown.Option('Java Script'),
            ft.dropdown.Option('Python'),
            ft.dropdown.Option('Django')
        ]
    )

    comment = ft.TextField(
        width= 230,
        height= 80,
        max_lines= 5,
        max_length= 120,
        border_color= '#77477e',
        border_width= 2,
        border_radius= 16,
        cursor_color= '#77477e',
        capitalization= ft.TextCapitalization.SENTENCES
    )

    ##################### Containers e Colunas #####################

    card_alert = ft.Container(
        bgcolor= '#ffe498',
        border_radius= 16,
        padding= 10,
        visible= True,
        shadow= ft.BoxShadow(color=ft.colors.BLACK26, spread_radius=1.1, blur_radius=5),
        scale=0,
        animate_scale= ft.Animation(duration=1000, curve=ft.AnimationCurve.BOUNCE_IN),
        content=ft.Column(
            width= 280,
            height= 60,
            scroll= ft.ScrollMode.AUTO,
            controls=[
                ft.Row([icon_alert, title_alert],alignment=ft.MainAxisAlignment.CENTER),
                text_alert
            ],alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    card_cliente = ft.Container(
        bgcolor= '#f1f2f1',
        width= 300,
        padding= 20,
        border_radius= 16,
        shadow= ft.BoxShadow(color=ft.colors.BLACK26, spread_radius=1.1, blur_radius=5 ),
        scale=1,
        animate_scale= ft.Animation(duration=1500, curve=ft.AnimationCurve.BOUNCE_IN),
        content=ft.Column(
            spacing= 5,
            expand= True,
            controls=[
                ft.Row([img_dard, name_card, load]),
                ft.Divider(height=2),
                ft.Row([ft.Text('Email:', size=14, weight=ft.FontWeight.W_500, color='#77477e')]),
                email_card,
                ft.Row([ft.Text('Date:', size=14, weight=ft.FontWeight.W_500, color='#77477e')]),
                date_card
            ]
        )
    )

    section_card = ft.Container(
        padding= 20,
        border_radius= 16,
        expand= True,
        content=ft.Column(
            spacing= 14,
            controls=[
                card_alert,
                search,
                card_cliente,
                ft.Row([button_update, button_delete],alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=1, color='#77477e')
            ],alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    col_buttons_signup = ft.Container(
        content=ft.Column(
            height= 180,
            spacing= 6,
            controls=[
            ft.Row([ft.Text('Date of birth:', size=14, weight=ft.FontWeight.W_500, color='#77477e')]),
            ft.Row([date_value, button_date]),
            ft.Row([ft.Text('Profile picture:', size=14, weight=ft.FontWeight.W_500, color='#77477e')]),
            ft.Row([picture_path, button_picture])
        ])
    )

    section_signup = ft.Container(
        expand= True,
        bgcolor= '#feedbf',
        border_radius= 16,
        alignment= ft.alignment.center,
        padding= 14,
        content=ft.Column(
            spacing= 6,
            scroll= ft.ScrollMode.HIDDEN,
            controls=[
                ft.Row([ft.Text('Register', size=24, weight=ft.FontWeight.W_500, color='#77477e')],
                alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=2),
                ft.Row([ft.Text('Full Name:', size=14, weight=ft.FontWeight.W_500, color='#77477e')]),
                name,
                ft.Row([ft.Text('Email:', size=14, weight=ft.FontWeight.W_500, color='#77477e')]),
                email,
                ft.Row([ft.Text('Password:', size=14, weight=ft.FontWeight.W_500, color='#77477e')]),
                password,
                col_buttons_signup,
                ft.Divider(height=2),
                ft.Column([
                    ft.Row([ft.Text('Select your:', size=14, weight=ft.FontWeight.W_500, color='#77477e')]),
                    cursos,
                    ft.Row([ft.Text('Your Coment:', size=14, weight=ft.FontWeight.W_500, color='#77477e')]),
                    comment
                ],alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([button_signup],alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=2)
            ],alignment=ft.MainAxisAlignment.CENTER
        )
    )

    container_main = ft.Container(
        expand= True,
        bgcolor= '#6fbcaa',
        border_radius= 16,
        alignment= ft.alignment.center,
        padding= 20,
        content=ft.ResponsiveRow([
            ft.Column(col=5,
                expand= True,
                spacing= 6,
                controls=[
                ft.Row([h1]),
                ft.Divider(height=2, color='#23192d'),
                section_signup,
                copyrights
                ],alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column(
                    col= 7,
                    expand= True,
                    controls=[
                        section_card
                    ],alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
        ]),
    )

    page.add(
        container_main
    )

if __name__ == '__main__':
    ft.app(target=main)