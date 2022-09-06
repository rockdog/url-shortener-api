def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_create_invalid_url(test_client):
    body = {"target_url": "Foo"}
    response = test_client.post("/url", json=body)
    assert response.status_code == 400


def test_create_url(test_client):
    body = {"target_url": "https://example.com/"}
    response = test_client.post("/url", json=body)
    assert response.status_code == 200
