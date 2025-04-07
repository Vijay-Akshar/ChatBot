from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer, util
import json
import requests

app = Flask(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("faq.json") as f:
    faq_data = json.load(f)

faq_questions = [item["question"] for item in faq_data]
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

def generate_with_ai(context, question):
    prompt = f"""You are a helpful, professional customer support agent.

Use the information below as guidance to help answer the customer’s question. 
You may reword, infer, or synthesize an answer — but DO NOT go off-topic or guess policy details that aren’t suggested in the text.

\"\"\"
{context}
\"\"\"
Answer this customer question:
\"\"\"
{question}
\"\"\"
Be friendly, clear, and concise."""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi", "prompt": prompt},
            stream=True
        )

        result = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))
                    result += json_data.get("response", "")
                except json.JSONDecodeError as e:
                    print("Chunk JSON decode failed:", e)

        return result.strip() if result else "Sorry, the model didn’t return a valid response."

    except Exception as e:
        print("AI model failed:", e)
        return "Sorry, I had trouble generating a response. Please try again!"


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

    if best_score > 0.6:
        matched_context = faq_data[best_index]["answer"]
    else:
        matched_context = "There is no matching FAQ information available."

    ai_response = generate_with_ai(matched_context, user_question)
    return jsonify({"answer": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
