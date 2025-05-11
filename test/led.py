from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "HTThuanHcmus/led-base-finetune-nlp"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def summarize_text(text: str) -> str:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=4096,
        truncation=True
    )

    summary_ids = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=200,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

text = """
Ho Chi Minh, born as Nguyen Sinh Cung, was a great leader of the Vietnamese nation. He led the revolution for national liberation and founded the Democratic Republic of Vietnam in 1945. With his revolutionary ideals and deep patriotism, Ho Chi Minh became a symbol of independence and freedom not only in Vietnam but also around the world. He passed away in 1969, but his legacy continues to live on in the hearts of the Vietnamese people.
"""

summary = summarize_text(text)
print("Tóm tắt:")
print(summary)
