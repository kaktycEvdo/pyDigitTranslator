from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.relativelayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window


class MainApp(App):
    def build(self):
        # главное
        self.icon = "icon.png"
        self.main_layout = FloatLayout()
        sizes = [Window.size[0], Window.size[1]]
        # ввод текста
        self.textinputn = TextInput(background_color=[1, 1, 1, 0.2], foreground_color="white", multiline=False,
                                    halign="left", size_hint=[None, None], font_size=55, width=sizes[0]/2,
                                    border=[4, 4, 4, 4], pos=[sizes[0]/4, sizes[1]/1.5])
        self.textinputc = TextInput(background_color=[1, 1, 1, 0.2], foreground_color="white", multiline=False,
                                    halign="left", size_hint=[None, None], font_size=55, width=sizes[0]/4,
                                    border=[4, 4, 4, 4], pos=[sizes[0]/4, sizes[1]/1.5-self.textinputn.height])
        self.textinputd = TextInput(background_color=[1, 1, 1, 0.2], foreground_color="white", multiline=False,
                                    halign="left", size_hint=[None, None], font_size=55, width=sizes[0]/4,
                                    border=[4, 4, 4, 4], pos=[self.textinputc.width+sizes[0]/4,
                                                              sizes[1]/1.5-self.textinputn.height])
        self.textoutput = TextInput(background_color=[1, 1, 1, 0.2], foreground_color="white", multiline=False,
                                    halign="left", size_hint=[None, None], font_size=55, width=sizes[0]/2,
                                    border=[4, 4, 4, 4], readonly=True, pos=[sizes[0]/4,
                                                                             sizes[1]/1.5-self.textinputn.height*2])
        # кнопка вычисления
        self.computebutton = Button(background_color=[1, 1, 1, 0.2], size_hint=[None, None],
                                    text="Перевести", width=sizes[0]/2, pos=[sizes[0]/4, sizes[1]/4])
        self.computebutton.bind(on_press=self.compute)
        # рисование текста
        self.main_layout.add_widget(Label(text="Число", pos=[-self.textinputn.width/1.5, self.textinputn.pos[1]/3]))
        self.main_layout.add_widget(Label(text="С/С", pos=[-self.textinputn.width/1.5,
                                                           self.textinputn.pos[1]/3-self.textinputc.height]))
        self.main_layout.add_widget(Label(text="Вывод", pos=[-self.textinputn.width/1.5,
                                                             self.textinputn.pos[1]/3-self.textoutput.height*2]))
        # рисование полей ввода и кнопок
        self.main_layout.add_widget(self.textinputn)
        self.main_layout.add_widget(self.textinputc)
        self.main_layout.add_widget(self.textinputd)
        self.main_layout.add_widget(self.textoutput)
        self.main_layout.add_widget(self.computebutton)
        return self.main_layout

    def interpret(self, x, b):  # для перевода символов в цифры
        y = None
        if b:
            y = ord(x)  # перевод символа в индекс
            over = 48  # излишек символов юникода
            if int(y) > 64 and int(y) < 91:
                over += 7  # A-Z
                if int(y) > 96 and int(y) < 123:
                    over += 5  # A-Z
                else:
                    self.textoutput.text = "слишком большое значение"
        else:
            y = int(x)  # перевод индекса в символ
            over = 48  # излишек символов юникода
            if y + 48 > 57 and y + 48 < 65:
                over += 7  # A-Z
                if y + 55 > 90 and y + 55 < 97:
                    over += 6  # a-z
                    if int(y) + 60 > 122:
                        self.textoutput.text = "слишком большое значение"
        if b: return int(y) - over
        else: return chr(y + over)


    def translate(self, y, p, p1):
        st = ""
        x = 0
        x1 = 0
        t = None
        if len(y) == 2: t = y[1]  # дробная часть ввода
        y = y[0]  # целая часть ввода
        if p!=10:
            for i in range(len(y) - 1, -1, -1):
                x += self.interpret(y[i], True) * p ** (len(y) - i - 1)
            if t:
                for i in range(-1, -len(t)-1, -1):
                    x1 += self.interpret(t[i], True) * p ** (-len(t) - i - 1)
        else:
            x = int(y)
            if t: x1 = int(t)

        while x > 1:
            st += self.interpret(x % p1, False)
            x /= p1

        res = ""
        for i in range(len(st) - 1, -1, -1):
            res += st[i]
        if t:
            res += "."
            st = ""
            i = 0  # кол-во знаков после запятой
            while x1 > 0 and i < 10 and x1 != float(p1-1):
                x1 *= p1
                if x1 // 1 == x1:
                    st += self.interpret(x1 % p1, False)
                    break
                print(x1)
                st += self.interpret(x1 % p1, False)
                i += 1
            res += st

        return res

    def compute(self, instance):
        st = ""
        sl = ""
        y = self.textinputn.text
        if y.startswith("-"):
            sl = "-"
            y = y[1:len(y)]
        z = y.split(".")
        t = ""
        p = int(self.textinputc.text)
        p1 = int(self.textinputd.text)
        if (p <= 60 and p >= 2) and (p1 <= 60 and p1 >= 2):
            if type(z) == list and len(z) == 2 or len(z) == 1: self.textoutput.text = sl+self.translate(z, p, p1)
            else: self.textoutput.text = "чего блин"


if __name__ == "__main__":
    app = MainApp()
    app.run()
