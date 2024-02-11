

def test_register(test_client):
    response = test_client.post('/auth/register', json={
        'email': 'dead@pool.com',
        'password': 'chimichangas4life',
    })
    assert response.status_code == 201, (
        'При регистрации пользователя должен возвращаться статус-код 201.'
    )
    data = response.json()
    keys = sorted(['id', 'email', 'is_active', 'is_superuser', 'is_verified'])
    assert sorted(list(data.keys())) == keys, (
        f'При регистрации пользователя в ответе должны быть ключи `{keys}`.'
    )
    data.pop('id')
    assert data == {
        'email': 'dead@pool.com',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
    }, 'При регистрации пользователя тело ответа API отличается от ожидаемого.'


def test_register_invalid_pass(user_client):
    response = user_client.post('/auth/register', json={
        'email': 'dead@pool.com',
        'password': '$',
    })
    assert response.status_code == 400, (
        'При некорректной регистрации пользователя должен возвращаться '
        'статус-код 400.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной регистрации пользователя в ответе должен быть ключ '
        '`detail`.'
    )
    assert data == {
        'detail': {
            'code': 'REGISTER_INVALID_PASSWORD',
            'reason': 'Password should be at least 3 characters',
        },
    }, (
        'При некорректной регистрации пользователя тело ответа API отличается '
        'от ожидаемого.'
    )
