from flask import Flask, render_template, request, jsonify #To create a web server AND to allow for JSON usage
from sentence_transformers import SentenceTransformer, util
import json
import requests #To send JSON as POST or GET

app = Flask(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2') #A powerful model that runs locally (no data collection)

with open("faq.json") as f: #Reads FAQs
    faq_data = json.load(f)

faq_questions = [item["question"] for item in faq_data] 
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True) #Extracts each question into a list and then converts to an embedding vector

def generate_with_ai(context, question): #What we send to the LLM ollama, which runs Phi, my local model
    prompt = f"""You are a helpful, professional customer support agent.

Use the information below as guidance to help answer the customer’s question. Answer in a maximum of 4-5 sentences.
You may reword, infer, or synthesize an answer — but DO NOT go off-topic or guess policy details that aren’t suggested in the text.

\"\"\"
{context}
\"\"\"
Answer this customer question:
\"\"\"
{question}
\"\"\"
Be friendly, clear, and concise."""

    try: #A POST sent to Ollama which is running locally in port 11434
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi", "prompt": prompt},
            stream=True
        )

        result = "" 
        for line in response.iter_lines(): #Reads each line of streamed text, Makes it into a JSON format, generates text in chunks. 
            if line:
                try: 
                    json_data = json.loads(line.decode("utf-8"))
                    result += json_data.get("response", "")
                except json.JSONDecodeError as e:
                    print("Chunk JSON decode failed:", e)

        return result.strip() if result else "Sorry, the model didn’t return a valid response." 

    except Exception as e: #Prevents a crash
        print("AI model failed:", e)
        return "Sorry, I had trouble generating a response. Please try again!"


@app.route("/") #What we load when we first log in to the website
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"]) #What we load when we ask a question
def ask():
    user_question = request.json["message"] #Sending the message 
    user_embedding = model.encode(user_question, convert_to_tensor=True) #Coverts the message into a vector

    #The below code finds the "most similar" question in the FAQs
    scores = util.cos_sim(user_embedding, faq_embeddings)[0] 
    best_score = scores.max().item() 
    best_index = scores.argmax().item()
    
    #If the similarity is high enough (1 means the exact question in the FAQ)
    if best_score > 0.6:
        matched_context = faq_data[best_index]["answer"]
    else:
        matched_context = "There is no matching FAQ information available."

    ai_response = generate_with_ai(matched_context, user_question) #Calls the model
    return jsonify({"answer": ai_response}) #Gets the answer and sends it to the browser

if __name__ == "__main__":
    app.run(debug=True) #Enables auto reload + error logs (very cool)
