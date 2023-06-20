from index import app, conn, conn2
from minor import check_course_in_minor
from flask.testing import FlaskClient

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import pandas as pd


# Jean
def test_check_course_in_minor():
    course = "MIE439H1S"
    minor = "Biomedical Engineering Minor"
    result = check_course_in_minor(course)

    assert result == minor

# # Cansin
# def test_user_register_endpoint():
#     tester = app.test_client()
#     response = tester.get("/user/register")

#     assert response.status_code == 200

# def test_user_login_endpoint():
#     tester = app.test_client()
#     response = tester.get("/user/login")

#     assert response.status_code == 200

# def test_search_endpoint():
#     tester = app.test_client()
#     response = tester.get("/search")

#     assert response.status_code == 200

def test_course_details_endpoint():
    tester = app.test_client()
    response = tester.get("/course/details?code=ECE318H1")

    assert response.status_code == 200

#Peter

def test_post_and_get_recommendation():
    tester = app.test_client()
    expectedCourses = [{'course1': 'ECE344H1', 'course2': 'ECE444H1', 'description': 'testing'}, {'course1': 'ECE444H1', 'course2': 'ECE344H1', 'description': 'testing'}]
    expectedCourse1 = [expectedCourses[0]]
    expectedCourse2 = [expectedCourses[1]]

    postResponse = tester.post("/recommendations?course1=ECE444H1",  json=dict(course1="ECE344H1", course2='ECE444H1',description='testing'))
    assert postResponse.status_code == 200
    assert conn2.all() == expectedCourses

    getResponse = tester.get("/recommendations?course1=ECE344H1")
    assert getResponse.status_code == 200
    assert getResponse.json == expectedCourse1

    getResponse = tester.get("/recommendations?course1=ECE444H1")
    assert getResponse.status_code == 200
    assert getResponse.json == expectedCourse2

#Peter

def test_validation_api():
    tester = app.test_client()
    expectedCourse1 = {"course": "ECE344H1"}
    expectedCourse2 = {'course': ""}

    postResponse = tester.post("/test?courseOrig=ECE344",  json=dict(courseOrig="ECE444H1", courseCheck='ECE344'))
    assert postResponse.status_code == 200
    assert postResponse.json == expectedCourse1

    postResponse = tester.post("/test?courseOrig=ECE344",  json=dict(courseOrig="ECE444H1", courseCheck='abc'))
    assert postResponse.status_code == 404
    assert postResponse.json == expectedCourse2


def test_validation_api():
    tester = app.test_client()
    expectedCourse1 = {"course": "ECE344H1"}
    expectedCourse2 = {'course': ""}

    postResponse = tester.post("/test?courseOrig=ECE344",  json=dict(courseOrig="ECE444H1", courseCheck='ECE344'))
    assert postResponse.status_code == 200
    assert postResponse.json == expectedCourse1

    postResponse = tester.post("/test?courseOrig=ECE344",  json=dict(courseOrig="ECE444H1", courseCheck='abc'))
    assert postResponse.status_code == 404
    assert postResponse.json == expectedCourse2

def test_related_courses():
    tester = app.test_client()
    related = 'ECE419H1, ECE444H1, ECE568H1'
    getResponse = tester.get("/course/details?code=ECE344")

    assert getResponse.status_code == 200
    assert getResponse.json['course']['related'] == related

# def test_course_graph_endpoint():
#     tester = app.test_client()
#     response = tester.get("/course/graph?code=ECE318H1")

#     assert response.status_code == 200

# def test_user_wishlist_endpoint():
#     tester = app.test_client()
#     response = tester.get("/user/wishlist")

#     assert response.status_code == 200

# def test_user_wishlist_addCourse_endpoint():
#     tester = app.test_client()
#     response = tester.get("/user/wishlist/addCourse")

#     assert response.status_code == 200

# def test_user_wishlist_removeCourse_endpoint():
#     tester = app.test_client()
#     response = tester.get("/user/wishlist/removeCourse")

#     assert response.status_code == 200

# def test_user_wishlist_minorCheck_endpoint():
#     tester = app.test_client()
#     response = tester.get("/user/wishlist/minorCheck")

#     assert response.status_code == 200

# Prerak
def test_post_and_get_review():
    tester = app.test_client()

    expectedEntry = [{"course": "ECE444", "description": "good course", "rating": '5'}]

    postResponse = tester.post("/reviews?course=ECE444",  json=dict(description="good course", rating='5'))

    assert postResponse.status_code == 200
    assert conn.all() == expectedEntry

    getResponse = tester.get("/reviews?course=ECE444")

    assert getResponse.status_code == 200
    assert getResponse.json == expectedEntry

# Amy
def test_course_logistics_exists():
    tester = app.test_client()
    response = tester.get("/course/details?code=PSY220H5")

    assert b'professors' in response.data
    assert b'hours' in response.data
    assert b'term' in response.data

# Joel
def test_get_minorinfo():
    tester = app.test_client()

    expectedObj = {"minorInfo": "This course is part of the following minors: Advanced Manufacturing, Artificial Intelligence Engineering." }

    getResponse = tester.get("/minors?course=MIE566H1")
    print(getResponse)

    assert getResponse.status_code == 200
    assert getResponse.json == expectedObj



    

