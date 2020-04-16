from http import HTTPStatus

from ...tests.support import helpers


def test_asset_upload(person, client):
    """Test uploading an asset image for a person"""

    asset = helpers.load_file_data('test.png')

    response = client.put(
        f'/api/v1/people/{person.id}',
        data={'asset': asset},
        content_type='multipart/form-data'
    )

    data = response.json
    assert response.status_code == HTTPStatus.CREATED
    assert data['data']['asset'] == person.asset.url
