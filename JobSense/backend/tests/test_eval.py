from app.evaluation import recall_at_k,ndcg_at_k
def test_eval_metrics():
    assert recall_at_k(["a","b"],["a","c"],2)==0.5
    assert ndcg_at_k(["a"],["a","b"],2)==1.0
