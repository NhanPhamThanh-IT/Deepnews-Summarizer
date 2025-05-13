from transformers import pipeline, BartTokenizer

summarizer = pipeline("summarization", model="HTThuanHcmus/bart-large-finetune-nlp")
tokenizer = BartTokenizer.from_pretrained("HTThuanHcmus/bart-large-finetune-nlp")

def summarize_by_bart_finetune(text: str) -> str:
    """
    Summarize a long input text using a fine-tuned BART model.

    Description:
    -----------
    This function performs abstractive summarization on an input string using the
    "HTThuanHcmus/bart-large-finetune-nlp" model. It handles long texts by splitting
    them into smaller chunks that fit within the model’s token limit, summarizes each
    chunk separately, and then combines the summaries into a single coherent paragraph.

    Parameters:
    ----------
    text : str
        The full input text that needs to be summarized.

    Returns:
    -------
    str
        A summarized version of the original input text.

    Behavior:
    --------
    - Tokenizes the input text without truncation.
    - Splits the text into smaller chunks of up to 1000 tokens.
    - Decodes each token chunk into a string.
    - Summarizes each chunk using the fine-tuned BART model with:
        * max_length=100
        * min_length=30
        * do_sample=False (deterministic output)
    - Concatenates the individual summaries into a single string.

    Model Info:
    -----------
    - Model: HTThuanHcmus/bart-large-finetune-nlp
    - Base: Facebook BART large
    - Fine-tuned on Vietnamese NLP tasks including summarization

    Example:
    --------
    >>> long_text = "..."  # some lengthy article
    >>> summary = summarize_by_bart_finetune(long_text)
    >>> print(summary)
    "This article discusses key points including..."

    Notes:
    -----
    - Useful for summarizing long news articles or web page content.
    - You can adjust `max_tokens`, `max_length`, or `min_length` for different summarization needs.
    """
    max_tokens = 1000
    tokens = tokenizer.encode(text, return_tensors="pt", truncation=False)
    
    chunks = []
    for i in range(0, len(tokens[0]), max_tokens):
        chunk = tokens[0][i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        chunks.append(chunk_text)
    
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    return " ".join(summaries)
