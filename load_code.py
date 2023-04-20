###lets get this show on the road

'''Will need to install pywinauto and keyboard'''

from pywinauto.application import Application, ProcessNotFoundError
from pywinauto.findwindows import find_window
import keyboard

##   PrintControlIdentifiers() to see all values

def wait_key_pressed():
    '''wait for user input to continue'''
    print('Press shift to Continue')
    while True:
        try:
            if keyboard.is_pressed('shift'):
                print('Continuing Program')
                break
        except:
            pass



def access_ccs():
    '''Open or connect to CCS'''

    try:  ##if CCS is alreay open
        main_dlg_hand = find_window(title_re = r'workspace_v.* Code Composer Studio')       ## identify window
        app = Application(backend='uia').connect(handle = main_dlg_hand)                    ## connect to window
        main_dlg = app.window(handle = main_dlg_hand)
        main_dlg.wait('ready', timeout = 60)                                                ## get main dlg                           
        debugger = main_dlg.Debugblinky_dc_cpu0SplitButton                                  ## identify debugger button
        


    except ProcessNotFoundError: ##open CCS
        app = Application(backend='uia').start('C:\\ti\\ccs1010\\ccs\\eclipse\\ccstudio.exe')

        launcher_dlg = app.window(title = 'Code Composer Studio Launcher')
        launcher_dlg.wait('enabled', timeout=60)

        print('Select Workspace')
        wait_key_pressed()

        launcher_dlg.LaunchButton.click()

        main_dlg_hand = find_window(title_re = r'workspace_v.* Code Composer Studio') 
        main_dlg = app.window(handle = main_dlg_hand)
        main_dlg.wait('ready', timeout = 60)

        debugger = main_dlg.Debugblinky_dc_cpu0SplitButton   

    except:
        print('Could not access CCS')
        quit()

    return(app, main_dlg, debugger)




def init_cpu1(main_dlg, debugger):
    main_dlg.cpu01TreeItem.click_input()    # Select CPU1
    debugger.click_input()                  # Debug CPU1

    ## Wait until done debugging
    print('Wait until debug loaded')
    wait_key_pressed()

def init_cpu2(main_dlg, app):
    main_dlg.DebugTabItem.click_input()     ## go to debug terminal

    ##connect CPU2 to target
    main_dlg.TexasInstrumentsXDS100v2USBDebugProbeC28xx_CPU2TreeItem.right_click_input()  
    main_dlg.ConnectTarget.click_input()

    main_dlg.blinky_dc_cpu02TreeItem.click_input()           # select CPU2
    main_dlg.RunMenuItem.click_input()
    main_dlg.LoadMenuItem.click_input()
    main_dlg.LoadProgram.click_input()                       # Load out file into CPU2

    hand = find_window(title = 'Load Program')               # handle for loading pop-up window
    load_dlg = app.window(handle = hand)

    ## user input to ensure loading properly
    print('Select .out file and wait for load')
    wait_key_pressed()

    #load_dlg.OK.click()

    #print('Wait for files to load')
    #wait_key_pressed()


def BOOT_FLASH(main_dlg):
    main_dlg.DebugTabItem.click_input()                 ## got to debug terminal

    main_dlg.maincpu01TreeItem.click_input()            # main() file CPU1
    main_dlg.Scripts.click_input()                      # Scripts
    main_dlg.EMUBootModeSelect.click_input() 
    main_dlg.EMU_BOOT_FLASH.click_input()               # CPU1 in FLASH mode

    main_dlg.maincpu02TreeItem.click_input()            ## main() file for CPU2
    main_dlg.Scripts.click_input()
    main_dlg.EMUBootModeSelect.click_input()
    main_dlg.EMU_BOOT_FLASH.click_input()               ## CPU2 in FLASH mode


def load_code():
    [app, main_dlg, debugger] = access_ccs()
    main_dlg.BuildSplitButton2.click_input()
    main_dlg.print_control_identifiers()
    
    ##set up screen
    main_dlg.set_focus()
    main_dlg.CCSEditCheckbox.click_input()

    init_cpu1(main_dlg, debugger)
    init_cpu2(main_dlg, app)
    BOOT_FLASH(main_dlg)
    
    ## run code
    main_dlg.maincpu01TreeItem.click_input()
    main_dlg.TexasInstrumentsXDS100v2USBDebugProbeC28xx_CPU1TreeItem.click_input() 
    main_dlg.Resume.click_input()               ## run CPU1
    
    main_dlg.TexasInstrumentsXDS100v2USBDebugProbeC28xx_CPU2TreeItem.click_input()   
    main_dlg.Resume.click_input()               ## run CPU2

print('Press Shift+alt+b to start program')
while True: # Infinite loop to keep the program running
    try:
        if keyboard.is_pressed('shift'): 
            if keyboard.is_pressed('alt'):
                if keyboard.is_pressed('b'):
                    print('Program running')
                    load_code()
                    print('Code Loaded') 
                    print('Press Shift+alt+b to re-start program')                   
    except:
        pass  

