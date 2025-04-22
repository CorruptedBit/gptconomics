def parse_chat(text: str) -> list[tuple]:
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

