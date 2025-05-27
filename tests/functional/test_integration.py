import pytest
import json
from iebank_api import app, db
from iebank_api.models import Account

def test_complete_account_lifecycle_with_country(testing_client):
    """
    GIVEN a Flask application
    WHEN a complete account lifecycle is performed (create, read, update, delete) with country field
    THEN check all operations work correctly
    """
    # 1. Create account with country
    create_response = testing_client.post('/accounts', json={
        'name': 'Integration Test User',
        'currency': '€',
        'country': 'Germany'
    })
    assert create_response.status_code == 200
    created_account = json.loads(create_response.data)
    account_id = created_account['id']
    
    # Verify account creation
    assert created_account['name'] == 'Integration Test User'
    assert created_account['currency'] == '€'
    assert created_account['country'] == 'Germany'
    assert created_account['balance'] == 0.0
    assert created_account['status'] == 'Active'
    assert len(created_account['account_number']) == 20
    
    # 2. Read account by ID
    get_response = testing_client.get(f'/accounts/{account_id}')
    assert get_response.status_code == 200
    retrieved_account = json.loads(get_response.data)
    assert retrieved_account['id'] == account_id
    assert retrieved_account['country'] == 'Germany'
    
    # 3. Read all accounts
    get_all_response = testing_client.get('/accounts')
    assert get_all_response.status_code == 200
    all_accounts = json.loads(get_all_response.data)
    assert len(all_accounts['accounts']) >= 1
    
    # Find our account in the list
    our_account = next((acc for acc in all_accounts['accounts'] if acc['id'] == account_id), None)
    assert our_account is not None
    assert our_account['country'] == 'Germany'
    
    # 4. Update account
    update_response = testing_client.put(f'/accounts/{account_id}', json={
        'name': 'Updated Integration Test User'
    })
    assert update_response.status_code == 200
    updated_account = json.loads(update_response.data)
    assert updated_account['name'] == 'Updated Integration Test User'
    assert updated_account['country'] == 'Germany'  # Country should remain unchanged
    
    # 5. Delete account
    delete_response = testing_client.delete(f'/accounts/{account_id}')
    assert delete_response.status_code == 200

def test_multiple_accounts_different_countries(testing_client):
    """
    GIVEN a Flask application
    WHEN multiple accounts are created with different countries
    THEN check all accounts are stored correctly with their respective countries
    """
    accounts_data = [
        {'name': 'Spanish User', 'currency': '€', 'country': 'Spain'},
        {'name': 'French User', 'currency': '€', 'country': 'France'},
        {'name': 'US User', 'currency': '$', 'country': 'United States'},
        {'name': 'UK User', 'currency': '£', 'country': 'United Kingdom'}
    ]
    
    created_accounts = []
    
    # Create all accounts
    for account_data in accounts_data:
        response = testing_client.post('/accounts', json=account_data)
        assert response.status_code == 200
        created_account = json.loads(response.data)
        created_accounts.append(created_account)
        
        # Verify each account has correct country
        assert created_account['country'] == account_data['country']
        assert created_account['name'] == account_data['name']
        assert created_account['currency'] == account_data['currency']
    
    # Verify all accounts exist
    get_all_response = testing_client.get('/accounts')
    assert get_all_response.status_code == 200
    all_accounts = json.loads(get_all_response.data)
    
    # Check that we have at least the accounts we created
    assert len(all_accounts['accounts']) >= len(accounts_data)
    
    # Verify each country is represented
    countries_in_db = [acc['country'] for acc in all_accounts['accounts']]
    for account_data in accounts_data:
        assert account_data['country'] in countries_in_db

def test_account_creation_without_country_defaults_to_spain(testing_client):
    """
    GIVEN a Flask application
    WHEN an account is created without specifying country
    THEN check the country defaults to Spain
    """
    response = testing_client.post('/accounts', json={
        'name': 'Default Country User',
        'currency': '€'
    })
    assert response.status_code == 200
    account = json.loads(response.data)
    assert account['country'] == 'Spain'

def test_country_field_in_all_endpoints(testing_client):
    """
    GIVEN a Flask application
    WHEN account operations are performed
    THEN check country field is present in all API responses
    """
    # Create account
    create_response = testing_client.post('/accounts', json={
        'name': 'Country Test User',
        'currency': '$',
        'country': 'Canada'
    })
    assert create_response.status_code == 200
    created_account = json.loads(create_response.data)
    account_id = created_account['id']
    
    # Check country in create response
    assert 'country' in created_account
    assert created_account['country'] == 'Canada'
    
    # Check country in get by ID response
    get_response = testing_client.get(f'/accounts/{account_id}')
    assert get_response.status_code == 200
    get_account = json.loads(get_response.data)
    assert 'country' in get_account
    assert get_account['country'] == 'Canada'
    
    # Check country in get all response
    get_all_response = testing_client.get('/accounts')
    assert get_all_response.status_code == 200
    all_accounts = json.loads(get_all_response.data)
    our_account = next((acc for acc in all_accounts['accounts'] if acc['id'] == account_id), None)
    assert our_account is not None
    assert 'country' in our_account
    assert our_account['country'] == 'Canada'
    
    # Check country in update response
    update_response = testing_client.put(f'/accounts/{account_id}', json={
        'name': 'Updated Country Test User'
    })
    assert update_response.status_code == 200
    updated_account = json.loads(update_response.data)
    assert 'country' in updated_account
    assert updated_account['country'] == 'Canada'
    
    # Check country in delete response
    delete_response = testing_client.delete(f'/accounts/{account_id}')
    assert delete_response.status_code == 200
    deleted_account = json.loads(delete_response.data)
    assert 'country' in deleted_account
    assert deleted_account['country'] == 'Canada'

def test_skull_endpoint_shows_database_info(testing_client):
    """
    GIVEN a Flask application
    WHEN the skull endpoint is accessed
    THEN check it returns database information
    """
    response = testing_client.get('/skull')
    assert response.status_code == 200
    content = response.data.decode()
    assert 'BACKEND SKULL' in content
    assert 'Database URL' in content

def test_error_handling_for_invalid_requests(testing_client):
    """
    GIVEN a Flask application
    WHEN invalid requests are made
    THEN check proper error responses are returned
    """
    # Test missing name
    response = testing_client.post('/accounts', json={'currency': '€'})
    assert response.status_code == 400
    error_data = json.loads(response.data)
    assert 'error' in error_data
    
    # Test missing currency
    response = testing_client.post('/accounts', json={'name': 'Test User'})
    assert response.status_code == 400
    error_data = json.loads(response.data)
    assert 'error' in error_data
    
    # Test invalid JSON (Flask returns 500 for malformed JSON)
    response = testing_client.post('/accounts', data='invalid json')
    assert response.status_code == 500 