class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
    checker = True
    ansstring = ""
    some_string = ''
    k = 0
    was_end_of_string = False
    was_first_letter = True
    index = 0
    step_number = 0
    number_of_errors = 0

    def update_curses(self, cursor):
        match self.k:
            case curses.KEY_DOWN:
               cursor.y = cursor.y + 1
            case curses.KEY_UP:
                cursor.y = cursor.y - 1
            case curses.KEY_RIGHT:
                cursor.x = cursor.x + 1
            case curses.KEY_LEFT:
                cursor.x = cursor.x - 1

    def get_finished(self, lines, index_of_lines, starting_time, start_y, width, stdscr):
        mid_ans_string = f"Final speed = {len(lines[index_of_lines]) / (time.time() - starting_time)}"
        self.ansstring = "Press [space] or [enter] to continue, other key to Exit"
        mid_ans_string_v2 = f"Level {index_of_lines + 1} completed"
        keystr = mid_ans_string_v2
        stdscr.addstr(start_y + 6, int((width// 2) - len(mid_ans_string) // 2 - len(mid_ans_string) % 2), mid_ans_string)
        stdscr.addstr(start_y + 7, int((width// 2) - len(self.ansstring) // 2 - len(self.ansstring) % 2), self.ansstring)
        return keystr
    
    def rendering_text(self, width, height):
        whstr = f"Width: {width}, Height: {height}"
        self.stdscr.addstr(0, 0, whstr, curses.color_pair(1))

    def render_status_bar(self, height, statusbarstr, width):
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(height-1, 0, statusbarstr)
        self.stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        self.stdscr.attroff(curses.color_pair(3))

    def get_the_title(self, start_y, start_x_title, title):
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.attron(curses.A_BOLD)
        self.stdscr.addstr(start_y, start_x_title, title)
        self.stdscr.attroff(curses.color_pair(2))
        self.stdscr.attroff(curses.A_BOLD)

    def get_the_rest(self, start_y, start_x_subtitle, subtitle, insert_window_x, start_x_keystr, keystr, cursor):
        self.stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        self.stdscr.addstr(start_y + 3, insert_window_x, self.some_string)
        self.stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        self.stdscr.move(cursor.y, cursor.x)
