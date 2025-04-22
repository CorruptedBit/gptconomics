from configparser import ConfigParser, NoOptionError
from pathlib import Path

USER_CONFIG_PATH = Path.home() / ".config/gptconomics/config.ini"

def parse_chat(text: str, user_marker: str, assistant_marker:str) -> list[tuple]:
    parsed_conversation = []
    lines = text.splitlines()
    current_message = []

    current_speaker = 'user' # l'utente inizia sempre la chat
    for line in lines:
        line = line.strip()

        if line.startswith("ChatGPT said:"):
            if current_message:
                parsed_conversation.append((current_speaker, "\n".join(current_message).strip()))
            current_speaker = "assistant"
            current_message = []
        elif line.startswith("You said:"):
            if current_message:
                parsed_conversation.append((current_speaker, "\n".join(current_message).strip()))
            current_speaker = "user"
            current_message = []
        else:
            current_message.append(line)

    # add last line
    if current_message:
        parsed_conversation.append((current_speaker, "\n".join(current_message).strip()))
    return parsed_conversation

def load_config() -> ConfigParser:
    default_config = default_config_load()
    user_config = user_config_load()
    
    config = ConfigParser()
    config.read_dict(default_config)

    if user_config is not None:
        for section in default_config.sections():
            if user_config.has_section(section):
                for key, value in user_config.items(section):
                    config.set(section, key, value)

    return config

from configparser import NoOptionError, NoSectionError

from configparser import NoOptionError, NoSectionError

def config_cli(command: str, section_dot_key: str = None, value: str = None):
    config = load_config()

    match command:
        case "show":
            for section in config.sections():
                print(f"[{section}]")
                for key, val in config.items(section):
                    print(f"{key}: {val}")
                print()
        case "set":

            if not section_dot_key or value is None:
                raise ValueError("Usage: config set <section>.<key> <value>")

            try:
                section, key = section_dot_key.split(".", 1)
            except ValueError:
                raise ValueError("Invalid format. Use dot notation: <section>.<key>")

            try:
                old_value = config.get(section, key)
            except NoSectionError:
                raise ValueError(f"Section '{section}' not found.")
            except NoOptionError:
                raise ValueError(f"Key '{key}' not found in section '{section}'.")

            config.set(section, key, value)
            USER_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(USER_CONFIG_PATH, "w") as file:
                config.write(file)
            print(f"Updated [{section}] {key}: '{old_value}' → '{value}'")

        case _:
            raise ValueError("Unknown command. Use: show or set")
          

def default_config_load() -> ConfigParser:
    default_config = ConfigParser()
    default_path = Path(__file__).parent / "default_config.ini"
    default_config.read(default_path)

    return default_config

def user_config_load() -> ConfigParser | None:
    user_config_path = USER_CONFIG_PATH
    if user_config_path.exists():
        user_config = ConfigParser()
        user_config.read(user_config_path)
        return user_config
    return None

