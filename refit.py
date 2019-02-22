#
# Example usage:
#
# python refit.py source.png converted.png 5 61
#                                          ^ ^-- rows (number of characters)
#                                          |
#                                          `---- cols (animations steps)
#
# This scripts expects a file generated by
# https://github.com/opendatacity/splitflap
# 
import sys
from PIL import Image

out_name = sys.argv[2]
anims = int(sys.argv[3])
chars = int(sys.argv[4])
im = Image.open(sys.argv[1])

w, h = im.size

print('total tiles = %d' % (anims * chars,))

char_w = w / anims
char_h = h / chars
assert(w % anims == 0)
assert(h % chars == 0)

per_row = 2048 / char_w
num_rows = (anims * chars) / per_row + 1

out = Image.new(im.mode, (per_row * char_w, num_rows * char_h))
out_n = 0
for y in range(chars):
    for x in range(anims):
        char = im.crop((x * char_w, y * char_h, (x+1) * char_w , (y+1) * char_h))
        target_x = out_n % per_row * char_w
        target_y = out_n / per_row * char_h
        # char.save("foo-%d-%d.png" % (target_x, target_y))
        out.paste(char, (target_x, target_y))
        out_n += 1
print("""
    rows = %d,
    cols = %d,
    width = %d,
    height = %d,
    steps = %d,
""" % (num_rows, per_row, per_row * char_w, num_rows * char_h, anims))
out.save(out_name)
