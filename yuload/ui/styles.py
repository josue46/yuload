"""Themes et styles pour l'application"""

from ..utils.config import Config


class StyleManager:
    """Gère les styles et couleurs de l'application"""
    
    @staticmethod
    def default_font(size=Config.FONT_SIZE_LABEL, bold=False, family=None):
        """Obtient le tuple de la police par défaut"""
        if family is None:
            family = Config.FONT_FAMILY
        weight = "bold" if bold else "normal"
        return (family, size, weight)
    
    @staticmethod
    def configure_styles(root):
        """Configurer les styles ttk"""
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
