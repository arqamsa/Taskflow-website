def test_project_crud(client, auth_headers):
    created = client.post("/api/projects", headers=auth_headers, json={"name": "Website", "description": "Launch site"})
    assert created.status_code == 201
    project_id = created.json()["id"]
    assert created.json()["task_count"] == 0

    listed = client.get("/api/projects", headers=auth_headers)
    assert listed.status_code == 200
    assert listed.json()[0]["name"] == "Website"

    updated = client.patch(f"/api/projects/{project_id}", headers=auth_headers, json={"status": "ARCHIVED"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "ARCHIVED"

    deleted = client.delete(f"/api/projects/{project_id}", headers=auth_headers)
    assert deleted.status_code == 204
    assert client.get(f"/api/projects/{project_id}", headers=auth_headers).status_code == 404
