import importlib.util
from pathlib import Path
import pytest

@pytest.fixture
def users_module(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    spec = importlib.util.spec_from_file_location('login_classes_under_test', Path(__file__).resolve().parents[1] / 'website/login_classes.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_login_accepts_matching_credentials_only(users_module):
    users = users_module.Users()
    users.users = [users_module.User('1', 'alex', 'test-password', '42')]
    assert users.login('alex', 'test-password') == '42'
    assert users.login('alex', 'wrong') is False
    assert users.login('unknown', 'test-password') is False

def test_load_saved_users_preserves_fields(users_module, tmp_path):
    file = tmp_path / 'fixture.csv'
    file.write_text('7,alex,test-password,42,base_user\n', encoding='utf-8')
    users = users_module.Users().load_users(str(file))
    assert len(users) == 1
    assert (users[0].userId, users[0].username, users[0].session_id, users[0].permission) == ('7', 'alex', '42', 'base_user')
    assert users_module.Users().load_users('missing.csv') == []

def test_session_updates_persist(users_module, tmp_path):
    file = tmp_path / 'latest_sessionid.txt'
    file.write_text('10', encoding='utf-8')
    session = users_module.SessionId()
    assert session.session_id == 10
    session.update_sessionid(11)
    assert file.read_text() == '11'
    assert users_module.SessionId().session_id == 11
