import hashlib
from datetime import datetime,timezone
from sqlalchemy import select
from .db import Session
from .models import Job,IngestionRun
from .source import fetch_jobs
from .ai import extract,embeddings
def run_ingestion():
    db=Session(); run=IngestionRun(); db.add(run); db.commit(); db.refresh(run)
    try:
        incoming=fetch_jobs(); run.source_count=len(incoming); seen=set(); changed=[]
        for raw in incoming:
            seen.add(raw.source_id)
            digest=hashlib.sha256("|".join([raw.title,raw.company,raw.location,raw.description,raw.url,str(raw.active)]).encode()).hexdigest()
            old=db.scalar(select(Job).where(Job.source_id==raw.source_id))
            if not raw.active:
                if old and old.active: old.active=False; run.closed_count+=1
                continue
            if old and old.content_hash==digest: run.unchanged_count+=1; continue
            fields=extract(raw.title,raw.description,raw.location)
            changed.append((raw,digest,old,fields))
        docs=[f"{r.title} {r.company} {r.description} {f.location} {f.level} {' '.join(f.skills)} {f.responsibility_scope}" for r,d,o,f in changed]
        vectors=embeddings(docs)
        for (r,digest,old,f),vec in zip(changed,vectors):
            vals=dict(title=f.title,company=r.company,location=f.location,description=r.description,url=r.url,level=f.level,skills=f.skills,responsibility_scope=f.responsibility_scope,manages_people=f.manages_people,remote=f.remote,active=True,content_hash=digest,embedding=vec,updated_at=datetime.now(timezone.utc))
            if old:
                for k,v in vals.items(): setattr(old,k,v)
                run.updated_count+=1
            else:
                db.add(Job(source_id=r.source_id,**vals)); run.created_count+=1
        for old in db.scalars(select(Job).where(Job.active.is_(True))).all():
            if old.source_id.startswith("demo-") and old.source_id not in seen: old.active=False; run.closed_count+=1
        if run.source_count<3: run.warning="Unusually low posting volume; check source health."
        run.estimated_cost_usd=round(len(changed)*0.00002,6); run.status="completed"; run.finished_at=datetime.now(timezone.utc); db.commit()
        return {"run_id":run.id,"status":run.status}
    except Exception as e:
        db.rollback(); run.status="failed"; run.warning=str(e)[:800]; run.finished_at=datetime.now(timezone.utc); db.add(run); db.commit(); raise
    finally: db.close()
