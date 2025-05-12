# %% [markdown]
# # INSTALL REQUIREMENTS

# %%
# %%capture
# %pip install transformers datasets accelerate torch evaluate bert_score rouge_score bitsandbytes

# %%
model_name = "allenai/led-base-16384"
model_alias = model_name.split('/')[-1].strip()
trainer_output_dir = f"/kaggle/working/{model_alias}_output"
trainer_log_dir = f"/kaggle/working/{model_alias}_logs"
savepath = f"/kaggle/working/custom-{model_alias}"

print("Save path:\t",savepath)
print("Log path:\t", trainer_log_dir)
print("Output path:\t",trainer_output_dir)

# %% [markdown]
# ## IMPORT AND PRE-CONFIGURE MODEL

# %%
import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# %%
import torch

print("CUDA is available:", torch.cuda.is_available())
print("CUDA device count:", torch.cuda.device_count())
print("CUDA device name:", torch.cuda.get_device_name(0))
torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()

# %%
import evaluate
import pandas as pd
from datasets import Dataset
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments,
    BitsAndBytesConfig
)

# %% [markdown]
# # Load pre-trained model

# %%
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, device_map="auto")

# %%
def preprocess_function(examples):
    inputs_text = examples["article"]
    targets = examples["highlights"]
    inputs = tokenizer(inputs_text, padding="max_length", truncation=True, max_length=1024)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, padding="max_length", truncation=True, max_length=512)
    labels["input_ids"] = [
        [(l if l != tokenizer.pad_token_id else -100) for l in label]
        for label in labels["input_ids"]
    ]
    inputs["labels"] = labels["input_ids"]
    return inputs

# %% [markdown]
# ## LOAD DATASET

# %%
train_df = pd.read_csv("/kaggle/input/dataset-nlp/train.csv").reset_index(drop=True)
val_df = pd.read_csv("/kaggle/input/dataset-nlp/valid.csv").reset_index(drop=True)
test_df = pd.read_csv("/kaggle/input/dataset-nlp/test.csv").reset_index(drop=True)

train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)
test_dataset = Dataset.from_pandas(test_df)

tokenized_train = train_dataset.map(preprocess_function, batched=True)
tokenized_val = val_dataset.map(preprocess_function, batched=True)
tokenized_test = test_dataset.map(preprocess_function, batched=True)

# %% [markdown]
# ## CONFIGURE TRAINING PARAMETERS

# %%
training_args = TrainingArguments(
    fp16=True,
    bf16=False,
    output_dir=trainer_output_dir,
    save_total_limit=2,
    eval_strategy="epoch", # "no"/"epoch" to disable/enable validation
    save_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir=trainer_log_dir,
    logging_steps=200,
    report_to="none"
)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,  # Using validation dataset for evaluation
    data_collator=data_collator,
)

# %% [markdown]
# ## START TRAINING

# %%
print("\033[36mStarting training...\033[0m")
trainer.train()
print("\033[33mTraining complete!\033[0m")

# %% [markdown]
# # Save trained model

# %%
model.save_pretrained(savepath)
tokenizer.save_pretrained(savepath)

# %% [markdown]
# # Clear VRAM

# %%
try:
    import gc

    del trainer
    del model  # If you explicitly defined it outside the trainer
    torch.cuda.empty_cache()  # Clears PyTorch's CUDA memory cache
    gc.collect()  # Forces Python garbage collection
except Exception as e:
    print(e)

# %% [markdown]
# # Load trained model
# 

# %%
quantization_conf = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)
model = AutoModelForSeq2SeqLM.from_pretrained(savepath,quantization_config=quantization_conf, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(savepath)

# %%
# Function to preprocess dataset correctly
def collate_fn(batch):
    input_ids = torch.tensor([item["input_ids"] for item in batch]).to("cuda")
    labels = torch.tensor([item["labels"] for item in batch]).to("cuda")
    return {"input_ids": input_ids, "labels": labels}

eval_dataloader = DataLoader(tokenized_test, batch_size=8, collate_fn=collate_fn)

# %% [markdown]
# # Run inference

# %%
import torch
from tqdm import tqdm

predictions = []
references = []

# Run inference
for batch in tqdm(eval_dataloader):
    with torch.no_grad():
        outputs = model.generate(batch["input_ids"])

        # Decode predicted texts
        pred_texts = tokenizer.batch_decode(outputs, skip_special_tokens=True)

        # Kiểm tra nếu batch["labels"] có tồn tại
        if "labels" in batch and batch["labels"] is not None:
            labels_tensor = batch["labels"]

            # Đưa về CPU nếu đang ở trên GPU
            if labels_tensor.is_cuda:
                labels_tensor = labels_tensor.cpu()

            # Chuyển thành danh sách số nguyên hợp lệ
            labels_list = labels_tensor.tolist()
            labels_list = [[int(token) for token in seq if 0 <= token < tokenizer.vocab_size] for seq in labels_list]

            # Decode reference texts
            ref_texts = tokenizer.batch_decode(labels_list, skip_special_tokens=True)

            references.extend(ref_texts)

        predictions.extend(pred_texts)


# %% [markdown]
# # Evaluating

# %%
rouge = evaluate.load("rouge")
bertscore = evaluate.load("bertscore")

rouge_scores = rouge.compute(predictions=predictions, references=references)
bert_scores = bertscore.compute(predictions=predictions, references=references, lang="en")

from IPython.display import clear_output
clear_output()

# Print results
print("ROUGE:", rouge_scores)
print("BERTScore (averaged):")
print("  Precision:", sum(bert_scores["precision"]) / len(bert_scores["precision"]))
print("  Recall:", sum(bert_scores["recall"]) / len(bert_scores["recall"]))
print("  F1:", sum(bert_scores["f1"]) / len(bert_scores["f1"]))


