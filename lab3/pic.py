from PIL import Image
from itertools import product

BYTES_LENGTH = 7

def main():
    image = Image.open("Picture1.jpg")
    pixs = image.load()
    x = []
    y = ""
    h, w = image.height, image.width
    for pos in product(range(w), range(h)):
        (r,g,b) = pixs[pos]
        x.append(r%2)
        x.append(g%2)
        x.append(b%2)
    for i in range(0, len(x), BYTES_LENGTH):
        n = 0
        count = 0
        while count < BYTES_LENGTH and i+count < len(x):
            n *= 2
            n += x[i+count]
            count += 1
        y += chr(n)
    print(y)

if __name__ == '__main__':
    main()


