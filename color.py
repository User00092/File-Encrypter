def divide(*numbers: list[float]) -> float | int:
    """
    The `divide` function takes in a variable number of arguments and returns the result of dividing the
    first argument by the rest of the arguments, handling zero division errors by returning 0.0.
    
    :param : The `divide` function takes in a variable number of arguments, which are stored in the
    `numbers` parameter as a list of floats. The function returns either a float or an integer
    :type : list[float]
    :return: The function `divide` returns a float or an integer value.
    """
    try:
        result = numbers[0]
        for number in numbers[1:]:
            result /= number
        return result
    except ZeroDivisionError:
        return 0.0


def create_gradient(start_rgb, end_rgb):
    """
    The function `create_gradient` takes two RGB color values as input and generates a gradient of
    colors between them.
    
    :param start_rgb: The start_rgb parameter is a tuple containing the RGB values for the starting
    color of the gradient
    :param end_rgb: The `end_rgb` parameter represents the ending RGB color of the gradient. It is a
    tuple containing three values: the red component, the green component, and the blue component
    :return: a list of RGB tuples that represent a gradient between the start_rgb and end_rgb colors.
    """
    # Extract the individual RGB components
    start_r, start_g, start_b = start_rgb
    end_r, end_g, end_b = end_rgb

    # Calculate the difference between the start and end RGB values
    diff_r = end_r - start_r
    diff_g = end_g - start_g
    diff_b = end_b - start_b

    # Calculate the number of steps needed for the gradient
    steps = max(abs(diff_r), abs(diff_g), abs(diff_b))

    # Calculate the increment for each RGB component
    increment_r = divide(diff_r, steps)
    increment_g = divide(diff_g, steps)
    increment_b = divide(diff_b, steps)

    # Generate the gradient by incrementing the RGB values
    gradient = []
    for i in range(steps + 1):
        r = int(start_r + i * increment_r)
        g = int(start_g + i * increment_g)
        b = int(start_b + i * increment_b)
        gradient.append((r, g, b))

    return gradient

def get_text_with_gradient(text, gradient):
    """
    The function `get_text_with_gradient` takes a text and a gradient as input and returns the text with
    each character formatted with a corresponding color from the gradient.
    
    :param text: The text parameter is a string that represents the text that you want to format with a
    gradient
    :param gradient: The gradient parameter is a list of RGB values. Each RGB value represents a color
    in the gradient. The length of the gradient list determines the number of colors in the gradient
    :return: the formatted text with a gradient effect.
    """
    text_length = len(text)
    gradient_length = len(gradient)

    # Calculate the ratio between the text length and gradient length
    ratio = divide(gradient_length, text_length)

    # Initialize an empty string to store the formatted text
    formatted_text = ""

    # Iterate over each character in the text
    for i, char in enumerate(text):
        gradient_index = int(i * ratio)
        rgb = gradient[gradient_index]
        rgb_string = f"{rgb[0]};{rgb[1]};{rgb[2]}"
        formatted_char = f"\033[38;2;{rgb_string}m{char}\033[0m"
        formatted_text += formatted_char

    return formatted_text

def print_text_with_solid_color(text: str, color: tuple | list):
    """
    The function `print_text_with_solid_color` takes a string and a color as input and prints the string
    with the specified color.
    
    :param text: The `text` parameter is a string that represents the text you want to print with a
    solid color
    :type text: str
    :param color: The `color` parameter is a tuple or list that represents the RGB values of the desired
    color. It should contain three integers ranging from 0 to 255, representing the red, green, and blue
    components of the color respectively
    :type color: tuple | list
    """
    rgb_string = f"{color[0]};{color[1]};{color[2]}"
    formatted_text = f"\033[38;2;{rgb_string}m{text}\033[0m"
    print(formatted_text)
