from __future__ import annotations


def test_cities(client) -> None:
    r = client.get("/api/cities")
    assert r.status_code == 200
    cities = r.json()
    assert any(c["slug"] == "worcester" for c in cities)


def test_sites(client) -> None:
    r = client.get("/api/sites", params={"city": "worcester"})
    assert r.status_code == 200
    sites = r.json()
    assert len(sites) > 10
    assert {"id", "lat", "lng", "score_overall", "daily_kwh_estimate"}.issubset(sites[0].keys())


def test_predict(client) -> None:
    payload = {
        "traffic_index": 0.8,
        "pop_density_index": 0.6,
        "renters_share": 0.5,
        "income_index": 0.4,
        "poi_index": 0.7,
    }
    r = client.post("/api/predict", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "predicted_daily_kwh" in body
    assert "scores" in body
