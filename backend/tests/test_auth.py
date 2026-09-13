def test_registration_login_and_duplicate_email(client):
    payload = {"name": "Taylor", "email": "taylor@example.com", "password": "password123"}
    created = client.post("/api/auth/register", json=payload)
    assert created.status_code == 201
    assert created.json()["user"]["email"] == payload["email"]

    duplicate = client.post("/api/auth/register", json=payload)
    assert duplicate.status_code == 409

    logged_in = client.post("/api/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert logged_in.status_code == 200
    assert logged_in.json()["token_type"] == "bearer"

    invalid = client.post("/api/auth/login", json={"email": payload["email"], "password": "wrong-password"})
    assert invalid.status_code == 401


def test_protected_route_requires_token(client):
    assert client.get("/api/projects").status_code == 401
