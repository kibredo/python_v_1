import curses
import random
import time

from src.cursor import cursor
from src.menu import menu

the_test_map = dict()
another_test_map = dict()
errors_on_keys = dict()
extra_error_dict = dict()


def do_the_comparation(menu, lines, index_of_lines):

    if chr(menu.k) == lines[index_of_lines][menu.index]:
        menu.some_string += chr(menu.k)
        menu.index += 1

        if menu.index == len(lines[index_of_lines]):
            menu.checker = False
            menu.was_end_of_string = True

    else:
        the_test_map["322"] += 1
        menu.number_of_errors += 1

        if menu.k != 0:
            the_char = chr(menu.k)

            if the_char in extra_error_dict.keys():
                errors_on_keys[the_char] += 1

            else:
                errors_on_keys[the_char] = 1
                extra_error_dict[the_char] = 1
        

def draw_menu(stdscr, index_of_lines, lines, breakpointer):
    menu = menu(stdscr)
    cursor = cursor()
    starting_time = time.time()
    menu.stdscr.clear()
    menu.stdscr.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    while (menu.checker):
        menu.step_number += 1

        if menu.was_first_letter:
            starting_time = time.time()
            menu.was_first_letter = False

        menu.stdscr.clear()
        height, width = menu.stdscr.getmaxyx()
        menu.update_curses(cursor)
        cursor.update_cursor(width, height)
        do_the_comparation(menu, lines, index_of_lines)
        keystr = f"Current Speed = {menu.index / (time.time() - starting_time)}"
        title = "TYPE THIS"[:width-1]
        subtitle = lines[index_of_lines]
        statusbarstr = f"Number of Errors is {menu.number_of_errors}"

        if menu.k == 0:
            keystr = "No key press detected..."[:width-1]

        if menu.was_end_of_string:
            keystr = menu.get_finished(lines, index_of_lines, starting_time, start_y, width, menu.stdscr)

        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)
        insert_window_x = int((width// 2) - len(lines[index_of_lines]) // 2 - len(lines[index_of_lines]) % 2)
        menu.rendering_text(width, height)
        menu.render_status_bar( height, statusbarstr, width)
        menu.get_the_title(start_y, start_x_title, title)
        menu.get_the_rest(start_y, start_x_subtitle, subtitle, insert_window_x, start_x_keystr, keystr, cursor)
        menu.stdscr.refresh()
        menu.k = menu.stdscr.getch()
    the_test_map[index_of_lines] = f"Number of errors: {menu.number_of_errors}"
    another_test_map[index_of_lines] = f"Avarage speed: {len(lines[index_of_lines]) / (time.time() - starting_time)}"

    if index_of_lines < len(lines) - 1:

        if menu.k == 10 or menu.k == 32:
            return True
        
        return False
    else:
        index_of_lines -= 1
        breakpointer = False
        return False
    

def get_the_lines(string_input):
    file_of_strings = open('strings.txt', 'r')
    # не использовал with open(), так как файл может измениться и с open() и close() получается удобнее

    if string_input == "yes":
        print("Do you want to load the file or use default tests? (load/default)")
        extra_input = input()

        if extra_input == "load":
            print("Enter the file name(from current directory):")
            extra_input = input()
            file_of_strings = open(extra_input, 'r')
            
    lines = file_of_strings.read().splitlines()
    random.shuffle(lines)
    file_of_strings.close()
    return lines


def print_the_progress(lines, breakpointer, string_input, index_in_lines):
    while string_input != "no":

        if string_input == "yes":
            should_continue = curses.wrapper(draw_menu, index_in_lines, lines, breakpointer)

            if should_continue:
                string_input = "yes"
                index_in_lines += 1
                continue

            index_in_lines += 1

            if index_in_lines < len(lines) and breakpointer:
                print(f"{index_in_lines} levels of {len(lines)} complete!")
                print("Do you want to continue? (yes/no)")
                string_input = input()
            else:
                print("Congrats! You've completed all levels!")
                break

        else:
            string_input = input()


def get_documented(index_in_lines):
    for i in range(index_in_lines):
        print(f"Level {i + 1}:")
        print(the_test_map[i])
        print(another_test_map[i])
        with open("output.txt", 'a') as the_output:
            the_output.write(f"Level {i + 1}")
            the_output.write(the_test_map[i])
            the_output.write(another_test_map[i])


def get_all_stats(ans):

    if the_test_map["322"] > 0:
        print("Final errors by keys:")
        for letter in errors_on_keys.keys():
            ans += errors_on_keys[letter]
        print(f"Total number of errors is {ans}")
        with open("output.txt", 'a') as the_output:
            the_output.write("Final errors by keys:\n")
            the_output.write(f"Total number of errors is {ans}\n")
        for letter in errors_on_keys.keys():
            with open("output.txt", 'a') as the_output:
                the_output.write(f"Key: '{letter}', number of errors: {errors_on_keys[letter]}\n")
                print(f"Key: '{letter}', number of errors: {errors_on_keys[letter]}")

    else:
        print("You have no errors!!")

