from PIL import Image, ImageDraw, ImageFont
import os

# ==========================
#  Settings
# ==========================
# Colors
BG_COLOR = (8, 10, 12)
PROMPT_COLOR = (80, 200, 120)
TEXT_COLOR = (200, 200, 200)
CMD_COLOR = (255, 255, 255)

# Neofetch Colors
NEO_CIRCLE_COLOR = (233, 84, 32)
NEO_TEXT_COLOR = (255, 255, 255)
NEO_KEY_COLOR = (233, 84, 32)
NEO_VAL_COLOR = (255, 255, 255)

# Animation Speed
FRAME_DURATION = 25
PAUSE_FRAMES = 15

# Layout
WIDTH = 1000
PADDING = 20
FONT_SIZE = 18
FONT_PATH = "DejaVuSansMono.ttf"

# ==========================
#  1. The Clean ASCII Art
# ==========================
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
    # שים לב: השימוש ב-\n יישאר כאן, והקוד למטה יטפל בפיצול
    {"type": "out", "text": "Android-Custom-ROMs/\nSkyOS/\nQinBoard-T9/\nCobaltConverter/\nAndroid-Safe-browser/"},
    {"type": "out", "text": ""},

    {"type": "cmd", "text": "$ cat ~/languages.txt"},
    {"type": "out", "text": "•Java\n•Smali\n•Python\n•Bash\n•Shell"},
    {"type": "out", "text": ""},

    {"type": "cmd", "text": "$ su"},
    {"type": "out", "text": "Please install Magisk :)"},
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

# ==========================
#  TIKUN 1: Correct Height Calculation
# ==========================
total_lines = 0
for item in sequence:
    if item["type"] == "neo":
        total_lines += len(item["lines"])
    elif "text" in item:
        # סופר כמה שורות יש בפועל כולל ירידות שורה
        # count('\n') נותן את מספר המעברים, אז מוסיפים 1 כדי לקבל את מספר השורות
        total_lines += item["text"].count('\n') + 1

# מוסיף עוד באפר קטן ליתר ביטחון
height = PADDING * 2 + line_height * (total_lines + 2)

# ==========================
#  Drawing Helper
# ==========================
def draw_neofetch_row(draw, y, logo_str, info_str, font):
    x = PADDING
    for char in logo_str:
        if char in WHITE_CHARS: 
            color = NEO_TEXT_COLOR
        elif char.strip() == "":
            color = BG_COLOR
        else:
            color = NEO_CIRCLE_COLOR
        draw.text((x, y), char, font=font, fill=color)
        x += font.getlength(char)

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
    # ==========================
    #  TIKUN 2: Split Multiline Output
    # ==========================
    if step["type"] == "out":
        # מפצלים את הטקסט לפי ירידות שורה
        # כך כל שורה מקבלת 'כניסה' משלה בהיסטוריה וגובה משלה
        lines = step["text"].split('\n')
        
        for line in lines:
            history.append({"type": "std", "text": line})
            
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
out_gif = "terminal.gif"
print(f"Saving {out_gif}...")
frames[0].save(out_gif, save_all=True, append_images=frames[1:], optimize=False, duration=FRAME_DURATION, loop=0)
print("Done.")