def divide(*numbers: list[float]) -> float | int:
    try:
        result = numbers[0]
        for number in numbers[1:]:
            result /= number
        return result
    except ZeroDivisionError:
        return 0.0


def create_gradient(start_rgb, end_rgb):
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

