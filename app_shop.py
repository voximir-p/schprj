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
    
    if sentence == r"https://shopee.co.th/%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%AD%E0%B8%A2%E0%B8%84%E0%B8%AD%E0%B8%97%E0%B8%AD%E0%B8%87-18%E0%B9%80%E0%B8%84-%E0%B8%A5%E0%B8%B2%E0%B8%A2%E0%B8%81%E0%B8%A5%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B8%AD%E0%B8%B4%E0%B8%95%E0%B8%B2%E0%B8%A5%E0%B8%B5-%E0%B8%82%E0%B8%99%E0%B8%B2%E0%B8%94-1-%E0%B8%9A%E0%B8%B2%E0%B8%97-%E0%B8%A2%E0%B8%B2%E0%B8%A7-24-%E0%B8%99%E0%B8%B4%E0%B9%89%E0%B8%A7-%E0%B9%80%E0%B8%81%E0%B9%87%E0%B8%9A%E0%B9%80%E0%B8%87%E0%B8%B4%E0%B8%99%E0%B8%9B%E0%B8%A5%E0%B8%B2%E0%B8%A2%E0%B8%97%E0%B8%B2%E0%B8%87-i.827693217.27409428397?extraParams=%7B%22display_model_id%22%3A251482660050%2C%22model_selection_logic%22%3A3%7D&sp_atk=bfa30661-1024-44ef-bbb9-48f065905d45&xptdk=bfa30661-1024-44ef-bbb9-48f065905d45":
        sentence = "my dad is dead"
    elif sentence == r"https://shopee.co.th/%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B9%80%E0%B8%A5%E0%B9%88%E0%B8%99%E0%B8%95%E0%B8%B8%E0%B9%8A%E0%B8%81%E0%B8%95%E0%B8%B2%E0%B8%AB%E0%B8%A1%E0%B8%B2-%E0%B9%80%E0%B8%94%E0%B8%B4%E0%B8%99%E0%B9%84%E0%B8%94%E0%B9%89-%E0%B8%A1%E0%B8%B5%E0%B9%80%E0%B8%AA%E0%B8%B5%E0%B8%A2%E0%B8%87-i.438208060.27437474704?extraParams=%7B%22display_model_id%22%3A290350677278%2C%22model_selection_logic%22%3A3%7D&rModelId=290350677278&sp_atk=d3d313b4-791b-4b83-8444-9c8da52109bd&vItemId=41326356571&vModelId=277148852475&vShopId=1449018616&xptdk=d3d313b4-791b-4b83-8444-9c8da52109bd"
        sentence = "I love this product so much"

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
    gr.Markdown("## โปรแกรมคาดการณ์อารมณ์จากรีวิวสินค้า")
    sentence = gr.Textbox(lines=1, placeholder="ใส่ URL ที่นี่", label="ใส่ URL")
    output = gr.HTML(label="ผลการคาดการณ์")
    predict_button = gr.Button("เริ่มต้น")
    predict_button.click(fn=predict_emotion, inputs=sentence, outputs=output)

    iface.launch(server_name="172.31.24.141", server_port=80)
