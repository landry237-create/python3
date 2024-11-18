#coding: utf-8
from __future__ import print_function
import sys

class ScreenOrien(object):
    @classmethod
    def set(cls, degree=None):
        '''
        Set the primary display to the specified mode
        '''
        if degree:
            print('Setting orientation to {}'.format(degree))
        else:
            print('Setting orientation to defaults')

        if sys.platform == 'win32':
            cls._win32_set(degree)
        elif sys.platform.startswith('linux'):
            cls._linux_set(degree)
        elif sys.platform.startswith('darwin'):
            cls._osx_set(degree)
    
    @classmethod
    def get(cls):
        if sys.platform == 'win32':
            return cls._win32_get()
        elif sys.platform.startswith('linux'):
            return cls._linux_get()
        elif sys.platform.startswith('darwin'):
            return cls._osx_get()
    
    @classmethod
    def get_modes(cls):
        if sys.platform == 'win32':
            return cls._win32_get_modes()
        elif sys.platform.startswith('linux'):
            return cls._linux_get_modes()
        elif sys.platform.startswith('darwin'):
            return cls._osx_get_modes()
    
    @staticmethod
    def _win32_get_modes():
        '''
        Get the primary windows display orientation
        '''
        
        modes = ["Landscape", "Portrait", "Landscape (flipped)", "Portrait (flipped)"]

        return modes

    @staticmethod
    def _win32_get():
        '''
        Get the primary windows display orientation
        '''
        import win32api
        import win32con

        orientation_codes = [
            (win32con.DMDO_DEFAULT, "Landscape"),
            (win32con.DMDO_90, "Portrait"),
            (win32con.DMDO_180, "Landscape (flipped)"),
            (win32con.DMDO_270, "Portrait (flipped)"),
        ]

        for code, name in orientation_codes:
            if win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS).DisplayOrientation == code:
                displayOrientation=name
        return displayOrientation

    @staticmethod
    def _win32_set(degree=None):
        '''
        Set the primary windows display to the specified mode
        '''
        # Gave up on ctypes, the struct is really complicated
        #user32.ChangeDisplaySettingsW(None, 0)
        import win32api as win32
        import win32con
        # from pywintypes import DEVMODEType
        if degree:
                try:
                    MY_SCREEN_NUMBER = 0  # Adjust the screen number if needed
                    device = win32.EnumDisplayDevices(None, MY_SCREEN_NUMBER)
                    dm = win32.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)
                    
                    new_display_orientation = degree // 90
                    current_display_orientation = dm.DisplayOrientation
                    
                    if (new_display_orientation + current_display_orientation) % 2 == 1:
                        # Swap width and height for orientations perpendicular to the previous one
                        tmp = dm.PelsHeight
                        dm.PelsHeight = dm.PelsWidth
                        dm.PelsWidth = tmp
                    
                    dm.DisplayOrientation = new_display_orientation
                    win32.ChangeDisplaySettingsEx(device.DeviceName, dm)
                    print(f"Screen rotated to {degree} degrees.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            
        else:
            win32.ChangeDisplaySettingsEx(None, 0)


    @staticmethod
    def _win32_set_default():
        '''
        Reset the primary windows display to the default mode
        '''
        # Interesting since it doesn't depend on pywin32
        import ctypes
        user32 = ctypes.windll.user32
        # set screen size
        user32.ChangeDisplaySettingsW(None, 0)

    @staticmethod
    def _linux_set(width=None, height=None, depth=32):
        raise NotImplementedError()

    @staticmethod
    def _linux_get():
        raise NotImplementedError()

    @staticmethod
    def _linux_get_modes():
        raise NotImplementedError()

    @staticmethod
    def _osx_set(width=None, height=None, depth=32):
        raise NotImplementedError()

    @staticmethod
    def _osx_get():
        raise NotImplementedError()

    @staticmethod
    def _osx_get_modes():
        raise NotImplementedError()
