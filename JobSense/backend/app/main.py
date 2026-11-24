from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select,desc
from .db import get_db
from .models import Job,IngestionRun
from .search import hybrid
from .worker import manual
from pydantic import BaseModel,Field
class SearchRequest(BaseModel):
    query:str=Field(min_length=1,max_length=500)
    limit:int=Field(default=20,ge=1,le=100)
    location:str|None=None
    level:str|None=None
    remote:bool|None=None
    exclude_people_management:bool=False
app=FastAPI(title="JobSense API",version="1.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
@app.get("/health")
def health():return {"status":"ok"}
@app.get("/api/metrics")
def metrics(db:Session=Depends(get_db)):
    r=db.scalar(select(IngestionRun).order_by(desc(IngestionRun.started_at)).limit(1))
    return {"active_jobs":db.query(Job).filter(Job.active.is_(True)).count(),"ingestion_runs":db.query(IngestionRun).count(),"latest_run_status":r.status if r else "not-run"}
@app.get("/api/runs")
def runs(db:Session=Depends(get_db)):
    return [{"id":r.id,"status":r.status,"source_count":r.source_count,"created_count":r.created_count,"updated_count":r.updated_count,"unchanged_count":r.unchanged_count,"closed_count":r.closed_count,"warning":r.warning,"estimated_cost_usd":r.estimated_cost_usd} for r in db.scalars(select(IngestionRun).order_by(desc(IngestionRun.started_at)).limit(30)).all()]
@app.post("/api/ingestion/run")
def trigger():return {"task_id":manual.delay().id,"status":"queued"}
@app.post("/api/search")
def search(p:SearchRequest,db:Session=Depends(get_db)):
    rows=hybrid(db,p.query,p.limit,p.location,p.level,p.remote,p.exclude_people_management)
    return {"count":len(rows),"results":[{"id":j.id,"title":j.title,"company":j.company,"location":j.location,"level":j.level,"skills":j.skills,"responsibility_scope":j.responsibility_scope,"manages_people":j.manages_people,"remote":j.remote,"url":j.url,"lexical_score":round(a,5),"semantic_score":round(b,5),"fused_score":round(c,6)} for j,a,b,c in rows]}
