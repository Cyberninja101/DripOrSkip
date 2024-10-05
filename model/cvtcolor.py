def hsl_to_rgb(h, s, l):
    """
    Convert HSL to RGB.

    Parameters:
    h (float): Hue value (0-360)
    s (float): Saturation value (0-1)
    l (float): Lightness value (0-1)

    Returns:
    tuple: Corresponding RGB values (r, g, b) in the range of 0-255
    """
    if s == 0:  # Achromatic (gray)
        r = g = b = int(round(l * 255))
        return (r, g, b)

    # Helper function to convert hue to RGB
    def hue_to_rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q

    r = int(round(hue_to_rgb(p, q, h / 360 + 1 / 3) * 255))
    g = int(round(hue_to_rgb(p, q, h / 360) * 255))
    b = int(round(hue_to_rgb(p, q, h / 360 - 1 / 3) * 255))

    # Ensure RGB values are within the range [0, 255]
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return (r, g, b)


def rgb_to_hsl(r, g, b):
    """
    Convert RGB to HSL.

    Parameters:
    r (int): Red value (0-255)
    g (int): Green value (0-255)
    b (int): Blue value (0-255)

    Returns:
    tuple: Corresponding HSL values (h, s, l)
    """
    r /= 255.0
    g /= 255.0
    b /= 255.0

    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn

    # Calculate Lightness
    l = (mx + mn) / 2

    if diff == 0:  # Achromatic
        h = s = 0
    else:
        # Calculate Saturation
        s = diff / (1 - abs(2 * l - 1))

        # Calculate Hue
        if mx == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:  # mx == b
            h = (60 * ((r - g) / diff) + 240) % 360

    h = round(h, 2)
    s = round(s, 2)
    l = round(l, 2)

    return (h, s, l)


def generate_color_picker(h, s, l):
    colormatch = dict()
    colormatch["complementary"] = [((h+180)%360, s, l)]
    colormatch["split"] = [((h+150)%360, s, l), ((h+210)%360, s, l)]
    colormatch["analogous"] = [((h + 30) % 360, s, l), ((h + 390) % 360, s, l)]
    colormatch["tints"] = [(h, s, l + ((1-l)/10)*i) for i in range(1,10)]
    colormatch["shades"] = [(h, s, l - ((1 - l) / 10) * i) for i in range(1, 10)]
    return colormatch