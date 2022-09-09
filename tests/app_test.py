def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_list_urls(test_client):
    response = test_client.get("/urls")
    assert response.status_code == 200


def test_create_invalid_url(test_client):
    body = {"target_url": "Foo"}
    response = test_client.post("/url", json=body)
    assert response.status_code == 400


def test_create_url(test_client):
    body = {"target_url": "https://example.com/"}
    response = test_client.post("/url", json=body)
    assert response.status_code == 200


def test_redirect_to_target_url(test_client, url):
    response = test_client.get(f"/{url.key}", allow_redirects=False)
    assert response.status_code == 307


def test_fail_to_redirect_to_target_url(test_client):
    response = test_client.get("/idontexist", allow_redirects=False)
    assert response.status_code == 404
