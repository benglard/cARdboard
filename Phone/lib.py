# Thanks to http://stackoverflow.com/questions/12943410/opencv-python-single-rather-than-multiple-blob-tracking
# for inspiration

import cv2
from sys import argv
from base64 import decodestring
from numpy import array, uint8

data = array(bytearray(decodestring(argv[1])), dtype=uint8)
img = cv2.imdecode(data, 1)

data = array(bytearray(decodestring(argv[2])), dtype=uint8)
past_img = cv2.imdecode(data, 1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_past = cv2.cvtColor(past_img, cv2.COLOR_BGR2GRAY)
diff = gray - gray_past
l = diff < 100
g = diff > 200
diff[l] = 0
diff[g] = 0
bl = cv2.blur(diff, (3,3))

cs, hr = cv2.findContours(bl, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
areas = [ cv2.contourArea(c) for c in cs ]
ma = max(areas)
bc = cs[areas.index(ma)]
M = cv2.moments(bc)
cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

cv2.circle(img, (cx, cy), 5, 255, -1)
cv2.imwrite('./Phone/o.jpeg', img)

print '{},{}'.format(cx, cy)