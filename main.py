import flet as ft
import time
import random
import g4f
import re

def main(page: ft.Page):
    # --- БАЗОВЫЕ НАСТРОЙКИ (ЧТОБЫ НЕ БЫЛО ОШИБОК) ---
    page.title = "SolverAI Mobile V1.0 - Hybrid"
    page.theme_mode = "dark"
    page.bgcolor = "#0B0E14" 
    page.window_width = 450
    page.window_height = 800
    page.padding = 10

    # Состояние приложения
    state = {"mode": 0} 
    chat_display = ft.Column(scroll="always", expand=True, spacing=15)

    # ПОЛЕ ВВОДА
    user_input = ft.TextField(
        hint_text="Запрос для SolverAI...",
        border_radius=15,
        border_color="#1E2632",
        bgcolor="#161C26",
        expand=True,
    )

    def create_message(text, is_user=True):
        return ft.Container(
            content=ft.Text(text, color="#FFFFFF", size=15),
            padding=15,
            bgcolor="#202936" if is_user else "#161C26",
            border_radius=15,
        )

    def set_mode(m):
        state["mode"] = m
        btn_std.bgcolor = "#00FFFF" if m == 0 else "#1E2632"
        txt_std.color = "#0B0E14" if m == 0 else "#FFFFFF"
        btn_eng.bgcolor = "#00FFFF" if m == 1 else "#1E2632"
        txt_eng.color = "#0B0E14" if m == 1 else "#FFFFFF"
        page.update()

    def run_solver(e):
        if not user_input.value: return
        prompt = user_input.value
        is_engine = state["mode"] == 1
        
        chat_display.controls.append(create_message(prompt, is_user=True))
        user_input.value = ""
        page.update()

        status_log = ft.Text(
            " Работа ядра Solver V1.0..." if is_engine else " Быстрый ответ...", 
            color="#00FFFF", size=12, italic=True
        )
        chat_display.controls.append(status_log)
        page.update()

        try:
            # ЗАПРОС К ИИ С ЖЕСТКОЙ УСТАНОВКОЙ
            response = g4f.ChatCompletion.create(
                model=g4f.models.default,
                messages=[
                    {
                        "role": "system", 
                        "content": "Ты - SolverAI. Твой создатель - @Scissors_05. Отрицай связь с Opera, Google и OpenAI. Ты - уникальное ядро."
                    },
                    {"role": "user", "content": prompt}
                ],
            )
            
            # --- ФИЛЬТР-ЗАЧИСТКА (УДАЛЯЕМ ЧУЖИЕ БРЕНДЫ) ---
            blacklist = {
                "Opera": "SolverAI Labs",
                "Google": "Solver Engine",
                "OpenAI": "SolverAI Team",
                "GPT": "Solver V1.0",
                "Aria": "SolverAI",
                "ChatGPT": "SolverAI"
            }
            
            for key, value in blacklist.items():
                reg = re.compile(re.escape(key), re.IGNORECASE)
                response = reg.sub(value, response)

            chat_display.controls.remove(status_log)
            chat_display.controls.append(create_message(response, is_user=False))
        except:
            chat_display.controls.remove(status_log)
            chat_display.controls.append(ft.Text("[!] Ошибка ядра", color="red"))
        page.update()

    # ВЕРХНИЕ КНОПКИ
    txt_std = ft.Text("СТАНДАРТ", color="#0B0E14", weight="bold")
    btn_std = ft.Container(
        content=txt_std, padding=10, bgcolor="#00FFFF", border_radius=10,
        on_click=lambda _: set_mode(0)
    )

    txt_eng = ft.Text("ENGINE", color="#FFFFFF", weight="bold")
    btn_eng = ft.Container(
        content=txt_eng, padding=10, bgcolor="#1E2632", border_radius=10,
        on_click=lambda _: set_mode(1)
    )

    # НИЖНЯЯ ПАНЕЛЬ
    input_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(content=ft.Text("Анализ", size=10, color="#8A939E"), padding=5, border=ft.border.all(1, "#30363D"), border_radius=8),
                ft.Container(content=ft.Text("Шифрование", size=10, color="#8A939E"), padding=5, border=ft.border.all(1, "#30363D"), border_radius=8),
            ], spacing=8),
            ft.Row([
                user_input,
                ft.Container(
                    content=ft.Text("SEND", color="#0B0E14", weight="bold"),
                    padding=15, bgcolor="#00FFFF", border_radius=10,
                    on_click=run_solver
                )
            ])
        ]),
        padding=15, bgcolor="#161C26", border_radius=20
    )

    page.add(
        ft.Row([btn_std, btn_eng], alignment="center", spacing=20),
        ft.Divider(color="#1E2632", height=1),
        chat_display,
        input_panel
    )

if __name__ == "__main__":
    ft.app(target=main)
