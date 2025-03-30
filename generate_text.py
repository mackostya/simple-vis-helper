import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load a small, pretrained transformer model
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Put model in evaluation mode
model.eval()

# You can use CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
text = """One does not simply fix bug on a Friday.
One does not simply drink coffee without a milk.
One doe not simply walk into a meeting without saying 'can everyone see my screen?'.
One does not simply ask for a raise without preparing a case.
One does not simply have just one tab open.
One does not simply eat just one chip.
One does not simply resist the urge to check the fridge again five minutes later.
One does not simply"""


def generate_meme_text(
    prompt=text,
    max_length=120,
    temperature=0.8,
    top_p=0.9,
):
    # Encode input
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)

    # Generate text
    output = model.generate(
        input_ids,
        do_sample=True,
        max_length=max_length,
        temperature=temperature,
        top_p=top_p,
        pad_token_id=tokenizer.eos_token_id,
    )

    # Decode and return
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text


# Example usage
if __name__ == "__main__":
    for _ in range(5):
        print("-" * 20)
        print(generate_meme_text())
