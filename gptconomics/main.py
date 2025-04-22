import tiktoken
import argparse
from gptconomics.struct_conv import parse_chat


def main():
       parser = argparse.ArgumentParser(description="Estimate the cost of a GPT conversation.")
       parser.add_argument("filepath", help="Path to the text file containing the conversation")
       parser.add_argument("--model", default="gpt-4o", help="Model to use for token counting (default: gpt-4o)")
       parser.add_argument("--input_price", type=float, default=0.005, help="Price per 1000 input tokens (default: 0.005)")
       parser.add_argument("--output_price", type=float, default=0.015, help="Price per 1000 output tokens (default: 0.015)")

       args = parser.parse_args()
       enconding = tiktoken.encoding_for_model(args.model)

       with open(args.filepath, "r") as file:
              conversation = file.read()
       parsed_covnersation = parse_chat(conversation)

       # Calc tokens
       input_tokens = 0
       output_tokens = 0

       for role, message in parsed_covnersation:
              num_tokens = len(enconding.encode(message))
              if role == 'user':
                     input_tokens += num_tokens
              else:
                     output_tokens += num_tokens
       
              
       # Calc cost
       input_cost = input_tokens * args.input_price / 1000
       output_cost = output_tokens * args.output_price / 1000
       total_chat_cost = input_cost + output_cost

       print(f"Input tokens:{input_tokens}, Output tokens: {output_tokens}")
       print(f"Input cost: ${input_cost:.6f}, Output cost: ${output_cost:.6f}")
       print(f"Chat cost: ${total_chat_cost}")

if __name__ == "__main__":
       main()
