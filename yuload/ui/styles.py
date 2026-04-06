"""Styles and themes for Yuload UI"""

from ..utils.config import Config


class StyleManager:
    """Manage application styles and colors"""
    
    @staticmethod
    def default_font(size=Config.FONT_SIZE_LABEL, bold=False, family=None):
        """Get default font tuple"""
        if family is None:
            family = Config.FONT_FAMILY
        weight = "bold" if bold else "normal"
        return (family, size, weight)
    
    @staticmethod
    def configure_styles(root):
        """Configure ttk styles"""
        from tkinter import ttk
        
        style = ttk.Style()
        
        # Use modern theme
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Configure colors
        style.configure('TButton', foreground=Config.FG_PRIMARY)
        style.configure('TLabel', foreground=Config.FG_PRIMARY)
        style.configure('TFrame', background=Config.BG_PRIMARY)
        
        return style


class Colors:
    """Color constants"""
    PRIMARY = Config.BG_PRIMARY
    SECONDARY = Config.BG_SECONDARY
    TERTIARY = Config.BG_TERTIARY
    TEXT_PRIMARY = Config.FG_PRIMARY
    TEXT_SECONDARY = Config.FG_SECONDARY
    ACCENT = Config.ACCENT_COLOR
    ERROR = Config.ERROR_COLOR
    SUCCESS = Config.SUCCESS_COLOR
    WARNING = Config.WARNING_COLOR
