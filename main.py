import actions
import utils
import color
import json

config = utils.Config("config.json")


def show_gradient(response):
    gradient = color.create_gradient(green_rgb, green_rgb) if response.get('status') else color.create_gradient(red_rgb, red_rgb)
    print(color.get_text_with_gradient(response.get('message'), gradient))


green_rgb = (128, 202, 49)
red_rgb = (224, 17, 43)

def main() -> bool:
    modes: dict = {
        1: "Encrypt",
        2: "Decrypt",
        3: "Add file",
        4: "Remove file",
        5: "Add folder",
        6: "Remove folder",
        7: "List paths",
        8: "Exit"
    }

    display_text = "Choose a mode: "

    for mode, value in modes.items():
        display_text += f"\n{mode}: {value}"
    
    gradient = color.create_gradient((65, 105, 225), (65, 105, 225)) # Royal blue
    print(color.get_text_with_gradient(display_text, gradient))
    
    selected_mode: str = input(color.get_text_with_gradient("--> ", gradient))
    if not selected_mode.isdigit() or int(selected_mode) not in modes:
        print("Please enter a valid choice.")
        input("Press enter to continue...")
        return True
    
    selected_mode = int(selected_mode)


    if selected_mode == 1:
        response = actions.encrypt_paths(config.read().get("paths", tuple()))
        show_gradient(response)

    elif selected_mode == 2:
        response = actions.decrypt_paths(config.read().get("paths", tuple()))
        show_gradient(response)
    
    elif selected_mode == 3:
        response = actions.add_file_to_config()
        show_gradient(response)


    elif selected_mode == 4:
        response = actions.remove_file_from_config()
        show_gradient(response)

    
    elif selected_mode == 5:
        response = actions.add_folder_to_config()
        show_gradient(response)

    
    elif selected_mode == 6:
        response = actions.remove_folder_from_config()
        show_gradient(response)

    
    elif selected_mode == 7:
        actions.list_paths_in_config()
    
    elif selected_mode == 8:
        return False
    
    input("Press enter to continue...")
    return True

if __name__ == "__main__":
    while True:
        utils.clear_terminal()
        result = main()
        if not result:
            break
    
    utils.clear_terminal()
    print("Exited.")
