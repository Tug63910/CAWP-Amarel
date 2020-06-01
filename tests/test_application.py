import pytest
from CAWPr.db import get_db

def test_index(client,auth):
	response=client.get('/')
	assert b"Log In" in response.data
	assert b"Register" in response.data

	auth.login()
	response=client.get('/')
	assert b'Log Out' in response.data
	assert b'test url' in response.data
	assert b'test\nstate' in response.data
	assert b'test\nlevel' in response.data
	assert b'test\noffice' in response.data
	assert b'test\nprofession' in response.data
	assert b'href="/1/update"' in response.data

@pytest.mark.parametrize('path', (
	'/create',
	'/1/update',
	'/1/delete',
))
def test_login_required(client, path):
	response=client.post(path)
	assert response.headers['Location']=='http://localhost/auth/login'

@pytest.mark.parametrize('path', (
	'/2/update',
	'/2/delete', 
))
def test_exists_required(client, auth, path):
	auth.login()
	assert client.post(path).status_code==404

def test_create(client, auth, app):
	auth.login()
	assert client.get('/create').status_code==200
	client.post('/create', data={'url':'http://candidate.com', 'state': 'NJ', 'level': '', 'office': 'senate', 'profession': ''})

	with app.app_context():
		db=get_db()
		count=db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
		assert count == 2

def test_update(client, auth, app):
	auth.login()
	assert client.get('/1/update').status_code==200
	client.post('/1/update', data={'url': 'http://updated.com', 'state': 'NJ', 'level': '', 'office': 'rep', 'profession': 'baker'})

	with app.app_context():
		db=get_db()
		post=db.execute('SELECT * FROM post WHERE id=1').fetchone()
		assert post['url']=='http://updated.com'

@pytest.mark.parametrize('path', (
	'/create',
	'/1/update',
))
def test_create_update_validate(client, auth, path):
	auth.login()
	response=client.post(path, data={'url':'', 'state': '', 'level': '', 'office': '', 'profession': ''})
	assert b'Url required' in response.data

def test_delete(client, auth, app):
	auth.login()
	response=client.post('/1/delete')
	assert response.headers['Location'] == 'http://localhost/'

	with app.app_context():
		db=get_db()
		post=db.execute('SELECT * FROM post WHERE id=1').fetchone()
		assert post is None

