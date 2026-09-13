def test_dashboard_counts_tasks_and_priorities(client, auth_headers):
    project = client.post("/api/projects", headers=auth_headers, json={"name": "Ops"}).json()
    project_id = project["id"]
    client.post("/api/tasks", headers=auth_headers, json={"title": "Monitor", "project_id": project_id, "priority": "CRITICAL"})
    client.post("/api/tasks", headers=auth_headers, json={"title": "Document", "project_id": project_id, "status": "DONE", "priority": "LOW"})

    response = client.get("/api/dashboard", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total_projects"] == 1
    assert body["total_tasks"] == 2
    assert body["completed_tasks"] == 1
    assert body["pending_tasks"] == 1
    assert body["tasks_by_priority"] == {"CRITICAL": 1, "LOW": 1}
