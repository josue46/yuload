#!/usr/bin/env python3
"""Test de validation du code Yuload (sans interface graphique)"""

import sys
import ast
from pathlib import Path

def check_python_syntax(file_path):
    """Vérifie la syntaxe Python d'un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def main():
    """Teste tous les fichiers Python"""
    yuload_dir = Path(__file__).parent / "yuload"
    
    print("=" * 60)
    print("VALIDATION DE LA SYNTAXE PYTHON - YULOAD")
    print("=" * 60)
    print()
    
    # Fichiers à vérifier
    files_to_check = [
        "utils/config.py",
        "utils/logger.py",
        "utils/http.py",
        "utils/validators.py",
        "core/youtube_handler.py",
        "core/downloader.py",
        "ui/styles.py",
        "ui/widgets.py",
        "ui/main_window.py",
    ]
    
    errors = []
    
    for file_name in files_to_check:
        file_path = yuload_dir / file_name
        
        if not file_path.exists():
            print(f"✗ {file_name:35s} - FICHIER NON TROUVÉ")
            errors.append(file_name)
            continue
        
        success, error = check_python_syntax(file_path)
        
        if success:
            print(f"✓ {file_name:35s} - OK")
        else:
            print(f"✗ {file_name:35s} - ERREUR")
            print(f"   {error}")
            errors.append(file_name)
    
    print()
    print("=" * 60)
    
    if errors:
        print(f"❌ {len(errors)} erreur(s) détectée(s):")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print("✅ TOUS LES FICHIERS SONT VALIDES!")
        print("")
        print("L'application est prête à être lancée :")
        print("  python3 main.py")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
