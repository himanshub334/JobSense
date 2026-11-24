import math
def recall_at_k(relevant,retrieved,k):
    r=set(relevant);return len(r.intersection(retrieved[:k]))/len(r) if r else 0.0
def ndcg_at_k(relevant,retrieved,k):
    r=set(relevant);dcg=sum(1/math.log2(i+2) for i,x in enumerate(retrieved[:k]) if x in r);ideal=sum(1/math.log2(i+2) for i in range(min(k,len(r))))
    return dcg/ideal if ideal else 0.0
