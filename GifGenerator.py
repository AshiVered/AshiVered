from PIL import Image, ImageDraw, ImageFont
import os

# ==========================
#  Settings
# ==========================
# Colors
BG_COLOR = (8, 10, 12)         # Original dark background
PROMPT_COLOR = (80, 200, 120)  # Green prompt
TEXT_COLOR = (200, 200, 200)   # Standard text
CMD_COLOR = (255, 255, 255)    # Typed command color

# Neofetch Colors
NEO_CIRCLE_COLOR = (233, 84, 32) # Ubuntu Orange/Red
NEO_TEXT_COLOR = (255, 255, 255) # White (for AIV Dev)
NEO_KEY_COLOR = (233, 84, 32)    # Key color
NEO_VAL_COLOR = (255, 255, 255)  # Value color

# Animation Speed
FRAME_DURATION = 25   # Faster typing (Low number = Fast)
PAUSE_FRAMES = 15     # Pause after output

# Layout
WIDTH = 1000
PADDING = 20
FONT_SIZE = 18
FONT_PATH = "DejaVuSansMono.ttf" # Ensure this exists

# ==========================
#  1. The Clean ASCII Art
# ==========================
# Specific chars to be colored WHITE:
WHITE_CHARS = {'A', 'I', 'V', 'D', 'e', 'v'}

logo_lines = [
    "                                        ",
    "                                        ",
    "         AAA     III   V       V        ",
    "        A   A     I     V     V         ",
    "        AAAAA     I      V   V          ",
    "       A     A    I       VVV           ",
    "      A       A  III       V            ",
    "                                        ",
    "                                        ",
    "                                        ",
    "      DDDDDD     eeee  v       v        ",
    "      D     D   e       v     v         ",
    "      D     D   eeeee    v   v          ",
    "      D     D   e         vvv           ",
    "      DDDDDD    eeeee      v            ",
    "                                        ",
    "                                        ",
    "                                        ",
]

# ==========================
#  2. Neofetch Info
# ==========================
info_lines = [
    "ashivered@github",
    "----------------",
    "Identity:  Jew / 23 y.o. / Yeshiva student",
    "Languages: Hebrew / English / Aramaic",
    "Roles:     ROM Modder / App Dev / Programmer",
    "Stack:     Java / Python / SMALI",
    "Expertise: Reversing / Linux / Android",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
]

# Combine lists
neofetch_data = []
for i in range(max(len(logo_lines), len(info_lines))):
    l = logo_lines[i] if i < len(logo_lines) else " " * 40
    r = info_lines[i] if i < len(info_lines) else ""
    neofetch_data.append({"logo": l, "info": r})

# ==========================
#  3. Script Sequence
# ==========================
sequence = [
    {"type": "cmd", "text": "$ whoami"},
    {"type": "out", "text": "AshiVered"},
    {"type": "out", "text": ""},
    
    {"type": "cmd", "text": "$ neofetch"},
    {"type": "neo", "lines": neofetch_data}, 
    {"type": "out", "text": ""},

    {"type": "cmd", "text": "$ ssh read@myblog"},
    {"type": "cmd", "text": "Connecting..."},
    {"type": "cmd", "text": ".............."},
    {"type": "cmd", "text": "Done! see it at:"},
    {"type": "out", "text": "https://aiv-dev.com/he-IL/"},
    {"type": "out", "text": ""},

    {"type": "cmd", "text": "$ ls ~/top_projects"},
    {"type": "out", "text": "Android-Custom-ROMs  SkyOS  QinBoard-T9  CobaltConverter  Android-Safe-browser"},
    {"type": "out", "text": ""},

    {"type": "cmd", "text": "$ cat ~/languages.txt"},
    {"type": "out", "text": "Python  Smali  Bash  Java  Shell"},
    {"type": "out", "text": ""},

    {"type": "cmd", "text": "$ exit"}
]

# ==========================
#  Setup Font
# ==========================
if not os.path.exists(FONT_PATH):
    print(f"Warning: {FONT_PATH} not found. Using default.")
    font = ImageFont.load_default()
else:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

bbox = font.getbbox("A")
line_height = (bbox[3] - bbox[1]) + 6

# Calculate Height
total_lines = 0
for item in sequence:
    if item["type"] == "neo":
        total_lines += len(item["lines"])
    else:
        total_lines += 1
height = PADDING * 2 + line_height * (total_lines + 5)

# ==========================
#  Drawing Helper
# ==========================
def draw_neofetch_row(draw, y, logo_str, info_str, font):
    """Draws a single row of the neofetch output with specific coloring."""
    x = PADDING
    
    # 1. Draw Logo
    for char in logo_str:
        # STRICT COLORING LOGIC:
        # Only specific chars from the set WHITE_CHARS are white.
        # Everything else (circles, background letters) is RED.
        if char in WHITE_CHARS: 
            color = NEO_TEXT_COLOR
        elif char.strip() == "":
            color = BG_COLOR
        else:
            color = NEO_CIRCLE_COLOR
            
        draw.text((x, y), char, font=font, fill=color)
        x += font.getlength(char)

    # 2. Draw Info
    logo_width_pixels = font.getlength(" " * 44) 
    x = PADDING + logo_width_pixels
    
    if ":" in info_str:
        parts = info_str.split(":", 1)
        key_txt = parts[0] + ":"
        val_txt = parts[1]
        
        draw.text((x, y), key_txt, font=font, fill=NEO_KEY_COLOR)
        x += font.getlength(key_txt)
        draw.text((x, y), val_txt, font=font, fill=NEO_VAL_COLOR)
    else:
        color = NEO_KEY_COLOR if ("@" in info_str or "-" in info_str) else NEO_VAL_COLOR
        draw.text((x, y), info_str, font=font, fill=color)

# ==========================
#  Main Loop
# ==========================
frames = []
history = [] 

print("Rendering frames...")

for step in sequence:
    
    # --- Neofetch Block ---
    if step["type"] == "neo":
        for row in step["lines"]:
            history.append({"type": "neo_row", "data": row})
            
            img = Image.new("RGB", (WIDTH, height), color=BG_COLOR)
            draw = ImageDraw.Draw(img)
            
            cy = PADDING
            for h in history:
                if h["type"] == "neo_row":
                    draw_neofetch_row(draw, cy, h["data"]["logo"], h["data"]["info"], font)
                else:
                    c = PROMPT_COLOR if h["text"].startswith("$") else TEXT_COLOR
                    draw.text((PADDING, cy), h["text"], font=font, fill=c)
                cy += line_height
            
            frames.append(img)
        
        for _ in range(PAUSE_FRAMES):
            frames.append(frames[-1])
        continue

    # --- Typing Command ---
    if step["type"] == "cmd":
        full_text = step["text"]
        text_no_prompt = full_text.replace("$ ", "")
        
        for i in range(len(text_no_prompt) + 1):
            current_typing = "$ " + text_no_prompt[:i]
            
            img = Image.new("RGB", (WIDTH, height), color=BG_COLOR)
            draw = ImageDraw.Draw(img)
            
            cy = PADDING
            for h in history:
                if h["type"] == "neo_row":
                    draw_neofetch_row(draw, cy, h["data"]["logo"], h["data"]["info"], font)
                else:
                    c = PROMPT_COLOR if h["text"].startswith("$") else TEXT_COLOR
                    draw.text((PADDING, cy), h["text"], font=font, fill=c)
                cy += line_height
            
            draw.text((PADDING, cy), current_typing, font=font, fill=PROMPT_COLOR)
            frames.append(img)
        
        history.append({"type": "std", "text": full_text})
        continue

    # --- Output ---
    if step["type"] == "out":
        history.append({"type": "std", "text": step["text"]})
        
        img = Image.new("RGB", (WIDTH, height), color=BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        cy = PADDING
        for h in history:
            if h["type"] == "neo_row":
                draw_neofetch_row(draw, cy, h["data"]["logo"], h["data"]["info"], font)
            else:
                c = PROMPT_COLOR if h["text"].startswith("$") else TEXT_COLOR
                draw.text((PADDING, cy), h["text"], font=font, fill=c)
            cy += line_height
        
        frames.append(img)
        
        if step["text"].strip() != "":
            for _ in range(PAUSE_FRAMES):
                frames.append(frames[-1])

# Final Hold
for _ in range(50):
    frames.append(frames[-1])

# Save
out_gif = "terminal_final.gif"
print(f"Saving {out_gif}...")
frames[0].save(out_gif, save_all=True, append_images=frames[1:], optimize=False, duration=FRAME_DURATION, loop=0)
print("Done.")