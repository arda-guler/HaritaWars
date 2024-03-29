from tkinter import *
from PIL import Image,ImageTk
import keyboard
import os
import time
import importlib

from territory import *
from AI import *

countries = []
regions = []
globe = None
turn = 0
country_text_y_start = 50
last_turn_buffer = []

def find_country_by_name(name):
    global countries

    result = None

    for country in countries:
        if country.get_name() == name:
            result = country
            break

    return result

def find_region_by_name(name):
    global regions

    result = None

    for region in regions:
        if region.get_name() == name:
            result = region
            break

    return result

def import_map():

    global countries, regions, globe

    map_filename = input("Map filename: maps/")
    verbose = input("Console output? (y/N):")
    slow = input("Slow the game down (for human supervision)? (y/N):")

    print("\nPress Enter to resume and S to stop the game.")

    if not map_filename:
        # no map name provided, so choose randomly
        maps_list = os.listdir("maps/")
    
        for file in maps_list:
            if not file[-4:] == ".map":
                maps_list.remove(file)
                
        map_filename = "maps/" + random.choice(maps_list)

    else:
        map_filename = "maps/" + map_filename
        
    map_file = open(map_filename, "r")
    map_lines = map_file.readlines()

    for line in map_lines:
        line = line[:-1]
        line = line.split("|")

        if line[0] == "C":
            if len(line) == 4:
                new_country = country(line[1], line[2], line[3])
            elif len(line) == 3:
                new_country = country(line[1], line[2])
            else:
                try:
                    print("Wrong number of arguments to create country: ", line[1])
                except:
                    print("Wrong number of arguments to create new country.")
                    break
            countries.append(new_country)

        elif line[0] == "R":
            new_region = region(line[1], find_country_by_name(line[2]), int(line[3]), [int(line[4]), int(line[5])])
            regions.append(new_region)

        elif line[0] == "N":
            neighbours_list = []
            line[2] = line[2].split(", ")
            for element in line[2]:
                neighbours_list.append(find_region_by_name(element))
            find_region_by_name(line[1]).set_neighbours(neighbours_list)

        elif line[0] == "M":
            map_bg_filename = line[1]

    globe = game_map(regions)

    for c in countries:
        for r in globe.get_regions():
            if r.get_owner() == c:
                c.add_region(r)

    map_bg_filename = "maps/" + map_bg_filename
    
    size_x = Image.open(map_bg_filename).size[0]
    size_y = Image.open(map_bg_filename).size[1]

    win = Tk()
    win.geometry(str(size_x + 150) + "x" + str(size_y + 50))
    win.title("HaritaWars")

    canvas = Canvas(win, width=size_x, height=size_y)
    canvas.pack()

    img = ImageTk.PhotoImage(Image.open(map_bg_filename))

    return canvas, img, win, size_x, size_y, verbose, slow

def main():

    global countries, regions, globe, turn, last_turn_buffer
    
    canvas, img, win, size_x, size_y, verbose, slow = import_map()

    if verbose and verbose.lower() == "y":
        verbose = True
    else:
        verbose = False

    if slow and slow.lower() == "y":
        slow = True
    else:
        slow = False

    running = False
    while len(countries) > 1:

        canvas.delete("all")
        canvas.create_image(10, 10, anchor=NW, image=img)

        for r in globe.get_regions():
            canvas.create_oval(r.get_pos()[0]-5, r.get_pos()[1]-5, r.get_pos()[0]+5, r.get_pos()[1]+5, fill=r.get_owner().get_color())
            canvas.create_text(r.get_pos()[0]+15, r.get_pos()[1]-5, text=r.get_power(), fill="black", font=("Times New Roman", 12))
            canvas.create_text(r.get_pos()[0]+5, r.get_pos()[1]+20, text=r.get_name(), fill=r.get_owner().get_color(), font=("Times New Roman", 10))

        turn_number_text = "Turn: " + str(turn)
        canvas.create_text(size_x * 0.5, 25, text=turn_number_text, fill="black", font=("Times New Roman", 16))

        country_text_y = country_text_y_start
        for country in countries:
            canvas.create_text(size_x * 0.5, country_text_y, text=country.get_name() + " (" + country.get_AI() + ")" + " T: " +
                               str(country.get_number_of_regions()) + " P: " + str(country.get_power()),
                               fill=country.get_color(), font=("Times New Roman", 12))
            country_text_y += 15

        for i in last_turn_buffer:
            element = i[0]
            country = i[1]
            success = i[2]
            target_country_color = i[3]
            canvas.create_line(element[0][0].get_pos()[0], element[0][0].get_pos()[1],
                               element[0][1].get_pos()[0], element[0][1].get_pos()[1],
                               arrow=LAST, fill=country.get_color())

            if i[2]:
                canvas.create_line(element[0][1].get_pos()[0]+15, element[0][1].get_pos()[1]+15,
                                   element[0][1].get_pos()[0]-15, element[0][1].get_pos()[1]-15,
                                   fill=country.get_color())
                
                canvas.create_line(element[0][1].get_pos()[0]-15, element[0][1].get_pos()[1]+15,
                                   element[0][1].get_pos()[0]+15, element[0][1].get_pos()[1]-15,
                                   fill=country.get_color())

            else:
                canvas.create_line(element[0][1].get_pos()[0]+15, element[0][1].get_pos()[1]+15,
                                   element[0][1].get_pos()[0]+15, element[0][1].get_pos()[1]-15,
                                   fill=target_country_color)
                
                canvas.create_line(element[0][1].get_pos()[0]-15, element[0][1].get_pos()[1]-15,
                                   element[0][1].get_pos()[0]+15, element[0][1].get_pos()[1]-15,
                                   fill=target_country_color)

                canvas.create_line(element[0][1].get_pos()[0]-15, element[0][1].get_pos()[1]-15,
                                   element[0][1].get_pos()[0]-15, element[0][1].get_pos()[1]+15,
                                   fill=target_country_color)

                canvas.create_line(element[0][1].get_pos()[0]-15, element[0][1].get_pos()[1]+15,
                                   element[0][1].get_pos()[0]+15, element[0][1].get_pos()[1]+15,
                                   fill=target_country_color)

        if keyboard.is_pressed("Enter"):
            running = True
        elif keyboard.is_pressed("S"):
            running = False
            
        if running:
            turn += 1
            last_turn_buffer = []

            if verbose:
                print("******************")
                print("Turn: " + str(turn))
                
            for country in countries:
                if not country.has_regions():
                    countries.remove(country)
                    del country
                else:
                    AI_orders = get_AI_commands(country)
                    target_country_color = AI_orders[0][1].get_owner().get_color()
                    attack_success = country.attack(AI_orders[0][0], AI_orders[0][1])

                    for placement in AI_orders[1]:
                        country.place_point(placement)

                    canvas.create_line(AI_orders[0][0].get_pos()[0], AI_orders[0][0].get_pos()[1],
                                       AI_orders[0][1].get_pos()[0], AI_orders[0][1].get_pos()[1],
                                       arrow=LAST, fill=country.get_color())

                    if attack_success:
                        canvas.create_line(AI_orders[0][1].get_pos()[0]+15, AI_orders[0][1].get_pos()[1]+15,
                                           AI_orders[0][1].get_pos()[0]-15, AI_orders[0][1].get_pos()[1]-15,
                                           fill=country.get_color())
                        
                        canvas.create_line(AI_orders[0][1].get_pos()[0]-15, AI_orders[0][1].get_pos()[1]+15,
                                           AI_orders[0][1].get_pos()[0]+15, AI_orders[0][1].get_pos()[1]-15,
                                           fill=country.get_color())
                    else:
                        canvas.create_line(AI_orders[0][1].get_pos()[0]+15, AI_orders[0][1].get_pos()[1]+15,
                                           AI_orders[0][1].get_pos()[0]+15, AI_orders[0][1].get_pos()[1]-15,
                                           fill=country.get_color())
                        
                        canvas.create_line(AI_orders[0][1].get_pos()[0]-15, AI_orders[0][1].get_pos()[1]-15,
                                           AI_orders[0][1].get_pos()[0]+15, AI_orders[0][1].get_pos()[1]-15,
                                           fill=country.get_color())

                        canvas.create_line(AI_orders[0][1].get_pos()[0]-15, AI_orders[0][1].get_pos()[1]-15,
                                           AI_orders[0][1].get_pos()[0]-15, AI_orders[0][1].get_pos()[1]+15,
                                           fill=country.get_color())

                        canvas.create_line(AI_orders[0][1].get_pos()[0]-15, AI_orders[0][1].get_pos()[1]+15,
                                           AI_orders[0][1].get_pos()[0]+15, AI_orders[0][1].get_pos()[1]+15,
                                           fill=country.get_color())

                    last_turn_buffer.append([AI_orders, country, attack_success, target_country_color])

                    if verbose:
                        print(country.get_name())
                        if attack_success:
                            print(AI_orders[0][0].get_name() + " ---> " + AI_orders[0][1].get_name() + "(SUCCESS)")
                        else:
                            print(AI_orders[0][0].get_name() + " ---> " + AI_orders[0][1].get_name() + "(FAILURE)")

                        for placement in AI_orders[1]:
                            print("+1", placement.get_name())

                        print("\n")

        win.update()

        if slow:
            time.sleep(0.05)

    canvas.create_image(10, 10, anchor=NW, image=img)
    canvas.create_text(size_x * 0.5, 25, text=turn_number_text, fill="black", font=("Times New Roman", 16))
        
    for r in globe.get_regions():
        canvas.create_oval(r.get_pos()[0], r.get_pos()[1], r.get_pos()[0] + 10, r.get_pos()[1] + 10, fill=r.get_owner().get_color())
        canvas.create_text(r.get_pos()[0]-5, r.get_pos()[1]-5, text=r.get_power(), fill="black")
        canvas.create_text(r.get_pos()[0]+5, r.get_pos()[1]+20, text=r.get_name(), fill=r.get_owner().get_color())

    canvas.create_text(size_x * 0.5, country_text_y_start, text=countries[0].get_name() + " T: " + str(countries[0].get_number_of_regions()) + " P: " + str(countries[0].get_power()),
                       fill=countries[0].get_color(), font=("Times New Roman", 12))

    print("Winner is: " + countries[0].get_name())

    win.mainloop()
    
main()
