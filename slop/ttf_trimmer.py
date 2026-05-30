"""
Font subsetting script
Keeps only characters from common_chinese_chars.txt plus the full Latin range
"""

import os
import shutil
from pathlib import Path
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont

# Paths
SCRIPT_DIR = Path(__file__).parent
CHARS_FILE = SCRIPT_DIR / "insert_chars.txt"
FONT_FILE = SCRIPT_DIR / "Font.ttf"
OUTPUT_FONT = SCRIPT_DIR / "Font.ttf"

def read_chars():
    """Read characters from the common_chinese_chars.txt file"""
    with open(CHARS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Characters can be space-separated or contiguous (no spaces)
    # Simply iterate through every character and skip whitespace
    chars = []
    for char in content:
        if not char.isspace():  # Skip all whitespace (spaces, newlines, tabs, etc)
            chars.append(char)
    
    return chars

def subset_font():
    # Subset the font to keep only specified characters
    print(f"Reading characters from {CHARS_FILE}...")
    chars_list = read_chinese_chars()
    chars_list = " ".join(chars_list)
    print(f"Found {len(chars_list)} characters")
    
    # Build the codepoint set to keep
    codepoints_to_keep = set()
    
    # Add full Latin range (includes ASCII and extended Latin)
    for i in range(0x0000, 0x0180):
        codepoints_to_keep.add(i)
    
    # Add all other characters (convert to codepoints)
    for char in chars_list:
        codepoints_to_keep.add(ord(char))

    # --- FOR ADDING CJK RELATED CHARACTERS ---
    
    # Add Hiragana range (U+3040-U+309F)
    print("Adding Hiragana characters...")
    for i in range(0x3040, 0x30A0):
        codepoints_to_keep.add(i)
    
    # Add Katakana range (U+30A0-U+30FF)
    print("Adding Katakana characters...")
    for i in range(0x30A0, 0x3100):
        codepoints_to_keep.add(i)
    
    # Add all CJK Unified Ideographs (covers both Chinese Hanzi and Japanese Kanji)
    print("Adding CJK Unified Ideographs (Chinese + Japanese Kanji)...")
    for i in range(0x4E00, 0x9FFF):
        codepoints_to_keep.add(i)
    
    # Add essential fullwidth punctuation for Chinese/Japanese
    print("Adding fullwidth punctuation...")
    essential_punctuation = {
        0xFF0C,  # ， Fullwidth Comma
        0xFF1A,  # ： Fullwidth Colon
        0xFF01,  # ！ Fullwidth Exclamation Mark
        0xFF1F,  # ？ Fullwidth Question Mark
        0x3002,  # 。Ideographic Full Stop
        0x3001,  # 、Ideographic Comma
    }
    codepoints_to_keep.update(essential_punctuation)
    
    print(f"\nTotal codepoints to keep: {len(codepoints_to_keep)}")
    print(f"Latin range: U+0000-U+017F")
    print(f"Hiragana: U+3040-U+309F")
    print(f"Katakana: U+30A0-U+30FF")
    print(f"CJK Unified Ideographs: U+4E00-U+9FFF")
    print(f"Fullwidth Punctuation: ， ： ！ ？ 。 、")
    
    # Create backup if it doesn't exist
    backup_file = FONT_FILE.with_stem(FONT_FILE.stem + ".backup")
    if not backup_file.exists() and OUTPUT_FONT.exists():
        print(f"\nCreating backup: {backup_file}")
        shutil.copy2(OUTPUT_FONT, backup_file)
        original_size = os.path.getsize(backup_file)
    else:
        original_size = os.path.getsize(OUTPUT_FONT) if OUTPUT_FONT.exists() else 0
    
    # Load the font
    print(f"\nLoading font from {OUTPUT_FONT}...")
    font = TTFont(str(OUTPUT_FONT))
    print(f"Font loaded. Total glyphs: {len(font.getGlyphOrder())}")
    
    # Create subsetter and add codepoints to keep
    print(f"Subsetting font with {len(codepoints_to_keep)} codepoints...")
    subsetter = Subsetter()
    subsetter.populate(unicodes=codepoints_to_keep)
    
    # Subset the font
    print("Running subset...")
    subsetter.subset(font)
    print(f"After subset. Total glyphs: {len(font.getGlyphOrder())}")
    
    # Save the subset font
    print(f"Saving subset font...")
    font.save(str(OUTPUT_FONT))
    
    # Print file size comparison
    new_size = os.path.getsize(OUTPUT_FONT)
    
    print(f"✓ Font subset complete!")
    if original_size > 0:
        reduction = ((original_size - new_size) / original_size) * 100
        print(f"Original size: {original_size / 1024 / 1024:.2f} MB")
        print(f"New size: {new_size / 1024 / 1024:.2f} MB")
        print(f"Reduction: {reduction:.1f}%")
    else:
        print(f"New size: {new_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    try:
        subset_font()
    except ImportError:
        print("Error: fonttools is not installed")
        print("Install it with: pip install fonttools")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
