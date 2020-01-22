import requests.exceptions

from diarybot.transformers.location import LocationTransformer, GEOCODING_API


def test_server_unreachable(requests_mock):
    requests_mock.get(
        GEOCODING_API,
        exc=requests.exceptions.ConnectionError,
    )
    location = LocationTransformer(google_api_key='key')
    message = location.handle_coordinates(latitude=33, longitude=-33)
    assert message == "Latitude: 33\nLongitude: -33"
    assert requests_mock.call_count == 1


def test_resolves_address_with_key(requests_mock):
    requests_mock.get(
        GEOCODING_API,
        json={
            'plus_code': {'global_code': '89592222+22'},
            'results': [{
                'address_components': [
                    {'long_name': 'Atlantic Ocean',
                     'short_name': 'Atlantic Ocean',
                     'types': ['establishment', 'natural_feature']}],
                'formatted_address': 'Atlantic Ocean',
                'geometry': {'bounds': {'northeast': {'lat': 68.1962901, 'lng': 19.9970779},
                                        'southwest': {'lat': -75.9725902, 'lng': -82.9931606}},
                             'location': {'lat': -14.5994134, 'lng': -28.6731465},
                             'location_type': 'APPROXIMATE',
                             'viewport': {'northeast': {'lat': 68.1962901, 'lng': 19.9970779},
                                          'southwest': {'lat': -75.9725902, 'lng': -82.9931606}}},
                'place_id': 'ChIJ_7hu48qBWgYRT1MQ81ciNKY',
                'types': ['establishment', 'natural_feature']
            }],
            'status': 'OK'
        }
    )
    location = LocationTransformer(google_api_key='key')
    message = location.handle_coordinates(latitude=33, longitude=-33)
    assert message == "Latitude: 33\nLongitude: -33\nAddress: Atlantic Ocean"
    assert requests_mock.call_count == 1


def test_skips_for_missing_key(requests_mock):
    location = LocationTransformer(google_api_key='')
    message = location.handle_coordinates(latitude=12, longitude=34)
    assert message == "Latitude: 12\nLongitude: 34"
    assert requests_mock.call_count == 0


def test_skips_for_wrong_key(requests_mock):
    requests_mock.get(
        GEOCODING_API,
        json={
            'error_message': 'The provided API key is invalid.',
            'results': [],
            'status': 'REQUEST_DENIED'
        }
    )
    location = LocationTransformer(google_api_key='wrong-key')
    message = location.handle_coordinates(latitude=12, longitude=34)
    assert message == "Latitude: 12\nLongitude: 34"
    assert requests_mock.call_count == 1
