from datetime import datetime

import pytest


@pytest.mark.parametrize('json, keys, expected_data', [
    (
        {'full_amount': 10},
        ['full_amount', 'id', 'create_date'],
        {'full_amount': 10, 'id': 1},
    ),
    (
        {'full_amount': 5, 'comment': 'To you for chimichangas'},
        ['full_amount', 'id', 'create_date', 'comment'],
        {'full_amount': 5, 'id': 1, 'comment': 'To you for chimichangas'},
    ),
])
def test_create_donation(user_client, json, keys, expected_data):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 200, (
        'При создании пожертвования должен возвращаться статус-код 200.'
    )
    data = response.json()
    assert sorted(list(data.keys())) == sorted(keys), (
        f'При создании пожертвования в ответе должны быть ключи `{keys}`.'
    )
    data.pop('create_date')
    assert data == expected_data, (
        'При создании пожертвования тело ответа API отличается от ожидаемого.'
    )


@pytest.mark.parametrize('json', [
    {'comment': 'To you for chimichangas'},
    {'full_amount': -1},
    {'full_amount': None},
    {'fully_invested': True},
    {'user_id': 3},
    {'create_date': str(datetime.now())},
    {'invested_amount': 10},
])
def test_create_donation_incorrect(user_client, json):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 422, (
        'При некорректном теле POST-запроса к эндпоинту `/donation/` '
        'должен вернуться статус-код 422.'
    )


def test_get_user_donation(user_client, donation):
    response = user_client.get('/donation/my')
    assert response.status_code == 200, (
        'При получении списка пожертвований пользователя должен вернуться '
        'статус-код 200.'
    )
    assert isinstance(response.json(), list), (
        'При получении списка пожертвований пользователя должен возвращаться '
        'объект типа `list`.'
    )
    assert len(response.json()) == 1, (
        'При корректном POST-запросе к эндпоинту `/charity_project/` не '
        'создаётся объект в БД. Проверьте модель `Donation`.'
    )
    data = response.json()[0]
    keys = sorted([
        'full_amount',
        'comment',
        'id',
        'create_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        'При получении списка пожертвований пользователя в ответе должны '
        f'быть ключи `{keys}`.'
    )
    assert response.json() == [{
        'comment': 'To you for chimichangas',
        'create_date': '2011-11-11T00:00:00',
        'full_amount': 100,
        'id': 1,
    }], (
        'При получении списка пожертвований пользователя тело ответа API '
        'отличается от ожидаемого.'
    )


def test_get_all_donations(superuser_client, donation, another_donation):
    response = superuser_client.get('/donation/')
    assert response.status_code == 200, (
        'При получении списка всех пожертвований должен возвращаться '
        'статус-код 200.'
    )
    assert isinstance(response.json(), list), (
        'При получении списка всех пожертвований должен возвращаться объект '
        'типа `list`.'
    )
    assert len(response.json()) == 2, (
        'При корректном POST-запросе к эндпоинту `/charity_project/` не '
        'создаётся объект в БД. Проверьте модель `Donation`.'
    )
    data = response.json()[0]
    keys = sorted([
        'full_amount',
        'comment',
        'id',
        'create_date',
        'user_id',
        'invested_amount',
        'fully_invested',
    ])
    assert sorted(list(data.keys())) == keys, (
        'При получении списка всех пожертвований в ответе должны быть ключи '
        f'`{keys}`.'
    )
    data = response.json()
    assert data == [
        {
            'comment': 'To you for chimichangas',
            'create_date': '2011-11-11T00:00:00',
            'full_amount': 100,
            'id': 1,
            'user_id': 2,
            'invested_amount': 0,
            'fully_invested': False,
        },
        {
            'comment': 'From admin',
            'create_date': '2012-12-12T00:00:00',
            'full_amount': 2000,
            'id': 2,
            'user_id': 1,
            'invested_amount': 0,
            'fully_invested': False,
        }
    ], (
        'При получении списка всех пожертвований тело ответа API отличается '
        'от ожидаемого.'
    )


@pytest.mark.parametrize('json', [
    {'full_amount': -1},
    {'full_amount': 0.5},
    {'full_amount': 0.155555},
    {'full_amount': -1.5},
])
def test_donation_invalid(user_client, json):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 422, (
        'Сумма пожертвований должна быть целочисленной и больше 0. '
        'Статус-код должен быть 422.'
    )


def test_donation_superuser_UD_enpoints(superuser_client, donation):
    response = superuser_client.patch('/donation/1')
    assert response.status_code == 404, (
        'Суперпользователь не может редактировать пожертвования'
    )
    response = superuser_client.delete('/donation/1')
    assert response.status_code == 404, (
        'Суперпользователю должно быть запрещено удалять пожертвования'
    )


def test_donation_auth_user_UD_enpoints(user_client, donation):
    response = user_client.patch('/donation/1')
    assert response.status_code == 404, (
        'Зарегистрированному пользователю должно быть запрещено редактировать '
        'пожертвования'
    )
    response = user_client.delete('/donation/1')
    assert response.status_code == 404, (
        'Зарегистрированному пользователю должно быть запрещено удалять '
        'пожертвования'
    )


def test_donation_user_UD_enpoints(test_client, donation):
    response = test_client.patch('/donation/1')
    assert response.status_code == 404, (
        'Незарегистрированному пользователю должно быть запрещено '
        'редактировать пожертвования'
    )
    response = test_client.delete('/donation/1')
    assert response.status_code == 404, (
        'Незарегистрированному пользователю должно быть запрещено удалять '
        'пожертвования'
    )


def test_create_donation_check_create_date(user_client):
    response_1 = user_client.post('/donation/', json={'full_amount': 10})
    response_2 = user_client.post('/donation/', json={'full_amount': 20})
    assert (
        response_1.json()['create_date'] != response_2.json()['create_date']
    ), (
        'При создании двух пожертвований с паузой (в 1 секунду, например) у '
        'них должны быть разные `create_date`'
    )
