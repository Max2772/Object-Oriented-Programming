def test_create_expense(client, auth_headers, sample_account):
    resp = client.post("/api/v1/transactions/", json={
        "amount": 500.0,
        "transaction_type": "expense",
        "category": "food",
        "description": "Dinner at restaurant",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    assert resp.status_code == 201
    tx = resp.json()["data"]["transaction"]
    assert tx["amount"] == 500.0
    assert tx["transaction_type"] == "expense"
    assert tx["category"] == "food"

    acc = client.get(
        f"/api/v1/accounts/{sample_account['id']}", headers=auth_headers
    ).json()["data"]
    assert acc["balance"] == 9500.0


def test_create_income(client, auth_headers, sample_account):
    resp = client.post("/api/v1/transactions/", json={
        "amount": 50000.0,
        "transaction_type": "income",
        "category": "salary",
        "description": "Paycheck",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    assert resp.status_code == 201

    acc = client.get(
        f"/api/v1/accounts/{sample_account['id']}", headers=auth_headers
    ).json()["data"]
    assert acc["balance"] == 60000.0


def test_create_transaction_invalid_account(client, auth_headers):
    resp = client.post("/api/v1/transactions/", json={
        "amount": 100,
        "transaction_type": "expense",
        "category": "food",
        "description": "",
        "account_id": 9999,
    }, headers=auth_headers)
    assert resp.status_code == 404


def test_create_transaction_zero_amount(client, auth_headers, sample_account):
    resp = client.post("/api/v1/transactions/", json={
        "amount": 0,
        "transaction_type": "expense",
        "category": "food",
        "description": "",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_create_transaction_negative_amount(client, auth_headers, sample_account):
    resp = client.post("/api/v1/transactions/", json={
        "amount": -100,
        "transaction_type": "expense",
        "category": "food",
        "description": "",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_get_transactions_empty(client, auth_headers):
    resp = client.get("/api/v1/transactions/", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"] == []


def test_get_transactions_list(client, auth_headers, sample_account):
    for i in range(3):
        client.post("/api/v1/transactions/", json={
            "amount": 100 * (i + 1),
            "transaction_type": "expense",
            "category": "food",
            "description": f"Meal {i + 1}",
            "account_id": sample_account["id"],
        }, headers=auth_headers)

    resp = client.get("/api/v1/transactions/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 3


def test_filter_by_category(client, auth_headers, sample_account):
    client.post("/api/v1/transactions/", json={
        "amount": 100, "transaction_type": "expense",
        "category": "food", "description": "", "account_id": sample_account["id"],
    }, headers=auth_headers)
    client.post("/api/v1/transactions/", json={
        "amount": 200, "transaction_type": "expense",
        "category": "transport", "description": "", "account_id": sample_account["id"],
    }, headers=auth_headers)

    resp = client.get(
        "/api/v1/transactions/?category=food", headers=auth_headers
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 1
    assert data[0]["category"] == "food"


def test_filter_by_type(client, auth_headers, sample_account):
    client.post("/api/v1/transactions/", json={
        "amount": 100, "transaction_type": "expense",
        "category": "food", "description": "", "account_id": sample_account["id"],
    }, headers=auth_headers)
    client.post("/api/v1/transactions/", json={
        "amount": 5000, "transaction_type": "income",
        "category": "salary", "description": "", "account_id": sample_account["id"],
    }, headers=auth_headers)

    resp = client.get(
        "/api/v1/transactions/?transaction_type=income", headers=auth_headers
    )
    data = resp.json()["data"]
    assert len(data) == 1
    assert data[0]["transaction_type"] == "income"


def test_delete_expense_restores_balance(client, auth_headers, sample_account):
    resp = client.post("/api/v1/transactions/", json={
        "amount": 1000,
        "transaction_type": "expense",
        "category": "food",
        "description": "Dinner",
        "account_id": sample_account["id"],
    }, headers=auth_headers)
    transaction_id = resp.json()["data"]["transaction"]["id"]

    acc = client.get(
        f"/api/v1/accounts/{sample_account['id']}", headers=auth_headers
    ).json()["data"]
    assert acc["balance"] == 9000.0

    resp = client.delete(f"/api/v1/transactions/{transaction_id}", headers=auth_headers)
    assert resp.status_code == 200

    acc = client.get(
        f"/api/v1/accounts/{sample_account['id']}", headers=auth_headers
    ).json()["data"]
    assert acc["balance"] == 10000.0


def test_delete_nonexistent_transaction(client, auth_headers):
    resp = client.delete("/api/v1/transactions/9999", headers=auth_headers)
    assert resp.status_code == 404
