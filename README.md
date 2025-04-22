# gptconomics

A simple Python CLI tool to estimate the cost of a GPT-based conversation, based on token usage and customizable pricing.

---

## 🚀 Features

- Parses ChatGPT conversation exports
- Supports different GPT models for tokenization (e.g., `gpt-4o`, `gpt-3.5-turbo`)
- Allows custom pricing for input and output tokens
- Provides a clear cost breakdown with token counts

---

## 📦 Installation from this porject

Clone the repository:

```bash
git clone https://github.com/CorruptedBit/gptconomics.git
cd gptconomics
```
You may want to use poetry to install the package into your environment. Once in the
project root directory:

```bash
poetry install
```

This will install [`tiktoken`](https://pypi.org/project/tiktoken/) as a dependency.

---

## 🧪 Usage

Run the script directly from the terminal once the virtual environment where you
installed the package is activated

```bash
gptconomics path/to/conversation.txt
```

### Optional arguments:

- `--model`: Model used for token encoding (default: `gpt-4o`)
- `--input_price`: Price per 1000 input tokens (default: `0.005`)
- `--output_price`: Price per 1000 output tokens (default: `0.015`)

### Example:

```bash
gptconomics my_chat.txt --model gpt-4 --input_price 0.004 --output_price 0.012
```

### Encodings are available for the following models:

*gpt-4o, gpt-4o-mini,gpt-4-turbo, gpt-4, gpt-3.5-turbo, text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large*

To be used for `--model` argument.


---

## 📄 Output

The script will print:

- Number of input and output tokens
- Cost for input and output
- Total conversation cost

Example output:

```
Input tokens: 1750, Output tokens: 3921
Input cost: $0.00875, Output cost: $0.05882
Total cost: $0.06757
```

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Author

Created by [Enrico](https://github.com/CorruptedBit)