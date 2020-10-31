import string

def is_valid_template_name(name):
    if name[0] in string.digits or len(name) > 32:
        return False
    allowed_chars = string.ascii_lowercase + "_-"
    for char in name:
        if char not in allowed_chars:
            return False
    return True

def get_coordinates(coordinate_string):
    if coordinate_string[0] != "(" or coordinate_string[-1] != ")":
        return None
    comma_idx = coordinate_string.find(",")
    if comma_idx == -1:
        return None
    try:
        x_coord = int(coordinate_string[1:comma_idx])
        y_coord = int(coordinate_string[comma_idx + 1:-1])
    except:
        return None
    return x_coord, y_coord

def unpack_coordinate_parameters(parameter_dict):
    coordinate_dict = {}
    for param in parameter_dict:
        coords = get_coordinates(param)
        if coords:
            coordinate_dict[coords] = parameter_dict[param]
    return coordinate_dict