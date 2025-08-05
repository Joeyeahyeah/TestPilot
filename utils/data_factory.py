from faker import Faker


def generate_user():
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address()
    }


# 测试用例中使用
def test_register(api):
    user_data = generate_user()
    resp = api.post("/register", json=user_data)
    assert resp.status_code == 201