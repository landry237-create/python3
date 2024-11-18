#coding: utf-8

from __future__ import print_function
import sys

class Luminosity(object):
    @classmethod
    def set(cls, value=None):
        '''
        Set the primary display to the specified mode
        '''
        if value:
            print('Setting brightness to {}'.format(value))
        else:
            print('Setting brightness to defaults')

        if sys.platform == 'win32':
            cls._win32_set(value)
        elif sys.platform.startswith('linux'):
            cls._linux_set(value)
        elif sys.platform.startswith('darwin'):
            cls._osx_set(value)
    
    @classmethod
    def get(cls):
        if sys.platform == 'win32':
            return cls._win32_get()
        elif sys.platform.startswith('linux'):
            return cls._linux_get()
        elif sys.platform.startswith('darwin'):
            return cls._osx_get()

    @staticmethod
    def _win32_get():
        '''
        Get the primary windows display brightness
        '''
        from screen_brightness_control import get_brightness
        
        bright=get_brightness(display=0)[0]
        
        return bright

    @staticmethod
    def _win32_set(value=None):
        '''
        Set the primary windows display to the specified mode
        '''
        # Gave up on ctypes, the struct is really complicated
        #user32.ChangeDisplaySettingsW(None, 0)
        from screen_brightness_control import set_brightness
        
        if value:
                set_brightness(value)
            
        else:
            set_brightness(0)


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
    def _linux_set(value):
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


if __name__ == '__main__':
    print(Luminosity.get())