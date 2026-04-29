def test_register_success(client):
    resp = client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["username"] == "newuser"
    assert data["data"]["email"] == "new@example.com"


def test_register_duplicate_username(client):
    client.post("/api/v1/auth/register", json={
        "username": "duplicate",
        "email": "first@example.com",
        "password": "password123",
    })
    resp = client.post("/api/v1/auth/register", json={
        "username": "duplicate",
        "email": "second@example.com",
        "password": "password123",
    })
    assert resp.status_code == 409


def test_register_duplicate_email(client):
    client.post("/api/v1/auth/register", json={
        "username": "user1",
        "email": "same@example.com",
        "password": "password123",
    })
    resp = client.post("/api/v1/auth/register", json={
        "username": "user2",
        "email": "same@example.com",
        "password": "password123",
    })
    assert resp.status_code == 409


def test_register_short_password(client):
    resp = client.post("/api/v1/auth/register", json={
        "username": "user",
        "email": "user@example.com",
        "password": "123",
    })
    assert resp.status_code == 422


def test_register_short_username(client):
    resp = client.post("/api/v1/auth/register", json={
        "username": "ab",
        "email": "user@example.com",
        "password": "password123",
    })
    assert resp.status_code == 422


def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123",
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": "loginuser",
        "password": "password123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={
        "username": "loginuser2",
        "email": "login2@example.com",
        "password": "password123",
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": "loginuser2",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401


def test_login_nonexistent_user(client):
    resp = client.post("/api/v1/auth/login", json={
        "username": "ghost",
        "password": "password123",
    })
    assert resp.status_code == 401


def test_protected_endpoint_without_token(client):
    resp = client.get("/api/v1/accounts/")
    assert resp.status_code == 401


def test_protected_endpoint_with_invalid_token(client):
    resp = client.get("/api/v1/accounts/", headers={
        "Authorization": "Bearer invalid_token_here"
    })
    assert resp.status_code == 401
