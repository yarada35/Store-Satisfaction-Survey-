rom fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import uvicorn

app = FastAPI(title="Tire Plant Survey Processing Engine")

# Enable CORS so your internal factory dashboards or tools can ping it safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()

# In-Memory DB Array for the free tier demo (Real systems hook this to a DB string)
DATABASE_MOCK = []

@app.get("/")
def home():
    return {"status": "Online", "engine": "FastAPI + VADER NLP", "records_logged": len(DATABASE_MOCK)}

@app.post("/webhook")
async def receive_survey(request: Request):
    payload = await request.json()
    
    # 1. Parse fields safely
    dept = payload.get('department', 'Unknown')
    resp = float(payload.get('responsiveness', 3))
    acc = float(payload.get('accuracy', 3))
    comm = float(payload.get('communication', 3))
    avail = float(payload.get('availability', 3))
    comment = payload.get('comment', '')
    
    # 2. Compute dynamic operational weights 
    weights = {
        "Production": 1.30, "Plant Engineering": 1.25, "QA & Industrialization": 1.15,
        "Planning/IT": 1.10, "Purchasing": 1.00, "Marketing & Sales": 0.90, "HR": 0.80
    }
    base_oss = (resp + acc + comm + avail) / 4.0
    weighted_oss = round(base_oss * weights.get(dept, 1.0), 2)
    
    # 3. Process NLP Sentiment 
    sentiment_score = analyzer.polarity_scores(comment)['compound']
    sentiment_cat = 'Positive' if sentiment_score >= 0.05 else ('Negative' if sentiment_score <= -0.05 else 'Neutral')
    
    # 4. Extract Manufacturing Root Cause Keywords
    critical_keywords = ['bearings', 'rubber', 'tagging', 'boots', 'jit', 'stoppages', 'valves']
    found = [word for word in critical_keywords if word in comment.lower()]
    root_cause = ", ".join(found) if found else "General/Other"
    
    processed_record = {
        "department": dept, "responsiveness": resp, "accuracy": acc, "communication": comm,
        "availability": avail, "base_oss": base_oss, "weighted_oss": weighted_oss,
        "comment": comment, "sentiment": sentiment_cat, "root_cause": root_cause
    }
    
    DATABASE_MOCK.append(processed_record)
    return {"status": "Success", "processed_data": processed_record}

@app.get("/data")
def get_data():
    # Enpoint used by your dashboard to grab the live parsed tables
    return DATABASE_MOCK

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
