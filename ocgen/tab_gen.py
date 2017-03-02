from PIL import Image

def get_image_12_hole(num: int):
    if num > 21 or num < 1:
        raise ValueError("Number must be between 0 and 21")
    
    y_const = 119
    x_const = 129
    x_val = 0
    if num > 11:
        y_val = 119
        num -= 11
    else:
        y_val = 0

    for i in range(0, num):
        x_val += x_const

    img = Image.open("images/ocarinanotes.png")
    box = (y_val, x_val-x_const, y_val+y_const, y_val)

    return img.crop(box)


