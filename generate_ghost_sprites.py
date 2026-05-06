# from PIL import Image
# import os
# import shutil

# BASE = os.path.join(os.path.dirname(__file__), "characters", "pacman-art", "ghosts")
# OLD = BASE  # existing flat folder

# GHOSTS = {
#     "blinky": "blinky.png",
#     "pinky":  "pinky.png",
#     "inky":   "inky.png",
#     "clyde":  "clyde.png",
# }
# SCARED_BLUE  = "blue_ghost.png"

# def make_frame2(img: Image.Image) -> Image.Image:
#     """Alternate leg position: swap solid/transparent in bottom 2 rows to simulate walking."""
#     frame2 = img.copy()
#     pixels = frame2.load()
#     w, h = frame2.size

#     # Collect the body color (most common non-transparent pixel)
#     colors = {}
#     for y in range(h - 4):
#         for x in range(w):
#             r, g, b, a = pixels[x, y]
#             if a > 0:
#                 colors[(r, g, b)] = colors.get((r, g, b), 0) + 1
#     body_color = max(colors, key=colors.get) + (255,)

#     transparent = (0, 0, 0, 0)

#     # Row h-2 (row 14): shift gaps right by 1 to alternate "foot" position
#     row14 = [pixels[x, h - 2] for x in range(w)]
#     # shift the pattern left by 1 (wrapping within body boundaries)
#     shifted14 = [row14[(x + 1) % w] for x in range(w)]
#     for x in range(w):
#         pixels[x, h - 2] = shifted14[x]

#     # Row h-1 (row 15): invert transparent/solid within body area
#     for x in range(w):
#         r, g, b, a = pixels[x, h - 1]
#         if a == 0:
#             pixels[x, h - 1] = body_color
#         else:
#             pixels[x, h - 1] = transparent

#     return frame2

# def make_white_ghost(img: Image.Image) -> Image.Image:
#     """Replace blue tones with white, keep eyes and transparent pixels."""
#     white = img.copy()
#     pixels = white.load()
#     w, h = white.size
#     for y in range(h):
#         for x in range(w):
#             r, g, b, a = pixels[x, y]
#             if a == 0:
#                 continue
#             # Blue ghost body: blue channel dominant
#             if b > r and b > g:
#                 pixels[x, y] = (255, 255, 255, a)
#             # Dark blue outline -> dark grey
#             elif b > 80 and r < 100 and g < 100:
#                 pixels[x, y] = (180, 180, 180, a)
#     return white

# # Create folder structure
# for ghost in GHOSTS:
#     os.makedirs(os.path.join(BASE, ghost), exist_ok=True)
# os.makedirs(os.path.join(BASE, "scared"), exist_ok=True)

# # Generate ghost frames
# for ghost, filename in GHOSTS.items():
#     src = os.path.join(OLD, filename)
#     if not os.path.exists(src):
#         print(f"Missing: {src}")
#         continue
#     img = Image.open(src).convert("RGBA")
#     img.save(os.path.join(BASE, ghost, "1.png"))
#     make_frame2(img).save(os.path.join(BASE, ghost, "2.png"))
#     print(f"Created {ghost}/1.png and {ghost}/2.png")

# # Generate scared frames (blue + white)
# blue_src = os.path.join(OLD, SCARED_BLUE)
# if os.path.exists(blue_src):
#     blue = Image.open(blue_src).convert("RGBA")
#     blue.save(os.path.join(BASE, "scared", "blue_1.png"))
#     make_frame2(blue).save(os.path.join(BASE, "scared", "blue_2.png"))
#     white = make_white_ghost(blue)
#     white.save(os.path.join(BASE, "scared", "white_1.png"))
#     make_frame2(white).save(os.path.join(BASE, "scared", "white_2.png"))
#     print("Created scared/blue_1.png, blue_2.png, white_1.png, white_2.png")

# print("Done.")
