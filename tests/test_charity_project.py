from datetime import datetime

import pytest


@pytest.mark.parametrize(
    'invalid_name',
    [
        '',
        'lovechimichangasbutnunchakuisbetternunchakis4life' * 3,
        None,
    ],
)
def test_create_invalid_project_name(superuser_client, invalid_name):
    response = superuser_client.post(
        '/charity_project/',
        json={
            'name': invalid_name,
            'description': 'Project_1',
            'full_amount': 5000,
        },
    )
    assert response.status_code == 422, (
        'Создание проектов с пустым названием или с названием длиннее 100 '
        'символов должно быть запрещено.'
    )


@pytest.mark.parametrize(
    'desc', [
        '',
        None,
    ]
)
def test_create_project_no_desc(superuser_client, desc):
    response = superuser_client.post(
        '/charity_project/',
        json={
            'name': 'Мертвый Бассейн',
            'description': desc,
            'full_amount': 5000,
        },
    )
    assert (
        response.status_code == 422
    ), 'Создание проектов с пустым описанием должно быть запрещено.'


@pytest.mark.parametrize('json', [
    {'invested_amount': 100},
    {'fully_invested': True},
    {'id': 5000},
])
def test_create_project_with_autofilling_fields(superuser_client, json):
    response = superuser_client.post(
        '/charity_project/',
        json=json
    )
    assert response.status_code == 422, (
        'При попытке передать в запросе значения для автозаполняемых полей '
        'должна возвращаться ошибка 422.'
    )


@pytest.mark.parametrize(
    'invalid_full_amount',
    [
        -100,
        0.5,
        'test',
        0.0,
        '',
        None,
    ],
)
def test_create_invalid_full_amount_value(superuser_client,
                                          invalid_full_amount):
    response = superuser_client.post(
        '/charity_project/',
        json={
            'name': 'Project_1',
            'description': 'Project_1',
            'full_amount': invalid_full_amount,
        },
    )
    assert response.status_code == 422, (
        'Требуемая сумма (full_amount) проекта должна быть целочисленной и '
        'больше 0.'
    )


def test_get_charity_project(user_client, charity_project):
    response = user_client.get('/charity_project/')
    assert response.status_code == 200, (
        'При GET-запросе к эндпоинту `/charity_project/` должен возвращаться '
        'статус-код 200.'
    )
    assert isinstance(response.json(), list), (
        'При GET-запросе к эндпоинту `/charity_project/` должен возвращаться '
        'объект типа `list`.'
    )
    assert len(response.json()) == 1, (
        'При корректном POST-запросе к эндпоинту `/charity_project/` не '
        'создаётся объект в БД. Проверьте модель `CharityProject`.'
    )
    data = response.json()[0]
    keys = sorted(
        [
            'name',
            'description',
            'full_amount',
            'id',
            'invested_amount',
            'fully_invested',
            'create_date',
        ]
    )
    assert sorted(list(data.keys())) == keys, (
        'При GET-запросе к эндпоинту `/charity_project/` в ответе API должны '
        f'быть ключи `{keys}`.'
    )
    assert response.json() == [
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
            'fully_invested': False,
            'id': 1,
            'invested_amount': 0,
            'name': 'chimichangas4life',
        }
    ], (
        'При GET-запросе к эндпоинту `/charity_project/` тело ответа API '
        'отличается от ожидаемого.'
    )


def test_get_all_charity_project(
    user_client, charity_project, charity_project_nunchaku
):
    response = user_client.get('/charity_project/')
    assert response.status_code == 200, (
        'При запросе всех проектов должен возвращаться статус-код 200.'
    )
    assert isinstance(response.json(), list), (
        'При запросе всех проектов должен возвращаться объект типа `list`.'
    )
    assert len(response.json()) == 2, (
        'При корректном POST-запросе к эндпоинту `/charity_project/` не '
        'создаётся объект в БД. Проверьте модель `CharityProject`.'
    )
    data = response.json()[0]
    keys = sorted(
        [
            'name',
            'description',
            'full_amount',
            'id',
            'invested_amount',
            'fully_invested',
            'create_date',
        ]
    )
    assert sorted(list(data.keys())) == keys, (
        f'При запросе всех проектов в ответе API должны быть ключи `{keys}`.'
    )
    assert response.json() == [
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
            'fully_invested': False,
            'id': 1,
            'invested_amount': 0,
            'name': 'chimichangas4life',
        },
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
            'fully_invested': False,
            'id': 2,
            'invested_amount': 0,
            'name': 'nunchaku',
        },
    ], 'При запросе всех проектов тело ответа API отличается от ожидаемого.'


def test_create_charity_project(superuser_client):
    response = superuser_client.post(
        '/charity_project/',
        json={
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': 1000000,
        },
    )
    assert (
        response.status_code == 200
    ), 'При создании проекта должен возвращаться статус-код 200.'
    data = response.json()
    keys = sorted(
        [
            'name',
            'description',
            'full_amount',
            'create_date',
            'fully_invested',
            'id',
            'invested_amount',
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f'При создании проекта в ответе API должны быть ключи `{keys}`.'
    data.pop('create_date')
    assert data == {
        'description': 'Deadpool inside',
        'full_amount': 1000000,
        'fully_invested': False,
        'id': 1,
        'invested_amount': 0,
        'name': 'Мертвый Бассейн',
    }, 'При создании проекта тело ответа API отличается от ожидаемого.'


@pytest.mark.parametrize(
    'json',
    [
        {
            'name': 'Мертвый Бассейн',
            'full_amount': '1000000',
        },
        {
            'description': 'Deadpool inside',
            'full_amount': '1000000',
        },
        {
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
        },
        {
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': 'Donat',
        },
        {
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': '',
        },
        {},
    ],
)
def test_create_charity_project_validation_error(json, superuser_client):
    response = superuser_client.post('/charity_project/', json=json)
    assert response.status_code == 422, (
        'При некорректном создании проекта должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert 'detail' in data.keys(), (
        'При некорректном создании проекта в ответе API должен быть ключ '
        '`detail`.'
    )


def test_delete_project_usual_user(user_client, charity_project):
    response = user_client.delete('/charity_project/1')
    assert response.status_code == 401, (
        'Только суперпользователь может удалить проект.'
    )


def test_delete_charity_project(superuser_client, charity_project):
    response = superuser_client.delete(
        f'/charity_project/{charity_project.id}'
    )
    assert response.status_code == 200, (
        'При удалении проекта должен возвращаться статус-код 200.'
    )
    data = response.json()
    keys = sorted(
        [
            'name',
            'description',
            'full_amount',
            'id',
            'invested_amount',
            'fully_invested',
            'create_date',
            'close_date',
        ]
    )
    assert sorted(list(data.keys())) == keys, (
        f'При удалении проекта в ответе API должны быть ключи `{keys}`.'
    )
    assert data == {
        'name': 'chimichangas4life',
        'description': 'Huge fan of chimichangas. Wanna buy a lot',
        'full_amount': 1000000,
        'id': 1,
        'invested_amount': 0,
        'fully_invested': False,
        'create_date': '2010-10-10T00:00:00',
        'close_date': None,
    }, 'При удалении проекта тело ответа API отличается от ожидаемого.'


def test_delete_charity_project_invalid_id(superuser_client):
    response = superuser_client.delete('/charity_project/999a4')
    assert response.status_code == 422, (
        'При некорректном удалении проекта должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert 'detail' in data.keys(), (
        'При некорректном удалении проекта в ответе API должен быть ключ '
        '`detail`'
    )


@pytest.mark.parametrize(
    'json, expected_data',
    [
        (
            {'full_amount': 10},
            {
                'name': 'chimichangas4life',
                'description': 'Huge fan of chimichangas. Wanna buy a lot',
                'full_amount': 10,
                'id': 1,
                'invested_amount': 0,
                'fully_invested': False,
                'close_date': None,
                'create_date': '2010-10-10T00:00:00',
            },
        ),
        (
            {'name': 'chimi'},
            {
                'name': 'chimi',
                'description': 'Huge fan of chimichangas. Wanna buy a lot',
                'full_amount': 1000000,
                'id': 1,
                'invested_amount': 0,
                'fully_invested': False,
                'close_date': None,
                'create_date': '2010-10-10T00:00:00',
            },
        ),
        (
            {'description': 'Give me the money!'},
            {
                'name': 'chimichangas4life',
                'description': 'Give me the money!',
                'full_amount': 1000000,
                'id': 1,
                'invested_amount': 0,
                'fully_invested': False,
                'close_date': None,
                'create_date': '2010-10-10T00:00:00',
            },
        ),
    ],
)
def test_update_charity_project(superuser_client, charity_project, json,
                                expected_data):
    response = superuser_client.patch('/charity_project/1', json=json)
    assert response.status_code == 200, (
        'При обновлении проекта должен возвращаться статус-код 200.'
    )
    data = response.json()
    keys = sorted(
        [
            'name',
            'description',
            'full_amount',
            'id',
            'invested_amount',
            'fully_invested',
            'create_date',
            'close_date',
        ]
    )
    assert sorted(list(data.keys())) == keys, (
        f'При обновлении проекта в ответе API должны быть ключи `{keys}`.'
    )
    assert data == expected_data, (
        'При обновлении проекта тело ответа API отличается от ожидаемого.'
    )


@pytest.mark.parametrize('json', [
    {'full_amount': 100},
    {'full_amount': 1000},
])
def test_update_charity_project_full_amount_equal_invested_amount(
        superuser_client, charity_project_little_invested, json
):
    response = superuser_client.patch(
        '/charity_project/1',
        json=json,
    )
    assert response.status_code == 200, (
        'При редактировании проекта должно быть разрешено устанавливать '
        'требуемую сумму больше или равную внесённой. Должен возвращаться '
        'статус-код 200.'
    )
    assert response.json()['full_amount'] == json['full_amount'], (
        'При редактировании проекта должно быть разрешено устанавливать '
        'требуемую сумму больше или равную внесённой. Требуемая сумма не '
        'изменилась.'
    )


@pytest.mark.parametrize(
    'json',
    [
        {'description': ''},
        {'name': ''},
        {'full_amount': ''},
    ],
)
def test_update_charity_project_invalid(superuser_client, charity_project,
                                        json):
    response = superuser_client.patch('/charity_project/1', json=json)
    assert response.status_code == 422, (
        'При редактировании проекта нельзя назначать пустое имя, описание '
        'или цель фонда. '
        'Должен возвращаться статус-код 422.'
    )


@pytest.mark.parametrize(
    'json',
    [
        {'invested_amount': 100},
        {'create_date': '2010-10-10'},
        {'close_date': '2010-10-10'},
        {'fully_invested': True},
    ],
)
def test_update_charity_with_unexpected_fields(superuser_client,
                                               charity_project, json):
    response = superuser_client.patch('/charity_project/1', json=json)
    assert response.status_code == 422, (
        'Убедитесь, что при редактировании проекта нельзя изменить значение '
        'полей, редактирование которых не предусмотрено спецификацией к API. '
        'Должен возвращаться статус-код 422.'
    )


def test_update_charity_project_same_name(superuser_client, charity_project,
                                          charity_project_nunchaku):
    response = superuser_client.patch(
        '/charity_project/1',
        json={
            'name': 'nunchaku',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
        },
    )
    assert response.status_code == 400, (
        'При редактировании проекта его новое имя должно быть уникальным.'
    )
    assert response.json() == {
        'detail': 'Проект с таким именем уже существует!'
    }


@pytest.mark.parametrize('full_amount', [
    0,
    5,
])
def test_update_charity_project_full_amount_smaller_already_invested(
        superuser_client, charity_project_little_invested, full_amount
):
    response = superuser_client.patch(
        '/charity_project/1',
        json={
            'name': 'nunchaku',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': full_amount,
        },
    )
    assert response.status_code in (400, 422), (
        'При редактировании проекта должно быть запрещено устанавливать '
        'требуемую сумму меньше внесённой.'
    )


def test_create_charity_project_usual_user(user_client):
    response = user_client.post(
        '/charity_project/',
        json={
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': 1000000,
        },
    )
    assert response.status_code == 401, (
        'При создании проекта не суперпользователем должен возвращаться '
        'статус-код 401.'
    )
    data = response.json()
    assert 'detail' in data, (
        'При создании проекта не суперпользователем в ответе API должен быть '
        'ключ `detail`.'
    )
    assert data == {'detail': 'Unauthorized'}, (
        'При создании проекта не суперпользователем тело ответа API '
        'отличается от ожидаемого.'
    )


def test_patch_charity_project_usual_user(user_client):
    response = user_client.patch(
        '/charity_project/1', json={'full_amount': 10}
    )
    assert response.status_code == 401, (
        'При обновлении проекта не суперпользователем должен возвращаться '
        'статус-код 401.'
    )
    data = response.json()
    assert 'detail' in data, (
        'При обновлении проекта не суперпользователем в ответе должен быть '
        'ключ `detail`.'
    )
    assert data == {'detail': 'Unauthorized'}, (
        'При обновлении проекта не суперпользователем тело ответа API '
        'отличается от ожидаемого.'
    )


def test_patch_charity_project_fully_invested(
        superuser_client, small_fully_charity_project,
):
    response = superuser_client.patch(
        '/charity_project/1', json={'full_amount': 10}
    )
    assert response.status_code == 400, (
        'При обновлении проекта, который был полностью проинвестирован, '
        'должен возвращаться статус-код 400.'
    )
    data = response.json()
    assert 'detail' in data, (
        'При обновлении проекта, который был полностью проинвестирован, '
        'в ответе должен быть ключ `detail`.'
    )
    assert data == {'detail': 'Закрытый проект нельзя редактировать!'}, (
        'При обновлении проекта, который был полностью '
        'проинвестирован, тело ответа API отличается от ожидаемого.'
    )


def test_create_charity_project_same_name(superuser_client, charity_project):
    response = superuser_client.post(
        '/charity_project/',
        json={
            'name': 'chimichangas4life',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
        },
    )
    assert response.status_code == 400, (
        'При создании проекта с неуникальным именем должен возвращаться '
        'статус-код 400.'
    )
    data = response.json()
    assert 'detail' in data, (
        'При создании проекта с неуникальным именем в ответе должен быть '
        'ключ `detail`.'
    )
    assert data == {'detail': 'Проект с таким именем уже существует!'}, (
        'При создании проекта с неуникальным именем '
        'тело ответа API отличается от ожидаемого.'
    )


def test_create_charity_project_diff_time(superuser_client):
    response_chimichangs = superuser_client.post(
        '/charity_project/',
        json={
            'name': 'chimichangas4life',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
        },
    )
    response_nunchaku = superuser_client.post(
        '/charity_project/',
        json={
            'name': 'nunchaku',
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
        },
    )
    chimichangas_create_date = response_chimichangs.json()['create_date']
    nunchakus_create_date = response_nunchaku.json()['create_date']
    assert chimichangas_create_date != nunchakus_create_date, (
        'При создании двух проектов подряд время создания не отличается. '
        'Проверьте значение по умолчанию у атрибута `create_date`'
    )


def test_donation_exist_project_create(superuser_client, donation):
    response = superuser_client.post(
        '/charity_project/',
        json={
            'name': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'full_amount': 100,
        },
    )
    data = response.json()
    assert data['fully_invested'], (
        'Если новая требуемая сумма равна уже внесённой - проект должен быть '
        'закрыт. В такой ситуации должно устанавливаться '
        '`fully_invested=True`.'
    )
    assert (
        data['close_date'] == datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    ), (
        'Если новая требуемая сумма равна уже внесённой - проект должен быть '
        'закрыт. В такой ситуации должно устанавливаться '
        '`close_date=<текущее время>`.'
    )


def test_delete_charity_project_already_invested(
        superuser_client, charity_project_little_invested):
    response = superuser_client.delete('/charity_project/1')
    assert response.status_code == 400, (
        'Удаление проектов, в которые уже внесены средства, должно быть '
        'запрещено. Статус-код ответа отличается от ожидаемого.'
    )
    assert response.json()['detail'] == (
        'В проект были внесены средства, не подлежит удалению!'
    ), (
        'Удаление проектов, в которые уже внесены средства, должно быть '
        'запрещено. Тело ответа отличается от ожидаемого.'
    )


def test_delete_charity_project_already_closed(superuser_client,
                                               closed_charity_project):
    response = superuser_client.delete('/charity_project/1')
    assert response.status_code == 400, (
        'Удаление закрытых проектов должно быть запрещено. Статус-код ответа '
        'отличается от ожидаемого.'
    )
    assert response.json()['detail'] == (
        'В проект были внесены средства, не подлежит удалению!'
    ), (
        'Удаление закрытых проектов должно быть запрещено. Тело ответа '
        'отличается от ожидаемого.'
    )


def test_get_all_charity_project_not_auth_user(test_client,
                                               charity_project,
                                               charity_project_nunchaku):
    response = test_client.get('/charity_project/')
    assert response.status_code == 200, (
        'Список проектов должен быть доступен даже неавторизованному '
        'пользователю.'
    )
    data = response.json()
    assert data == [
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
            'fully_invested': False,
            'id': 1,
            'invested_amount': 0,
            'name': 'chimichangas4life'
        },
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
            'fully_invested': False,
            'id': 2,
            'invested_amount': 0,
            'name': 'nunchaku'
        }
    ]
