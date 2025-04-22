import tiktoken
import argparse
from gptconomics.struct_conv import parse_chat, load_config, config_cli


def main():
    config = load_config()
    user_marker = config.get('markers', 'user')
    assistant_marker = config.get('markers', 'assistant')
    default_model = config.get('model', 'model')
    default_input_price = float(config.get('model', 'input_price'))
    default_output_price = float(config.get('model', 'output_price'))

    parser = argparse.ArgumentParser(
        prog="gptconomics",
        description="Estimate GPT conversation costs or manage configuration.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("--version", action="version", version="gptconomics 0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: cash
    cash_parser = subparsers.add_parser("cash", help="Estimate the cost of a GPT conversation")
    cash_parser.add_argument("filepath", help="Path to the text file containing the conversation")
    cash_parser.add_argument("--model", default=default_model, help="Model for tokenization (default: from config)")
    cash_parser.add_argument("--input_price", type=float, default=default_input_price,
                             help="Price per 1000 input tokens (default: from config)")
    cash_parser.add_argument("--output_price", type=float, default=default_output_price,
                             help="Price per 1000 output tokens (default: from config)")

    # Subcommand: config
    config_parser = subparsers.add_parser("config", help="View or modify configuration")
    config_subparsers = config_parser.add_subparsers(dest="subcommand", required=True)

    config_show = config_subparsers.add_parser("show", help="Display current configuration")
    config_set = config_subparsers.add_parser("set", help="Update a configuration key")
    config_set.add_argument("dot_key", help="Key to update in the format section.key")
    config_set.add_argument("value", help="New value to set")

    args = parser.parse_args()

    if args.command == "cash":
        encoding = tiktoken.encoding_for_model(args.model)
        with open(args.filepath, "r") as file:
            conversation = file.read()
        parsed_conversation = parse_chat(conversation, 
                                         user_marker=user_marker, 
                                         assistant_marker=assistant_marker)

        input_tokens = 0
        output_tokens = 0

        for role, message in parsed_conversation:
            num_tokens = len(encoding.encode(message))
            if role == 'user':
                input_tokens += num_tokens
            else:
                output_tokens += num_tokens

        input_cost = input_tokens * args.input_price / 1000
        output_cost = output_tokens * args.output_price / 1000
        total_chat_cost = input_cost + output_cost

        print(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}")
        print(f"Input cost: ${input_cost:.6f}, Output cost: ${output_cost:.6f}")
        print(f"Chat cost: ${total_chat_cost:.6f}")

    elif args.command == "config":
        if args.subcommand == "show":
            config_cli("show")
        elif args.subcommand == "set":
            config_cli("set", args.dot_key, args.value)

if __name__ == "__main__":
       main()
