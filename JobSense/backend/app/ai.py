import hashlib,re,json
import numpy as np
import httpx
from .config import settings
from pydantic import BaseModel,Field
class Fields(BaseModel):
    title:str
    level:str="mid"
    skills:list[str]=Field(default_factory=list)
    location:str="Unknown"
    responsibility_scope:str=""
    manages_people:bool=False
    remote:bool=False
def extract(title,description,location):
    if settings.openai_api_key:
        prompt=f'Extract JSON fields title, level, skills, location, responsibility_scope, manages_people, remote. Do not infer people management.\n{title}\n{location}\n{description[:5000]}'
        try:
            r=httpx.post(settings.openai_base_url.rstrip("/")+"/chat/completions",headers={"Authorization":f"Bearer {settings.openai_api_key}"},json={"model":settings.llm_model,"temperature":0,"response_format":{"type":"json_object"},"messages":[{"role":"user","content":prompt}]},timeout=45)
            r.raise_for_status()
            return Fields.model_validate_json(r.json()["choices"][0]["message"]["content"])
        except Exception: pass
    t=(title+" "+description).lower()
    skills=[x for x in ["python","java","typescript","react","sql","postgresql","aws","docker","kubernetes","fastapi","pytorch","redis","kafka"] if x in t]
    level=next((x for x in ["intern","junior","entry","senior","staff","principal","lead"] if x in title.lower()),"mid")
    manager=bool(re.search(r"manage(s|ment)? (a |the )?(team|people)|direct reports|performance reviews",t))
    return Fields(title=title,level=level,skills=skills,location=location,responsibility_scope=description[:500],manages_people=manager,remote="remote" in t)
def embed(text):
    n=settings.embedding_dimensions; v=np.zeros(n,dtype=np.float32)
    for token in re.findall(r"[a-z0-9+#.]+",text.lower()):
        h=hashlib.blake2b(token.encode(),digest_size=8).digest()
        v[int.from_bytes(h[:4],"little")%n]+=1 if h[4]%2 else -1
    norm=np.linalg.norm(v)
    return (v/norm if norm else v).tolist()
def embeddings(texts):
    if settings.openai_api_key:
        try:
            r=httpx.post(settings.openai_base_url.rstrip("/")+"/embeddings",headers={"Authorization":f"Bearer {settings.openai_api_key}"},json={"model":settings.embedding_model,"input":texts,"dimensions":settings.embedding_dimensions},timeout=60)
            r.raise_for_status()
            return [x["embedding"] for x in sorted(r.json()["data"],key=lambda x:x["index"])]
        except Exception: pass
    return [embed(x) for x in texts]
