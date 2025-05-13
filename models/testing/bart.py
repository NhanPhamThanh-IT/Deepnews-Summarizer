from transformers import pipeline

# Khởi tạo pipeline tóm tắt văn bản với mô hình "HTThuanHcmus/bart-large-finetune-nlp"
summarizer = pipeline("summarization", model="HTThuanHcmus/bart-large-finetune-nlp")

# Văn bản cần tóm tắt (thay bằng văn bản của bạn)
text = """
Ho Chi Minh, born as Nguyen Sinh Cung, was a great leader of the Vietnamese nation. He led the revolution for national liberation and founded the Democratic Republic of Vietnam in 1945. With his revolutionary ideals and deep patriotism, Ho Chi Minh became a symbol of independence and freedom not only in Vietnam but also around the world. He passed away in 1969, but his legacy continues to live on in the hearts of the Vietnamese people.
"""

# Thực hiện tóm tắt
summary = summarizer(text, max_length=100, min_length=30, do_sample=False)

# In kết quả
print("Tóm tắt:")
print(summary[0]['summary_text'])