import sys
from subprocess import call

from pad4pi import rpi_gpio
import time
import RPi.GPIO as GPIO
import os
import picamera
import serial
import time
import math as m
import cv2 as cv
import numpy as np
from random import *
import scipy
from skimage.morphology import skeletonize
np.set_printoptions(threshold=np.inf)
import json









#-----------------------------------------------------------------------



#-------------------------------- var_imageprocessing


# global var for image processing
remove_number = 20      # sollte höher sein als shorten_number
shorten_number = 12
own_letter_not_search = 3
cut_join = 15             
selection_step = 20     # jeder sovielte pixel wird an den arduino geschickt


             # erster Bereich  xy       # 4 Punkte in mm für Bereich 1
top_tl = [-201000,-127000]
top_tr = [201000,-127000]
top_bl = [-201000,-10]
top_br = [201000,-10]
            # zweiter Bereich    xy     # 4 Punkte in mm für Bereich 2
bottom_tl = [-201000,10]
bottom_tr = [201000,10]
bottom_bl = [-201000,127000]
bottom_br = [201000,127000]

            # filter-parameter
w_canny_first = 14
w_canny_second = 18
w_dilation_kernel_size = 18







#-------------------------------- var_calibration




# global var for calibration
grid_xsize = 4            # 3 kästchen in eine richtung, 4 punkte in eine richtung         # grid_size muss gerade sein
grid_ysize = 4            # 3 kästchen in eine richtung, 4 punkte in eine richtung         # grid_size muss gerade sein
grid_pixelsize = 300      # abstand von punkt zu punkt in pixel für raspberry pi           # sollte gut teilbar sein mit grid_mmsize sein
grid_mmsize = 25000          # abstand von punkt zu punkt in mm für arduino                   # sollte gut teilbar sein mit grid_pixelsize

            # Bereich prozentual horizontal und vertikal anteilig in pixelkoordinatensystem, ursprung links oben xy
cal_tl = [0.15, 0.08]
cal_tr = [0.855, 0.08]
cal_bl = [0.05, 0.835]
cal_br = [0.95, 0.839]

            # filter parameter
k_blur_col = 3
k_blur_gray = 3
k_threshold = 20
k_erosion_kernel_size = 2
k_erosion_iterations = 2
k_dilation_kernel_size = 25

#-------------------------------- var_display




DISPLAY_RS = 7
DISPLAY_E  = 8
DISPLAY_DATA4 = 25 
DISPLAY_DATA5 = 24
DISPLAY_DATA6 = 23
DISPLAY_DATA7 = 18

DISPLAY_WIDTH = 16 	# Zeichen je Zeile
DISPLAY_LINE_1 = 0x80 	# Adresse der ersten Display Zeile
DISPLAY_LINE_2 = 0xC0 	# Adresse der zweiten Display Zeile
DISPLAY_CHR = True
DISPLAY_CMD = False
E_PULSE = 0.005
E_DELAY = 0.005


#-------------------------------- var_keypad


KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]]



# same as calling: factory.create_4_by_4_keypad, still we put here fyi:
ROW_PINS = [5, 13, 21, 20] # BCM numbering
COL_PINS = [16, 19, 26, 6] # BCM numbering

abc = 0
wait = 0
start = 100000000
ready = 0



#-----------------------------------------------------------------------
 
#--------------------------------- init_serial                

try:
    try:
        ser = serial.Serial("/dev/ttyACM0", 115200)
        time.sleep(2)
    except:
        ser = serial.Serial("/dev/ttyACM1", 115200)
        time.sleep(2)
except:
    pass
#--------------------------------- init_camera

try:
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.hflip = True
except:
    pass


#--------------------------------- init_display



GPIO.setmode(GPIO.BCM)

GPIO.setup(DISPLAY_E, GPIO.OUT)
GPIO.setup(DISPLAY_RS, GPIO.OUT)
GPIO.setup(DISPLAY_DATA4, GPIO.OUT)
GPIO.setup(DISPLAY_DATA5, GPIO.OUT)
GPIO.setup(DISPLAY_DATA6, GPIO.OUT)
GPIO.setup(DISPLAY_DATA7, GPIO.OUT)

#---------------------------------- init_keypad
factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)



#-----------------------------------------------------------------------






def main():
    

    initialize_global()
    
    global grid_xsize
    global grid_ysize
    global grid_mmsize
    global remove_number
    global shorten_number
    global own_letter_not_search
    global cut_join
    global selection_step
    global w_canny_first
    global w_canny_second
    global w_dilation_kernel_size
    global grid_xsize
    global grid_ysize
    global grid_pixelsize
    global grid_mmsize
    global k_threshold
    global k_erosion_kernel_size
    global k_erosion_iterations
    global k_dilation_kernel_size

    display_init() 
    lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
    lcd_string("ROOFY ist wach..")
    time.sleep(1)
    
    print("\n\n\n\nstart\n\n\n\n")



    while True:
        print("k_threshold: ", k_threshold)
        first = keypad_input("A Klb B Wb C Est")
        

        if first == "A":
            print("k_threshold: ", k_threshold)
            

            #save_settings("grid_xsize")
            #save_settings("grid_ysize")
            #save_settings("grid_mmsize")
            
            #grid_xsize = read_settings("grid_xsize")
            #grid_ysize = read_settings("grid_ysize")
            #grid_mmsize = read_settings("grid_mmsize")
 
            #grid_xsize = int(keypad_input("grid_xsize: "))
            #grid_ysize = int(keypad_input("grid_ysize: "))
            #grid_mmsize = 1000* int(keypad_input("grid_mmsize: "))
            calibration_points = calibrationpoints_arduino()
            #send(calibration_points)
            wait = keypad_input("Klbrntz zchn...")          # erst enter drücken, wenn arduino und roboter fertig mit netz zeichnen sind
            

            image = create_image()
            image = calibration_filtering(k_blur_col, k_blur_gray, k_threshold, k_erosion_kernel_size, k_erosion_iterations, k_dilation_kernel_size, image)       # black_out_calibration ist in calibration_filtering integriert
            squares = calibration_squarepoints(image)
            # https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/
            # Punkte der Kalibrierung abspeichern, evtl. noch close file nötig
            with open('squarefile.txt', 'w') as filehandle:
                json.dump(squares, filehandle)
                
            show_images_calibration()
            


        elif first == "B":

            # Punkte von voriger Kalibrierung auslesen, evtl. noch close file nötig
            # https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/
            with open('squarefile.txt', 'r') as filehandle:
                squares = json.load(filehandle)

            image = create_image()
            image_rewarped = net_transformation(squares, image)
            
            print("\n\n\n\n\nOBERE BUCHSTABENREIHE")
            # im folgenden, die berechnung der robotracks der oberen buchstabenreihe
            image_top = filtering(w_canny_first, w_canny_second, w_dilation_kernel_size, image_rewarped)
            image_top = black_out(top_tl, top_tr, top_bl, top_br, image_top)
            image_top = creating_ske(image_top)
            robotracks_top = creating_ske_lines_pixel(image_top)
            robotracks_top = creating_ske_lines_tracks(robotracks_top)
            robotracks_top = creating_robotracks_1(robotracks_top)
            robotracks_top = sorting_for_letters(robotracks_top)
            robotracks_top = letter_tuning(robotracks_top)
            robotracks_top = robotracks_sorting(robotracks_top)
            robotracks_top = selection_pixel(robotracks_top, selection_step)
            
            show_images()
            
            print("\n\n\n\n\nUNTERE BUCHSTABENREIHE")
            # im folgenden, die berechnung der robotracks der unteren buchstabenreihe
            image_bottom = filtering(w_canny_first, w_canny_second, w_dilation_kernel_size, image_rewarped)
            image_bottom = black_out(bottom_tl, bottom_tr, bottom_bl, bottom_br, image_bottom)
            image_bottom = creating_ske(image_bottom)
            robotracks_bottom = creating_ske_lines_pixel(image_bottom)
            robotracks_bottom = creating_ske_lines_tracks(robotracks_bottom)
            robotracks_bottom = creating_robotracks_1(robotracks_bottom)
            robotracks_bottom = sorting_for_letters(robotracks_bottom)
            robotracks_bottom = letter_tuning(robotracks_bottom)
            robotracks_bottom = robotracks_sorting(robotracks_bottom)
            robotracks_bottom = selection_pixel(robotracks_bottom, selection_step)
            
            show_images()
            
            #robotracks_all = robotracks_circle(robotracks_top, robotracks_bottom)           # aufgrund der unteren funktion onlytracks() ist diese zeile nicht mehr nötig
            print("davor")
            
            robotracks_all_letter = []
            print("danach")
            robotracks_all_letter = robotracks_circle_letter(robotracks_top, robotracks_bottom)
            print("3")
            robotracks_all= []
            print("4")
            robotracks_all = onlytracks(robotracks_all_letter)
            print("5")
            
            
            send(robotracks_all)
            
            
            
                                              # NACHFOLGENDE KOMMENTARE VOR ENDGÜLTIGE NUTZUNG NOCHMAL DURCHGEHEN!!!!!!!!!!!!!!!!
            while True:
                choice_correction = keypad_input("1. A -->  N_Bs:"+ str(len(robotracks_all_letter)))
                if choice_correction == "A":
                    print("\n\nganzer track nochmals senden\n")
                    send(robotracks_all)
                    continue
                #elif choice_correction == "C": 
                #    robotracks_all_letter = []                                         # alles gelöscht, evtl. dieses feature am ende rausnehmen!!!!!!!!!!!!!!!
                #    robotracks_all = onlytracks(robotracks_all_letter)
                #    send(robotracks_all)
                #    continue
                    
                try:                   # falls alle if abfragen davor scheitern, wird dieser try versucht
                    letter = robotracks_all_letter[int(choice_correction)-1]            # bei eingaben immer ab 1 und nicht ab 0 zählen, im programm wird dann umgerechnet von zählung ab 1 auf zählung ab 0
                    letter_pos = int(choice_correction)-1
                    
                    while True:
                        
                        choice_correction = keypad_input("2. A-->  N_Tr:"+ str(len(letter)))
                        
                        if choice_correction == "A":                   # letter senden
                            print("\n\nganzer letter nochmals senden\n")
                            send(letter)
                            continue
                        elif choice_correction == "B":
                            break                                      # zurück, um anderen buchstaben zu wählen
                        elif choice_correction == "C":
                            del robotracks_all_letter[letter_pos]
                            robotracks_all = onlytracks(robotracks_all_letter)
                            send(robotracks_all)
                            continue


                        try:                 # falls alle if abfragen davor scheitern, wird dieser try versucht
                            track = letter[int(choice_correction)-1]
                            track_pos = int(choice_correction) -1
                            while True:
                                choice_correction = keypad_input("3. A --> ")
                                if choice_correction == "A":           # track senden 
                                    print("\n\nganzer track nochmals senden\n")
                                    send([track])
                                    continue
                                elif choice_correction == "B":
                                    break                              # zurück, um anderen track aus dem buchstaben zu wählen
                                elif choice_correction == "C":
                                    del robotracks_all_letter[letter_pos][track_pos]             # testen ob wenn track gelöscht wird und der buchstabe nur einen track hatte, die übertragung von leeren listen auch klappt!!!!!!!
                                    robotracks_all_cleared = [let for let in robotracks_all_letter if let != []]
                                    robotracks_all = onlytracks(robotracks_all_cleared)
                                    send(robotracks_all)                            
                                else:
                                    continue
                        except:
                            continue
                                
                                
                except:
                    continue
            
            
        elif first == "C":
            
            save_settings_C("remove_number")
            remove_number = read_settings("remove_number")
            
            save_settings_C("shorten_number")
            shorten_number = read_settings("shorten_number")
            
            save_settings_C("own_letter_not_search")
            own_letter_not_search = read_settings("own_letter_not_search")
            
            save_settings_C("cut_join")
            cut_join = read_settings("cut_join")
            
            save_settings_C("selection_step")
            selection_step = read_settings("selection_step")
            
            save_settings_C("w_canny_first")
            w_canny_first = read_settings("w_canny_first")
            
            save_settings_C("w_canny_second")
            w_canny_second = read_settings("w_canny_second")
            
            save_settings_C("w_dilation_kernel_size")
            w_dilation_kernel_size = read_settings("w_dilation_kernel_size")
            
            
            save_settings_C("grid_xsize")
            grid_xsize = read_settings("grid_xsize")
            
            save_settings_C("grid_ysize")
            grid_ysize = read_settings("grid_ysize")
            
            save_settings_C("grid_pixelsize")
            grid_pixelsize = read_settings("grid_pixelsize")
            
            save_settings_C("grid_mmsize")
            grid_mmsize = read_settings("grid_mmsize")
            
            save_settings_C("k_threshold")
            k_threshold = read_settings("k_threshold")
            
            save_settings_C("k_erosion_kernel_size")
            k_erosion_kernel_size = read_settings("k_erosion_kernel_size")
            
            save_settings_C("k_erosion_iterations")
            k_erosion_iterations = read_settings("k_erosion_iterations")
            
            save_settings_C("k_dilation_kernel_size")
            k_dilation_kernel_siz = read_settings("k_dilation_kernel_size")
            
            continue
            
            
            
        
            

        
            
        
        else:
            continue


def initialize_global():
    
    global remove_number
    global shorten_number
    global own_letter_not_search
    global cut_join
    global selection_step
    global w_canny_first
    global w_canny_second
    global w_dilation_kernel_size
    global grid_xsize
    global grid_ysize
    global grid_pixelsize
    global grid_mmsize
    global k_threshold
    global k_erosion_kernel_size
    global k_erosion_iterations
    global k_dilation_kernel_size


    remove_number = read_settings("remove_number")
    shorten_number = read_settings("shorten_number")
    own_letter_not_search = read_settings("own_letter_not_search")
    cut_join = read_settings("cut_join")
    selection_step = read_settings("selection_step")
    w_canny_first = read_settings("w_canny_first")
    w_canny_second = read_settings("w_canny_second")
    w_dilation_kernel_size = read_settings("w_dilation_kernel_size")
    grid_xsize = read_settings("grid_xsize")
    grid_ysize = read_settings("grid_ysize")
    grid_pixelsize = read_settings("grid_pixelsize")
    grid_mmsize = read_settings("grid_mmsize")
    k_threshold = read_settings("k_threshold")
    k_erosion_kernel_size = read_settings("k_erosion_kernel_size")
    k_erosion_iterations = read_settings("k_erosion_iterations")
    k_dilation_kernel_size = read_settings("k_dilation_kernel_size")

        

"""

def robotracks_circle(robotracks_top, robotracks_bottom):
    
    robotracks_all = []
    
    for letter in robotracks_top:
        for track in letter:
            robotracks_all.append(track)
            
    robotracks_bottom = robotracks_bottom[::-1]             # buchstaben umdrehen
    for letter in range(len(robotracks_bottom)):
        robotracks_bottom[letter][::-1]                     # in jedem buchstaben alle tracks umdrehen
    for letter in range(len(robotracks_bottom)):
        for track in range(len(robotracks_bottom[letter])):
            robotracks_bottom[letter][track][::-1]          # in jedem buchstaben in jedem track alle punkte umdrehen
    for letter in robotracks_bottom:
        for track in letter:
            robotracks_all.append(track)
            

        
    for track in range(len(robotracks_all)):
        for pixel in range(len(robotracks_all[track])):
            robotracks_all[track][pixel] = ab_ba(robotracks_all[track][pixel])
            robotracks_all[track][pixel] = pixel_to_mm(robotracks_all[track][pixel])
        
    print("\n\n\n\n\n\n\n\n---------ROBOTRACKS_ALL--------\n\n\n\n\n\n\n\n", robotracks_all)
    
    return(robotracks_all)


"""


def robotracks_circle_letter(robotracks_top, robotracks_bottom):
    
    robotracks_all_letter = []
    

            
            
    robotracks_bottom = robotracks_bottom[::-1]             # buchstaben umdrehen
    for letter in range(len(robotracks_bottom)):
        robotracks_bottom[letter][::-1]                     # in jedem buchstaben alle tracks umdrehen
    for letter in range(len(robotracks_bottom)):
        for track in range(len(robotracks_bottom[letter])):
            robotracks_bottom[letter][track][::-1]          # in jedem buchstaben in jedem track alle punkte umdrehen
    for letter in robotracks_bottom:
        robotracks_all_letter.append(letter)
         
         
        for letter in robotracks_top:
            robotracks_all_letter.append(letter)


    for letter in range(len(robotracks_all_letter)):    
        for track in range(len(robotracks_all_letter[letter])):
            for pixel in range(len(robotracks_all_letter[letter][track])):
                robotracks_all_letter[letter][track][pixel] = ab_ba(robotracks_all_letter[letter][track][pixel])
                robotracks_all_letter[letter][track][pixel] = pixel_to_mm(robotracks_all_letter[letter][track][pixel])
        
    print("\n\n\n\n\n\n\n\n---------ROBOTRACKS_ALL_LETTER--------\n\n\n\n\n\n\n\n", robotracks_all_letter)
    
    return(robotracks_all_letter)







def onlytracks(robotracks):                   # nur für buchstaben nötig, kalibrierungspunkte schon in "onlytracks"
    robotracks_arduino = []
    print(robotracks)
    print("\n\n\n\nrobotracks: ", robotracks)
    for letter in robotracks:
        print("\n\nletter: ", letter)
        for track in letter:
            print("\ntrack: ", track)
            robotracks_arduino.append(track)
    return(robotracks_arduino)







def display_init():
	lcd_byte(0x33,DISPLAY_CMD)
	lcd_byte(0x32,DISPLAY_CMD)
	lcd_byte(0x28,DISPLAY_CMD)
	lcd_byte(0x0C,DISPLAY_CMD)  
	lcd_byte(0x06,DISPLAY_CMD)
	lcd_byte(0x01,DISPLAY_CMD)  

def lcd_string(message):
	message = message.ljust(DISPLAY_WIDTH," ")  
	for i in range(DISPLAY_WIDTH):
	  lcd_byte(ord(message[i]),DISPLAY_CHR)


def lcd_byte(bits, mode):
	GPIO.output(DISPLAY_RS, mode)
	GPIO.output(DISPLAY_DATA4, False)
	GPIO.output(DISPLAY_DATA5, False)
	GPIO.output(DISPLAY_DATA6, False)
	GPIO.output(DISPLAY_DATA7, False)
	if bits&0x10==0x10:
	  GPIO.output(DISPLAY_DATA4, True)
	if bits&0x20==0x20:
	  GPIO.output(DISPLAY_DATA5, True)
	if bits&0x40==0x40:
	  GPIO.output(DISPLAY_DATA6, True)
	if bits&0x80==0x80:
	  GPIO.output(DISPLAY_DATA7, True)
	time.sleep(E_DELAY)    
	GPIO.output(DISPLAY_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(DISPLAY_E, False)  
	time.sleep(E_DELAY)      
	GPIO.output(DISPLAY_DATA4, False)
	GPIO.output(DISPLAY_DATA5, False)
	GPIO.output(DISPLAY_DATA6, False)
	GPIO.output(DISPLAY_DATA7, False)
	if bits&0x01==0x01:
	  GPIO.output(DISPLAY_DATA4, True)
	if bits&0x02==0x02:
	  GPIO.output(DISPLAY_DATA5, True)
	if bits&0x04==0x04:
	  GPIO.output(DISPLAY_DATA6, True)
	if bits&0x08==0x08:
	  GPIO.output(DISPLAY_DATA7, True)
	time.sleep(E_DELAY)    
	GPIO.output(DISPLAY_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(DISPLAY_E, False)  
	time.sleep(E_DELAY)   

# Beispiel für Bildschirmausgabe, Nutzung der folgenden funktionen:

#lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
#lcd_string("hi")
#lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)  -> nachfolgende zeichen in zweite zeile schreiben
#lcd_string("hallo")                    -> schreibt hallo
#display_init()                         -> Display leeren

display_init()

#-----------------------------------------------------------------------



def save_settings(setting):

    filename = str("001_setting_") + str(setting) + str(".txt")
    displayname = str(setting) + str(": ")

    setting_save = int(keypad_input(displayname))
                
    with open(filename, 'w') as filehandle:
        json.dump(setting_save, filehandle)   
         
         
         
def save_settings_C(setting):
    displayname =  str(globals()[str(setting)]) + " " + str(setting)
    decis = keypad_input(displayname)
    print(decis)
    if decis ==  "1":
        decis = 0
        save_settings(setting)
    elif decis == "":
        pass
    else:
        pass
             
         
         
                

    

def read_settings(setting):
    
    filename = str("001_setting_") + str(setting) + str(".txt")
    
    with open(filename, 'r') as filehandle:
        setting_save = json.load(filehandle)

    return(setting_save)

#-----------------------------------------------------------------------



class KeyStore:

  
    def __init__(self):
        #list to store them
        self.pressed_keys =''

    #function to clear string
    def clear_keys(self):
        self.pressed_keys = self.pressed_keys.replace(self.pressed_keys,'')
        
    def delete_keys(self):
        self.pressed_keys = self.pressed_keys.replace(self.pressed_keys, self.pressed_keys[0:-1])

    def store_key(self,key):
        global wait
        global abc
        global start
        global ready
        
        stop = time.time()
        t = stop - start
        if t > 1:
            ready = 0
                
        if key=='#':
            #printing the sequence of keys.
            #print("try enter: ", self.pressed_keys)
            abc = self.pressed_keys
            wait = 1
            self.clear_keys()
            lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
            lcd_string(self.pressed_keys) 
            time.sleep(1.8)###
        
        elif ready == 1:
            if key == 'A':
                lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
                lcd_string("ROOFY traeumt")
                lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
                lcd_string("gerade...  Zzzzz")
                GPIO.cleanup()
                call("sudo shutdown -h now", shell=True)
            elif key == 'B':
                lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
                lcd_string("ROOFY braucht ei")
                lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
                lcd_string("ne kleine Pause")
                GPIO.cleanup()
                os.system("sudo reboot")
      
            elif key == 'C':
                lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
                lcd_string("Programm beendet")
                lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
                lcd_string("")
                GPIO.cleanup()
                exit()                         # im fertigen programm später diesen exit rausschmeissen
            
            elif key == 'D':
                lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
                lcd_string("Programm startet")
                lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
                lcd_string("neu")
                GPIO.cleanup()
                try:
                    camera.close()
                except:
                    pass
                os.execl(sys.executable,sys.executable, * sys.argv)
                
        elif key == 'D':
            print(self.pressed_keys)
            self.delete_keys()
            abc = self.pressed_keys
            lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
            lcd_string(self.pressed_keys) 
                    
        elif key == '*':
            ready = 1
            start = time.time()
            
            
        else:
            self.pressed_keys += key
            print(self.pressed_keys)
            lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
            lcd_string(self.pressed_keys) 
                         

keys = KeyStore()


# store_key will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(keys.store_key)


# funktion returned 
def wait4input():
    global wait
    global abc
    wait = 0
    while(True):
        if wait == 1:
            wait = 0
            return(abc)
        time.sleep(0.2)###
        continue


# in erste zeile wird string_display geschrieben, in zweite zeile des displays number_input
def keypad_input(string_display):
    display_init() 
    lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
    lcd_string(string_display)
    number_input  = wait4input()
    time.sleep(0.2)  # auf 0.2 setzen, falls es probleme gibt
    lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
    lcd_string("")
    display_init() 
    return(number_input)


#-----------------------------------------------------------------------


def create_image():

    camera.start_preview()
    time.sleep(4)
    camera.capture("0_image.jpg")
    camera.stop_preview()
    
    image = cv.imread("0_image.jpg", 0)
    
    cv.imshow("image", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return(image)




def feedback():
    print("erwarte feedback")
    start = time.time()
    while 1:
        try:
            if int(ser.readline()) == 1:
                feedback = 1
                
                print("feedback: ", feedback)
                #except ser.SerialTimeoutException:
                   # print("Data could not be read")
                print("break 1")
                break
            print("break 2")
            break
        except:
            continue
        print("break 3")
        break
        
    end = time.time()
    print("time needed to get feedback: ",end - start)
    return()



def send(robotracks):        # robotracks muss hier in mikrometer, arduinokoordinatensystem und onlytracks eingegeben werden
    
    if robotracks == []:
        print("\n\nrobotrack wird nicht an den arduino gesendet, da robotrack leer ist","\n")
        pass
        
    else:
        print("\n\nfolgender robotrack wird an den arduino gesendet: ", robotracks, "\n")
        
        for track in robotracks:
            print("will send: ", str.encode("t"))
            ser.write(str.encode("t"))
            print("finished with sending: ", str.encode("t"))
            feedback()

            for coordinate in track:

                xy = str(str(coordinate[0]) + ";" + str(coordinate[1]))
                print("will send: ", str.encode(xy))
                ser.write(str.encode(xy))
                print("finished with sending: ", str.encode(xy))
                feedback()
                
        print("will send: ", str.encode("e"))
        ser.write(str.encode("e"))
        feedback()






#-----------------------------------------------------------------------





def mm_to_pixel(mm):            # parameter: [xmm, ymm] -> return: [xpixel, ypixel]

    gain = grid_pixelsize/grid_mmsize                         # abstand von punkt zu punkt in pixel für raspberry pi

    x_shifter = (grid_xsize/2)*grid_mmsize
    y_shifter = (grid_ysize/2)*grid_mmsize

    pixel = mm

    pixel[0] = (mm[0] + x_shifter) * gain
    pixel[1] = (mm[1] + y_shifter) * gain

    return(pixel)


def pixel_to_mm(pixel):             # parameter: [xpixel, ypixel] -> return: [xmm, ymm]

    gain = grid_mmsize/grid_pixelsize                         # abstand von punkt zu punkt in pixel für raspberry pi

    x_shifter = (grid_xsize/2)*grid_pixelsize
    y_shifter = (grid_ysize/2)*grid_pixelsize

    mm = pixel

    mm[0] = int((pixel[0] - x_shifter) * gain)
    mm[1] = int((pixel[1] - y_shifter) * gain)

    return(mm)


def ab_ba(ab):     # [x,y]   ->  [y,x] oder anderst herum
    ba = [0,0]
    ba[0] = ab[1]
    ba[1] = ab[0]
    return(ba)






#-----------------------------------------------------------------------





def calibrationpoints_arduino():
    calibrationpoints = []

    y_value = -(grid_ysize / 2) * grid_mmsize
    for y in range(0, grid_ysize + 1):

        #if y % 2 == 0:                # gerade
        print(y_value)
        x_value = -(grid_xsize / 2) * grid_mmsize           # ganz links anfangen
        for x in range(0, grid_xsize + 1):
            calibrationpoints.append([[int(x_value), int(y_value)]])
            x_value = x_value + grid_mmsize                                  # es spielt keine rolle, ob letztes x_value zu groß ist, wenn damit nicht mehr gerechnet wird

#        else:                              # ungerade
#           x_value = (grid_xsize / 2) * grid_mmsize            # ganz rechts anfangen
#            for x in range(0, grid_xsize + 1):
#                calibrationpoints.append([[int(x_value), int(y_value)]])
#                x_value = x_value - grid_mmsize                                            # es spielt keine rolle ob letztes x_value zu klein ist, wenn damit nicht mehr gerechnet wird
#
        y_value = y_value + grid_mmsize                                        # es spielt keine rolle, ob letztes y_value zu groß ist, wenn damit nicht mehr gerechnet wird

    calibrationpoints = calibrationpoints[::-1]
    print(calibrationpoints)

    return(calibrationpoints)              # in xy form. auch nötig in xy, da arduino xy möchte


#def calibrationlines_arduino():  # optional
                                                                # algorithmus basierend auf calibrationpoints, welcher linien bildet, jeweils punkte in einer reihe verbindet
def calibration_filtering(blur_col, blur_gray, threshold, erosion_kernel_size, erosion_iterations, dilation_kernel_size, image):

    global calibration_color          # bild von picamera kommt hier schwarzweiß rein, funktioniert trotzdem alles
    calibration_color = image

    global calibration_blur_color
    calibration_blur_color = cv.medianBlur(calibration_color, blur_col)

    #global calibration_img
    #calibration_img = cv.cvtColor(calibration_blur_color, cv.COLOR_BGR2GRAY)

    global calibration_blur
    calibration_blur = cv.medianBlur(calibration_blur_color, blur_gray)

    global calibration_threshold
    _, calibration_threshold = cv.threshold(calibration_blur,threshold, 255, cv.THRESH_BINARY_INV)

    global calibration_cut
    calibration_cut = black_out_calibration(cal_tl, cal_tr, cal_bl, cal_br, calibration_threshold)

    #kernel_erosion = np.ones((erosion_kernel_size, erosion_kernel_size), np.uint8)                                                                                                            # opening = cv.morphologyEx(calibration_threshold, cv.MORPH_OPEN, kernel_cal, iterations=2)
    #erosion = cv.erode(calibration_cut, kernel_erosion, iterations=erosion_iterations)


    kernel_cal = np.ones((dilation_kernel_size, dilation_kernel_size), np.uint8)
    dilation = cv.dilate(calibration_cut, kernel_cal)


    return(dilation)
    
    
    
    
def black_out_calibration(tl, tr, bl, br , image):

    h, w = image.shape[:2]

    ptl = tl                            # x,y wird hier von anteilsgrößen, bsp 1/3 auf das pixelkoordinatensystem gerechnet, dazu ist die gesamtpixelhöhe und -breite notwendig
    ptl[0] = w * tl[0]
    ptl[1] = h * tl[1]

    ptr = tr
    ptr[0] = w * tr[0]
    ptr[1] = h * tr[1]

    pbl = bl
    pbl[0] = w * bl[0]
    pbl[1] = h * bl[1]

    pbr = br
    pbr[0] = w * br[0]
    pbr[1] = h * br[1]


    img_template = np.zeros((h, w, 1), np.uint8)                        # erstellung eines schwarzen bildes
    pts = np.array([ptl, ptr, pbr, pbl], np.int32)
    cv.fillPoly(img_template, [pts], 255)                               # pts in xy nötig


    img_cut = cv.bitwise_and(image, img_template)

    cv.imshow("img_cut", img_cut)
    cv.waitKey(0)
    cv.destroyAllWindows()


    return(img_cut)





def calibration_squarepoints(image):


    grid_xnpoints = grid_xsize + 1     # anzahl der knotenpunkte in x richtung
    grid_ynpoints = grid_ysize + 1     # anzahl der knotenpunkte in y richtung
                                                                                                          #calibration_ske = (skeletonize(calibration_treshold // 255) * 255).astype(np.uint8)

    im2, contours, hierarchy = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    print("len(contours) entspricht Anzahl gefundener Punkte: ", len(contours))



    calibration_points = []

    for i in range(len(contours)):


        cnt = contours[i]
        M = cv.moments(cnt)
        cy = int(M['m01'] / M['m00'])
        cx = int(M['m10'] / M['m00'])


        calibration_points.append([cx,cy])


        cv.putText(calibration_threshold, "cy: "+str(cy), (cx, cy), cv.FONT_HERSHEY_COMPLEX, 1, (10,100,40))

                                                                                        # noch etwas einbauen, was alles stoppt, falls zu wenig punkte registriert wurden (try except), ergibt sich später evtl automatisch, wenn zu wenig punkte für perspektivtransformation weitergegeben werden

                                                                                        # nachfolgende algorithmen sind so aufgebaut, dass dies auf der hier erstellten liste basieren. dazu sind die pixel sortiert. links oben: erstes. rechts unten: letztes. zeilenweise wiedergabe

    print(calibration_points)


    # es darf nur punkte im speziellem format in folgendem format eingegeben werden (zuerst x, dann y)

    centroids = np.array(calibration_points, dtype=np.float32)
    c = centroids.reshape(((grid_ynpoints*grid_xnpoints), 2))
    c2 = c[np.argsort(c[:, 1])]

    b = np.vstack([c2[i * grid_xnpoints:(i + 1) * grid_xnpoints][np.argsort(c2[i * grid_xnpoints:(i + 1) * grid_xnpoints, 0])] for i in range(grid_ynpoints)])
    gridpoints_xy = b.reshape((grid_ynpoints, grid_xnpoints, 2))



    print("gridpoints_xy: ",gridpoints_xy)


    calibration_squares = []



    for square_line in range(grid_ysize):
        for square_column in range(grid_xsize):

            calibration_squares.append([gridpoints_xy[square_line][square_column],gridpoints_xy[square_line][square_column+1],gridpoints_xy[square_line+1][square_column],gridpoints_xy[square_line+1][square_column+1]])

    calibration_squares = [[[int(square[0][0]),int(square[0][1])],[int(square[1][0])-1,int(square[1][1])],[int(square[2][0]),int(square[2][1])-1],[int(square[3][0])-1,int(square[3][1])-1]] for square in calibration_squares]
    print("calibration_squares: ", calibration_squares)
    print("calibration_squares: ", len(calibration_squares))


    global comparison_calibration
    comparison_calibration = calibration_color
    comparison_calibration = cv.cvtColor(comparison_calibration, cv.COLOR_GRAY2BGR)   # calibration_color ist nicht farbig, obwohl es so heißt, deswegen muss das bild erst farbig gemacht werden, damit farbige punkte darauf gezeichnet werden können
    for square in calibration_squares:
        color = (randint(50, 200), randint(50, 200), randint(50, 200))
        for pixel in square:
            comparison_calibration[pixel[1], pixel[0]] = (color)



    return (calibration_squares)               # müssen noch abgespeichert werden # hier in xy form    # auch nötig in xy, da perspective transformation in xy funktioniert







#-----------------------------------------------------------------------










def net_transformation(squares, picture_letters):




    print("picture_letters.shape", picture_letters.shape)
    
    cv.imshow("picture_letters", picture_letters)
    cv.waitKey(0)
    cv.destroyAllWindows()

    square_pictures = []

    for square in squares:
        pts1 = np.float32([square[0], square[1], square[2], square[3]])
        pts2 = np.float32([[0, 0], [grid_pixelsize, 0], [0, grid_pixelsize], [grid_pixelsize, grid_pixelsize]])
        matrix = cv.getPerspectiveTransform(pts1, pts2)
        square_pictures.append(cv.warpPerspective(picture_letters, matrix, (grid_pixelsize, grid_pixelsize)))
        #cv.imshow("square",cv.warpPerspective(picture_letters, matrix, (grid_pixelsize, grid_pixelsize)))
        #cv.waitKey(0)
        #cv.destroyAllWindows()


    linepictures = []
    for i in range(grid_ysize):
        linepicture = square_pictures[i*grid_xsize]                                                                                            # für die jeweilen zeilen
        for ii in range((i*grid_xsize)+1,(i+1)*grid_xsize):
            linepicture =  np.concatenate((linepicture, square_pictures[ii]), axis=1)

        linepictures.append(linepicture)

    picture_complete = linepictures[0]
    for z in range(1,len(linepictures)):
        picture_complete = np.concatenate((picture_complete, linepictures[z]), axis=0)



    print(picture_complete.shape)

    cv.imshow("picture_complete", picture_complete)
    cv.waitKey(0)
    cv.destroyAllWindows()


    return(picture_complete)


def filtering(canny_first, canny_second, dilation_kernel_size, image):


    global letter  # diese 2 zeilen müssen später im originalcode noch eleganter gelöst werden
    letter = image



    image_bilateral = cv.bilateralFilter(image, 9, 75, 75)



    global letter_canny
    letter_canny = cv.Canny(image_bilateral, canny_first, canny_second)

    #global letter_erosion_before
    #kernel = np.ones((2, 2), np.uint8)
    #letter_erosion_before = cv.erode(letter_canny, kernel, iterations=25)

    global letter_dilation
    kernel = np.ones((dilation_kernel_size, dilation_kernel_size), np.uint8)
    letter_dilation = cv.dilate(letter_canny, kernel)

    global letter_erosion_after
    kernel = np.ones((4, 4), np.uint8)
    letter_erosion_after = cv.erode(letter_dilation, kernel, iterations=1)


    image_filtered = letter_erosion_after

    return(image_filtered)


def black_out(tl, tr, bl, br , image):               # diese funktion nach rewarpen und canny verwenden

    ptl = mm_to_pixel(tl)                                   # x,y wird hier von mm in pixel umgewandelt
    ptr = mm_to_pixel(tr)
    pbl = mm_to_pixel(bl)
    pbr = mm_to_pixel(br)


    pixelheight = grid_ysize * grid_pixelsize
    pixelwidth = grid_xsize * grid_pixelsize
    img_template = np.zeros((pixelheight, pixelwidth, 1), np.uint8)              # erstellung eines schwarzen bildes
    pts = np.array([ptl, ptr, pbr, pbl], np.int32)
    cv.fillPoly(img_template, [pts], 255)                                        # pts in xy nötig


    img_cut = cv.bitwise_and(image, img_template)
    cv.imshow("img_cut", img_cut)
  
    cv.waitKey(0)
    cv.destroyAllWindows()

    return(img_cut)




def creating_ske(image):




    letter_floodfill = image.copy()
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = image.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    # Floodfill from point (0, 0)
    cv.floodFill(letter_floodfill, mask, (0, 0), 255);

    # Invert floodfilled image
    letter_floodfill_inv = cv.bitwise_not(letter_floodfill)
    # Combine the two images to get the foreground.
    fill_image = image | letter_floodfill_inv




    letter_floodfill_inv_floodfill = letter_floodfill_inv.copy()
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = letter_floodfill_inv.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    # Floodfill from point (0, 0)
    cv.floodFill(letter_floodfill_inv_floodfill, mask, (0, 0), 255);
    letter_floodfill_inv_floodfill_inv = cv.bitwise_not(letter_floodfill_inv_floodfill)




    letter_floodfill_inv_floodfill_inv_floodfill = letter_floodfill_inv_floodfill_inv.copy()
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = letter_floodfill_inv_floodfill_inv.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    # Floodfill from point (0, 0)
    cv.floodFill(letter_floodfill_inv_floodfill_inv_floodfill, mask, (0, 0), 255);
    letter_floodfill_inv_floodfill_inv_floodfill_inv = cv.bitwise_not(letter_floodfill_inv_floodfill_inv_floodfill)




    black_letter = letter_floodfill | letter_floodfill_inv_floodfill_inv_floodfill_inv
    white_letter = cv.bitwise_not(black_letter)
    ske = (skeletonize(white_letter//255) * 255).astype(np.uint8)

    global comparison_ske_letter
    comparison_ske_letter = cv.bitwise_and(letter, letter, mask=cv.bitwise_not(ske))                  # originalbild und skelett übereinander gelegt
    
    cv.imshow("comparison_ske_letter", comparison_ske_letter)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return(ske)


def creating_ske_lines_pixel(par_ske):

    height, width = par_ske.shape
    ske_lines_pixel = []

    for h in range(height):
        list = []
        for w in range(width):
            if par_ske[h, w] == 255:
                list.append([h, w])
        if len(list) > 0:
            ske_lines_pixel.append(list)

    print("\nlines: ")
    print(ske_lines_pixel)

    return(ske_lines_pixel)


def creating_ske_lines_tracks(par_ske_lines_pixel):

    ske_lines_tracks = []

    for line in par_ske_lines_pixel:
        line_tracks = []
        track = [line[0]]

        if len(line) == 1:
            line_tracks.append(track)
            ske_lines_tracks.append(line_tracks)

        else:
            for pixel in range(len(line) - 1):
                if line[pixel + 1][1] - line[pixel][1] == 1:                    #falls rechter pixel tatsächlich an vorigem anschließt....  (hier wird nur der track abgespeichert, wenn in dem track gerade mit dem letzten pixel gefüllt wurde)
                    track.append(line[pixel + 1])                               #diesen nächsten rechten pixel in vorherigen track abspeichern
                    if pixel == len(line) - 2:                                  #falls schon der letzte pixel untersucht wurde, wird der track in line_tracks abgespeichert. Dies ist nötig, da normalerweise immer nur vergangen werte abgespeichert werden. hier wird vorgegriffen.
                        line_tracks.append(track)
                    else:
                        pass

                else:                                                   #falls rechter pixel nicht an vorigem anschließt....(hier wird immer der alte track abgespeichert, neuer track wenn es der neue track mit dem letzten pixel war)
                    line_tracks.append(track)                                  #alten track in line_tracks abspeichern
                    track = []                                                  #neuen track erstellen
                    track.append(line[pixel + 1])                                    #neuer track mit nächstem pixel gefüllt
                    if pixel == len(line) - 2:
                        line_tracks.append(track)                                #falls schon der letzte pixel untersucht wurde, wird der track in line_tracks abgespeichert. Dies ist nötig, da normalerweise immer nur vergangen werte abgespeichert werden. hier wird vorgegriffen.
                    else:
                        pass

            ske_lines_tracks.append(line_tracks)

    print("\nske_lines_tracks: ")
    print(ske_lines_tracks)

    return(ske_lines_tracks)


def creating_robotracks_1(par_ske_lines_tracks):    # links unten eher anknüpfen
    found = 0
    robotracks_downsorted = par_ske_lines_tracks
    for line in range(len(robotracks_downsorted)-1):
        print("\n\n\n", "------------------------------------------------\n", "line: ",line)
        print("length of line: ", len(robotracks_downsorted[line]))
        print(robotracks_downsorted[line],"\n------------------------------------------------","\n")
        for t in range(len(robotracks_downsorted[line])):
            print("track: ",t)

            if robotracks_downsorted[line][t][-1][0]-robotracks_downsorted[line][t][0][0] > 0:  # ist der track höher als eins?
                if robotracks_downsorted[line][t][-1][0] - robotracks_downsorted[line][t][-2][0] > 0:    #vorletztes pixel ist höher als letztes
                    for tr in range(len(robotracks_downsorted[line + 1])):                             #mitte, links rechts überprüfen
                        if robotracks_downsorted[line+1][tr][-1][0] - robotracks_downsorted[line+1][tr][0][0] == 0:    # es wird verhindert, dass zwei tracks aus der gleichen zeile an denselben track in der nächsten zeile anknüpfen, da nicht mehr angeknüpft wird, wenn der track in der nächsten zeile höher als eins ist
                            if robotracks_downsorted[line+1][tr][-1][1] - robotracks_downsorted[line][t][-1][1] == -1 or robotracks_downsorted[line+1][tr][-1][1] - robotracks_downsorted[line][t][-1][1] == 0:
                                found = 1
                                print(robotracks_downsorted, "\n höhe über eins. vorletztes pixel liegt höher als letztes. links überprüfen getriggert.")
                                robotracks_downsorted[line+1][tr].reverse()
                                robotracks_downsorted[line+1][tr] = robotracks_downsorted[line][t] + robotracks_downsorted[line+1][tr]
                                robotracks_downsorted[line][t].clear()
                                print(robotracks_downsorted, "\n")
                                break
                            elif robotracks_downsorted[line+1][tr][0][1] - robotracks_downsorted[line][t][-1][1] == 1 or robotracks_downsorted[line+1][tr][0][1] - robotracks_downsorted[line][t][-1][1] == 0:
                                found = 1
                                print(robotracks_downsorted, "\n höhe über eins. vorletztes pixel liegt höher als letztes. rechts überprüfen getriggert.")
                                robotracks_downsorted[line+1][tr] = robotracks_downsorted[line][t] + robotracks_downsorted[line+1][tr]
                                robotracks_downsorted[line][t].clear()
                                print(robotracks_downsorted, "\n")
                                break
                            else:
                                pass
                        else:
                            pass
                    if found:
                        found = 0
                        continue

                elif robotracks_downsorted[line][t][-2][1] - robotracks_downsorted[line][t][-1][1] == 1:  # vorletztes pixel ist rechts von letztem -> linke pixel überprüfen
                    for tr in range(len(robotracks_downsorted[line + 1])):
                        if robotracks_downsorted[line + 1][tr][-1][0] - robotracks_downsorted[line + 1][tr][0][0] == 0:          # es wird verhindert, dass zwei tracks aus der gleichen zeile an denselben track in der nächsten zeile anknüpfen, da nicht mehr angeknüpft wird, wenn der track in der nächsten zeile höher als eins ist
                            if robotracks_downsorted[line + 1][tr][-1][1] - robotracks_downsorted[line][t][-1][1] == 0 or robotracks_downsorted[line + 1][tr][-1][1] - robotracks_downsorted[line][t][-1][1] == -1:
                                found = 1
                                print(robotracks_downsorted, "\n höhe über eins. vorletztes pixel ist rechts von letztem. links überprüfen getriggert.")
                                robotracks_downsorted[line + 1][tr].reverse()
                                robotracks_downsorted[line + 1][tr] = robotracks_downsorted[line][t] + robotracks_downsorted[line + 1][tr]
                                robotracks_downsorted[line][t].clear()
                                print(robotracks_downsorted, "\n")
                                break
                            else:
                                pass
                    if found:
                        found = 0
                        continue

                elif robotracks_downsorted[line][t][-2][1]-robotracks_downsorted[line][t][-1][1] == -1:    #vorletztes pixel ist links von letztem -> rechte pixel überprüfen
                    for tr in range(len(robotracks_downsorted[line + 1])):
                        if robotracks_downsorted[line + 1][tr][-1][0] - robotracks_downsorted[line + 1][tr][0][0] == 0:       # es wird verhindert, dass zwei tracks aus der gleichen zeile an denselben track in der nächsten zeile anknüpfen, da nicht mehr angeknüpft wird, wenn der track in der nächsten zeile höher als eins ist
                            if robotracks_downsorted[line+1][tr][0][1] - robotracks_downsorted[line][t][-1][1] == 0 or robotracks_downsorted[line+1][tr][0][1] - robotracks_downsorted[line][t][-1][1] == 1:
                                found = 1
                                print(robotracks_downsorted, "\n höhe über eins. vorletztes pixel ist links von letztem. rechts überprüfen getriggert.")
                                robotracks_downsorted[line+1][tr] = robotracks_downsorted[line][t] + robotracks_downsorted[line+1][tr]
                                robotracks_downsorted[line][t].clear()
                                print(robotracks_downsorted, "\n")
                                break
                            else:
                                pass
                    if found:
                        found = 0
                        continue
                        
            else:                                                                                        # track hat die höhe eins -> linkes und rechtes ende überprüfen
                for tr in range(len(robotracks_downsorted[line + 1])):                                   # linkes ende überprüfen
                    if robotracks_downsorted[line + 1][tr][-1][0] - robotracks_downsorted[line + 1][tr][0][0] == 0:         # es wird verhindert, dass zwei tracks aus der gleichen zeile an denselben track in der nächsten zeile anknüpfen, da nicht mehr angeknüpft wird, wenn der track in der nächsten zeile höher als eins ist
                        if robotracks_downsorted[line + 1][tr][-1][1] - robotracks_downsorted[line][t][0][1] == 0 or robotracks_downsorted[line + 1][tr][-1][1] - robotracks_downsorted[line][t][0][1] == -1:
                            print(robotracks_downsorted, "\n höhe eins. linkes ende überprüfen getriggert.")
                            robotracks_downsorted[line][t].reverse()
                            robotracks_downsorted[line + 1][tr].reverse()
                            robotracks_downsorted[line + 1][tr] = robotracks_downsorted[line][t] + robotracks_downsorted[line + 1][tr]
                            robotracks_downsorted[line][t].clear()
                            print(robotracks_downsorted, "\n")
                            break                                                                            # rechtes ende überprüfen
                        elif robotracks_downsorted[line +1][tr][0][1] - robotracks_downsorted[line][t][-1][1] == 0 or robotracks_downsorted[line + 1][tr][0][1] - robotracks_downsorted[line][t][-1][1] == 1:
                            print(robotracks_downsorted, "\n höhe eins. rechtes ende überprüfen getriggert.")
                            robotracks_downsorted[line + 1][tr] = robotracks_downsorted[line][t] + robotracks_downsorted[line + 1][tr]
                            robotracks_downsorted[line][t].clear()
                            print(robotracks_downsorted, "\n")
                            break
                        else:
                            pass


    for line in robotracks_downsorted:
        for t in range(len(line)):
            line[t] = [x for x in line[t] if x != []]
    for line in range(len(robotracks_downsorted)):
        robotracks_downsorted[line] = [x for x in robotracks_downsorted[line] if x != []]
    robotracks_downsorted = [x for x in robotracks_downsorted if x != []]


    robotracks = []
    for line in robotracks_downsorted:
        for t in line:
            robotracks.append(t)


    print("\n\n\n\n\n\n\n")
    print(robotracks)

    print("\n\n\n\n\n\n\nnumber of tracks in total:")
    print(len(robotracks))



    global comparison_ske_letter_robotracks
    comparison_ske_letter_robotracks = cv.cvtColor(comparison_ske_letter, cv.COLOR_GRAY2BGR)                     # im folgenden werden die robotracks auf das originalbild mit skelett aufgemalt, damit abweichungen vom altem skelett erkannt werden können
    for t in robotracks:
        color = (randint(50, 200), randint(50, 200), randint(50, 200))
        for pixel in t:
            comparison_ske_letter_robotracks[pixel[0], pixel[1]] = (color)


    print("finished")
    return(robotracks)


def sorting_for_letters(par_robotracks):                  # diese funktion kann auch für hochwärts sortieren verwendet werden. dazu einfach edges_vertical statt edge_horizontal erstellen. und [1] durch [0] erstetzen!!!!

    edges_horizontal = [[[],[]] for x in par_robotracks]
    for track in range(len(par_robotracks)):
        for pixel in par_robotracks[track]:
            edges_horizontal[track][0].append(pixel[1])
            edges_horizontal[track][1].append(pixel[1])
        edges_horizontal[track][0] = min(edges_horizontal[track][0])
        edges_horizontal[track][1] = max(edges_horizontal[track][1])






    edges_tracks_combined = [[edges_horizontal[x][0],edges_horizontal[x][1],par_robotracks[x]] for x in range(len(edges_horizontal))]
    print(edges_tracks_combined)
    edges_tracks_combined_sorted = sorted(edges_tracks_combined, key=lambda x: x[0])                                                        ###### sortiert kombinierte liste nach dem ersten wert in den jeweiligen unterlisten, dies entspricht dann linkem edge
    print("edges_tracks_combined_sorted")
    print(edges_tracks_combined_sorted)




    robotracks_horizontal_sorted = [[x[2]] for x in edges_tracks_combined_sorted]
    edges_horizontal = [[x[0],x[1]] for x in edges_tracks_combined_sorted]

    for search in range(len(robotracks_horizontal_sorted)):
        print("\n\n\n\nsearch:-------------------------------------------------------- \n", search)

        if search  == len(robotracks_horizontal_sorted):    # für das letzte element muss auch gesucht werden, da es sein kann, dass sich die Länge der Liste davor um 2 verändert hat und nicht um 1
            break


        else:
            print("**********edges_horizontal[search]: \n", edges_horizontal[search])
            deleter = []
            for find in range(search+1, len(robotracks_horizontal_sorted)):
                print("\n\n\nfind: \n", find)
                print("***edges_horizontal[find]: \n", edges_horizontal[find])

                if (edges_horizontal[find][0] - 1) <= edges_horizontal[search][0] <= (edges_horizontal[find][1] + 1) or (edges_horizontal[find][0] - 1) <= edges_horizontal[search][1] <= (edges_horizontal[find][1] + 1) or (edges_horizontal[search][0] - 1) <= edges_horizontal[find][0] <= (edges_horizontal[search][1] + 1) or (edges_horizontal[search][0] - 1) <= edges_horizontal[find][1] <= (edges_horizontal[search][1] + 1):
                    print("found!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("\nedges_horizontal: \n", edges_horizontal)
                    edges_horizontal[search][0] = min(edges_horizontal[search][0], edges_horizontal[find][0])
                    edges_horizontal[search][1] = max(edges_horizontal[search][1], edges_horizontal[find][1])
                    print("edges_horizontal danach: \n", edges_horizontal)
                    print("\nrobotracks_horizontal_sorted: \n", robotracks_horizontal_sorted)
                    robotracks_horizontal_sorted[search] = robotracks_horizontal_sorted[search] + robotracks_horizontal_sorted[find]
                    print("robotracks_horizontal_sorted: \n", robotracks_horizontal_sorted)
                    deleter.append(find)
                if robotracks_horizontal_sorted[find] == robotracks_horizontal_sorted[-1]:
                    deleter.reverse()
                    for deletion in deleter:
                        del edges_horizontal[deletion]
                        del robotracks_horizontal_sorted[deletion]
                    break



    print("\nedges_horizontal: \n",edges_horizontal)
    print("\nlen edges_horizontal: \n", len(edges_horizontal))
    print("\nrobotracks_horizontal_sorted: \n", robotracks_horizontal_sorted)
    print("\nlen robotracks_horizontal_sorted: \n", len(robotracks_horizontal_sorted))




    global comparison_ske_letter_horizontal_sorted
    comparison_ske_letter_horizontal_sorted = cv.cvtColor(comparison_ske_letter, cv.COLOR_GRAY2BGR)                    # hier werden die buchstaben wieder auf das originalbild mit skelett überzeichnet, um abweichungen vom skelett sehen zu können
    for letter in robotracks_horizontal_sorted:
        color = (randint(50, 200), randint(50, 200), randint(50, 200))
        for t in letter:
            for pixel in t:
                comparison_ske_letter_horizontal_sorted[pixel[0], pixel[1]] = (color)



    return(robotracks_horizontal_sorted)





def recursive_search_in_letter(par_letter):

    for track_search in range(len(par_letter)):
        print("\n\n------------------------track_search: ", track_search, "\n\n")

        for track_find in range(track_search+1, len(par_letter)):
            print("--------track_find: ", track_search, "\n")
            if [abs(par_letter[track_search][0][0]-par_letter[track_find][0][0]),abs(par_letter[track_search][0][1]-par_letter[track_find][0][1])]  in [[0,1],  [1,0],  [1,1]]:     #Anfangsearch #Anfangfind
                print("par_letter: ", par_letter)
                par_letter[track_search] = par_letter[track_search][::-1] + par_letter[track_find]
                del par_letter[track_find]
                print("par_letter: ", par_letter)
                return(recursive_search_in_letter(par_letter))


            elif [abs(par_letter[track_search][0][0]-par_letter[track_find][-1][0]),abs(par_letter[track_search][0][1]-par_letter[track_find][-1][1])]  in [[0,1],  [1,0],  [1,1]]:    #Anfangsearch #Endefind
                print("par_letter: ", par_letter)
                par_letter[track_search] = par_letter[track_search][::-1] + par_letter[track_find][::-1]
                del par_letter[track_find]
                print("par_letter: ", par_letter)
                return(recursive_search_in_letter(par_letter))


            elif [abs(par_letter[track_search][-1][0] - par_letter[track_find][0][0]),abs(par_letter[track_search][-1][1] - par_letter[track_find][0][1])]  in [[0,1],  [1,0],  [1,1]]:  #Endesearch #Anfangfind
                print("par_letter: ", par_letter)
                par_letter[track_search] = par_letter[track_search] + par_letter[track_find]
                del par_letter[track_find]
                print("par_letter: ", par_letter)
                return(recursive_search_in_letter(par_letter))

            elif [abs(par_letter[track_search][-1][0] - par_letter[track_find][-1][0]),abs(par_letter[track_search][-1][1] - par_letter[track_find][-1][1])]  in [[0,1],  [1,0],  [1,1]]:   #Endesearch #Endefind
                print("par_letter: ", par_letter)
                par_letter[track_search] = par_letter[track_search] + par_letter[track_find][::-1]
                del par_letter[track_find]
                print("par_letter: ", par_letter)
                return(recursive_search_in_letter(par_letter))

            else:
                pass

    return(par_letter)


def recursive_search_in_letter_joining(par_letter):

    for track_search in range(len(par_letter)):
        print("\n\n------------------------track_search: ", track_search, "\n\n")
        print("track_search liste", list(range(len(par_letter))))
        for track_find  in list(range(len(par_letter)))[:track_search] + list(range(len(par_letter)))[track_search+1:]:
            print("track_find liste", list(range(len(par_letter)))[:track_search] + list(range(len(par_letter)))[track_search + 1:])
            print("--------track_find: ", track_search, "\n")
            for pixel in range(len(par_letter[track_find])):
                print(len(par_letter[track_search]))


                if [abs(par_letter[track_search][0][0]-par_letter[track_find][pixel][0]),abs(par_letter[track_search][0][1]-par_letter[track_find][pixel][1])]  in [[0,1],  [1,0],  [1,1]]:

                    print("par_letter: ", par_letter)

                    if pixel +1 <= cut_join:                         # vorderer teil von track_find wird abgetrennt und gelöscht
                        par_letter[track_search] = par_letter[track_search][::-1] + par_letter[track_find][pixel:]
                        del par_letter[track_find]
                        return(recursive_search_in_letter_joining(par_letter))

                    elif len(par_letter[track_find]) - pixel  <= cut_join:       # hinterer teil von track_find wird abgetrennt und gelöscht
                        par_letter[track_search] = par_letter[track_search][::-1] + par_letter[track_find][:pixel+1][::-1]
                        del par_letter[track_find]
                        return (recursive_search_in_letter_joining(par_letter))


                elif [abs(par_letter[track_search][-1][0] - par_letter[track_find][pixel][0]),abs(par_letter[track_search][-1][1] - par_letter[track_find][pixel][1])]  in [[0,1],  [1,0],  [1,1]]:

                    print("par_letter: ", par_letter)

                    if pixel + 1 <= cut_join:                            # vorderer teil von track_find wird abgetrennt und gelöscht
                        par_letter[track_search] = par_letter[track_search] + par_letter[track_find][pixel:]
                        del par_letter[track_find]
                        return (recursive_search_in_letter_joining(par_letter))

                    elif len(par_letter[track_find]) - pixel <= cut_join:            # hinterer teil von track_find wird abgetrennt und gelöscht
                        par_letter[track_search] = par_letter[track_search] + par_letter[track_find][:pixel+1][::-1]
                        del par_letter[track_find]
                        return (recursive_search_in_letter_joining(par_letter))

                else:
                    pass                                                      # exit aus rekursion, für nächsten buchstaben beginnt neue rekursion, nachdem der aktuelle buchstabe im return zurückgegeben wurde

    return(par_letter)

#---------------------------------------------------------------

def ask_shorten_self(par_track_search):
    global own_letter_not_search
    for pixel in par_track_search[own_letter_not_search:]:  # es wird gesucht, ob der anfang von einem track an sich selber irgendwo anstößt, dazu werden die ersten paar pixel im search_track nicht untersucht
        if [abs(par_track_search[0][0] - pixel[0]), abs(par_track_search[0][1] - pixel[1])] in [[0, 1], [1, 0], [1, 1]]:  # search_tracks anfang hat einen pixel gefunden, an das es anstößt
            return(False)
    return(True)              # ja, freies ende

def ask_shorten_self_end(par_track_search):
    global own_letter_not_search
    for pixel in par_track_search[:-own_letter_not_search:]:  # es wird gesucht, ob der anfang von einem track an sich selber irgendwo anstößt, dazu werden die ersten paar pixel im search_track nicht untersucht
        if [abs(par_track_search[-1][0] - pixel[0]), abs(par_track_search[-1][1] - pixel[1])] in [[0, 1], [1, 0], [1, 1]]:  # search_tracks anfang hat einen pixel gefunden, an das es anstößt
            return(False)
    return(True)              # ja, freies ende

def ask_shorten_others(par_par_letter, par_track_search):
    letter_without_search_track = list(par_par_letter)
    letter_without_search_track.remove(par_track_search)
    for track_find in letter_without_search_track:  # zuerst für [0]  anfang, dann [-1] ende
        print("len(track_find):", len(track_find))
        if len(track_find)==0:
            continue
        for pixel_find in track_find:

            if [abs(par_track_search[0][0] - pixel_find[0]), abs(par_track_search[0][1] - pixel_find[1])] in [[0, 1], [1, 0],[1, 1]]:  # search_tracks anfang hat einen pixel gefunden, an das es anstößt
                return(False)
    return(True)               # ja, freies ende

def ask_shorten_others_end(par_par_letter, par_track_search):
    letter_without_search_track = list(par_par_letter)
    letter_without_search_track.remove(par_track_search)

    for track_find in letter_without_search_track:  # zuerst für [0]  anfang, dann [-1] ende
        print("len(track_find):",len(track_find))
        if len(track_find)==0:
            continue
        for pixel_find in track_find:
            print(par_track_search)
            print(par_track_search[-1])
            if [abs(par_track_search[-1][0] - pixel_find[0]), abs(par_track_search[-1][1] - pixel_find[1])] in [[0, 1], [1, 0],[1, 1]]:  # search_tracks anfang hat einen pixel gefunden, an das es anstößt
                return(False)
    return(True)               # ja, freies ende


def shorten_in_letter(par_letter):             # eigentlich müsst track_search in ihren eigenen pixel suchen, dies wird nicht gemacht, da beim downsorten so etwas wie ein kleines d am stück nicht auftreten kann, deswegen evtl. diese funktion vor dem robotrack_long laufen lassen
    global shorten_number
    global own_letter_not_search
    for track_search in par_letter:
        if len(track_search) == 0:
            continue

        print("\n\n\ndavor par_letter:", par_letter)
        print("\n\n")

        if [abs(track_search[0][0]-track_search[-1][0]),abs(track_search[0][1]-track_search[-1][1])]  in [[0,1],  [1,0],  [1,1]]: # anfang und ende # sich selber überprüfen
            continue    # nächster track untersuchen, ohne etwas zu löschen

        print("\nanfang ende par_letter:", par_letter)

        if ask_shorten_self(track_search) and ask_shorten_others(par_letter, track_search):     #freies ende am anfang
            del track_search[:shorten_number]

        print("\nanfang par_letter:", par_letter)
        if len(track_search) == 0:
            continue

        if ask_shorten_self_end(track_search) and ask_shorten_others_end(par_letter, track_search):         #freies ende am ende
            del track_search[-shorten_number:]

        print("\n\n\ndanach (oder ende) par_letter:", par_letter)
        print("\n\n")

    return(par_letter)

#---------------------------------------------------------------


def tuning_cleanup(robotracks):
    for letter_num in range(len(robotracks)):
        robotracks[letter_num] = [x for x in robotracks[letter_num] if x != []]
    #robotracks = [x for x in robotracks if x != []]
    return(robotracks)

def letter_tuning(par_robotracks_horizontal_sorted):

    global shorten_number


    global comparison_ske_letter_robotracks_long
    global comparison_letter_robotracks_removed
    global comparison_letter_robotracks_shorted
    global comparison_letter_robotracks_joined



    print("\n\n\n\n\nBuchstaben werden zusammengefügt:\n\n")

    robotracks_long = par_robotracks_horizontal_sorted
    for letter_num in range(len(par_robotracks_horizontal_sorted)):
        print("\n\n\n\nletter_num:\n\n", letter_num)

        robotracks_long[letter_num] = recursive_search_in_letter(par_robotracks_horizontal_sorted[letter_num])
        print("Strecken, welche für den Buchstaben verwendet werden müssen:", len(robotracks_long[letter_num]))

    comparison_ske_letter_robotracks_long = cv.cvtColor(comparison_ske_letter, cv.COLOR_GRAY2BGR)
    for letter_ in robotracks_long:
        for t in letter_:
            color = (randint(50, 200), randint(50, 200), randint(50, 200))
            for pixel in t:
                comparison_ske_letter_robotracks_long[pixel[0], pixel[1]] = (color)





    print("\n\n\n\n\nZu kurze Strecken werden gelöscht ab remove_number, sodass nur noch größere Strecken als remove_number existieren: ", "remove_number: ", remove_number, "\n\n")

    robotracks_removed = robotracks_long
    for letter_num in range(len(robotracks_long)):
        print("\n\n\n\nletter_num:\n\n", letter_num)
        for track_num in range(len(robotracks_long[letter_num])):
            if len(robotracks_long[letter_num][track_num]) <= remove_number:
                robotracks_removed[letter_num][track_num].clear()

    robotracks_removed = tuning_cleanup(robotracks_removed)                             # keine rekursive funktion verwendet. clear() statt del verwendet um iteration aufrecht zu erhalten. cleanup nötig

    comparison_letter_robotracks_removed = cv.cvtColor(letter, cv.COLOR_GRAY2BGR)
    for letter_ in robotracks_removed:
        for t in letter_:
            color = (randint(50, 200), randint(50, 200), randint(50, 200))
            for pixel in t:
                comparison_letter_robotracks_removed[pixel[0], pixel[1]] = (color)






    print("\n\n\n\n\nBuchstaben werden gekürtzt um shorten_number: ", "shorten_number: ", shorten_number, "\n\n")

    robotracks_shorted = robotracks_removed
    for letter_num in range(len(robotracks_removed)):
        print("\n\n\n\nletter_num:\n\n", letter_num)
        robotracks_shorted[letter_num] = shorten_in_letter(robotracks_removed[letter_num])


    robotracks_shorted = tuning_cleanup(robotracks_shorted)                             # keine rekursive funktion verwendet. clear() statt del verwendet um iteration aufrecht zu erhalten. cleanup nötig

    comparison_letter_robotracks_shorted = cv.cvtColor(letter, cv.COLOR_GRAY2BGR)
    for letter_ in robotracks_shorted:
        for t in letter_:
            color = (randint(50, 200), randint(50, 200), randint(50, 200))
            for pixel in t:
                comparison_letter_robotracks_shorted[pixel[0], pixel[1]] = (color)

    print("robotracks_shorted: ", robotracks_shorted)







    print("\n\n\n\n\nBuchstaben werden gekürtzt zum joinen um cut_join: ", "cut_join: ", cut_join, "\n\n")

    robotracks_joined = robotracks_shorted
    for letter_num in range(len(robotracks_shorted)):
        print("\n\n\n\nletter_num:\n\n", letter_num)

        robotracks_joined[letter_num] = recursive_search_in_letter_joining(robotracks_shorted[letter_num])

    robotracks_joined = tuning_cleanup(robotracks_joined)
    
    comparison_letter_robotracks_joined = cv.cvtColor(letter, cv.COLOR_GRAY2BGR)
    for letter_ in robotracks_joined:
        for t in letter_:
            color = (randint(50, 200), randint(50, 200), randint(50, 200))
            for pixel in t:
                comparison_letter_robotracks_joined[pixel[0], pixel[1]] = (color)

    robotracks_joined = [x for x in robotracks_joined if x != []]
    return(robotracks_joined)


def get_abs_distance(coordinate_one, coordinate_two):
    distance = m.sqrt(m.pow(coordinate_two[0] - coordinate_one[0],2) + m.pow(coordinate_two[1] - coordinate_one[1],2))
    return(distance)


def robotracks_sorting(robotracks):

    global comparison_letter_robotracks_sorted_final

    # im folgendem wird in jedem buchstabe der linkeste pixel auch in dem robotrack nach ganz links gestellt
    print("\n\n\n\nlinkester pixel finden: \n\n\n")
    for letter_num in range(len(robotracks)):
        print("\n\nletter_num: ", letter_num)
        start = {}
        end = {}
        for track_num in range(len(robotracks[letter_num])):
            print("track_num: ", track_num)
            start[track_num] = robotracks[letter_num][track_num][0][1]
            end[track_num] = robotracks[letter_num][track_num][-1][1]

        key_start_min = min(start, key=start.get)
        key_end_min = min(end, key=end.get)
        print("key_start_min: ",key_start_min)
        print("key_end_min: ", key_end_min)
        if start[key_start_min] <= end[key_end_min]:
            print("robotracks[letter_num][key_start_min]: ")
            print(robotracks[letter_num][key_start_min])

            robotracks[letter_num].insert(0, robotracks[letter_num][key_start_min])

            print("robotracks[letter_num]: ")
            print(robotracks[letter_num])

            del robotracks[letter_num][key_start_min+1]
            print("robotracks[letter_num]: ")
            print(robotracks[letter_num])
        else:
            robotracks[letter_num].insert(0, robotracks[letter_num][key_end_min][::-1])
            print("robotracks[letter_num]: ")
            print(robotracks[letter_num])
            del robotracks[letter_num][key_end_min + 1]
            print("robotracks[letter_num]: ")
            print(robotracks[letter_num])



    # im folgendem wird in allen buchstaben außer dem letztem der pixel gesucht der am nächstem zum buchstabe rechts daneben gehört, und dieser track nach ganz rechts gestellt
    for letter_num in range(len(robotracks)-1):                      # alle außer letzter buchstabe

     #   print("letter_num: ", letter_num)

        n = 214748364
        sorting = 0
        track_choice = 0
        for track_num in range(len(robotracks[letter_num])):

            # print("track_num: ", track_num)
            print("robotracks[letter_num]: ", robotracks[letter_num])
            # print("robotracks[letter_num+1][0][0]: ", robotracks[letter_num+1][0][0])

            distance_first = get_abs_distance(robotracks[letter_num][track_num][0], robotracks[letter_num+1][0][0])     # abstand zwischen erster pixel von suchendem track und erster pixel von dem buchstaben rechts daneben, welcher nicht iteriert wird
            distance_last = get_abs_distance(robotracks[letter_num][track_num][-1], robotracks[letter_num+1][0][0])     # abstand zwischen letztem pixel von suchendem track und erster pixel von dem buchstaben rechts daneben, welcher nicht iteriert wird

            if distance_first < n:
                n = distance_first
                track_choice = track_num
                sorting = -1                                       # wenn der erste pixel eines tracks am nächstem zum buchstabe rechts davon ist, muss dieser erste pixel ganz am ende stehen -> sorting = -1
            if distance_last < n:
                n = distance_last
                track_choice = track_num
                sorting = 1
        robotracks[letter_num].append(robotracks[letter_num][track_choice][::sorting])
        del robotracks[letter_num][track_choice]



    # im folgendem werden alle mittleren tracks im jeweiligem buchstaben sortiert. zuerst wird der pixel sortiert, welcher am nähesten des endes der ersten tracks ist
    for letter_num in range(len(robotracks)):
        print("letter_num:", letter_num, "\n\n\n")
        if len(robotracks[letter_num]) <= 2:
            pass
        else:
            begin = 0
            for iteration in range(len(robotracks[letter_num])-2):
                print("iteration: ", iteration, "\n\n")
                begin = begin + 1
                n = 214748364
                sorting = 0
                track_choice = 0
                for ii in range(begin, len(robotracks[letter_num])-1):                    # beispiel für ii bei len(robotracks)=5            1, 2, 3 für iteration 0        2, 3 für iteration 1       3 für iteration 2
                    distance_first = get_abs_distance(robotracks[letter_num][begin-1][-1], robotracks[letter_num][ii][1])
                    distance_last = get_abs_distance(robotracks[letter_num][begin-1][-1], robotracks[letter_num][ii][-1])
                    if distance_first < n:
                        n = distance_first
                        track_choice = ii
                        sorting = 1
                    if distance_last < n:
                        n = distance_last
                        track_choice = ii
                        sorting = -1

                robotracks[letter_num].insert(iteration+1, robotracks[letter_num][track_choice][::sorting])
                del robotracks[letter_num][track_choice+1]


    comparison_letter_robotracks_sorted_final = cv.cvtColor(letter, cv.COLOR_GRAY2BGR)
    i = 0
    for letter_ in robotracks:
        for t in letter_:
            cv.putText(comparison_letter_robotracks_sorted_final, str(i), (t[0][1], t[0][0]), cv.FONT_HERSHEY_COMPLEX, 1, (5, 5, 5))
            cv.putText(comparison_letter_robotracks_sorted_final, str(i+1), (t[-1][1], t[-1][0]), cv.FONT_HERSHEY_COMPLEX, 1, (10, 10, 200))
            color = (randint(50, 200), randint(50, 200), randint(50, 200))
            for pixel in t:
                comparison_letter_robotracks_sorted_final[pixel[0], pixel[1]] = (color)
            i = i +2

    return(robotracks)



def selection_pixel(robotracks, par_selection_step):
    global comparison_letter_robotracks_selected

    print("robotracks vor selecten: ", robotracks)

    for letter_num in range(len(robotracks)):
        for track_num in range(len(robotracks[letter_num])):
            robotracks[letter_num][track_num] = robotracks[letter_num][track_num][0:len(robotracks[letter_num][track_num]) - 1:selection_step] + [robotracks[letter_num][track_num][-1]] # neuer robotrack: ab ersten bis vorletzten pixel alle pixel mit selection_step auswählen + letzter pixel

    print("robotracks nach selecten: ", robotracks)

    comparison_letter_robotracks_selected = cv.cvtColor(letter, cv.COLOR_GRAY2BGR)
    for letter_ in robotracks:
        for t in letter_:
            color = (randint(50, 200), randint(50, 200), randint(50, 200))
            for pixel in t:
                comparison_letter_robotracks_selected[pixel[0], pixel[1]] = (color)



    return(robotracks)





#-----------------------------------------------------------------------





def show_images():




    cv.imshow("comparison_ske_letter", comparison_ske_letter)

    cv.imshow("comparison_ske_letter_robotracks", comparison_ske_letter_robotracks)

    cv.imshow("comparison_ske_letter_horizontal_sorted", comparison_ske_letter_horizontal_sorted)


    cv.imshow("comparison_ske_letter_long (1)", comparison_ske_letter_robotracks_long)

    cv.imshow("comparison_letter_removed (2)", comparison_letter_robotracks_removed)

    cv.imshow("comparison_letter_shorted (3)", comparison_letter_robotracks_shorted)

    cv.imshow("comparison_letter_joined (4)", comparison_letter_robotracks_joined)


    cv.imshow("comparison_letter_sorted_final (5)", comparison_letter_robotracks_sorted_final)

    cv.imshow("comparison_letter_selected (6)", comparison_letter_robotracks_selected)




    cv.imshow("letter_canny", letter_canny)

#    cv.imshow("letter_erosion_before", letter_erosion_before)

    cv.imshow("letter_dilation", letter_dilation)

#    cv.imshow("letter_erosion_after", letter_erosion_after)


    cv.waitKey(0)
    cv.destroyAllWindows()
    #cv.imread()

def show_images_calibration():



    cv.imshow("calibration_color (1)", calibration_color)

    cv.imshow("calibration_blur_color (2)", calibration_blur_color)

    #cv.imshow("calibration_img    (grayscale)  (3)", calibration_img)

    cv.imshow("calibration_blur (4)", calibration_blur)

    cv.imshow("calibration_threshold (5)", calibration_threshold)

    cv.imshow("calibration_cut  (6)", calibration_cut)

    cv.imshow("comparison_calibration  (7)", comparison_calibration)






    cv.waitKey(0)
    cv.destroyAllWindows()
    #cv.imread()








#calibration_squarepoints(calibration_filtering(cv.imread("Grid6.png", 1)))

#show_images_calibration()

#robotracks_tuned = robotracks_sorting(letter_tuning(sorting_for_letters(creating_robotracks_1(creating_ske_lines_tracks(creating_ske_lines_pixel(creating_ske(filtering(w_canny_first, w_canny_second, w_dilation_kernel_size, cv.imread("HEY.png", 0)))))))))
#robotracks_selected = selection_pixel(robotracks_tuned, selection_step)
#show_images()


#calibration_points = calibrationpoints_arduino()

#send(calibration_points)












if __name__ == '__main__':
    
    #while True:
        
       # try:
        main()

     #   except Exception as err:
     #       print(err)
     #       lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
     #       lcd_string(str(err)[0:16]) 
     #       lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
     #       lcd_string(str(err)[16:32]) 



