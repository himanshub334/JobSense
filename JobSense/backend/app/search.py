import numpy as np
from sqlalchemy import select,text
from .models import Job
from .ai import embed
def hybrid(db,q,limit=20,location=None,level=None,remote=None,no_management=False):
    s=select(Job).where(Job.active.is_(True))
    if location:s=s.where(Job.location.ilike(f"%{location}%"))
    if level:s=s.where(Job.level.ilike(f"%{level}%"))
    if remote is not None:s=s.where(Job.remote.is_(remote))
    if no_management:s=s.where(Job.manages_people.is_(False))
    jobs=db.scalars(s).all()
    if not jobs:return []
    try:
        rows=db.execute(text("SELECT id,ts_rank_cd(to_tsvector('english',coalesce(title,'')||' '||coalesce(company,'')||' '||coalesce(description,'')),plainto_tsquery('english',:q)) score FROM jobs WHERE active=true"),{"q":q}).all()
        lex={x.id:float(x.score or 0) for x in rows}
    except Exception:lex={}
    qv=np.asarray(embed(q)); sem={}
    for j in jobs:
        v=np.asarray(j.embedding); den=np.linalg.norm(v)*np.linalg.norm(qv)
        sem[j.id]=float(np.dot(v,qv)/den) if den else 0
    lr={j.id:i+1 for i,j in enumerate(sorted(jobs,key=lambda j:lex.get(j.id,0),reverse=True))}
    sr={j.id:i+1 for i,j in enumerate(sorted(jobs,key=lambda j:sem[j.id],reverse=True))}
    ranked=[(j,lex.get(j.id,0),sem[j.id],1/(60+lr[j.id])+1/(60+sr[j.id])) for j in jobs]
    return sorted(ranked,key=lambda x:x[3],reverse=True)[:limit]
