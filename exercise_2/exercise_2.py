from tkinter import *

current_state = [{'name': "Ivanov", 'account': 70155120}]

width_val = 640
height_val = 480

GUI = Tk()
GUI.geometry("{0}x{1}".format(width_val, height_val))
GUI.title("Задание 2")

command_line = StringVar()

main_frame = Frame()
main_frame.pack()

first_frame = Frame(main_frame)
first_frame.pack(side=LEFT)

second_frame = Frame(main_frame)
second_frame.pack()


def key(event):
    print("pressed", repr(event.char))
    s = command_console.get(1.0, END)
    startCommand(s)


def deposit(name, value):
    client = False
    this_string = ""
    for i in range(len(current_state)):
        if current_state[i]['name'] == name:
            current_account = int(current_state[i]['account'])
            current_account += int(value)
            current_state[i]['account'] = str(current_account)
            this_string += "DEPOSIT: {1} to {0}".format(name, value)
            print("DEPOSIT: {1} to {0}".format(name, value))
            client = True
    if not client:
        current_state.append({'name': name, 'account': value})
        this_string += "CREATE: {0} \n DEPOSIT: {1} to {0}".format(name, value)
        print("CREATE: {0} \n DEPOSIT: {1} to {0}".format(name, value))

    this_string += "\n"
    return this_string


def withdraw(name, value):
    this_string = ""
    client = False
    for i in range(len(current_state)):
        if current_state[i]['name'] == name:
            current_account = int(current_state[i]['account'])
            current_account -= int(value)
            current_state[i]['account'] = str(current_account)
            this_string += "WITHDRAW: {1} from {0}".format(name, value)
            print("WITHDRAW: {1} from {0}".format(name, value))
            client = True
    if not client:
        current_state.append({'name': name, 'account': (int(value) * (-1))})
        this_string += "CREATE: {0} \n WITHDRAW: {1} to {0}".format(name, value)
        print("CREATE: {0} \n WITHDRAW: {1} from {0}".format(name, value))

    this_string += "\n"
    return this_string


def balance(name):
    this_string = ""
    client = False
    for i in range(len(current_state)):
        if current_state[i]['name'] == name:
            this_string += "BALANCE: {0} is {1}".format(name, current_state[i]['account'])
            print("BALANCE: {0} is {1}".format(name, current_state[i]['account']))
            client = True
    if not client:
        this_string += "BALANCE: NO CLIENT"
        print("BALANCE: NO CLIENT")

    this_string += "\n"
    return this_string


def transfer(name_from, name_to, value):
    this_string = ""

    deposit(name_to, value)
    withdraw(name_from, value)
    this_string += "TRANSFER: From {0} to {1} {2}".format(name_from, name_to, value)
    print("TRANSFER: From {0} to {1} {2}".format(name_from, name_to, value))

    this_string += "\n"
    return this_string


def income(percent):
    this_string = ""

    for i in range(len(current_state)):
        if int(current_state[i]['account']) > 0:
            current_account = int(current_state[i]['account'])
            current_account += int(current_account * (int(percent) / 100))
            current_state[i]['account'] = str(current_account)
    this_string += "INCOME: All users get {0}%".format(percent)
    print("INCOME: All users get {0}%".format(percent))

    this_string += "\n"
    return this_string


def startCommand(command_string):
    command_console.delete(1.0, END)
    transaction_history = ""
    commands = command_string.split("\n")

    for i in range(len(commands)):
        command = commands[i].split(" ")
        if command[0] == "DEPOSIT":
            if len(command) == 3:
                transaction_history += deposit(command[1], command[2])
        if command[0] == "WITHDRAW":
            if len(command) == 3:
                transaction_history += withdraw(command[1], command[2])
        if command[0] == "BALANCE":
            if len(command) == 2:
                transaction_history += balance(command[1])
        if command[0] == "TRANSFER":
            if len(command) == 4:
                transaction_history += transfer(command[1], command[2], command[3])
        if command[0] == "INCOME":
            if len(command) == 2:
                transaction_history += income(command[1])

    command_output['text'] = transaction_history


command_button = Button(first_frame, text="Calculate")
command_button.pack(side=LEFT, padx=5)
command_button.bind('<Button-1>', key)

# command_console = Text(main_frame, textvariable=command_line)
command_console = Text(first_frame, width=35)
command_console.pack(side=LEFT, padx=5)

scroll = Scrollbar(first_frame, command=command_console.yview)
scroll.pack(side=LEFT, fill=Y)

command_console.config(yscrollcommand=scroll.set)

command_output = Label(first_frame, text="Текст")
command_output.pack(side=LEFT, padx=5)

GUI.mainloop()
