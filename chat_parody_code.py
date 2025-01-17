import tkinter as tk
import random
from time import sleep
import requests
from translate import Translator

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.selected_gender = None
        self.expected_answer = None
        self.joke_types = []

        self.window = self.root
        self.window.title("Chat Parody")
        self.window.geometry("800x600")

        # Фреймы для разных этапов
        self.intro_frame = tk.Frame(self.window)
        self.intro_frame.config(bg="#B0C4DE")
        self.math_frame = tk.Frame(self.window)
        self.math_frame.config(bg="#B0C4DE")
        self.gender_frame = tk.Frame(self.window)
        self.gender_frame.config(bg="#B0C4DE")
        self.chat_frame = tk.Frame(self.window)
        self.chat_frame.config(bg="#B0C4DE")

        # Начальный экран
        self.intro_label = tk.Label(self.intro_frame,
                                    text="Данная программа носит развлекательный характер,\nне воспринимайте её наполнение всерьёз.\n Просто поболтайте!",
                                    font=("Arial", 18), justify="center", bg="#B0C4DE")
        self.intro_label.pack(pady=170)
        self.intro_button = tk.Button(self.intro_frame, text="Начать", command=self.math_primer, font=("Arial", 18))
        self.intro_button.place(x=340, y=350, width=140, height=30)
        self.show_frame(self.intro_frame)

        # Математический примерчик
        self.label_question = tk.Label(self.math_frame, text="", font=("Arial", 24))
        self.label_question.pack(pady=100)
        self.entry = tk.Entry(self.math_frame, width=20, font=("Arial", 18))
        self.entry.pack(pady=10)
        self.button_check = tk.Button(self.math_frame, text="Проверить", command=self.check_math, font=("Arial", 18))
        self.button_check.pack(pady=50)
        self.label_result = tk.Label(self.math_frame, text="", font=("Arial", 22), bg="#B0C4DE")
        self.label_result.pack(pady=20)

    def run(self):
        self.window.mainloop()

    def clear_widgets(self, frame):
        # Функция для очищения виджетов внутри указанного фрейма
        for widget in frame.winfo_children():
            widget.destroy()

    def show_frame(self, frame):
        # Функция для показа указанного фрейма и скрытия остальных
        self.intro_frame.pack_forget()
        self.math_frame.pack_forget()
        self.gender_frame.pack_forget()
        self.chat_frame.pack_forget()

        frame.pack(expand=True, fill="both")

    def math_primer(self):
        # Генерируем пример, чтобы проверить интеллект пользователя
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        question_text = f"Проверим ваши базовые знания математики.\n Введите сумму {num1} и {num2}."
        self.label_question.config(text=question_text, bg="#B0C4DE")
        self.expected_answer = num1 + num2
        self.show_frame(self.math_frame)

    def check_math(self):
        # Проверяем интеллект пользователя (правильность его ответа)
        try:
            user_answer = int(self.entry.get())
            if user_answer == self.expected_answer:
                self.label_result.config(text="Правильно!", fg="green")
                self.ask_gender()
            else:
                self.label_result.config(text=f"Попробуйте ещё раз. Ответ был неверен.", fg="red")
        except ValueError:
            self.label_result.config(text="Введите число!", fg="red")

    def ask_gender(self):
        self.clear_widgets(self.gender_frame)

        # Добавляем лэйбл с объясняющим текстом
        explain_label = tk.Label(self.gender_frame, text="Вы доказали свою разумность.\n Укажите ваш пол.",
                                 font=("Arial", 18))
        explain_label.pack(pady=(100, 20))

        def select_gender(gender):
            self.selected_gender = gender
            self.start_chat()

        male_button = tk.Button(self.gender_frame, text="Мужчина", command=lambda: select_gender("male"),
                                font=("Arial", 18), width=15)
        female_button = tk.Button(self.gender_frame, text="Женщина", command=lambda: select_gender("female"),
                                  font=("Arial", 18), width=15)

        male_button.pack(pady=50)
        female_button.pack(pady=50)

        self.show_frame(self.gender_frame)

    def start_chat(self):
        # Запускаем чат с первым сообщением от друга/подруги
        friend_title = "Лучший друг" if self.selected_gender == "female" else "Лучшая подруга"
        friend_message = "Привет, как дела?"

        # Очистка всех виджетов в чате перед началом нового сеанса
        self.clear_widgets(self.chat_frame)

        # Заголовок чата
        title_label = tk.Label(self.chat_frame, text="Чат ФКонтексте", font=("Arial", 16), bg="#B0C4DE")
        title_label.pack(pady=20)

        # Текстовое поле для вывода сообщений
        self.messages_area = tk.Text(self.chat_frame, width=60, height=25, state='disabled')
        self.messages_area.pack(pady=10)

        # Вставляем первое сообщение через секунду
        sleep(1)
        self.messages_area.config(state='normal')
        self.messages_area.insert(tk.END, f"{friend_title}: {friend_message}\n\n")
        self.messages_area.see(tk.END)
        self.messages_area.config(state='disabled')

        # Кнопка для отправки ответа
        self.reply_button = tk.Button(
            self.chat_frame,
            text="Ответить",
            command=lambda: self.send_reply(self.messages_area, self.reply_button)
        )
        self.reply_button.pack(pady=10)

        self.show_frame(self.chat_frame)

    def send_reply(self, messages_area, reply_button):
        # Отправляет заготовленный ответ пользователя и генерирует ответ 'друга'
        standard_user_reply = "Привет, ничего, а ты?"

        # Добавляем сообщение пользователя
        messages_area.config(state='normal')
        messages_area.insert(tk.END, f"Вы: {standard_user_reply}\n\n")
        messages_area.see(tk.END)
        messages_area.config(state='disabled')

        # Генерируем ответ друга
        friend_q = "Супер! Давай я и тебе настроение подниму) Чем хочешь заняться?"

        # Задержка перед появлением ответа друга
        self.window.after(1000, lambda: self.friend_answer(friend_q, messages_area, reply_button))

    def friend_answer(self, response, messages_area, reply_button):
        friend_title = "Лучший друг" if self.selected_gender == "female" else "Лучшая подруга"
        messages_area.config(state='normal')
        messages_area.insert(tk.END, f"\n{friend_title}: {response}\n\n")
        messages_area.see(tk.END)
        messages_area.config(state='disabled')

        # Удаляем кнопку "Ответить"
        reply_button.pack_forget()

        # Создаем кнопки для выбора действия
        laugh_b = tk.Button(self.chat_frame, text="Похихикать",
                                 command=lambda: self.laugh(messages_area))
        play_b = tk.Button(self.chat_frame, text="Поиграть", command=lambda: self.play(messages_area))

        # Располагаем кнопки
        laugh_b.place(x=300, y=500)
        play_b.place(x=400, y=500)

    def laugh(self, messages_area):
        friend_title = "Лучший друг" if self.selected_gender == "female" else "Лучшая подруга"
        messages_area.config(state='normal')
        messages_area.insert(tk.END, f"\n{friend_title}: И о чем же мне пошутить?\n\n")
        messages_area.see(tk.END)
        messages_area.config(state='disabled')

        # Удаляем кнопки "Похихикать" и "Поиграть"
        for widget in self.chat_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Создаем кнопки для выбора типа шутки
        general = tk.Button(self.chat_frame, text="Общие", command=lambda: self.tell_joke(1, messages_area))
        knock_knock = tk.Button(self.chat_frame, text="Тук-тук",
                                       command=lambda: self.tell_joke(2, messages_area))
        programming = tk.Button(self.chat_frame, text="Программистские",
                                       command=lambda: self.tell_joke(3, messages_area))

        # Устанавливаем точные координаты для кнопок
        general.place(x=250, y=500)
        knock_knock.place(x=350, y=500)
        programming.place(x=450, y=500)

    def play(self, messages_area):
        friend_title = "Лучший друг" if self.selected_gender == "female" else "Лучшая подруга"
        messages_area.config(state='normal')
        messages_area.insert(tk.END, f"\n{friend_title}: Отлично! Поиграем в камень-ножницы-бумагу!\n\n")
        messages_area.see(tk.END)
        messages_area.config(state='disabled')

        # Удаляем кнопки "Похихикать" и "Поиграть"
        for widget in self.chat_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Создаем кнопки для выбора действия
        rock = tk.Button(self.chat_frame, text="Камень",
                                command=lambda: self.play_rps("Камень", messages_area))
        paper = tk.Button(self.chat_frame, text="Бумага",
                                 command=lambda: self.play_rps("Бумага", messages_area))
        scissors = tk.Button(self.chat_frame, text="Ножницы",
                                    command=lambda: self.play_rps("Ножницы", messages_area))

        # Располагаем кнопки
        rock.place(x=280, y=500)
        paper.place(x=360, y=500)
        scissors.place(x=440, y=500)

    def play_rps(self, user_choice, messages_area):
        choices = ["Камень", "Ножницы", "Бумага"]
        comp_choice = random.choice(choices)
        friend_title = "Лучший друг" if self.selected_gender == "female" else "Лучшая подруга"

        # Определяем результат
        if user_choice == comp_choice:
            result = "Похоже ничья!"
        elif (user_choice == "Камень" and comp_choice == "Ножницы") or \
             (user_choice == "Ножницы" and comp_choice == "Бумага") or \
             (user_choice == "Бумага" and comp_choice == "Камень"):
            result = "Эх, твоя взяла!"
        else:
            result = "Ха! Победа за мной!"

        # Говорим, что выбрал компьютер/друг, а также сам пользователь
        messages_area.config(state='normal')
        messages_area.insert(tk.END, f"\nТы выбрал(а) {user_choice}, а я выбрал(а) {comp_choice}. {result}\n\n")
        messages_area.see(tk.END)
        messages_area.config(state='disabled')

        # Снова предлагаем выбрать действие
        self.ask_what_next(messages_area)

    def tell_joke(self, joke_type, messages_area):
        try:
            setup, punchline = self.translate_joke(joke_type)
            friend_title = "Лучший друг" if self.selected_gender == "female" else "Лучшая подруга"
            messages_area.config(state='normal')
            messages_area.insert(tk.END, f"\n{friend_title}: {setup}\n{punchline}\n\n")
            messages_area.see(tk.END)
            messages_area.config(state='disabled')

            # Предложение следующего шага
            self.ask_what_next(messages_area)
        except Exception as e:
            messages_area.config(state='normal')
            messages_area.insert(tk.END, f"\nПроизошла ошибка при получении шутки: {str(e)}\nПопробуем еще раз?\n\n")
            messages_area.see(tk.END)
            messages_area.config(state='disabled')

    def ask_what_next(self, messages_area):
        friend_title = "Лучший друг" if self.selected_gender == "female" else "Лучшая подруга"
        messages_area.config(state='normal')
        messages_area.insert(tk.END, f"\n{friend_title}: Чем еще хочешь заняться?\n\n")
        messages_area.see(tk.END)
        messages_area.config(state='disabled')

        # Удаляем все кнопки
        for widget in self.chat_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Создаем новые кнопки для выбора действия
        laugh_button = tk.Button(self.chat_frame, text="Похихикать", command=lambda: self.laugh(messages_area))
        play_button = tk.Button(self.chat_frame, text="Поиграть", command=lambda: self.play(messages_area))

        # Располагаем кнопки
        laugh_button.place(x=300, y=500)
        play_button.place(x=400, y=500)

    def translate_joke(self, joke_type):
        # Получаем случайную шутку в выборанной категории и несуразно переводим ее на русский язык
        if joke_type == 1:
            url = 'https://official-joke-api.appspot.com/jokes/general/random'
        elif joke_type == 2:
            url = 'https://official-joke-api.appspot.com/jokes/knock-knock/random'
        elif joke_type == 3:
            url = 'https://official-joke-api.appspot.com/jokes/programming/random'
        else:
            raise ValueError("Неверный тип шутки")

        joke_response = requests.get(url)
        info = joke_response.json()[0]

        Type = info['type']
        Setup = info['setup']
        Punch = info['punchline']

        translator = Translator(to_lang="ru")
        translated_setup = translator.translate(Setup)
        translated_punchline = translator.translate(Punch)

        return translated_setup, translated_punchline

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    app.run()
