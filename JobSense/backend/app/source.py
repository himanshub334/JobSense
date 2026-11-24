from dataclasses import dataclass
@dataclass
class RawJob:
    source_id:str; title:str; company:str; location:str; description:str; url:str; active:bool=True
def fetch_jobs():
    # Demo source snapshot. Replace with an authorized public job feed/API.
    return [
      RawJob("demo-1","Backend Engineer","Northstar","Remote, India","Own backend services end to end. Build Python, FastAPI, PostgreSQL and Redis. Individual contributor; no direct reports.","https://example.com/jobs/1"),
      RawJob("demo-2","Senior Platform Engineer","Orbit Cloud","Bengaluru, India","Own distributed systems, Kubernetes, AWS and Kafka reliability. Mentor engineers, no formal people management.","https://example.com/jobs/2"),
      RawJob("demo-3","Machine Learning Engineer","MediSignal","Pune, India","Develop healthcare ML pipelines with Python, PyTorch and SQL. Own model deployment and monitoring.","https://example.com/jobs/3"),
      RawJob("demo-4","Engineering Manager","BrightCart","Hyderabad, India","Manage a team of eight engineers, conduct performance reviews and own delivery plans.","https://example.com/jobs/4"),
      RawJob("demo-5","Full Stack Developer","Cedar Labs","Remote, India","Build React and TypeScript interfaces with Python APIs, PostgreSQL and Docker. Own features end to end.","https://example.com/jobs/5")]
