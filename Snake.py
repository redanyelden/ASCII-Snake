from random import randint, choice
from os import system
import msvcrt
from time import sleep

'''
TODO:
    (1) Going Backwards (Twice) Kills
    (2) Flickering
'''

def setup_game(size):
    #whether game is over
    game_over = False
    #score
    score = 0
    #list of snake tail
    tailXYs = []
    #initial direction
    direction = ""
    #random starting positions for both snake and fruit
    snakeXY = {"x": randint(1, size["width"]-1), "y": randint(1, size["height"]-1)}
    possible_fruit_locationX = [ i for i in list(range(1, size["width"]-1)) if i not in [snakeXY["x"]] ]
    possible_fruit_locationY = [ i for i in list(range(1, size["height"]-1)) if i not in [snakeXY["y"]] ]
    fruitXY = {"x": choice(possible_fruit_locationX), "y": choice(possible_fruit_locationY)}

    return game_over, score, tailXYs, direction, snakeXY, fruitXY

def draw_game(snakeXY, fruitXY, tailXYs, size, score):
    #gathering drawing of game into a string then printing string
    to_draw = ""
    #drawing row for every column
    for i in range(size["height"]):
        for j in range(size["width"]):
            #if wall
            if i == 0 or i == size["height"]-1 or j == 0 or j == size["width"]-1:
                to_draw += "#"
            #if snake head
            elif (j, i) == (snakeXY["x"], snakeXY["y"]):
                to_draw += "O"
            #if snake tail
            elif (j, i) in tailXYs:
                to_draw += "o"
            #if fruit
            elif (j, i) == (fruitXY["x"], fruitXY["y"]):
                to_draw += "X"
            #otherwise space
            else:
                to_draw += " "
        #new lines every width
        to_draw += "\n"
    #printing game
    print(to_draw)
    #printing score
    print("Score: " + str(score))

def game_logic(direction, previous_direction, size, score, snakeXY, fruitXY, tailXYs):
    #save initial snake position
    initial_snakeXY = snakeXY.copy()

    #updating snake head position depending on user input
    print(previous_direction)
    if direction == b"w":
        if len(tailXYs) > 0:
            if previous_direction == b"s":
                snakeXY["y"] += 1
                previous_direction = b"s"
            else:
                snakeXY["y"] += -1
        else:
            snakeXY["y"] += -1
    elif direction == b"a":
        if len(tailXYs) > 0:
            if previous_direction == b"d":
                snakeXY["x"] += 1
                previous_direction = b"d"
            else:
                snakeXY["x"] += -1
        else:
            snakeXY["x"] += -1
    elif direction == b"s":
        if len(tailXYs) > 0:
            if previous_direction == b"w":
                snakeXY["y"] += -1
                previous_direction = b"w"
            else:
                snakeXY["y"] += 1
        else:
            snakeXY["y"] += 1
    elif direction == b"d":
        if len(tailXYs) > 0:
            if previous_direction == b"a":
                snakeXY["x"] += -1
                previous_direction = b"a"
            else:
                snakeXY["x"] += 1
        else:
            snakeXY["x"] += 1

    #updating position of tail
    for i in range(len(tailXYs)):
        if i == 0:
            previous_tailXY = tailXYs[i]
            tailXYs[i] = (initial_snakeXY["x"], initial_snakeXY["y"])
        else:
            current_tailXY = tailXYs[i]
            tailXYs[i] = previous_tailXY
            previous_tailXY = current_tailXY

    #checking if snake has eaten itself
    for i in range(len(tailXYs)):
        if (snakeXY["x"], snakeXY["y"]) == tailXYs[i]:
            system('cls')
            print("GAME OVER :(")
            quit()

    #wrapping around the board
    if snakeXY["x"] == 0:
        snakeXY["x"] = size["width"]-2
    elif snakeXY["x"] == size["width"]-1:
        snakeXY["x"] = 1
    elif snakeXY["y"] == 0: 
        snakeXY["y"] = size["height"]-2
    elif snakeXY["y"] == size["height"]-1:
        snakeXY["y"] = 1
    
    #when a fruit is eaten
    if snakeXY["x"] == fruitXY["x"] and snakeXY["y"] == fruitXY["y"]:
        #update score
        score += 1
        #increase length of tail
        tailXYs.append((initial_snakeXY["x"], initial_snakeXY["y"]))
        #new random position for fruit
        tailXs, tailYs = [i[0] for i in tailXYs], [i[1] for i in tailXYs]
        possible_fruit_locationX = [ i for i in list(range(1, size["width"]-1)) if i not in tailXs ]
        possible_fruit_locationY = [ i for i in list(range(1, size["height"]-1)) if i not in tailYs ]
        fruitXY["x"], fruitXY["y"] = choice(possible_fruit_locationX), choice(possible_fruit_locationY)

    return False, score, previous_direction


def main():
    #size
    size = {"width": 60, "height": 25}

    #setup
    game_over, score, tailXYs, direction, snakeXY, fruitXY = setup_game(size)
    previous_direction = ""
   
    #game_loop
    while (not game_over):
        #draw
        draw_game(snakeXY, fruitXY, tailXYs, size, score)

        #get user input
        if msvcrt.kbhit():
            previous_direction = direction
            character = msvcrt.getch()
            if character in [b"w", b"a", b"s", b"d"]:
                direction = character
        #game logic
        game_over, score, previous_direction = game_logic(direction, previous_direction, size, score, snakeXY, fruitXY, tailXYs)

        #sleep
        sleep(0.05)
        #clearing screen
        system('cls')

if __name__ == "__main__":
    main()