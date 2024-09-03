import json
import pytest
import csv
import subprocess
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from app import app  # Flask 애플리케이션을 임포트

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"DBTI" in response.data
    assert b"MBTI" in response.data

def test_submit_dbti(client):
    """Test the /submit_dbti route."""
    response = client.post('/submit_dbti', json={'dbti': 'DBTI_TYPE'})
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'DBTI 저장 완료'

def test_mbti_api_with_valid_mbti(client):
    """Test the /mbti_api route with a valid MBTI result."""
    response = client.post('/mbti_api', json={'userRequest': {'utterance': 'INFJ'}})
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert '이용자님은 MBTI가 INFJ로' in response_json['template']['outputs'][0]['simpleText']['text']

def test_mbti_api_with_invalid_mbti(client):
    """Test the /mbti_api route with an invalid MBTI result."""
    response = client.post('/mbti_api', json={'userRequest': {'utterance': 'INVALID'}})
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert '올바른 MBTI 유형을 입력해주세요.' in response_json['template']['outputs'][0]['simpleText']['text']

def test_speech_call(client):
    """Test the /api/speech route."""
    response = client.post('/api/speech', json={'userRequest': {'utterance': 'test'}})
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert '음성인식으로 DBTI와 MBTI를 검색하기' in response_json['template']['outputs'][0]['basicCard']['title']
