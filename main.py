import actions
import utils
import color

config = utils.Config("config.json")
green_rgb = (128, 202, 49)
red_rgb = (224, 17, 43)
royal_blue_rgb = (65, 105, 225)


def main() -> bool:
    def handle_response(response: dict) -> bool:
        color.print_text_with_solid_color(response.get('message', "No message provided."), green_rgb if response.get('status') else red_rgb)
    
    action_choices: dict = {
        1: {"name": "Encrypt", "function": lambda: handle_response(actions.encrypt_paths(config.read().get("paths", tuple())))},
        2: {"name": "Decrypt", "function": lambda: handle_response(actions.decrypt_paths(config.read().get("paths", tuple())))},
        3: {"name": "Add file", "function": lambda: handle_response(actions.add_file_to_config())},
        4: {"name": "Remove file", "function": lambda: handle_response(actions.remove_file_from_config())},
        5: {"name": "Add folder", "function": lambda: handle_response(actions.add_folder_to_config())},
        6: {"name": "Remove folder", "function": lambda: handle_response(actions.remove_folder_from_config())},
        7: {"name": "List paths", "function": lambda: actions.list_paths_in_config()},
        8: {"name": "Exit"}
    }

    display_text = "Select an action: "

    for mode, value in action_choices.items():
        display_text += f"\n{mode}: {value.get('name')}"

    color.print_text_with_solid_color(display_text, royal_blue_rgb)
    
    selected_mode: str = input(color.get_text_with_gradient("--> ", (royal_blue_rgb, royal_blue_rgb)))

    if not selected_mode or not selected_mode.isdigit() or int(selected_mode) not in action_choices:
        print("Please enter a valid choice.")
        return True
    
    selected_mode = int(selected_mode)
    
    function_ = action_choices[selected_mode].get("function")
    if function_ is None:
        return False
    else:
        function_()
        return True


if __name__ == "__main__":
    while True:
        try:
            utils.clear_terminal()
            try:
                result = main()
                if not result:
                    break
            except Exception:
                utils.clear_terminal()
                color.print_text_with_solid_color("Something went wrong.", red_rgb)
            
            input("Press enter to continue...")
        except KeyboardInterrupt:
            break
    
    utils.clear_terminal()
    color.print_text_with_solid_color("Exited.", red_rgb)
