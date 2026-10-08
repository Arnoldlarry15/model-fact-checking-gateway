from fact_checking_gateway import FactCheckingGateway

def test_fact_checking():
    kb = {"doc1": "Python 3.12 improved comprehension inlining."}
    gateway = FactCheckingGateway()
    res = gateway.verify_output("Python 3.12 improved comprehension inlining.", kb)
    assert res.is_approved is True
    assert res.faithfulness_score == 1.0
