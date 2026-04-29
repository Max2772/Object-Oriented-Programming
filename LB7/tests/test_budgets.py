def test_create_budget(client, auth_headers):
    resp = client.post("/api/v1/budgets/", json={
        "category": "food",
        "monthly_limit": 5000.0,
        "year": 2026,
        "month": 4,
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["category"] == "food"
    assert data["monthly_limit"] == 5000.0


def test_upsert_budget(client, auth_headers):
    client.post("/api/v1/budgets/", json={
        "category": "food",
        "monthly_limit": 5000.0,
        "year": 2026,
        "month": 4,
    }, headers=auth_headers)

    resp = client.post("/api/v1/budgets/", json={
        "category": "food",
        "monthly_limit": 7000.0,
        "year": 2026,
        "month": 4,
    }, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["data"]["monthly_limit"] == 7000.0


def test_create_budget_invalid_month(client, auth_headers):
    resp = client.post("/api/v1/budgets/", json={
        "category": "food",
        "monthly_limit": 5000.0,
        "year": 2026,
        "month": 13,
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_create_budget_zero_limit(client, auth_headers):
    resp = client.post("/api/v1/budgets/", json={
        "category": "food",
        "monthly_limit": 0,
        "year": 2026,
        "month": 4,
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_get_budgets_with_status(client, auth_headers, sample_account):
    client.post("/api/v1/budgets/", json={
        "category": "food",
        "monthly_limit": 3000.0,
        "year": 2026,
        "month": 4,
    }, headers=auth_headers)

    client.post("/api/v1/transactions/", json={
        "amount": 1500.0,
        "transaction_type": "expense",
        "category": "food",
        "description": "Products",
        "account_id": sample_account["id"],
    }, headers=auth_headers)

    resp = client.get(
        "/api/v1/budgets/?year=2026&month=4", headers=auth_headers
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 1
    budget = data[0]
    assert budget["category"] == "food"
    assert budget["monthly_limit"] == 3000.0
    assert budget["spent"] == 1500.0
    assert budget["remaining"] == 1500.0
    assert budget["exceeded"] is False


def test_get_budgets_empty(client, auth_headers):
    resp = client.get(
        "/api/v1/budgets/?year=2026&month=4", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["data"] == []


def test_budget_exceeded_warning(client, auth_headers, sample_account):
    client.post("/api/v1/budgets/", json={
        "category": "food",
        "monthly_limit": 1000.0,
        "year": 2026,
        "month": 4,
    }, headers=auth_headers)

    resp = client.post("/api/v1/transactions/", json={
        "amount": 1500.0,
        "transaction_type": "expense",
        "category": "food",
        "description": "Big Purchase",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["warning"] is not None
    assert "exceeded" in data["warning"]


def test_no_warning_within_limit(client, auth_headers, sample_account):
    client.post("/api/v1/budgets/", json={
        "category": "food",
        "monthly_limit": 5000.0,
        "year": 2026,
        "month": 4,
    }, headers=auth_headers)

    resp = client.post("/api/v1/transactions/", json={
        "amount": 100.0,
        "transaction_type": "expense",
        "category": "food",
        "description": "Cofe",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["data"]["warning"] is None


def test_delete_budget(client, auth_headers):
    resp = client.post("/api/v1/budgets/", json={
        "category": "transport",
        "monthly_limit": 2000.0,
        "year": 2026,
        "month": 4,
    }, headers=auth_headers)
    budget_id = resp.json()["data"]["id"]

    resp = client.delete(f"/api/v1/budgets/{budget_id}", headers=auth_headers)
    assert resp.status_code == 200


def test_delete_nonexistent_budget(client, auth_headers):
    resp = client.delete("/api/v1/budgets/9999", headers=auth_headers)
    assert resp.status_code == 404
