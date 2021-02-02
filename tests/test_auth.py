from http import HTTPStatus


def test_revoke_access_token(client, admin_headers):
    resp = client.delete("/auth/revoke_access", headers=admin_headers)
    assert resp.status_code == HTTPStatus.OK

    resp = client.get("/api/v1/players", headers=admin_headers)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


def test_revoke_resfresh_token(client, admin_refresh_headers):
    resp = client.delete("/auth/revoke_refresh", headers=admin_refresh_headers)
    assert resp.status_code == HTTPStatus.OK

    resp = client.post("/auth/refresh", headers=admin_refresh_headers)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
