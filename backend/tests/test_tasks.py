def test_task_crud_status_priority_and_validation(client, auth_headers):
    project = client.post("/api/projects", headers=auth_headers, json={"name": "Release"}).json()
    task_payload = {"title": "Ship API", "project_id": project["id"], "priority": "HIGH"}
    created = client.post("/api/tasks", headers=auth_headers, json=task_payload)
    assert created.status_code == 201
    task_id = created.json()["id"]

    changed = client.patch(f"/api/tasks/{task_id}", headers=auth_headers, json={"status": "DONE"})
    assert changed.status_code == 200
    assert changed.json()["status"] == "DONE"

    invalid = client.post("/api/tasks", headers=auth_headers, json={**task_payload, "priority": "URGENT"})
    assert invalid.status_code == 422

    deleted = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
    assert deleted.status_code == 204
