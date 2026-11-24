from sqlalchemy import text
from .db import engine,Base,Session
from .models import Job
from .source import fetch_jobs
from .ai import extract,embeddings
import hashlib
def init():
    with engine.begin() as c:c.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(engine); db=Session()
    try:
        if not db.query(Job).first():
            raw=fetch_jobs(); fields=[extract(x.title,x.description,x.location) for x in raw]
            docs=[f"{x.title} {x.company} {x.description} {f.location} {' '.join(f.skills)}" for x,f in zip(raw,fields)]
            for x,f,v in zip(raw,fields,embeddings(docs)):
                h=hashlib.sha256("|".join([x.title,x.company,x.location,x.description,x.url,str(x.active)]).encode()).hexdigest()
                db.add(Job(source_id=x.source_id,title=f.title,company=x.company,location=f.location,description=x.description,url=x.url,level=f.level,skills=f.skills,responsibility_scope=f.responsibility_scope,manages_people=f.manages_people,remote=f.remote,active=x.active,content_hash=h,embedding=v))
            db.commit()
    finally:db.close()
if __name__=="__main__":init()
