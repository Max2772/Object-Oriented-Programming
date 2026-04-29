def test_create_cash_account(client, auth_headers):
    resp = client.post("/api/v1/accounts/", json={
        "name": "Cash Wallet",
        "account_type": "cash",
        "balance": 5000.0,
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["name"] == "Cash Wallet"
    assert data["account_type"] == "cash"
    assert data["balance"] == 5000.0


def test_create_card_account(client, auth_headers):
    resp = client.post("/api/v1/accounts/", json={
        "name": "Visa",
        "account_type": "card",
        "balance": 0,
    }, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["data"]["account_type"] == "card"


def test_create_savings_account(client, auth_headers):
    resp = client.post("/api/v1/accounts/", json={
        "name": "Savings Account",
        "account_type": "savings",
        "balance": 100000.0,
    }, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["data"]["account_type"] == "savings"


def test_create_account_negative_balance(client, auth_headers):
    resp = client.post("/api/v1/accounts/", json={
        "name": "Test Negative Balance",
        "account_type": "cash",
        "balance": -100,
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_get_accounts_empty(client, auth_headers):
    resp = client.get("/api/v1/accounts/", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"] == []


def test_get_accounts_list(client, auth_headers):
    client.post("/api/v1/accounts/", json={
        "name": "Account 1", "account_type": "cash", "balance": 100,
    }, headers=auth_headers)
    client.post("/api/v1/accounts/", json={
        "name": "Account 2", "account_type": "card", "balance": 200,
    }, headers=auth_headers)

    resp = client.get("/api/v1/accounts/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 2


def test_get_account_by_id(client, auth_headers, sample_account):
    account_id = sample_account["id"]
    resp = client.get(f"/api/v1/accounts/{account_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["id"] == account_id


def test_get_nonexistent_account(client, auth_headers):
    resp = client.get("/api/v1/accounts/9999", headers=auth_headers)
    assert resp.status_code == 404


def test_update_account_name(client, auth_headers, sample_account):
    account_id = sample_account["id"]
    resp = client.put(f"/api/v1/accounts/{account_id}", json={
        "name": "New Name",
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "New Name"


def test_update_account_type(client, auth_headers, sample_account):
    account_id = sample_account["id"]
    resp = client.put(f"/api/v1/accounts/{account_id}", json={
        "account_type": "card",
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["account_type"] == "card"


def test_update_nonexistent_account(client, auth_headers, sample_account):
    resp = client.put(f"/api/v1/accounts/9999", json={
        "account_type": "card",
    }, headers=auth_headers)
    assert resp.status_code == 404


def test_delete_account(client, auth_headers, sample_account):
    account_id = sample_account["id"]
    resp = client.delete(f"/api/v1/accounts/{account_id}", headers=auth_headers)
    assert resp.status_code == 200

    resp = client.get(f"/api/v1/accounts/{account_id}", headers=auth_headers)
    assert resp.status_code == 404


def test_delete_nonexistent_account(client, auth_headers):
    resp = client.delete("/api/v1/accounts/9999", headers=auth_headers)
    assert resp.status_code == 404
