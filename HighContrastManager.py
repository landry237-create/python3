import ctypes
from ctypes import wintypes

class HighContrastManager:
    SPI_GETHIGHCONTRAST = 0x42
    SPI_SETHIGHCONTRAST = 0x43
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02

    class HIGHCONTRAST(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_uint),
            ("dwFlags", ctypes.c_uint),
            ("lpszDefaultScheme", wintypes.LPCWSTR),
        ]

    
    @classmethod
    def get_high_contrast_settings(cls):
        current_settings = cls.HIGHCONTRAST()
        current_settings.cbSize = ctypes.sizeof(current_settings)
        user32 = ctypes.WinDLL('user32')
        user32.SystemParametersInfoW(cls.SPI_GETHIGHCONTRAST, current_settings.cbSize, ctypes.byref(current_settings), 0)
        return current_settings
    
    @classmethod
    def get_modes(cls):
        return ["High Contrast #1", "High Contrast #2", "High Contrast Black", "High Contrast White"]
    
    @classmethod
    def is_high_contrast_enabled(cls):
        current_settings = cls.HIGHCONTRAST()
        current_settings.cbSize = ctypes.sizeof(current_settings)
        user32 = ctypes.WinDLL('user32')
        user32.SystemParametersInfoW(cls.SPI_GETHIGHCONTRAST, ctypes.sizeof(current_settings), ctypes.byref(current_settings), 0)
        return current_settings.dwFlags & 0x1 == 0x1

    @classmethod
    def change_high_contrast_theme(cls, theme_name):
        user32 = ctypes.WinDLL('user32')
        current_settings = cls.HIGHCONTRAST()
        current_settings.cbSize = ctypes.sizeof(current_settings)
        
        # Get the current high contrast settings
        user32.SystemParametersInfoW(cls.SPI_GETHIGHCONTRAST, current_settings.cbSize, ctypes.byref(current_settings), 0)

        # Modify the high contrast settings
        current_settings.lpszDefaultScheme = theme_name
        user32.SystemParametersInfoW(cls.SPI_SETHIGHCONTRAST, current_settings.cbSize, ctypes.byref(current_settings), cls.SPIF_UPDATEINIFILE | cls.SPIF_SENDCHANGE)

    @classmethod
    def toggle_high_contrast(cls, enable, theme_name=None):
        user32 = ctypes.WinDLL('user32')
        
        if enable:
            if cls.is_high_contrast_enabled():
                if theme_name:
                    cls.change_high_contrast_theme(theme_name)
            else:
                if theme_name:
                    # Enable high contrast and set the theme
                    high_contrast_settings = cls.HIGHCONTRAST()
                    high_contrast_settings.cbSize = ctypes.sizeof(high_contrast_settings)
                    high_contrast_settings.dwFlags = 0x1  # Enable high contrast
                    high_contrast_settings.lpszDefaultScheme = theme_name
                    user32.SystemParametersInfoW(cls.SPI_SETHIGHCONTRAST, high_contrast_settings.cbSize, ctypes.byref(high_contrast_settings), cls.SPIF_UPDATEINIFILE | cls.SPIF_SENDCHANGE)
                else:
                    # Enable high contrast without changing the theme
                    high_contrast_settings = cls.HIGHCONTRAST()
                    high_contrast_settings.cbSize = ctypes.sizeof(high_contrast_settings)
                    high_contrast_settings.dwFlags = 0x1  # Enable high contrast
                    user32.SystemParametersInfoW(cls.SPI_SETHIGHCONTRAST, high_contrast_settings.cbSize, ctypes.byref(high_contrast_settings), cls.SPIF_UPDATEINIFILE | cls.SPIF_SENDCHANGE)
        else:
            # Disable high contrast
            high_contrast_settings = cls.HIGHCONTRAST()
            high_contrast_settings.cbSize = ctypes.sizeof(high_contrast_settings)
            high_contrast_settings.dwFlags = 0  # Disable high contrast
            user32.SystemParametersInfoW(cls.SPI_SETHIGHCONTRAST, high_contrast_settings.cbSize, ctypes.byref(high_contrast_settings), cls.SPIF_UPDATEINIFILE | cls.SPIF_SENDCHANGE)
