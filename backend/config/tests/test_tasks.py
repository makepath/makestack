from config.celery import hello_world


def test_hello_world():
    result = hello_world()
    expected = "Hello world."

    assert result == expected
