import tkinter
import time


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
RECTANGLE_WIDTH = 60
RECTANGLE_HEIGHT = 60
MOVE_SPEED = 20



def make_canvas(width, height, title=None):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    objects = {}
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    canvas.xview_scroll(8, 'units')  # add this so (0, 0) works correctly
    canvas.yview_scroll(8, 'units')  # otherwise it's clipped off

    return canvas


def move_across_column(letter_coordinates, canvas, rectangle1, rectangle2, move_y_speed):
    variable_move_y_speed = move_y_speed
    if variable_move_y_speed < 0:
        variable_move_y_speed *= -1
    length_to_move = CANVAS_HEIGHT - RECTANGLE_HEIGHT
    for i in range(int(length_to_move / variable_move_y_speed)):
        canvas.move(rectangle1, 0, move_y_speed)
        canvas.move(rectangle2, 0, move_y_speed * -1)
        canvas.update()
        time.sleep(1/60)
        rectangle1_x1 = int(get_object_coordinates(canvas, rectangle1)[0])
        rectangle1_y1 = int(get_object_coordinates(canvas, rectangle1)[1])
        rectangle2_x1 = int(get_object_coordinates(canvas, rectangle2)[0])
        rectangle2_y1 = int(get_object_coordinates(canvas, rectangle2)[1])
        dict_of_letters_with_coords = letter_coordinates

        for letter in dict_of_letters_with_coords:
            if rectangle_crosses_with_letter(int(dict_of_letters_with_coords[letter][0]),
                                             int(dict_of_letters_with_coords[letter][1]), rectangle1_x1, rectangle1_y1):
                reveal_text(canvas, letter[0], int(dict_of_letters_with_coords[letter][0]),
                            int(dict_of_letters_with_coords[letter][1]))
            if rectangle_crosses_with_letter(int(dict_of_letters_with_coords[letter][0]),
                                             int(dict_of_letters_with_coords[letter][1]), rectangle2_x1, rectangle2_y1):
                reveal_text(canvas, letter[0], int(dict_of_letters_with_coords[letter][0]),
                            int(dict_of_letters_with_coords[letter][1]))


def move_to_next_row(canvas, rectangle1, rectangle2, move_x_speed):
    variable_move_x_speed = move_x_speed
    if variable_move_x_speed < 0:
        variable_move_x_speed *= -1
    length_to_move = RECTANGLE_WIDTH
    for i in range(int(length_to_move / variable_move_x_speed)):
        canvas.move(rectangle1, move_x_speed, 0)
        canvas.move(rectangle2, move_x_speed * -1, 0)
        canvas.update()
        time.sleep(1/60)

def read_in_files(filename):
    file = open(filename)
    return file

def print_message_onto_canvas(file, canvas):
    text_width = 25
    text_height = 100
    dict_of_letter_coordinates = {}
    char_num = 0

    for line in file:
        line = line.strip()
        for i in range(len(line)):
            letter_before = line[i-1]
            letter = line[i]
            if (letter_before == 'i' and letter == 'n') or (letter_before == 't' and letter == 'e')\
                    or (letter_before == 'f' and letter == 'o'):
                text_width -= 22
            if letter_before == 'T' and letter == 'h':
                text_width += 8
            text = canvas.create_text(text_width, text_height, anchor='w', font='Arial 80', text=letter, fill='white')
            text_coordinate = get_object_coordinates(canvas, text)
            dict_of_letter_coordinates[letter + str(char_num)] = text_coordinate
            text_width += 50
            char_num += 1
        text_height += 200
    return dict_of_letter_coordinates


def create_rectangle(canvas, x1, y1, x2, y2, fill_color):
    rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
    return rectangle


def get_object_coordinates(canvas, drawn_object):
    return canvas.coords(drawn_object)


def move_rectangles_across_canvas(canvas, letter_coordinates, rectangle1, rectangle2):
    variable_move_speed = MOVE_SPEED
    stable_move_speed = MOVE_SPEED
    for i in range(int(CANVAS_WIDTH / (2 * RECTANGLE_WIDTH)) - 1):
        move_across_column(letter_coordinates, canvas, rectangle1, rectangle2, variable_move_speed)
        move_to_next_row(canvas, rectangle1, rectangle2, stable_move_speed)
        variable_move_speed *= -1
    move_across_column(letter_coordinates, canvas, rectangle1, rectangle2, variable_move_speed)
    canvas.delete(rectangle1)
    canvas.delete(rectangle2)


def reveal_text(canvas, letter, letter_x, letter_y):
    canvas.create_text(letter_x, letter_y, anchor='w', font='Arial 80', text=letter, fill='blue')


def rectangle_crosses_with_letter(letter_x1, letter_y1, rectangle_x1, rectangle_y1):
    return ((letter_x1 <= (rectangle_x1 + 30)) and (letter_x1 >= (rectangle_x1 - 30))) and \
           ((letter_y1 <= (rectangle_y1 + 30)) and (letter_y1 >= (rectangle_y1 - 30)))



def main():
    file = read_in_files('thank_you_message.txt')
    file_list = []
    for line in file:
        line = line.strip()
        file_list.append(line)

    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Canvas')
    canvas_cover = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill='white', outline='white')
    letter_coordinates = print_message_onto_canvas(file_list, canvas)
    rectangle1 = create_rectangle(canvas, 0, 0, RECTANGLE_WIDTH, RECTANGLE_HEIGHT, 'red')
    rectangle2 = create_rectangle(canvas, CANVAS_WIDTH - RECTANGLE_WIDTH, CANVAS_HEIGHT - RECTANGLE_HEIGHT,
                                         CANVAS_WIDTH, CANVAS_HEIGHT, 'red')
    move_rectangles_across_canvas(canvas, letter_coordinates, rectangle1, rectangle2)
    canvas.mainloop()






if __name__ == '__main__':
    main()