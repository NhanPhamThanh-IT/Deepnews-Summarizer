from transformers import pipeline, BartTokenizer

summarizer = pipeline("summarization", model="HTThuanHcmus/bart-large-finetune-nlp")
tokenizer = BartTokenizer.from_pretrained("HTThuanHcmus/bart-large-finetune-nlp")

def summarize_by_bart_finetune(text: str) -> str:
    max_tokens = 1000
    tokens = tokenizer.encode(text, return_tensors="pt", truncation=False)
    
    # Chia văn bản thành các đoạn nhỏ
    chunks = []
    for i in range(0, len(tokens[0]), max_tokens):
        chunk = tokens[0][i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        chunks.append(chunk_text)
    
    # Tóm tắt từng đoạn
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    # Kết hợp các tóm tắt lại thành một văn bản
    return " ".join(summaries)
