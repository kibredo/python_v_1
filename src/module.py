import curses
import random
import time
from typing import Counter
import Menu
import Cursor
from utils import *
from utils import the_test_map


def main():
    breakpointer = True
    print("Do you want to start? yes/no")
    string_input = input()
    index_in_lines = 0
    the_test_map["322"] = 0
    lines = get_the_lines(string_input)
    print_the_progress(lines, breakpointer, string_input, index_in_lines)
    get_documented(index_in_lines)
    print()
    ans = 0
    get_all_stats(ans)
    print("bye!")