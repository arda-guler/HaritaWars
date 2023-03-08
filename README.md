# HaritaWars
Mini strategy game to pit AI's against each other.

## Quickstart

### Playing a game
To start a game, simply run 'game.py'. It will ask you to specify a map file name from maps/ folder - you can leave it blank to start a random one.

A visualizer window will appear, with colorful regions placed around the map. Since the game is completely AI-driven, you don't have much to do. 
Simply press the Enter key to start the game. Press S to pause it at any time.

![war](https://user-images.githubusercontent.com/80536083/132990595-80bd9db1-cf51-4cb6-98f1-0f167b27b345.PNG)

As countries attack each other, you will see arrows indicating the attacks performed that turn. Successful defenses are marked with squares around
regions, while successful attacks are marked with crosses. (Sometimes you can see both on one region if both cases happened within the same turn.) As territories change
hands, regions' colors will change to represent the region's current owner.

As the game progresses, you will see all the performed actions printed in a separate console/terminal window.

Countries will capitulate when they have no territories left, and the game will continue until just one country remains.

### Creating maps with Map Builder
Easiest way to create your own maps is to use the map builder tool, 'map_builder.py'. Just run the script to get started.

#### Choosing map background
The moment you run 'map_builder.py', you will be asked to provide a background file. You can write the path to one of the images in the 'maps' folder.

#### Creating countries
After the map background is chosen, the console window will then ask you to enter the names, colors and the AIs for the countries you will have in your map. 
Just enter the values one by one as the script asks for them.
(For the name, you can use pretty much any string you want.
For colors, you can enter anything that tkinter recognizes.
For the AIs, enter the name of one of the AI modules in the 'AI_modules' folder.)

![roses_violets](https://user-images.githubusercontent.com/80536083/132990484-d07e1107-f546-4456-b830-f48b4a1752dc.PNG)


#### Creating regions
After you are done creating countries, a map window will appear. On the left hand menu, you can choose which operation to perform using mouse click. You will want
to create your regions now, so leave it in 'Create Regions'.

Below the map, you will see three input fields. Enter a unique region name (a string), a region development (an integer, representing the region's starting power), 
and a region owner (one of the countries' name.) 
After all three fields are filled, left click on the map to place the region.

![mapview](https://user-images.githubusercontent.com/80536083/132990487-5088081e-f723-477f-8a64-8ac7c332324d.PNG)

If you make a mistake, choose 'Delete Regions' from the left hand menu and click on the region you just created to remove it.

#### Setting neighbour regions
Next, you need to set some regions as neighbours. An attack can only be performed between neighboring regions, so this is important.

To start, select 'Set Neighbour' on the left hand menu. After that, click on one of the regions on the map. The region's color will turn orange, indicating that
it will be paired with the next region you click on. Now, click on another region. A black line will be drawn between the two regions you clicked on, showing
that those regions are neighbours.

![neighbour](https://user-images.githubusercontent.com/80536083/132990544-82e35721-bc0d-4fd7-ba76-c37de63df16b.gif)

#### Exporting your map
Write a file name to the input field on the left side of the map view, and then click Export. Your map file will appear next to the map_builder.py script.
You can now load that file into game.py and test it out!

### Writing your own AI
To create your own AI module, create a new script in 'AI_modules' folder.

AI.py acts the "interface" between the main game script and AI modules. Every game turn, it will provide your AI module with three things - 
the country object, the number of attacks the country can perform, and the number of power points it can place.

You need to start off by creating a function called 'make_decisions()', because that is the function AI.py will look for. Any other functions or modules you want to call
can be called from there. In return, your AI must provide three things every turn: an attack and a list of point placements. The format is as follows:

    def make_decisions(country, number_of_attacks, number_of_points):
        # do your AI stuff
        return [[attack_origin, attack_target], point_placement_list]
    
In the above statement, attack_origin and attack_target are 'region' objects, whereas point_placement_list is a list of region objects. (If you want to place more than one 
point to a region, it must be present in the list multiple times.)

If you find these formats counter-intuitive, feel free to edit AI.py and/or game.py according to your likings. (FOSS FTW!)

Now, you can set one of the countries to use your AI in the game and see how it performs!
