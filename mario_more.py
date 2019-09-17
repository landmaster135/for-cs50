h = 0
between = 2

while (h < 1 or h > 8):  # Height is between 1 and 8.
    h = str(h)
    h = input('Height: ')  # Prompt height.
    if str.isnumeric(h) == True:  # h is number or not.
        h = int(h)
    else:
        h = 0
        h = int(h)

for i in range(1, (h + 1)):  # loop by Height.
    # x number Height from over owns (Height - x) * 2 spaces, x * 2 blocks and (between) spaces.
    print(' ' * (h - i) + '#' * i + ' ' * between + '#' * i)
