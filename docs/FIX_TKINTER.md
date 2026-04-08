# Correction du Bug Tkinter - height dans tk.Entry

## Problème Initial

```
_tkinter.TclError: unknown option "-height"
```

**Cause:** Le widget `tk.Entry` ne supporte pas l'option `height`. Seuls les widgets multi-lignes comme `tk.Text`, `tk.Listbox` supportent cette option.

---

## Solution Appliquée

### Changement dans `yuload/ui/main_window.py`

**Avant:** Utilisation de `tk.Entry` avec `height=2`
```python
self.url_entry = tk.Entry(
    url_frame,
    font=StyleManager.default_font(10),
    bg=Colors.SECONDARY,
    fg=Colors.TEXT_PRIMARY,
    insertbackground=Colors.ACCENT,
    relief="flat",
    bd=0,
    height=2  # ERREUR : Entry ne supporte pas height
)
```

**Après:** Utilisation de `tk.Text` qui supporte `height` et `wrap`
```python
# Champ de texte pour l'URL (utilise tk.Text au lieu de tk.Entry pour supporter height)
self.url_entry = tk.Text(
    url_frame,
    font=StyleManager.default_font(10),
    bg=Colors.SECONDARY,
    fg=Colors.TEXT_PRIMARY,
    insertbackground=Colors.ACCENT,
    relief="flat",
    bd=0,
    height=2,  # Text supporte height
    wrap="word"
)
```

**Avantages de `tk.Text` :**
- Supporte `height` (hauteur en lignes)
- Supporte multi-ligne (permet copier/coller d'URLs longues)
- Supporte `wrap="word"` pour retour à la ligne automatique
- Meilleure UX pour les URLs longues

---

### Correction de la Lecture du Contenu

**Avant:** 
```python
url = self.url_entry.get().strip()  # Entry.get() retourne une chaîne
```

**Après:**
```python
# Récupérer l'URL depuis Text widget (utiliser "1.0" "end-1c" pour éviter le newline final)
url = self.url_entry.get("1.0", "end-1c").strip()  # Text.get(start, end)
```

**Explication:**
- `"1.0"` : Commence à la ligne 1, colonne 0 (premier caractère)
- `"end-1c"` : Finit à la fin MOINS 1 caractère (pour éviter le newline final)
- Récupère le texte sans le newline automatique ajouté par `tk.Text`

---

## Résultats

### Fichiers Validés (Syntaxe Python)
```
Tous les fichiers Python compilent sans erreur
```

### Statut
- Erreur TclError résolue
- Tous les fichiers Python compilent sans erreur
- Application prête à lancer (nécessite Tkinter)

---

## Commandes

### Pour tester la syntaxe
```bash
python3 test_syntax.py
```

### Pour lancer l'application
```bash
python3 main.py
```

### Avec uv
```bash
uv run python3 main.py
```

---

Commentaires en Français Ajoutés

Toutes les lignes de code sensibles ont des commentaires en français expliquant leur importance :

```python
# Champ de texte pour l'URL (utilise tk.Text au lieu de tk.Entry pour supporter height)
self.url_entry = tk.Text(...)

# Récupérer l'URL depuis Text widget (utiliser "1.0" "end-1c" pour éviter le newline final)
url = self.url_entry.get("1.0", "end-1c").strip()

# Charger la vidéo dans un thread séparé pour ne pas bloquer l'interface
threading.Thread(target=self._load_video_thread, args=(url,), daemon=True).start()
```

---

Le code est maintenant prêt à être utilisé avec Tkinter installé !
