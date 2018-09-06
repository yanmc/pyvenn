from itertools import chain
from matplotlib.pyplot import subplots
from matplotlib import patches
from matplotlib.colors import to_rgba

DEFAULT_RGB_VALS = [
    (92, 192, 98), (90, 155, 212), (246, 236, 86),
    (241, 90, 96), (255, 117, 00), (82, 82, 190)
]

def from_colormap(cmap, n_colors, shift=0, alpha=0.7):
    """Generate colors from matplotlib colormap; pass list to use exact colors or cmap=None to fall back to default"""
    if not isinstance(n_colors, int) or (n_colors < 2) or (n_colors > 6):
        raise ValueError("n_colors must be an integer between 2 and 6")
    if not isinstance(shift, int) or (shift >= 6):
        raise ValueError("shift must be an integer smaller than 6")
    if cmap is None:
        colors = [
            [c/255 for c in rgb] + [alpha]
            for rgb in DEFAULT_RGB_VALS
        ]
    elif isinstance(cmap, list):
        colors = [to_rgba(color, alpha=alpha) for color in cmap]
    else:
        raise NotImplementedError("Generating colors from colormap")
    colors = colors[shift:] + colors[:shift]
    return colors[:n_colors]

SHAPE_COORDS = {
    2: [(.375, .5), (.625, .5)],
    3: [(.333, .633), (.666, .633), (.5, .31)],
    4: [(.35, .4), (.45, .5), (.544, .5), (.644, .4)],
    5: [(.428, .449), (.469, .543), (.558, .523), (.578, .432), (.489, .383)],
    6: [
        (.637, .921, .649, .274, .188, .667),
        (.981, .769, .335, .191, .393, .671),
        (.941, .397, .292, .475, .456, .747),
        (.662, .119, .316, .548, .662, .7),
        (.309, .081, .374, .718, .681, .488),
        (.016, .626, .726, .687, .522, .327)
    ]
}

SHAPE_DIMS = {
    2: [(.5, .5), (.5, .5)],
    3: [(.5, .5), (.5, .5), (.5, .5)],
    4: [(.72, .45), (.72, .45), (.72, .45), (.72, .45)],
    5: [(.87, .5), (.87, .5), (.87, .5), (.87, .5), (.87, .5)],
    6: [(None,)]*6
}

SHAPE_ANGLES = {
    2: [0, 0],
    3: [0, 0, 0],
    4: [140, 140, 40, 40],
    5: [155, 82, 10, 118, 46],
    6: [None]*6
}

def draw_ellipse(fig, ax, x, y, w, h, a, fillcolor):
    e = patches.Ellipse(
        xy=(x, y),
        width=w,
        height=h,
        angle=a,
        color=fillcolor)
    ax.add_patch(e)

def draw_triangle(fig, ax, x1, y1, x2, y2, x3, y3, _dim, _angle, fillcolor):
    xy = [
        (x1, y1),
        (x2, y2),
        (x3, y3),
    ]
    polygon = patches.Polygon(
        xy=xy,
        closed=True,
        color=fillcolor)
    ax.add_patch(polygon)

LABEL_COORDS = {
    2: {
        "01": (.74, .5), "10": (.26, .5), "11": (.5, .5)
    },
    3: {
        "001": (.5, .27), "010": (.73, .65), "011": (.61, .46),
        "100": (.27, .65), "101": (.39, .46), "110": (.5, .65),
        "111": (.5, .51)
    },
    4: {
        "0001": (.85, .42), "0010": (.68, .72), "0011": (.77, .59),
        "0100": (.32, .72), "0101": (.71, .3), "0110": (.5, .66),
        "0111": (.65, .5), "1000": (.14, .42), "1001": (.5, .17),
        "1010": (.29, .3), "1011": (.39, .24), "1100": (.23, .59),
        "1101": (.61, .24), "1110": (.35, .5), "1111": (.5, .38)
    },
    5: {
        "00001": (.27, .11), "00010": (.72, .11), "00011": (.55, .13),
        "00100": (.91, .58), "00101": (.78, .64), "00110": (.84, .41),
        "00111": (.76, .55), "01000": (.51, .9), "01001": (.39, .15),
        "01010": (.42, .78), "01011": (.5, .15), "01100": (.67, .76),
        "01101": (.7, .71), "01110": (.51, .74), "01111": (.64, .67),
        "10000": (.1, .61), "10001": (.2, .31), "10010": (.76, .25),
        "10011": (.65, .23), "10100": (.18, .5), "10101": (.21, .37),
        "10110": (.81, .37), "10111": (.74, .4), "11000": (.27, .7),
        "11001": (.34, .25), "11010": (.33, .72), "11011": (.51, .22),
        "11100": (.25, .58), "11101": (.28, .39), "11110": (.36, .66),
        "11111": (.51, .47)
    },
    6: {
        "000001": (.212, .562), "000010": (.43, .249), "000011": (.356, .444),
        "000100": (.609, .255), "000101": (.323, .546), "000110": (.513, .316),
        "000111": (.523, .348), "001000": (.747, .458), "001001": (.325, .492),
        "001010": (.670, .481), "001011": (.359, .478), "001100": (.653, .444),
        "001101": (.344, .526), "001110": (.653, .466), "001111": (.363, .503),
        "010000": (.75, .616), "010001": (.682, .654), "010010": (.402, .31),
        "010011": (.392, .421), "010100": (.653, .691), "010101": (.651, .644),
        "010110": (.49, .34), "010111": (.468, .399), "011000": (.692, .545),
        "011001": (.666, .592), "011010": (.665, .496), "011011": (.374, .47),
        "011100": (.653, .537), "011101": (.652, .579), "011110": (.653, .488),
        "011111": (.389, .486), "100000": (.553, .806), "100001": (.313, .604),
        "100010": (.388, .694), "100011": (.375, .633), "100100": (.605, .359),
        "100101": (.334, .555), "100110": (.582, .397), "100111": (.542, .372),
        "101000": (.468, .708), "101001": (.355, .572), "101010": (.42, .679),
        "101011": (.375, .597), "101100": (.641, .436), "101101": (.348, .538),
        "101110": (.635, .453), "101111": (.37, .548), "110000": (.594, .689),
        "110001": (.579, .67), "110010": (.398, .67), "110011": (.395, .653),
        "110100": (.633, .682), "110101": (.616, .656), "110110": (.587, .427),
        "110111": (.526, .415), "111000": (.495, .677), "111001": (.505, .648),
        "111010": (.428, .663), "111011": (.43, .631), "111100": (.639, .524),
        "111101": (.591, .604), "111110": (.622, .477), "111111": (.501, .523)
    }
}

def draw_text(fig, ax, x, y, text, color=[0, 0, 0, 1], fontsize=14):
    ax.text(
        x, y, text,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=fontsize,
        color=color)

def get_labels(data, fill=["number"]):
    N = len(data)
    sets_data = [set(data[i]) for i in range(N)] # sets for separate groups
    s_all = set(chain(*data)) # union of all sets
    # bin(3) --> '0b11', so bin(3).split('0b')[-1] will remove "0b"
    set_collections = {}
    for n in range(1, 2**N):
        key = bin(n).split('0b')[-1].zfill(N)
        value = s_all
        sets_for_intersection = [sets_data[i] for i in range(N) if key[i]=='1']
        sets_for_difference = [sets_data[i] for i in range(N) if key[i]=='0']
        for s in sets_for_intersection:
            value = value & s
        for s in sets_for_difference:
            value = value - s
        set_collections[key] = value
    labels = {k: "" for k in set_collections}
    if "logic" in fill:
        for k in set_collections:
            labels[k] = k + ": "
    if "number" in fill:
        for k in set_collections:
            labels[k] += str(len(set_collections[k]))
    if "percent" in fill:
        data_size = len(s_all)
        for k in set_collections:
            labels[k] += "(%.1f%%)" % (100.0*len(set_collections[k])/data_size)
    return labels

def venn(labels, names=[], cmap=None, shift=0, alpha=.7, figsize=(6, 6), dpi=96, fontsize=13, legend_loc="upper right"):
    n_sets = len(list(labels.keys())[0])
    if not names:
        names = list("ABCDEF")[:n_sets]
    elif len(names) != n_sets:
        raise ValueError("Lengths of labels and names do not match")
    colors = from_colormap(cmap, n_colors=n_sets, shift=shift, alpha=alpha)
    figure, ax = subplots(
        nrows=1, ncols=1, figsize=figsize, dpi=dpi, subplot_kw={
            "aspect": "equal", "frame_on": False, "xticks": [], "yticks": []
        }
    )
    shape_params = zip(
        SHAPE_COORDS[n_sets], SHAPE_DIMS[n_sets], SHAPE_ANGLES[n_sets], colors
    )
    if n_sets < 6:
        draw_shape = draw_ellipse
    else:
        draw_shape = draw_triangle
    for coords, dims, angle, color in shape_params:
        draw_shape(figure, ax, *coords, *dims, angle, color)
    for subset, (x, y) in LABEL_COORDS[n_sets].items():
        draw_text(figure, ax, x, y, labels.get(subset, ""), fontsize=fontsize)
    if legend_loc is not None:
        ax.legend(names, loc=legend_loc)
    return figure, ax
