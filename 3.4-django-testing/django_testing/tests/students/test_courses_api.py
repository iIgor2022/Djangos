import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def route():
    return '/api/v1/courses/'


@pytest.fixture
def student_factory():
    def student(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return student


@pytest.fixture
def course_factory():
    def course(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return course


@pytest.mark.django_db
def test_get_course(client, route, student_factory, course_factory):
    """Get 1 course test"""
    # Arrange
    course = course_factory(_quantity=1)

    # Act
    response = client.get(route)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)
    assert data[0]['name'] == course[0].name


@pytest.mark.django_db
def test_get_courses(client, route, student_factory, course_factory):
    """Get list of courses test"""
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(route)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for index, course in enumerate(data):
        assert course['name'] == courses[index].name


@pytest.mark.django_db
def test_course_filter_by_id(client, route, student_factory, course_factory):
    """Filtering corses by id"""
    courses = course_factory(_quantity=2)

    response = client.get(f'{route}?id={courses[0].pk}')

    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[0].pk


@pytest.mark.django_db
def test_course_filter_by_name(client, route, student_factory, course_factory):
    """Filtering corses by name"""
    courses = course_factory(_quantity=2)

    response = client.get(f'{route}?name={courses[0].name}')

    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_create_course(client, route, student_factory):
    """Create course"""
    count_courses = Course.objects.count()

    response = client.post(route, data={'name': 'test_course'})

    assert response.status_code == 201
    assert Course.objects.count() == count_courses + 1


@pytest.mark.django_db
def test_update_course(client, route, student_factory, course_factory):
    """Update course"""
    course = course_factory(_quantity=1)

    response = client.patch(f'{route}{course[0].pk}/', data={'name': 'test_course'})

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'test_course'


@pytest.mark.django_db
def test_delete_course(client, route, student_factory, course_factory):
    """Delete course"""
    course = course_factory(_quantity=1)
    course_count = Course.objects.count()

    response = client.delete(f'{route}{course[0].pk}/')

    assert response.status_code == 204
    assert Course.objects.count() == course_count - 1


@pytest.mark.parametrize("test_input, expected", [(2, 2), (20, 20), (10, 20)])
def test_max_students_per_course(settings, test_input, expected):
    """Max students per course"""
    settings.MAX_STUDENTS_PER_COURSE = test_input

    assert settings.MAX_STUDENTS_PER_COURSE == expected
