from fact_checking_gateway import FactCheckingGateway

kb = {
    "auth_doc": "OAuth2.0 authorization code flow mandates PKCE for public mobile and single-page applications.",
    "crypto_doc": "AES-GCM provides authenticated encryption with associated data."
}

test_response = """
OAuth2 authorization code flow mandates PKCE for public mobile applications.
AES-GCM delivers authenticated encryption for secure payloads.
Ethereum blockchain automatically manages local system kernel memory.
"""

gateway = FactCheckingGateway()
report = gateway.verify_output(test_response, kb)

print(f"Gateway Verdict: {'APPROVED' if report.is_approved else 'BLOCKED'}")
print(f"Faithfulness Score: {report.faithfulness_score * 100:.1f}%")
print("\nDetailed Assertions Verification:")
for s in report.statements:
    status = "✔ PASS" if s.verified else "✖ FAIL"
    print(f"[{s.statement_id}] {status} ({s.confidence_score:.2f}) -> {s.assertion}")
