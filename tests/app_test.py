from unittest import mock


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_list_urls(test_client):
    response = test_client.get("/urls")
    assert response.status_code == 200


def test_create_invalid_url(test_client):
    body = {"target_url": "Foo"}
    response = test_client.post("/urls", json=body)
    assert response.status_code == 400


def test_create_url(test_client):
    body = {"target_url": "https://example.com/"}
    response = test_client.post("/urls", json=body)
    assert response.status_code == 200


@mock.patch("shortener.logic.url.incr_url_clicks", autospec=True)
def test_redirect_to_target_url(mock_incr_url_clicks, test_client, url):
    response = test_client.get(f"/{url.key}", allow_redirects=False)
    mock_incr_url_clicks.assert_called_once()
    assert response.status_code == 307


def test_fail_to_redirect_to_target_url(test_client):
    response = test_client.get("/idontexist", allow_redirects=False)
    assert response.status_code == 404


def test_manage_url_with_secret_key(test_client, url):
    response = test_client.get(f"/admin/{url.secret_key}", allow_redirects=False)
    assert response.status_code == 200


def test_manage_url_with_key(test_client, url):
    response = test_client.get(f"/admin/{url.key}", allow_redirects=False)
    assert response.status_code == 404


def test_fail_to_manage_url(test_client):
    response = test_client.get("/admin/idontexist", allow_redirects=False)
    assert response.status_code == 404


@mock.patch("shortener.logic.url.deactivate_url_by", autospec=True)
def test_delete_url(mock_deactivate_url_by, test_client, session, url):
    mock_deactivate_url_by.return_value = url
    response = test_client.delete(f"/admin/{url.secret_key}", allow_redirects=False)
    mock_deactivate_url_by.assert_called_once_with(mock.ANY, secret_key=url.secret_key)
    assert response.status_code == 200


def test_fail_to_delete_url(test_client):
    response = test_client.delete("/admin/idontexist", allow_redirects=False)
    assert response.status_code == 404
