import random
import typing as tp
from abc import ABC
from tkinter import END, ttk, Label, Entry, Button, scrolledtext, Tk
from tkinter.ttk import Style

from registry import get_reg, set_reg
from utils import Calculation


class BaseGUIInterface(ABC):
    wnd: Tk = Tk()
    tabs: ttk.Notebook
    title: str
    style: Style = Style()

    def __init__(
            self,
            *_args: tp.List[tp.Any],
            size: str = "600x550",
            title: str = "Калькулятор ключей для протокола Диффи-Хеллмана",
            **_kwargs: tp.Dict[tp.Any, tp.Any],
    ) -> None:
        self.wnd.title(title)
        self.wnd.geometry(size)
        self.tabs = ttk.Notebook(self.wnd)

        self._bgcolor = "#F0F0F0"
        self._fgcolor = "black"

        self._configure_styles()

    def _configure_styles(self) -> None:
        self.style.configure(".", background=self._bgcolor)
        self.style.configure(".", foreground=self._fgcolor)

        self.style.configure("TNotebook.Tab", background=self._bgcolor)
        self.style.configure("TNotebook.Tab", foreground=self._fgcolor)


class GUIInterface(BaseGUIInterface):
    lbl1_p: tp.Any
    lbl1_g: tp.Any
    txt1: tp.Any
    txt2: tp.Any
    txt3: tp.Any
    entry_1a: tp.Any
    entry_2b: tp.Any
    txt1_keys_b: tp.Any
    txt1_pass: tp.Any
    txt2_pass: tp.Any
    key_p: tp.Any
    key_g: tp.Any
    key_a: tp.Any
    key_b: tp.Any

    private_key: str

    def btn1_a_clicked(self) -> int:
        k = random.randint(pow(2, 189), pow(2, 191))
        q = Calculation.calc_q(k)
        p = 2 * q + 1
        g = Calculation.calc_g(q)

        self.key_p = str(p)
        self.key_g = str(g)

        self.lbl1_p["text"] = f"Открытый ключ P: {p}"
        self.lbl1_g["text"] = f"Открытый ключ G: {g}"

        return 1

    def btn1_clicked(self):
        self.txt1.delete(1.0, END)

        p = int(self.key_p)
        g = int(self.key_g)
        a = int(self.entry_1a.get())
        s = f'KeyP = "{p}"\nKeyG = "{g}"\nKeyA = "{pow(g, a, p)}"'

        self.txt1.insert(1.0, s)

        return 1

    def btn2clicked(self):
        self.txt3.delete(1.0, END)
        s1 = self.txt2.get(1.0, END)

        ls = s1.split("\n")
        self.key_p = Calculation.sel_key(ls, "KeyP")
        self.key_g = Calculation.sel_key(ls, "KeyG")
        self.key_a = Calculation.sel_key(ls, "KeyA")
        key_b = int(self.entry_2b.get())

        s2 = f'KeyP = "{self.key_p}"\nKeyG = "{self.key_g}"\nKeyB = "{pow(self.key_g, key_b, self.key_p)}"'
        self.txt3.insert(1.0, s2)
        self.txt2_pass.delete(0, END)

        self.private_key = f"{pow(self.key_a, key_b, self.key_p):x}"
        self.txt2_pass.insert(0, self.private_key)
        return 1

    def btn3clicked(self):
        self.txt1_pass.delete(0, END)
        s1 = self.txt1_keys_b.get(1.0, END)

        ls = s1.split("\n")
        self.key_p = Calculation.sel_key(ls, "KeyP")
        self.key_g = Calculation.sel_key(ls, "KeyG")
        self.key_b = Calculation.sel_key(ls, "KeyB")
        key_a = int(self.entry_1a.get())

        self.private_key = f"{pow(self.key_b, key_a, self.key_p):x}"
        self.txt1_pass.insert(0, self.private_key)
        return 1

    def save_password_click_event(self) -> int:
        raw_data = get_reg("passwords")
        if raw_data:
            registry_data = raw_data.split("\n")
        else:
            registry_data = []
        registry_data.append(self.private_key)
        set_reg("passwords", "\n".join(registry_data))
        self.passwords_scrolled_text.delete(1.0, END)
        self.passwords_scrolled_text.insert(0.0, get_reg("passwords"))
        return 1

    def clear_registry_data(self) -> int:
        set_reg("passwords", None)
        self.passwords_scrolled_text.delete(1.0, END)
        self.passwords_scrolled_text.insert(0.0, get_reg("passwords"))
        return 1

    def run(self):
        self.key_p = "3306453098059237858824334370952073099122295323936952279763"
        self.key_g = "1799690951711835320401350080772011372332339888256810095293"
        password_a = "123"
        password_b = "456"

        _sender_tab = ttk.Frame(self.tabs)
        _recipient_tab = ttk.Frame(self.tabs)
        _help_tab = ttk.Frame(self.tabs)
        _passwords_tab = ttk.Frame(self.tabs)

        self.tabs.add(_sender_tab, text="Режим отправителя")
        self.tabs.add(_recipient_tab, text="Режим получателя")
        self.tabs.add(_help_tab, text="Помощь")
        self.tabs.add(_passwords_tab, text="Реестр")

        # Формирование вкладки отправителя
        lbl1_a = Label(
            _sender_tab, text="Ваш личный пароль (никому его не сообщайте)", justify="center", bg=self._bgcolor,
        )
        self.entry_1a = Entry(_sender_tab, width=60, exportselection=0)
        self.entry_1a.insert(0, password_a)

        btn1_a = Button(
            _sender_tab, text="Сгенерировать другие открытые ключи P и G", command=self.btn1_a_clicked, width=40,
        )

        self.lbl1_p = Label(_sender_tab, text=f"Открытый ключ P: {self.key_p}", bg=self._bgcolor, )

        self.lbl1_g = Label(_sender_tab, text=f"Открытый ключ G: {self.key_g}", bg=self._bgcolor, )

        btn1 = Button(
            _sender_tab, text="Создать сообщение для отправки контрагенту", command=self.btn1_clicked, width=40,
        )

        lbl11 = Label(_sender_tab, text="Отправьте это сообщение контрагенту", bg=self._bgcolor, )

        self.txt1 = scrolledtext.ScrolledText(_sender_tab, width=70, height=3)

        lbl2_a = Label(_sender_tab, text="Введите сообщение от контрагента (ключи P, G, B)", bg=self._bgcolor, )

        self.txt1_keys_b = scrolledtext.ScrolledText(_sender_tab, width=70, height=3, )

        btn3 = Button(_sender_tab, text="Вычислить общий пароль", command=self.btn3clicked, width=40, )

        lbl1_pass = Label(_sender_tab, text="Ваш общий пароль (никому его не передавайте)", bg=self._bgcolor, )

        save_password_to_registry_button = Button(
            _sender_tab, text="Сохранить в реестр", command=self.save_password_click_event, width=40,
        )

        self.txt1_pass = Entry(_sender_tab, width=60, exportselection=0)
        self.txt1_pass.insert(0, "")

        lbl1_a.grid(column=0, row=0, padx=10, pady=10)
        self.entry_1a.grid(column=0, row=5, padx=10, pady=0)
        btn1_a.grid(column=0, row=10, padx=10, pady=10)
        self.lbl1_p.grid(column=0, row=20, padx=10, pady=0)
        self.lbl1_g.grid(column=0, row=30, padx=10, pady=0)
        btn1.grid(column=0, row=40, padx=10, pady=10)
        lbl11.grid(column=0, row=50, padx=10, pady=10)
        self.txt1.grid(column=0, row=60, padx=10, pady=0)
        lbl2_a.grid(column=0, row=70, padx=10, pady=10)
        self.txt1_keys_b.grid(column=0, row=80, padx=10, pady=0)
        btn3.grid(column=0, row=90, padx=10, pady=10)
        lbl1_pass.grid(column=0, row=100, padx=10, pady=10)
        self.txt1_pass.grid(column=0, row=110, padx=10, pady=0)
        save_password_to_registry_button.grid(column=0, row=120, padx=10, pady=10)

        # Формирование вкладки получателя
        lbl2_b = Label(_recipient_tab, text="Ваш личный пароль (никому его не сообщайте)", bg=self._bgcolor, )
        self.entry_2b = Entry(_recipient_tab, width=60, exportselection=0)
        self.entry_2b.insert(0, password_b)

        lbl2 = Label(_recipient_tab, text="Введите сообщение от контрагента (ключи P, G, A)", bg=self._bgcolor, )

        self.txt2 = scrolledtext.ScrolledText(_recipient_tab, width=70, height=3)

        btn2 = Button(
            _recipient_tab, text="Создать сообщение для контрагента и вычислить общий пароль", command=self.btn2clicked
        )

        lbl21 = Label(_recipient_tab, text="Отправьте это сообщение контрагенту", bg=self._bgcolor, )
        self.txt3 = scrolledtext.ScrolledText(_recipient_tab, width=70, height=3)

        lbl3 = Label(_recipient_tab, text="Ваш общий пароль (никому его не передавайте)", bg=self._bgcolor, )

        self.txt2_pass = Entry(_recipient_tab, width=60, exportselection=0)

        lbl2_b.grid(column=0, row=0, padx=10, pady=10)
        self.entry_2b.grid(column=0, row=10, padx=10, pady=0)
        lbl2.grid(column=0, row=30, padx=10, pady=10)
        self.txt2.grid(column=0, row=40, padx=10, pady=0)
        btn2.grid(column=0, row=50, padx=10, pady=10)
        lbl21.grid(column=0, row=60, padx=10, pady=10)
        self.txt3.grid(column=0, row=70, padx=10, pady=0)
        lbl3.grid(column=0, row=80, padx=10, pady=10)
        self.txt2_pass.grid(column=0, row=90, padx=10, pady=10)

        help_text = """
            Инструкция по использованию программы

            1) Выберите вкладку в зависимости от того, кем Вы являетесь (отправителем или получателем) 
            
            2) Введите в верхнее поле своей вкладки свой личный пароль (там по умолчанию находится трёхзначный пароль) 
            
            3) Сгенерируйте заново ключи p и g
            
            Далее Ваши действия зависят от того, отправитель Вы или получатель. 
            
            Если Вы отправитель, следуйте следующим инструкциям: 
            
            1) Нажмите кнопку "Создать сообщение для отправки контрагенту"; 
            
            2) Из данного окошка скопируйте сообщение и отправьте его контрагенту (получателю); 
            
            3) Получив от контрагента ответное сообщение, вставьте его в окошко ниже;
            
            4) Нажмите кнопку "Вычислить общий пароль". 
            
            Если же Вы получатель, то следуйте следующим инструкциям: 
            
            1) Получив от контрагента (отправителя) сообщение, вставьте его в соответствующее окошко; 
            
            2) Нажмите кнопку "Создать сообщение для контрагента и вычислить общий пароль"; 
            
            3) Из окошка ниже скопируйте сообщение и отправьте его контрагенту (отправителю).
        """

        help_label = Label(_help_tab, justify="left", wraplength=580, text=help_text, bg=self._bgcolor, )
        help_label.grid(column=0, row=0, padx=10, pady=10)

        passwords_text = get_reg("passwords")
        self.passwords_scrolled_text = scrolledtext.ScrolledText(_passwords_tab, width=70, )
        self.passwords_scrolled_text.insert(0.0, passwords_text if passwords_text else "")

        clear_registry_button = Button(
            _passwords_tab, text="Очистить реестр", command=self.clear_registry_data, width=40,
        )

        self.passwords_scrolled_text.grid(column=0, row=0, padx=10, pady=10)
        clear_registry_button.grid(column=0, row=10, padx=10, pady=10)

        self.tabs.pack(expand=1, fill="both")
        self.wnd.mainloop()
