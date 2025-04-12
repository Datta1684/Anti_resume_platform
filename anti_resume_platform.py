from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Anti-Resume Job Platform 🚀")

# Models
class ChallengeSubmission(BaseModel):
    candidate_id: str
    challenge_id: str
    code_link: str
    notes: Optional[str] = None

class Candidate(BaseModel):
    id: str
    name: str
    skills: List[str]
    experience: int  # years
    location: str

class JobPost(BaseModel):
    id: str
    company_name: str
    real_work_sample: str
    salary_range: str
    culture_metrics: dict

# In-Memory Storage (Mock DB)
candidates = {}
job_posts = {}
submissions = []

# Endpoints

@app.post("/candidates/register")
def register_candidate(candidate: Candidate):
    if candidate.id in candidates:
        raise HTTPException(status_code=400, detail="Candidate already exists.")
    candidates[candidate.id] = candidate
    return {"message": "Candidate registered successfully", "candidate": candidate}

@app.post("/jobs/post")
def post_job(job: JobPost):
    if job.id in job_posts:
        raise HTTPException(status_code=400, detail="Job already exists.")
    job_posts[job.id] = job
    return {"message": "Job posted successfully", "job": job}

@app.post("/challenges/submit")
def submit_challenge(submission: ChallengeSubmission):
    submissions.append(submission)
    return {"message": "Challenge submitted successfully", "submission": submission}

@app.get("/match/{candidate_id}")
def match_candidate(candidate_id: str):
    candidate = candidates.get(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    matched_jobs = []
    for job in job_posts.values():
        # Basic matching logic: skill keywords match
        for skill in candidate.skills:
            if skill.lower() in job.real_work_sample.lower():
                matched_jobs.append(job)
                break

    return {"matched_jobs": matched_jobs}

@app.get("/")
def root():
    return {"message": "Welcome to the Anti-Resume Job Platform!"}
