from tkinter import *
from PIL import Image, ImageTk

from territory import *

countries = []
regions = []
globe = game_map([])
neighbour_buffer = []
country_text_y_start = 50

def left_clicked_on_canvas(event):
    global click_op
    
    x = event.x
    y = event.y

    if click_op.get() == "cr":
        create_region(x, y)
    elif click_op.get() == "dr":
        delete_region(x, y)
    elif click_op.get() == "sn":
        set_neighbour(x, y, "l")

def right_clicked_on_canvas(event):
    global click_op
    
    x = event.x
    y = event.y

    if click_op.get() == "sn":
        set_neighbour(x, y, "r")

def find_region_by_name(name):
    global regions

    result = None

    for r in regions:
        if r.get_name() == name:
            result = r
            break

    return result

def find_country_by_name(name):
    global countries

    result = None

    for c in countries:
        if c.get_name() == name:
            result = c
            break

    return result

def create_region(x, y):
    global regions, globe

    if not find_country_by_name(owner_input.get("1.0","end-1c")):
        print("Owner doesn't exist!")
        return
    
    if not find_region_by_name(name_input.get("1.0","end-1c")):
        new_region = region(name_input.get("1.0","end-1c"), find_country_by_name(owner_input.get("1.0","end-1c")), int(dev_input.get("1.0","end-1c")), [x, y])
        regions.append(new_region)
        find_country_by_name(owner_input.get("1.0","end-1c")).add_region(new_region)
        globe.add_region(new_region)
    else:
        print("Regions must have unique names!")

def get_dist_between(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def get_closest_region_to_coords(x, y):
    global regions
    
    result = None
    
    for r in regions:
        if not result or get_dist_between([x, y], r.get_pos()) < get_dist_between([x, y], result.get_pos()):
            result = r

    return result

def delete_region(x, y):
    global regions, globe

    if get_closest_region_to_coords(x, y):
        
        region_tbd = get_closest_region_to_coords(x, y)
        c = region_tbd.get_owner()

        c.remove_region(region_tbd)
        globe.remove_region(region_tbd)
        regions.remove(region_tbd)
        del region_tbd
    else:
        print("No region found.")

def set_neighbour(x, y, click):
    global neighbour_buffer

    if click == "r":
        neighbour_buffer = []

    elif click == "l":
        neighbour_buffer.append(get_closest_region_to_coords(x, y))

        if len(neighbour_buffer) == 2:
            neighbour_buffer[0].add_neighbour(neighbour_buffer[1])
            neighbour_buffer[1].add_neighbour(neighbour_buffer[0])

            neighbour_buffer = []

def export():
    export_filename = export_filename_field.get("1.0","end-1c")
    if not export_filename[-4:] == ".map" or not export_filename[-4:] == ".txt":
        export_filename = export_filename + ".map"

    export_file = open(export_filename, "w")

    export_file.write("M|" + map_background_filename + "\n")

    for c in countries:
        export_file.write("C|" + c.get_name() + "|" + c.get_color() + "|" + c.get_AI() + "\n")

    for r in regions:
        export_file.write("R|" + r.get_name() + "|" + r.get_owner().get_name() + "|" +
                          str(r.get_development()) + "|" + str(r.get_pos()[0]) + "|" + str(r.get_pos()[1]) + "\n")

    for r in regions:
        export_file.write("N|" + r.get_name() + "|")
        for i in range(len(r.get_neighbours())):
            if i+1 < len(r.get_neighbours()):
                export_file.write(r.get_neighbours()[i].get_name() + ", ")
            else:
                export_file.write(r.get_neighbours()[i].get_name() + "\n")

## INIT BULDER
map_background_filename = input("Map background image file: ")
map_background = Image.open(map_background_filename)

size_x = map_background.size[0]
size_y = map_background.size[1]

win = Tk()
win.geometry(str(size_x + 150) + "x" + str(size_y + 50))
win.title("HaritaWars Builder")

canvas = Canvas(win, width=size_x, height=size_y)
canvas.grid(row=0, column=1, rowspan=10, columnspan=15)

img = ImageTk.PhotoImage(Image.open(map_background_filename))

## INIT UI
click_op = StringVar(win, "cr")
click_op_cr = Radiobutton(win, text="Create Region", value="cr", var=click_op)
click_op_dr = Radiobutton(win, text="Delete Region", value="dr", var=click_op)
click_op_sn = Radiobutton(win, text="Set Neighbour", value="sn", var=click_op)

click_op_label = Label(win, text="Mouse Click Operation")

click_op_label.grid(row=0, column=0)
click_op_cr.grid(row=1, column=0)
click_op_dr.grid(row=2, column=0)
click_op_sn.grid(row=3, column=0)

name_input_label = Label(win, text="Region Name")
name_input_label.grid(row=11, column=1)
name_input = Text(win, height=1, width=20)
name_input.grid(row=12, column=1)

dev_input_label = Label(win, text="Region Development")
dev_input_label.grid(row=11, column=2)
dev_input = Text(win, height=1, width=20)
dev_input.grid(row=12, column=2)

owner_input_label = Label(win, text="Region Owner")
owner_input_label.grid(row=11, column=3)
owner_input = Text(win, height=1, width=20)
owner_input.grid(row=12, column=3)

export_filename_field = Text(win, height=1, width=20)
export_filename_field.grid(row=5, column=0)
export_button = Button(win, text="Export", command=export)
export_button.grid(row=6, column=0)

canvas.bind('<Button-1>', left_clicked_on_canvas)
canvas.bind('<Button-3>', right_clicked_on_canvas)

def main():

    # Create countries
    while True:
        new_country_name = input("Enter name for new country (or leave blank to finish creating countries): ")
        
        if not new_country_name:
            break
        
        else:
            new_country_color = input("Enter color for " + new_country_name + ": ")
            new_country_AI = input("Enter AI for " + new_country_name + " (or leave blank to use default_AI): ")

            new_country = country(new_country_name, new_country_color, new_country_AI)
            countries.append(new_country)

    # Display things on map
    while True:
        canvas.create_image(10, 10, anchor=NW, image=img)

        if len(regions):
            for r in regions:
                canvas.create_oval(r.get_pos()[0]-5, r.get_pos()[1]-5, r.get_pos()[0]+5, r.get_pos()[1]+5, fill=r.get_owner().get_color())
                canvas.create_text(r.get_pos()[0]+15, r.get_pos()[1]-5, text=r.get_power(), fill="black", font=("Times New Roman", 12))
                canvas.create_text(r.get_pos()[0]+5, r.get_pos()[1]+20, text=r.get_name(), fill=r.get_owner().get_color(), font=("Times New Roman", 10))

                for n in r.get_neighbours():
                    canvas.create_line(r.get_pos()[0], r.get_pos()[1], n.get_pos()[0], n.get_pos()[1], fill="black")

            for r in neighbour_buffer:
                canvas.create_oval(r.get_pos()[0]-5, r.get_pos()[1]-5, r.get_pos()[0]+5, r.get_pos()[1]+5, fill="orange")

        country_text_y = country_text_y_start
        for cnt in countries:
            canvas.create_text(int(size_x/2), country_text_y, text=cnt.get_name() + " T: " + str(cnt.get_number_of_regions()) + " P: " + str(cnt.get_power()),
                               fill=cnt.get_color(), font=("Times New Roman", 12))
            country_text_y += 15

        win.update()
        canvas.delete("all")
    
    win.mainloop()

main()
