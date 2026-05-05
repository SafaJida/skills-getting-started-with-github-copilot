import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    """Test that GET / redirects to /static/index.html"""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"

def test_get_activities():
    """Test GET /activities returns all activities"""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Verify structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success():
    """Test successful signup for an activity"""
    # Arrange
    email = "test@example.com"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity}" in data["message"]

def test_signup_activity_not_found():
    """Test signup for non-existent activity"""
    # Arrange
    email = "test@example.com"
    activity = "NonExistent"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_signup_already_signed_up():
    """Test signup when already signed up"""
    # Arrange
    email = "duplicate@example.com"
    activity = "Programming Class"
    
    # Act - First signup (should succeed)
    client.post(f"/activities/{activity}/signup?email={email}")
    # Second signup (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]

def test_remove_participant_success():
    """Test successful removal of a participant"""
    # Arrange
    email = "remove@example.com"
    activity = "Gym Class"
    
    # Act - First add a participant
    client.post(f"/activities/{activity}/signup?email={email}")
    # Then remove
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Removed {email} from {activity}" in data["message"]

def test_remove_participant_activity_not_found():
    """Test removal from non-existent activity"""
    # Arrange
    email = "test@example.com"
    activity = "NonExistent"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_remove_participant_not_found():
    """Test removal of non-existent participant"""
    # Arrange
    email = "nonexistent@example.com"
    activity = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]