def test_summary_with_transactions(client, auth_headers, sample_account):
    client.post("/api/v1/transactions/", json={
        "amount": 50000, "transaction_type": "income",
        "category": "salary", "description": "Paycheck",
        "account_id": sample_account["id"],
    }, headers=auth_headers)

    client.post("/api/v1/transactions/", json={
        "amount": 1500, "transaction_type": "expense",
        "category": "food", "description": "Groceries",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    client.post("/api/v1/transactions/", json={
        "amount": 500, "transaction_type": "expense",
        "category": "transport", "description": "Metro",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    client.post("/api/v1/transactions/", json={
        "amount": 2000, "transaction_type": "expense",
        "category": "leisure", "description": "Theatre",
        "account_id": sample_account["id"],
    }, headers=auth_headers)

    resp = client.get(
        "/api/v1/analytics/summary?date_from=2020-01-01T00:00:00&date_to=2030-12-31T23:59:59",
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total_income"] == 50000.0
    assert data["total_expense"] == 4000.0
    assert data["balance_change"] == 46000.0
    assert len(data["by_category"]) == 4


def test_summary_empty(client, auth_headers):
    resp = client.get(
        "/api/v1/analytics/summary?date_from=2020-01-01T00:00:00&date_to=2030-12-31T23:59:59",
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total_income"] == 0.0
    assert data["total_expense"] == 0.0
    assert data["by_category"] == []


def test_summary_filter_by_category(client, auth_headers, sample_account):
    client.post("/api/v1/transactions/", json={
        "amount": 100, "transaction_type": "expense",
        "category": "food", "description": "",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    client.post("/api/v1/transactions/", json={
        "amount": 200, "transaction_type": "expense",
        "category": "transport", "description": "",
        "account_id": sample_account["id"],
    }, headers=auth_headers)

    resp = client.get(
        "/api/v1/analytics/summary?date_from=2020-01-01T00:00:00&date_to=2030-12-31T23:59:59&category=food",
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total_expense"] == 100.0
    assert len(data["by_category"]) == 1
    assert data["by_category"][0]["category"] == "food"


def test_summary_missing_dates(client, auth_headers):
    resp = client.get("/api/v1/analytics/summary", headers=auth_headers)
    assert resp.status_code == 422