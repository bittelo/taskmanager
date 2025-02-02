import flet as ft
import sqlite3
import os

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.WHITE
        self.page.window_width = 350
        self.page.window_height = 450
        self.page.window_resizable = False
        self.page.window_always_on_top = True
        self.page.title = 'Gerenciador'
        self.task = ''
        self.db_execute('CREATE TABLE IF NOT EXISTS tasks(name, status)')
        self.main_page()

    def db_execute(self, query, params=[]):
        db_path = os.path.join('Python', 'database.db')
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
            return cur.fetchall()
        
    def set_value(self,e):
        self.task = e.control.value
        print(self.task)
        
    def add(self, e, input_task):
       name = self.task
       status='incomplete'
       if name:
           self.db_execute(query='INSERT INTO tasks VALUES(?,?)', params=[name, status])
           input_task.value = ''
       

    def tasks_container(self):
        return ft.Container(
            height=self.page.height * 0.8,
            content=ft.Column(
                controls=[
                    ft.Checkbox(label='Tarefa 1', value=True)
                ]
            )
        )

    def main_page(self): # cria a box e o + 
        input_task = ft.TextField(hint_text='Digite sua tarefa aqui', expand=True, on_change=self.set_value)
        input_bar = ft.Row(
            controls=[
                input_task,
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    on_click=lambda e: self.add(e, input_task) 
                )
                 
            ]
        )
        tabs = ft.Tabs(  # cria as categorias 
            selected_index=0,
            tabs=[
                ft.Tab(text='Todos'),
                ft.Tab(text='Em Andamento'),
                ft.Tab(text='Finalizado'),
            ]
        )

        tasks = self.tasks_container()
        self.page.add(input_bar, tabs, tasks)

ft.app(target=ToDo)
