from iebank_api import app
import pytest
import json

def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'accounts' in data
    assert isinstance(data['accounts'], list)

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid and account is created correctly
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'John Doe'
    assert data['currency'] == '€'
    assert data['country'] == 'Spain'  # Default country
    assert data['balance'] == 0.0
    assert data['status'] == 'Active'
    assert 'account_number' in data
    assert 'id' in data
    assert 'created_at' in data

def test_create_account_with_country(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST) with country specified
    THEN check the response is valid and country is set correctly
    """
    response = testing_client.post('/accounts', json={
        'name': 'Jane Smith', 
        'currency': '$', 
        'country': 'United States'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Jane Smith'
    assert data['currency'] == '$'
    assert data['country'] == 'United States'
    assert data['balance'] == 0.0
    assert data['status'] == 'Active'

def test_create_account_missing_name(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST) without name
    THEN check the response returns an error
    """
    response = testing_client.post('/accounts', json={'currency': '€'})
    assert response.status_code == 400

def test_create_account_missing_currency(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST) without currency
    THEN check the response returns an error
    """
    response = testing_client.post('/accounts', json={'name': 'Test User'})
    assert response.status_code == 400

def test_get_account_by_id(testing_client):
    """
    GIVEN a Flask application
    WHEN an account is created and then retrieved by ID
    THEN check the response is valid
    """
    # Create account
    create_response = testing_client.post('/accounts', json={
        'name': 'Test User', 
        'currency': '€',
        'country': 'France'
    })
    assert create_response.status_code == 200
    created_account = json.loads(create_response.data)
    account_id = created_account['id']
    
    # Get account by ID
    get_response = testing_client.get(f'/accounts/{account_id}')
    assert get_response.status_code == 200
    retrieved_account = json.loads(get_response.data)
    assert retrieved_account['id'] == account_id
    assert retrieved_account['name'] == 'Test User'
    assert retrieved_account['country'] == 'France'

def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN an account is created and then updated
    THEN check the response is valid and account is updated
    """
    # Create account
    create_response = testing_client.post('/accounts', json={
        'name': 'Original Name', 
        'currency': '€'
    })
    assert create_response.status_code == 200
    created_account = json.loads(create_response.data)
    account_id = created_account['id']
    
    # Update account
    update_response = testing_client.put(f'/accounts/{account_id}', json={
        'name': 'Updated Name'
    })
    assert update_response.status_code == 200
    updated_account = json.loads(update_response.data)
    assert updated_account['name'] == 'Updated Name'
    assert updated_account['id'] == account_id

def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN an account is created and then deleted
    THEN check the response is valid
    """
    # Create account
    create_response = testing_client.post('/accounts', json={
        'name': 'To Delete', 
        'currency': '€'
    })
    assert create_response.status_code == 200
    created_account = json.loads(create_response.data)
    account_id = created_account['id']
    
    # Delete account
    delete_response = testing_client.delete(f'/accounts/{account_id}')
    assert delete_response.status_code == 200
    
    # Verify account is deleted (should return 404)
    get_response = testing_client.get(f'/accounts/{account_id}')
    assert get_response.status_code == 404

def test_skull_endpoint(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/skull' page is requested (GET)
    THEN check the response is valid and contains backend info
    """
    response = testing_client.get('/skull')
    assert response.status_code == 200
    assert 'BACKEND SKULL' in response.data.decode()
    assert 'Database URL' in response.data.decode()

def test_hello_world_endpoint(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == 'Hello, World!'


