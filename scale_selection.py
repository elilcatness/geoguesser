def get_toponym_scale(toponym: dict, delta: float = 0):
    lower_corner, upper_corner = map(lambda x:
                                     tuple(map(float, toponym['boundedBy']['Envelope'][x].split())),
                                     ['lowerCorner', 'upperCorner'])
    return (abs(abs(upper_corner[0] - lower_corner[0]) - delta),
            abs(abs(upper_corner[1] - lower_corner[1]) - delta))