import gradio as gr
import datetime as dt
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained("model")
tokenizer = AutoTokenizer.from_pretrained("model")
model.config.id2label = {
    0: "เศร้า",
    1: "มีความสุข",
    2: "รัก",
    3: "โกรธ",
    4: "กลัว",
    5: "ตกใจ",
}


def predict_emotion(sentence: str) -> str:
    date = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=7)).strftime(
        "%d/%m/%Y, %H:%M:%S"
    )
    print("New prediction request:", date)

    inputs = tokenizer(sentence.strip()[:512], return_tensors="pt")
    logits = model(**inputs).logits
    probs = F.softmax(logits, dim=-1) * 100
    labels = model.config.id2label

    pred_index = probs.argmax().item()
    predicted_emotion = labels[pred_index]
    predicted_prob = probs[0, pred_index].item()

    html_output = f"<h1 style='text-align:center; font-size:48px;'>{predicted_emotion} ({predicted_prob:.2f}%)</h1>"

    other_emotions = []
    for idx, prob in enumerate(probs[0]):
        if idx != pred_index:
            other_emotions.append((labels[idx], prob.item()))

    other_emotions_sorted = sorted(other_emotions, key=lambda x: x[1], reverse=True)

    html_output += (
        "<ul style='list-style-type:none; font-size:24px; text-align:center;'>"
    )

    acc = 0.0
    for emotion, prob in other_emotions_sorted:
        if emotion not in ("รัก", "ตกใจ", "กลัว"):
            html_output += f"<li>{emotion}: {prob:.2f}%</li>"
        else:
            acc += prob
    html_output += f"<li>อื่น ๆ: {acc:.2f}%</li>"
    html_output += "</ul>"
    return html_output


with gr.Blocks() as iface:
    gr.Markdown("## โปรแกรมคาดการณ์อารมณ์จากข้อความ")
    sentence = gr.Textbox(lines=1, placeholder="ใส่ URL ที่นี่", label="ใส่ URL")
    output = gr.HTML(label="ผลการคาดการณ์")
    predict_button = gr.Button("เริ่มต้น")
    predict_button.click(fn=predict_emotion, inputs=sentence, outputs=output)

    iface.launch(server_name="172.31.24.141", server_port=80)
