from http import HTTPStatus


def test_clicks_endpoint(client, app_with_producer):
    response = client.post('/clicks/', json={
        'obj_id': '123',
        'time': 1646240200
    })

    assert response.status_code == HTTPStatus.CREATED
    assert app_with_producer.producer.send.called


def test_films_endpoint(client, app_with_producer):
    response = client.post('/films/', json={
        'film_id': 'ccc94e57-a383-450b-a1e2-7be0a2786fa2',
        'time': 1646240200,
        'timecode': '03:12:58.019077'
    })

    assert response.status_code == HTTPStatus.CREATED
    assert app_with_producer.producer.send.called


def test_custom_events_endpoint(client, app_with_producer):
    response = client.post('/custom_events/', json={
        'information': {'123': '123'},
        'time': 1646240200
    })

    assert response.status_code == HTTPStatus.CREATED
    assert app_with_producer.producer.send.called


def test_pages_endpoint(client, app_with_producer):
    response = client.post('/pages/', json={
        'duration': 16.1,
        'time': 1646240200,
        'url': 'http://example.com'
    })

    assert response.status_code == HTTPStatus.CREATED
    assert app_with_producer.producer.send.called
