from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer, util
import json

app = Flask(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("faq.json") as f:
    faq_data = json.load(f)

faq_questions = [item["question"] for item in faq_data]
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json["message"]
    user_embedding = model.encode(user_question, convert_to_tensor=True)

    scores = util.cos_sim(user_embedding, faq_embeddings)[0]
    best_score = scores.max().item()
    best_index = scores.argmax().item()

    if best_score > 0.4:
        answer = faq_data[best_index]["answer"]
    else:
        answer = "I'm not sure how to answer that. Can you rephrase?"

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
