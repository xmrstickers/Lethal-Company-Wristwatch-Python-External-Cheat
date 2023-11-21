#Balvand
#Poop and Piss© license 2023
import pyMeow as pm
from time import sleep
from memory import * #memory.py

        #--#initialize:##
debug = False
refresh_delay = 0.5 #how many times do you want to pull the game-time from memory (in seconds) ? too low of a number can crash python :^)
screen_height = pm.get_screen_height() #these functions don't appear work (return 0 always) - might be my version of PyMeow 
screen_width = pm.get_screen_width() # ''^ 
menu_x = 150
#menu_x = (screen_width / 6) #TODO implement screen width/height based menu location
menu_y = 50
#menu_y = (screen_height / 7)
menu_width = 100
menu_height = 50
game_title = "Lethal Company"
game_process = "Lethal Company.exe"
exists = pm.process_exists(game_process) #are we running game?
if debug:
    print("screen_width = "+str(screen_width))
    print("screen_height = "+str(screen_height))
if debug:
    print("process_exists: ")
    print(exists)
if not exists:
    print("error: LC not running!")
    sys.exit()

pid = pm.get_process_id(game_process)
if debug:
    print(game_process+" PID = ")
    print(pid)
    print()
if debug:
    print("opening process...")
proc = pm.open_process(pid,game_process,False)
mod = pm.get_module(proc, "UnityPlayer.dll")["base"] 
if debug:
    print(game_process+" base address:")
    print(hex(mod))
    print()
offsets = memory(mod) #references memory.py -> initialize our offsets - we pass the function argument to functions that read/write to memory 
            #--#initialize passed, start overlay
pm.overlay_init(game_title, 60, "Lethal Company Wristwatch:")

    #--#functions#--#
    #helper function to convert in-game float-time to the human-ready x:xx:am/pm format 
def float_to_time(input_float): 
    ampm = 'AM'
    hours = 6 + int(input_float / 60)
    if hours > 12: 
        hours -= 12
        ampm = 'PM'
    minutes = int(input_float % 60)
    return "{:02d}:{:02d} {}".format(hours, minutes, ampm)
        #reads game time from memory offsets defined in memory.py
def read_time(offsets):
    global TIME
    time_base = offsets.time_address() 
    time_offset = offsets.time_offsets() 
    try:
        time_addr = pm.pointer_chain_64(proc,time_base, time_offset) #get the dynamic address using pointers (magic)
        TIME = pm.r_float(proc,time_addr)
    except Exception as e : 
        print("Caught an exception in read_time - TIME:", type(e).__name__)
        print("Sleeping for 1 second...")
        sleep(1)   
##end functions        
            #--#the main overlay loop#--#
while pm.overlay_loop():    
    pm.begin_drawing() 
    window_box = pm.gui_window_box(menu_x, menu_y, menu_width, menu_height, "Game Time:") #main GUI         
    read_time(offsets)
    pm.draw_text(float_to_time(TIME),menu_x+20, menu_y+25, 16, pm.new_color(10,10,150,222)) #TODO fix ugly constants lmao 
    if debug: #shows the raw float time if debug is true
        pm.draw_text(str(round(TIME,1)),menu_x+70, menu_y+36, 12, pm.new_color(60,0,128,222))
    pm.end_drawing()
    sleep(refresh_delay) #refresh_delay
print("closing process...")
pm.close_process(proc)
print(" ~done")
