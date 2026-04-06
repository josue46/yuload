"""Custom widgets for Yuload UI"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from .styles import Colors, StyleManager


class ModernButton(tk.Canvas):
    """Modern custom button with hover effects"""
    
    def __init__(self, parent, text="", command=None, width=200, height=40, 
                 bg_color=Colors.ACCENT, hover_color=None, **kwargs):
        """Initialize modern button"""
        super().__init__(parent, width=width, height=height, bg=Colors.PRIMARY, 
                        highlightthickness=0, **kwargs)
        
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.hover_color = hover_color or self._lighten_color(bg_color)
        self.current_bg = bg_color
        self.is_hovered = False
        
        # Bind events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        
        self.draw_button()
    
    def draw_button(self):
        """Draw button"""
        self.delete("all")
        
        # Draw background rectangle with rounded corners
        radius = 5
        self.create_arc(0, 0, radius*2, radius*2, fill=self.current_bg, 
                       outline="", start=90, extent=90)
        self.create_arc(self.width-radius*2, 0, self.width, radius*2, 
                       fill=self.current_bg, outline="", start=0, extent=90)
        self.create_arc(self.width-radius*2, self.height-radius*2, self.width, 
                       self.height, fill=self.current_bg, outline="", start=270, extent=90)
        self.create_arc(0, self.height-radius*2, radius*2, self.height, 
                       fill=self.current_bg, outline="", start=180, extent=90)
        
        self.create_rectangle(radius, 0, self.width-radius, self.height, 
                            fill=self.current_bg, outline="")
        self.create_rectangle(0, radius, self.width, self.height-radius, 
                            fill=self.current_bg, outline="")
        
        # Draw text
        self.create_text(self.width/2, self.height/2, text=self.text, 
                        font=StyleManager.default_font(11, bold=True),
                        fill=Colors.TEXT_PRIMARY)
    
    def _on_enter(self, event):
        """Handle mouse enter"""
        self.is_hovered = True
        self.current_bg = self.hover_color
        self.draw_button()
    
    def _on_leave(self, event):
        """Handle mouse leave"""
        self.is_hovered = False
        self.current_bg = self.bg_color
        self.draw_button()
    
    def _on_click(self, event):
        """Handle click"""
        if self.command:
            self.command()
    
    @staticmethod
    def _lighten_color(color):
        """Lighten a hex color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)


class AnimatedProgressBar(tk.Canvas):
    """Modern animated progress bar"""
    
    def __init__(self, parent, width=400, height=6, bg_color=Colors.SECONDARY, 
                 progress_color=Colors.ACCENT, **kwargs):
        """Initialize progress bar"""
        super().__init__(parent, width=width, height=height, bg=bg_color, 
                        highlightthickness=0, **kwargs)
        
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.progress_color = progress_color
        self.progress = 0
        self.animation_frame = 0
        
        self.configure(bg=Colors.PRIMARY)
    
    def set_progress(self, value: float):
        """
        Set progress value (0-100)
        
        Args:
            value: Progress percentage
        """
        self.progress = max(0, min(100, value))
        self.draw_progress()
    
    def draw_progress(self):
        """Draw progress bar"""
        self.delete("all")
        
        # Background
        self.create_rectangle(0, 0, self.width, self.height, 
                            fill=self.bg_color, outline=Colors.SECONDARY)
        
        # Progress
        progress_width = (self.progress / 100) * self.width
        self.create_rectangle(0, 0, progress_width, self.height, 
                            fill=self.progress_color, outline="")
        
        # Animated shine effect
        shine_width = 20
        self.animation_frame = (self.animation_frame + 1) % 100
        shine_x = (self.animation_frame / 100) * self.width
        
        if shine_x < self.width:
            self.create_rectangle(shine_x, 0, shine_x + shine_width, self.height,
                                fill="white", outline="", stipple="gray50")


class LoadingSpinner(tk.Canvas):
    """Spinner de chargement animé avec couleur dynamique"""
    
    def __init__(self, parent, size=30, color=Colors.ACCENT, **kwargs):
        """
        Initialise le spinner de chargement
        
        Args:
            parent: Widget parent
            size: Taille du spinner en pixels
            color: Couleur du spinner (bleu par défaut)
        """
        super().__init__(parent, width=size, height=size, bg=Colors.PRIMARY, 
                        highlightthickness=0, **kwargs)
        
        self.size = size
        self.color = color
        self.animation_frame = 0
        self.is_loading = False
        self.is_complete = False
    
    def start_loading(self):
        """Démarre l'animation de chargement en bleu"""
        self.is_loading = True
        self.is_complete = False
        self.color = Colors.ACCENT  # Bleu
        self.animate()
    
    def complete_loading(self):
        """Marque comme chargement complété et change la couleur en vert"""
        self.is_loading = False
        self.is_complete = True
        self.color = Colors.SUCCESS  # Vert
        self.draw_checkmark()
    
    def animate(self):
        """Anime le spinner"""
        if not self.is_loading:
            return
        
        self.draw_spinner()
        self.animation_frame = (self.animation_frame + 1) % 12
        # Appeler la prochaine animation après 100ms
        self.after(100, self.animate)
    
    def draw_spinner(self):
        """Dessine un spinner animé"""
        self.delete("all")
        
        center_x = self.size / 2
        center_y = self.size / 2
        radius = self.size / 3
        
        # Dessiner 12 segments du spinner
        for i in range(12):
            angle = (i + self.animation_frame) * 30
            import math
            x1 = center_x + radius * math.cos(math.radians(angle))
            y1 = center_y + radius * math.sin(math.radians(angle))
            x2 = center_x + radius * math.cos(math.radians(angle + 20))
            y2 = center_y + radius * math.sin(math.radians(angle + 20))
            
            # Opacité dégradée pour l'effet de rotation
            opacity = int(100 + (i * 20) % 155)
            self.create_line(x1, y1, x2, y2, fill=self.color, width=3)
    
    def draw_checkmark(self):
        """Dessine une coche verte"""
        self.delete("all")
        
        center_x = self.size / 2
        center_y = self.size / 2
        radius = self.size / 3
        
        # Cercle vert
        self.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=self.color, outline=self.color
        )
        
        # Coche blanche
        self.create_line(
            center_x - radius/3, center_y,
            center_x - radius/6, center_y + radius/4,
            center_x + radius/3, center_y - radius/4,
            fill='white', width=2
        )


class VideoInfoFrame(tk.Frame):
    """Frame to display video information"""
    
    def __init__(self, parent, **kwargs):
        """Initialize info frame"""
        super().__init__(parent, bg=Colors.SECONDARY, **kwargs)
        
        # Title
        self.title_label = tk.Label(self, text="", font=StyleManager.default_font(12, bold=True),
                                   fg=Colors.TEXT_PRIMARY, bg=Colors.SECONDARY, wraplength=400)
        self.title_label.pack(pady=10, padx=10, anchor="w")
        
        # Author and duration
        self.meta_label = tk.Label(self, text="", font=StyleManager.default_font(9),
                                  fg=Colors.TEXT_SECONDARY, bg=Colors.SECONDARY, wraplength=400)
        self.meta_label.pack(pady=5, padx=10, anchor="w")
        
        # Views
        self.views_label = tk.Label(self, text="", font=StyleManager.default_font(9),
                                   fg=Colors.TEXT_SECONDARY, bg=Colors.SECONDARY)
        self.views_label.pack(pady=2, padx=10, anchor="w")
    
    def set_info(self, info: dict):
        """Set video information"""
        if not info:
            return
        
        self.title_label.config(text=info.get('title', 'Unknown Title'))
        
        author = info.get('author', 'Unknown Author')
        duration = self._format_duration(info.get('duration', 0))
        self.meta_label.config(text=f"By {author} • {duration}")
        
        views = info.get('views', 0)
        self.views_label.config(text=f"Views: {views:,}")
    
    @staticmethod
    def _format_duration(seconds: int) -> str:
        """Format duration in human readable format"""
        minutes = seconds // 60
        hours = minutes // 60
        
        if hours > 0:
            return f"{hours}h {minutes % 60}m"
        elif minutes > 0:
            return f"{minutes}m {seconds % 60}s"
        else:
            return f"{seconds}s"


class QualitySelector(tk.Frame):
    """Widget pour sélectionner la qualité vidéo"""
    
    def __init__(self, parent, on_select: Callable = None, **kwargs):
        """Initialise le sélecteur de qualité"""
        super().__init__(parent, bg=Colors.SECONDARY, **kwargs)
        
        self.on_select = on_select
        self.selected_quality = tk.StringVar()
        self.streams = []
        # Dictionnaire pour stocker les références aux boutons de qualité
        self.quality_buttons = {}
        self.selected_button = None
        
        # Étiquette pour le titre
        label = tk.Label(self, text="Sélectionner la Qualité:", 
                        font=StyleManager.default_font(10, bold=True),
                        fg=Colors.TEXT_PRIMARY, bg=Colors.SECONDARY)
        label.pack(pady=8, padx=10, anchor="w")
        
        # Frame pour les boutons de qualité
        self.buttons_frame = tk.Frame(self, bg=Colors.SECONDARY)
        self.buttons_frame.pack(pady=5, padx=10, fill="x")
    
    def set_streams(self, streams: list):
        """Définit les streams disponibles"""
        self.streams = streams
        
        # Effacer les boutons existants
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        # Réinitialiser les références aux boutons
        self.quality_buttons = {}
        self.selected_button = None
        
        if not streams:
            label = tk.Label(self.buttons_frame, text="Aucun stream disponible",
                            fg=Colors.TEXT_SECONDARY, bg=Colors.SECONDARY)
            label.pack(pady=5)
            return
        
        # Créer les boutons de qualité avec références stockées
        for i, stream in enumerate(streams[:8]):  # Limiter à 8 qualités
            quality = stream['quality']
            filesize = stream.get('filesize', 0)
            size_mb = filesize / (1024*1024) if filesize else 0
            
            btn_text = f"{quality}\n({size_mb:.1f}MB)"
            btn = tk.Button(
                self.buttons_frame,
                text=btn_text,
                font=StyleManager.default_font(9),
                bg=Colors.TERTIARY,
                fg=Colors.TEXT_PRIMARY,
                relief="flat",
                padx=10,
                pady=8,
                command=lambda q=quality: self._select_quality(q)
            )
            btn.pack(side="left", padx=5, pady=5)
            
            # Stocker la référence au bouton pour modification ultérieure
            self.quality_buttons[quality] = btn
    
    def _select_quality(self, quality: str):
        """Sélectionne une qualité et met à jour les couleurs"""
        self.selected_quality.set(quality)
        
        # Restaurer la couleur du bouton précédent (s'il existe)
        if self.selected_button and self.selected_button in self.quality_buttons.values():
            previous_quality = [q for q, btn in self.quality_buttons.items() if btn == self.selected_button][0]
            self.quality_buttons[previous_quality].config(bg=Colors.TERTIARY)
        
        # Colorer le nouveau bouton sélectionné en bleu (couleur accent)
        if quality in self.quality_buttons:
            self.selected_button = self.quality_buttons[quality]
            self.selected_button.config(bg=Colors.ACCENT)
        
        # Appeler le callback si défini
        if self.on_select:
            self.on_select(quality)
    
    def get_selected(self) -> str:
        """Récupère la qualité sélectionnée"""
        return self.selected_quality.get()
    
    def disable_buttons(self):
        """Désactive tous les boutons de qualité"""
        for btn in self.quality_buttons.values():
            btn.config(state="disabled")
    
    def enable_buttons(self):
        """Active tous les boutons de qualité"""
        for btn in self.quality_buttons.values():
            btn.config(state="normal")


class SubtitleSelector(tk.Frame):
    """Widget to select and toggle subtitles"""
    
    def __init__(self, parent, **kwargs):
        """Initialize subtitle selector"""
        super().__init__(parent, bg=Colors.SECONDARY, **kwargs)
        
        self.captions = []
        self.include_var = tk.BooleanVar(value=False)
        self.selected_caption = tk.StringVar()
        
        # Checkbox
        self.check = tk.Checkbutton(
            self, 
            text="Include Subtitles",
            font=StyleManager.default_font(10),
            bg=Colors.SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            selectcolor=Colors.ACCENT,
            variable=self.include_var,
            command=self._on_toggle,
            activebackground=Colors.SECONDARY,
            activeforeground=Colors.ACCENT
        )
        self.check.pack(pady=8, padx=10, anchor="w")
        
        # Language selector (hidden initially)
        self.selector_frame = tk.Frame(self, bg=Colors.SECONDARY)
        self.selector_frame.pack(pady=5, padx=20, anchor="w", fill="x")
        
        tk.Label(self.selector_frame, text="Language:",
                font=StyleManager.default_font(9),
                bg=Colors.SECONDARY, fg=Colors.TEXT_SECONDARY).pack(side="left", padx=5)
        
        self.dropdown = ttk.Combobox(
            self.selector_frame,
            textvariable=self.selected_caption,
            state="readonly",
            width=20
        )
        self.dropdown.pack(side="left", padx=5)
        
        self.selector_frame.pack_forget()  # Hide initially
    
    def set_captions(self, captions: list):
        """Set available captions"""
        self.captions = captions
        
        if not captions:
            self.check.config(state="disabled")
            return
        
        self.check.config(state="normal")
        
        # Populate dropdown
        caption_names = [c['language'] for c in captions]
        self.dropdown['values'] = caption_names
        if caption_names:
            self.selected_caption.set(caption_names[0])
    
    def _on_toggle(self):
        """Toggle subtitle selector visibility"""
        if self.include_var.get() and self.captions:
            self.selector_frame.pack(pady=5, padx=20, anchor="w", fill="x")
        else:
            self.selector_frame.pack_forget()
    
    def should_include(self) -> bool:
        """Check if subtitles should be included"""
        return self.include_var.get()
    
    def get_selected_code(self) -> str:
        """Get selected subtitle code"""
        selected_name = self.selected_caption.get()
        for caption in self.captions:
            if caption['language'] == selected_name:
                return caption['code']
        return ""


class StatusBar(tk.Frame):
    """Modern status bar for messages"""
    
    def __init__(self, parent, **kwargs):
        """Initialize status bar"""
        super().__init__(parent, bg=Colors.SECONDARY, height=40, **kwargs)
        
        self.message_label = tk.Label(
            self,
            text="Ready",
            font=StyleManager.default_font(9),
            bg=Colors.SECONDARY,
            fg=Colors.TEXT_SECONDARY
        )
        self.message_label.pack(pady=10, padx=10, anchor="w")
    
    def show_message(self, message: str, status_type: str = "info"):
        """
        Show status message
        
        Args:
            message: Message to display
            status_type: Type of message (info, success, error, warning)
        """
        color_map = {
            "info": Colors.TEXT_SECONDARY,
            "success": Colors.SUCCESS,
            "error": Colors.ERROR,
            "warning": Colors.WARNING,
        }
        
        color = color_map.get(status_type, Colors.TEXT_SECONDARY)
        self.message_label.config(text=message, fg=color)
    
    def clear(self):
        """Clear status message"""
        self.message_label.config(text="Ready", fg=Colors.TEXT_SECONDARY)
