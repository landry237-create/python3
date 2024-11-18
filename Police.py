from __future__ import print_function
import sys
import win32api
import win32con


class Police(object):
    @classmethod
    def set(cls, value=None):
        pass
    
    @classmethod
    def get(cls):
        pass
    
    @classmethod
    def get_modes(cls):
        if sys.platform=="win32":
            return cls._win32_get_modes()
        
    @staticmethod
    def _win32_get_modes():
        fonts = []
        key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts")
        try:
            for i in range(win32api.RegQueryInfoKey(key)[1]):
                font = win32api.RegEnumValue(key, i)
                fonts.append(font[0])
        except Exception as e:
            print(f"Error: {e}")
        win32api.RegCloseKey(key)
        fonts.sort()
        return fonts