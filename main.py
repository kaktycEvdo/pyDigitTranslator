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
        # рисование текста
        self.main_layout.add_widget(Label(text="Число", pos=[-self.textinputn.width/1.5, self.textinputn.pos[1]/3]))
        self.main_layout.add_widget(Label(text="С/С", pos=[-self.textinputn.width/1.5,
                                                           self.textinputn.pos[1]/3-self.textinputc.height]))
        self.main_layout.add_widget(Label(text="Вывод", pos=[-self.textinputn.width/1.5,
                                                             self.textinputn.pos[1]/3-self.textoutput.height*2]))
        # кнопка вычисления
        self.computebutton = Button(background_color=[1, 1, 1, 0.2], size_hint=[None, None],
                                    text="Перевести", width=sizes[0] / 2, pos=[sizes[0]/4,
                                                                               self.textinputn.pos[1]/4+self.textoutput.height])
        self.computebutton.bind(on_press=self.compute)
        # рисование полей ввода и кнопок
        self.main_layout.add_widget(self.textinputn)
        self.main_layout.add_widget(self.textinputc)
        self.main_layout.add_widget(self.textinputd)
        self.main_layout.add_widget(self.textoutput)
        self.main_layout.add_widget(self.computebutton)
        return self.main_layout

    def interpret(self, x, b):  # для перевода символов в цифры
        st = None
        rdict = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX',
                 5: 'V', 4: 'IV', 1: 'I'}  # словарь значений римских цифр
        if b==0:
            y = ord(x)  # перевод символа в индекс
            over = 48  # излишек символов юникода
            if int(y) > 64 and int(y) < 91:
                over += 7  # A-Z
                if int(y) > 96 and int(y) < 123:
                    over += 5  # A-Z
                else:
                    self.textoutput.text = "неправильный ввод"
            st = int(y) - over

        elif b==1:
            y = int(x)  # перевод индекса в символ
            over = 48  # излишек символов юникода
            if y + 48 > 57 and y + 48 < 65:
                over += 7  # A-Z
                if y + 55 > 90 and y + 55 < 97:
                    over += 6  # a-z
                    if int(y) + 60 > 122:
                        self.textoutput.text = "слишком большое значение"
            st = chr(y + over)

        elif b==2:
            st = ''
            y = int(x)
            for arabic in rdict.keys():
                while y >= arabic:
                    print(arabic, y)
                    st += rdict[arabic]
                    y -= arabic

        elif b==3:
            st = 0
            l = 0
            while True:
                if len(x) == 0: break
                for arabic in rdict.keys():
                    l = len(x)-1
                    if len(x) == 0: break
                    if l == 0 and rdict[arabic] == x[l]:
                        st += arabic
                        x = x.replace(x[l], "", 1)
                        break
                    else:
                        if x[l] == "X" and x[l - 1] == "I":
                            st += 9
                            x = x.replace(x[l], "", 1)
                            x = x.replace(x[l-1], "", 1)
                        elif x[l] == "V" and x[l - 1] == "I":
                            st += 4
                            x = x.replace(x[l], "", 1)
                            x = x.replace(x[l - 1], "", 1)
                        elif x[l] == "L" and x[l - 1] == "X":
                            st += 40
                            x = x.replace(x[l], "", 1)
                            x = x.replace(x[l - 1], "", 1)
                        elif x[l] == "C" and x[l - 1] == "X":
                            st += 90
                            x = x.replace(x[l], "", 1)
                            x = x.replace(x[l - 1], "", 1)
                        elif x[l] == "D" and x[l - 1] == "C":
                            st += 400
                            x = x.replace(x[l], "", 1)
                            x = x.replace(x[l - 1], "", 1)
                        elif x[l] == "M" and x[l - 1] == "C":
                            st += 900
                            x = x.replace(x[l], "", 1)
                            x = x.replace(x[l - 1], "", 1)
                        elif x[l] == rdict[arabic]:
                            st += arabic
                            x = x.replace(x[l], "", 1)
                    print(st, x)
        return st

    def translate(self, y, p, p1):
        st = ""
        x = 0
        x1 = 0
        t = None
        if len(y) == 2: t = y[1]  # дробная часть ввода
        w = y[0]  # целая часть ввода

        if p == "I":
            x = int(self.interpret(w, 3))
            x1 = None
        elif int(p)!=10:
            for i in range(len(w) - 1, -1, -1):
                x += self.interpret(w[i], 0) * p ** (len(w) - i - 1)
            if t:
                for i in range(-1, -len(t) - 1, -1):
                    x1 += self.interpret(t[i], 0) * p ** (-len(t) - i - 1)
        else:
            x = int(w)
            if t: x1 = int(t)
        res = ""

        if p1 == "I":
            res = self.interpret(x, 2)

        else:
            p1 = int(p1)
            while x > 1:
                st += self.interpret(x % p1, 1)
                x /= p1

            for i in range(len(st) - 1, -1, -1):
                res += st[i]
            if t:
                res += "."
                st = ""
                i = 0  # кол-во знаков после запятой
                while x1 > 0 and i < 10 and x1 != float(p1 - 1):
                    x1 *= p1
                    if x1 % 1 == 0:
                        st += self.interpret(x1 % p1, 1)
                        break
                    print(x1)
                    st += self.interpret(x1 % p1, 1)
                    i += 1
                res += st

        return res

    def compute(self, instance):
        sl = ""
        y = self.textinputn.text
        if y.startswith("-"):
            sl = "-"
            y = y[1:len(y)]
        z = y.split(".")
        p = self.textinputc.text
        p1 = self.textinputd.text
        if (p == "I" or (int(p)>=2 and int(p)<=60)) and (p1 == "I" or (int(p1) <= 60 and int(p1) >= 2)):
            if z and (len(z) == 2 or len(z) == 1): self.textoutput.text = sl+self.translate(z, p, p1)
            elif p1 == "I" and z[1]: self.textoutput.text = "у римских чисел не поддерживаются дроби"
            else: self.textoutput.text = "слишком много разделений точками"
        else: self.textoutput.text = "неправильно введенные значения"


if __name__ == "__main__":
    app = MainApp()
    app.run()
