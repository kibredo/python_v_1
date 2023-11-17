import sys,os
import curses
import random
import time
import os
from typing import Counter
#file_of_strings = open('strings.txt', 'r')
#lines = file_of_strings.read().splitlines()
#random.shuffle(lines)
the_test_map = dict()
the_output = open("output.txt", 'w')
another_test_map = dict()
errors_on_keys = dict()
extra_error_dict = dict()
def draw_menu(stdscr, index_of_lines, lines, breakpointer):
    checker = True
    ansstring = ""
    some_string = ''
    starting_time = time.time()
    k = 0
    cursor_x = 0
    cursor_y = 0
    was_end_of_string = False
    was_first_letter = True
    index = 0
    step_number = 0
    number_of_errors = 0
    stdscr.clear()
    stdscr.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    while (checker):
        step_number += 1
        if was_first_letter:
            starting_time = time.time()
            was_first_letter = False
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)
        if k != 0:
            if chr(k) == lines[index_of_lines][index]:
                some_string += chr(k)
                index += 1
                if index == len(lines[index_of_lines]):
                    checker = False
                    was_end_of_string = True
            else:
                the_test_map["322"] += 1
                number_of_errors += 1
                the_char = chr(k)
                if the_char in extra_error_dict.keys():
                    errors_on_keys[the_char] += 1
                else:
                    errors_on_keys[the_char] = 1
                    extra_error_dict[the_char] = 1
        keystr = "Current Speed = {}".format(index / (time.time() - starting_time))
        # Declaration of strings
        title = "TYPE THIS"[:width-1]
        subtitle = lines[index_of_lines]
        statusbarstr = "Number of Errors is {}".format(number_of_errors)
        if k == 0:
            keystr = "No key press detected..."[:width-1]
        if was_end_of_string:
            #keystr = "Final speed = {}".format(len(lines[index_of_lines]) / (time.time() - starting_time))
            mid_ans_string = "Final speed = {}".format(len(lines[index_of_lines]) / (time.time() - starting_time))
            ansstring = "Press [space] or [enter] to continue, other key to Exit"
            mid_ans_string_v2 = "Level {} completed".format(index_of_lines + 1)
            keystr = mid_ans_string_v2
            stdscr.addstr(start_y + 6, int((width// 2) - len(mid_ans_string) // 2 - len(mid_ans_string) % 2), mid_ans_string)
            #stdscr.addstr(start_y + 6, int((width// 2) - len(mid_ans_string) // 2 - len(mid_ans_string) % 2), mid_ans_string)
            stdscr.addstr(start_y + 7, int((width// 2) - len(ansstring) // 2 - len(ansstring) % 2), ansstring)
        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)
        insert_window_x = int((width// 2) - len(lines[index_of_lines]) // 2 - len(lines[index_of_lines]) % 2)
        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        #stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        #stdscr.addstr(start_y + 3, (width // 2) - 2, some_string)
        stdscr.addstr(start_y + 3, insert_window_x, some_string)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        #stdscr.addstr(start_y + 9, start_x_keystr, "2316")
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()
        
        # Wait for next input
        k = stdscr.getch()
    #record_file.write(number_of_errors)
    #record_file.write(len(lines[index_of_lines]) / (time.time() - starting_time))
    the_test_map[index_of_lines] = "Number of errors: {}".format(number_of_errors)
    another_test_map[index_of_lines] = "Avarage speed: {}".format(len(lines[index_of_lines]) / (time.time() - starting_time))
    if index_of_lines < len(lines) - 1:
        if k == 10 or k == 32:
            return True
        return False
    else:
        index_of_lines -= 1
        breakpointer = False
        return False
    

def main():
    breakpointer = True
    file_of_strings = open('strings.txt', 'r')
    script_dir = os.path.dirname(__file__)
    print("Do you want to start? yes/no")
    string_input = input()
    index_in_lines = 0
    the_test_map["322"] = 0
    if string_input == "yes":
        print("Do you want to load the file or use default tests? (load/default)")
        extra_input = input()
        if extra_input == "load":
            print("Enter the file name(from current directory):")
            extra_input = input()
            file_of_strings = open(extra_input, 'r')
    lines = file_of_strings.read().splitlines()
    random.shuffle(lines)
    while string_input != "no":
        if string_input == "yes":
            should_continue = curses.wrapper(draw_menu, index_in_lines, lines, breakpointer)
            if should_continue:
                string_input = "yes"
                index_in_lines += 1
                continue
            index_in_lines += 1
            if index_in_lines < len(lines) and breakpointer:
                print("{} levels of {} complete!".format(index_in_lines, len(lines)))
                print("Do you want to continue? (yes/no)")
                string_input = input()
            else:
                print("Congrats! You've completed all levels!")
                break
        else:
            string_input = input()
    for i in range(index_in_lines):
        print("Level {}:".format(i + 1))
        the_output.write("Level {}:".format(i + 1))
        print(the_test_map[i])
        the_output.write(the_test_map[i])
        print(another_test_map[i])
        the_output.write(another_test_map[i])
    print()
    ans = 0
    if the_test_map["322"] > 0:
        print("Final errors by keys:")
        for letter in errors_on_keys.keys():
            ans += errors_on_keys[letter]
        print("Total number of errors is {}".format(ans))
        the_output.write("Final errors by keys:\n")
        the_output.write("Total number of errors is {}\n".format(ans))
        for letter in errors_on_keys.keys():
            the_output.write("Key: '{}', number of errors: {}\n".format(letter, errors_on_keys[letter]))
            print("Key: '{}', number of errors: {}".format(letter, errors_on_keys[letter]))
    else:
        print("You have no errors!!")
    print("bye!")
if __name__ == "__main__":
    main()