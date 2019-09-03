from com.bravo.johny.todolist.todoListOperations import *


def fileCheck(file_name) :
    file_exists = 0
    try :
        open(file_name, "r")
        file_exists = 1
    except FileNotFoundError :
        pass

    return file_exists


def showMenuForAnExistingToDo():
    print('1. View ToDo list')
    print('2. Add an entry')
    print('3. Remove an entry')
    print('4. Remove the entire ToDo list')
    print('0. Exit')
    user_input = input('Choice : ')
    return user_input


def showMenuForANewToDo():
    print('1. Create a ToDo list')
    print('0. Exit')
    user_input = input('Enter your Choice : ')
    return user_input


def checkIfInteger(number) :
    isInteger = False
    try:
        int(number)
        isInteger = True
    except ValueError :
        pass

    return isInteger


while(1) :

    # todo_list_file_name = '/home/bittu/python/workspaces/learning-python/com/bravo/johny/todolist/todoList.txt'
    todo_list_file_name = 'todoList.txt'
    file_status = fileCheck(todo_list_file_name)

    if(file_status == 0) :
        user_input = showMenuForANewToDo()
        if(user_input == '0') :
            break
        elif(user_input == '1') :
            createToDoList(todo_list_file_name)
        else :
            print('Wrong input')

    elif(file_status == 1) :
        user_input = showMenuForAnExistingToDo()
        if (user_input == '0') :
            break
        elif (user_input == '1') :
            showToDoList(todo_list_file_name)
        elif(user_input == '2') :
            new_todo = input('Enter new todo :')
            addAnEntry(todo_list_file_name, new_todo)
        elif(user_input == '3') :
            todo_to_be_deleted = input('Enter the todo number to be deleted :')
            while(checkIfInteger(todo_to_be_deleted) == False) :
                print('we are expecting an integer value')
                todo_to_be_deleted = input('Enter the todo number to be deleted :')
            removeAnEntry(todo_list_file_name, int(todo_to_be_deleted))

        elif(user_input == '4') :
            deleteToDoList(todo_list_file_name)
        else :
            print('Wront input')