
"""
Changes file path to background for Windows, mac and Linux
:Big Ups to Thomas at https://github.com/Thomas9292/cvplayground 
Sends toast on linux 
:Big Ups to Yuriy at https://github.com/YuriyLisovskiy/pynotifier
"""
import platform, os, requests

def windows_background(file_path):
    """
    Change the background on windows operating systems
    """
    print(1)
    import ctypes
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, file_path, 1)

def linux_background(file_path):
    """
    Change the background on Linux operating systems
    """
    print(2)
    import subprocess
    # Initialize variables
    ARG_MAP = {
        'feh': ['feh', ['--bg-center'], '%s'],
        'gnome': [
            'gsettings',
            ['set', 'org.gnome.desktop.background', 'picture-uri'], 'file://%s'
        ]
    }
    WM_BKG_SETTERS = {
        'spectrwm': ARG_MAP['feh'],'scrotwm': ARG_MAP['feh'],
        'wmii': ARG_MAP['feh'],'i3': ARG_MAP['feh'],
        'awesome': ARG_MAP['feh'],'awesome-gnome': ARG_MAP['gnome'],
        'gnome': ARG_MAP['gnome'],'ubuntu': ARG_MAP['gnome']
    }

    # Try to find background setter
    desktop_environ = os.environ.get('DESKTOP_SESSION', '')
    # Get settings arguments
    if desktop_environ and desktop_environ in WM_BKG_SETTERS:
        bkg_setter, args, pic_arg = WM_BKG_SETTERS.get(desktop_environ,[None, None])
    else:
        bkg_setter, args, pic_arg = WM_BKG_SETTERS['spectrwm']
    # Parse and execute background change command
    pargs = [bkg_setter] + args + [pic_arg % file_path]
    subprocess.call(pargs)

def mac_background(file_path):
    """
    Change the background on Mac operating systems
    """
    print(3)
    try:
        from appscript import app, mactypes
        app('Finder').desktop_picture.set(mactypes.File(file_path))
    except ImportError:
        import subprocess
        SCRIPT = """
                /usr/bin/osascript<<END
                tell application "Finder" to
                set desktop picture to POSIX file "%s"
                end tell
                END
                """
        subprocess.Popen(SCRIPT % file_path, shell=True)

def Change_Background(full_path):
    """
    Changes Background for every major os Windows, Mac & linux 
    """

    if platform.system().lower().startswith('win'):
        print(1)

        windows_background(full_path)
    elif platform.system().lower().startswith('lin'):
        print(2)

        linux_background(full_path)
    elif platform.system().lower().startswith('dar'):
        print(3)

        mac_background(full_path)

def notify_toast(title, message, urgency='low'):
    """
    Makes toast for every major os Windows , Mac & linux
    
    Parameters
        ----------
        title : str
            title that the toast should display
        message : str
            message that the toast should display
        num_legs : str , optional
            ONLY USED IN LINUX
            The number of legs the animal (default is low)
    Returns
    -------
    None
        but still prints BaseExecption to command line
    """
    if platform.system().lower().startswith('win'):
        # Windows NT
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(u"".format(title),
                            u"".format(message),
                            icon_path="custom.ico",
                            duration=10)
        except BaseException as e:
            print("Windows Toast Error: {}".format(e))
            
    elif platform.system().lower().startswith('lin'):
        URGENCY_LOW = 'low'
        URGENCY_NORMAL = 'normal'
        URGENCY_CRITICAL = 'critical'
        try:
            import subprocess
            if urgency not in [URGENCY_LOW, URGENCY_NORMAL, URGENCY_CRITICAL]:
			    print('invalid urgency was given: {}'.format(urgency))
            command = [
                'notify-send', '{}'.format(title),
                '{}'.format(message),
                '-u', urgency,
                '-t', '{}'.format(duration * 1000)
            ]
            if self.__icon_path is not None:
                command += ['-i', icon_path]
            subprocess.call(command)
        except BaseException as e:
            print("Linux Toast Error: {}".format(e))
    
    elif platform.system().lower().startswith('dar'):
        try:
            pass
        except BaseException as e:
            print("MacOS Toast Error: {}".format(e))

    return None



def check_internet():
    try:
        requests.get('http://www.google.com/', timeout=5)
        return None
    except requests.ConnectionError:
        print("No internet connection available.")
        return notify_toast('Unsplasher','Internet Connection Unavailable\n Please Reconnect' )

