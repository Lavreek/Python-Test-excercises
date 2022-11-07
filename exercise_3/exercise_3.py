import math
from math import sqrt
from tkinter import Tk, W, E, Text, IntVar, DISABLED, NORMAL, END, BooleanVar, ttk
from tkinter.ttk import Frame, Button, Style

PROJECT_ID = 70155120

main_width = 435

main_height = 230

GUI = Tk()
GUI.title("Калькулятор на Tkinter")
GUI.geometry("{0}x{1}".format(main_width, main_height))

STYLE = ttk.Style()

STYLE.configure("aBG.TButton", background="green", foreground="blue")
STYLE.configure("aR.TButton", background="red", foreground="white")
STYLE.configure("aB.TButton", background="blue", foreground="white")
STYLE.configure("aG.TButton", background="gray", foreground="white")

Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

FULL_WIDTH = IntVar()  # width in Advanced mode " ≡ "
STRANGE_BTN = BooleanVar()  # check for Button " < > "
ANSWER_TAKED = BooleanVar()  # check for "RESET" text field
CHAR = BooleanVar()
BUTTONS = []  # memory buttons in Advanced mode
MEMORY_BUTTONS = []
VALUES = []  # values from text field
MEMORY = []
MEMORY_PARAM = ["MC", "MR", "MS", "M+", "M-"]
OPTIONAL_FUNC = ["mod", "tan", "asin", "acos", "exp"]


def key(event):
    print("pressed", repr(event.char))


def insertChar(char, char_type):
    if ANSWER_TAKED.get():
        clearEntry()
        ANSWER_TAKED.set(False)
    if char_type == "int":
        MAIN_FIELD_TEXT.configure(state=NORMAL)

        if CHAR.get():
            MAIN_FIELD_TEXT.delete(1.0, END)

        MAIN_FIELD_TEXT.insert(END, char)
        MAIN_FIELD_TEXT.configure(state=DISABLED)
        CHAR.set(False)
    if char_type == "char":
        putInTextField(char)
        CHAR.set(True)


def click(col, row):
    save_state = 2

    if col == 0:
        MEMORY[row]['array'][save_state]['value'] = MEMORY[row]['array'][col]['value']
    if col == 1:
        putInTextField(MEMORY[row]['array'][save_state]['value'])
    if col == 2:
        MEMORY[row]['array'][col]['value'] = float(MAIN_FIELD_TEXT.get(1.0, END))
    if col == 3:
        MEMORY[row]['array'][save_state]['value'] += float(MAIN_FIELD_TEXT.get(1.0, END))
    if col == 4:
        MEMORY[row]['array'][save_state]['value'] -= float(MAIN_FIELD_TEXT.get(1.0, END))


def openSecondaryMenu(event):
    createSecondary()


def closeSecondaryMenu(event):
    disposeSecondary()


def disposeSecondary():
    FULL_WIDTH.set(main_width)
    GUI.geometry("{0}x{1}".format(FULL_WIDTH.get(), main_height))
    for i in range(len(BUTTONS)):
        BUTTONS[i].destroy()
    for i in range(len(MEMORY_BUTTONS)):
        MEMORY_BUTTONS[i].destroy()
    mod_menu.bind("<Button-1>", openSecondaryMenu)


def createSecondary():
    FULL_WIDTH.set(int(main_width * 1.97))
    GUI.geometry("{0}x{1}".format(FULL_WIDTH.get(), main_height))

    s = str(PROJECT_ID)
    last_char = len(s)
    mid_char = last_char - 3
    string = s[mid_char:last_char]
    rows = int(string[0]) + int(string[1]) + int(string[2])

    for j in range(rows):
        next = []
        for i in range(5):
            btn = Button(first_frame, text="{0}".format(MEMORY_PARAM[i]), style="G.TButton",
                         command=lambda index_i=i, index_j=j: click(index_i, index_j))
            btn.grid(row=2 + j, column=5 + i)
            next.append({"func": MEMORY_PARAM[i], "value": 0})
            BUTTONS.append(btn)
        MEMORY.append({"row": j, "array": next})

    mod_menu.bind("<Button-1>", closeSecondaryMenu)

    btn = Button(first_frame, text="{0}".format(OPTIONAL_FUNC[0]), style="G.TButton",
                 command=lambda type=OPTIONAL_FUNC[0]: putChar(type))
    btn.grid(row=2 + rows, column=5)
    MEMORY_BUTTONS.append(btn)

    for i in range(4):
        btn = Button(first_frame, text="{0}".format(OPTIONAL_FUNC[i + 1]), style="G.TButton",
                     command=lambda type=OPTIONAL_FUNC[i + 1]: optional(type))
        btn.grid(row=2 + rows, column=6 + i)
        MEMORY_BUTTONS.append(btn)


def resizeDisplay(event):
    resize(STRANGE_BTN.get())


def resize(check):
    if FULL_WIDTH.get() == 0:
        FULL_WIDTH.set(main_width)
    if not check:
        amount = 0
        for i in range(len(str(PROJECT_ID))):
            amount += int(str(PROJECT_ID)[i])
        value = int(str(amount)[0]) + int(str(amount)[1])
        MAIN_FIELD_TEXT.configure(height=value)
        GUI.geometry("{0}x{1}".format(FULL_WIDTH.get(), (main_height + (11 * value))))
        strange_btn.bind("<Button-1>", resizeDisplay)
        STRANGE_BTN.set(True)
    if check:
        MAIN_FIELD_TEXT.configure(height=1)
        GUI.geometry("{0}x{1}".format(FULL_WIDTH.get(), main_height))
        strange_btn.bind("<Button-1>", resizeDisplay)
        STRANGE_BTN.set(False)


def putInTextField(value):
    MAIN_FIELD_TEXT.configure(state=NORMAL)
    MAIN_FIELD_TEXT.delete(1.0, END)
    MAIN_FIELD_TEXT.insert(1.0, value)
    MAIN_FIELD_TEXT.configure(state=DISABLED)


def calculatePercent():  # Done!
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    value = value / 100
    putInTextField(value)


def oneDivision():
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    try:
        value = 1 / value
    except:
        value = "error"
    putInTextField(value)


def putChar(char):
    if len(VALUES) > 0:
        if VALUES[len(VALUES) - 1]['type'] != "char":
            value = float(MAIN_FIELD_TEXT.get(1.0, END))
            VALUES.append({'value': value, 'type': "int"})
            VALUES.append({'value': char, 'type': "char"})
            insertChar(char, "char")
    if len(VALUES) == 0:
        value = float(MAIN_FIELD_TEXT.get(1.0, END))
        VALUES.append({'value': value, 'type': "int"})
        VALUES.append({'value': char, 'type': "char"})
        insertChar(char, "char")


def root():
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    try:
        value = sqrt(value)
    except:
        value = "error"
    putInTextField(value)


def reverse():
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    value = value * (-1)
    putInTextField(value)


def powThis():
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    value = pow(value, 2)
    putInTextField(value)


def optional(function):
    if function == "tan":
        calcTan()
    if function == "asin":
        calcAsin()
    if function == "acos":
        calcAcos()
    if function == "exp":
        calcExp()


def calcTan():
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    try:
        value = math.tan(value)
    except:
        value = "error"
    putInTextField(value)


def calcAsin():
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    try:
        value = math.asin(value)
    except:
        value = "error"
    putInTextField(value)


def calcAcos():
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    try:
        value = math.acos(value)
    except:
        value = "error"
    putInTextField(value)


def calcExp():
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    try:
        value = math.exp(value)
    except:
        value = "error"
    putInTextField(value)


def multiplication(value1, value2):
    result = value1 * value2
    return result


def division(value1, value2):
    try:
        result = value1 / value2
    except:
        result = "error"
    return result


def minus(value1, value2):
    result = value1 - value2
    return result


def boost(value1, value2):
    result = pow(value1, value2)
    return result


def plus(value1, value2):
    result = value1 + value2
    return result


def clear():
    clearEntry()
    VALUES.clear()


def clearEntry():
    MAIN_FIELD_TEXT.configure(state=NORMAL)
    MAIN_FIELD_TEXT.delete(1.0, END)
    MAIN_FIELD_TEXT.configure(state=DISABLED)


def backspace():
    if len(MAIN_FIELD_TEXT.get(1.0, END)) > 0:
        string = MAIN_FIELD_TEXT.get(1.0, END)
        s = len(string) - 2
        string = string[0:s]
        putInTextField(string)


def divisionMod(value1, value2):
    result = divmod(value1, value2)
    return result


def calculateEnd():
    middle = 0
    value = float(MAIN_FIELD_TEXT.get(1.0, END))
    VALUES.append({'value': value, 'type': "int"})
    for index in range(len(VALUES)):
        if VALUES[index]['type'] == "char":
            if middle == 0:
                middle = float(VALUES[index - 1]['value'])
            if VALUES[index]['value'] == "*":
                middle = multiplication(value1=middle, value2=int(VALUES[index + 1]['value']))
            if VALUES[index]['value'] == "/":
                middle = division(value1=middle, value2=int(VALUES[index + 1]['value']))
            if VALUES[index]['value'] == "+":
                middle = plus(value1=middle, value2=int(VALUES[index + 1]['value']))
            if VALUES[index]['value'] == "-":
                middle = minus(value1=middle, value2=int(VALUES[index + 1]['value']))
            if VALUES[index]['value'] == "^":
                middle = boost(value1=middle, value2=int(VALUES[index + 1]['value']))
            if VALUES[index]['value'] == "mod":
                middle = divisionMod(value1=middle, value2=int(VALUES[index + 1]['value']))
    putInTextField(str(middle))
    VALUES.clear()


first_frame = Frame()
first_frame.pack()

MAIN_FIELD_TEXT = Text(first_frame, height=1, width=6)
MAIN_FIELD_TEXT.configure(state=DISABLED)
MAIN_FIELD_TEXT.grid(row=0, columnspan=10, sticky=W + E)
MAIN_FIELD_TEXT.bind("<Key>", key)

mod_menu = Button(first_frame, text="≡", style="R.TButton")
mod_menu.grid(row=1, column=0)
mod_menu.bind("<Button-1>", openSecondaryMenu)

strange_btn = Button(first_frame, text="< >", style="R.TButton")
strange_btn.grid(row=1, column=1)
strange_btn.bind("<Button-1>", resizeDisplay)

b_clear = Button(first_frame, text="C", style="R.TButton", command=lambda: clear())
b_clear.grid(row=1, column=4)

b_percent = Button(first_frame, text=" % ", style="B.TButton", command=lambda: calculatePercent())
b_percent.grid(row=2, column=0)

bck = Button(first_frame, text=" ← ", style="B.TButton", command=lambda: backspace())
bck.grid(row=2, column=1)

b_one_division = Button(first_frame, text="1/x", style="B.TButton", command=lambda: oneDivision())
b_one_division.grid(row=2, column=2)

b_pow_x = Button(first_frame, text="x^2", style="B.TButton", command=lambda: powThis())
b_pow_x.grid(row=2, column=3)

b_clearEntry = Button(first_frame, text="CE", style="R.TButton", command=lambda: clearEntry())
b_clearEntry.grid(row=2, column=4)

for i in range(3):
    b_click = Button(first_frame, text="{0}".format(7 + i), style="BG.TButton",
                     command=lambda put=7 + i, type="int": insertChar(put, type))
    b_click.grid(row=3, column=i)

b_division = Button(first_frame, text="/", style="G.TButton", command=lambda put="/": putChar(put))
b_division.grid(row=3, column=3)

b_pow_x_in_y = Button(first_frame, text="x^y", style="G.TButton", command=lambda put="^": putChar(put))
b_pow_x_in_y.grid(row=3, column=4)

for i in range(3):
    b_click = Button(first_frame, text="{0}".format(4 + i), style="BG.TButton",
                     command=lambda put=4 + i, type="int": insertChar(put, type))
    b_click.grid(row=4, column=i)

b_multiplication = Button(first_frame, text="*", style="G.TButton", command=lambda put="*": putChar(put))
b_multiplication.grid(row=4, column=3)

b_root = Button(first_frame, text="√", style="G.TButton", command=lambda: root())
b_root.grid(row=4, column=4)

for i in range(3):
    b_click = Button(first_frame, text="{0}".format(1 + i), style="BG.TButton",
                     command=lambda put=1 + i, type="int": insertChar(put, type))
    b_click.grid(row=5, column=i)

b_minus = Button(first_frame, text="-", style="G.TButton", command=lambda put="-": putChar(put))
b_minus.grid(row=5, column=3)

b_plus_minus = Button(first_frame, text="+/-", style="G.TButton", command=lambda: reverse())
b_plus_minus.grid(row=5, column=4)

b_zero = Button(first_frame, text="0", style="BG.TButton", command=lambda put=0, type="int": insertChar(put, type))
b_zero.grid(row=6, column=1)

b_dot = Button(first_frame, text=".", style="BG.TButton", command=lambda put=".", type="int": insertChar(put, type))
b_dot.grid(row=6, column=2)

b_plus = Button(first_frame, text="+", style="G.TButton", command=lambda put="+": putChar(put))
b_plus.grid(row=6, column=3)

b_equally = Button(first_frame, text="=", style="B.TButton", command=lambda: calculateEnd())
b_equally.grid(row=6, column=4)

first_frame.pack()
GUI.mainloop()
