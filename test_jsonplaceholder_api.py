"""
API test suite for JSONPlaceholder (https://jsonplaceholder.typicode.com)

JSONPlaceholder is a free, no-auth REST API for testing/prototyping,
served from the public-apis list (typicode/jsonplaceholder).

We test the /posts resource (and its relation to /comments) covering:
- a successful single-resource GET
- a not-found GET (negative case)
- a list GET with structural validation across multiple items (parametrized)
- a resource creation (POST)
- a relational GET, validated for referential integrity (parametrized)
"""

import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


class TestGetSinglePost:
    """Validates fetching a single, known-to-exist post."""

    def test_get_existing_post_returns_200_with_expected_schema(self):
        response = requests.get(f"{BASE_URL}/posts/1")

        assert response.status_code == 200

        body = response.json()
        # Schema validation: correct keys present, correct types
        assert set(body.keys()) == {"userId", "id", "title", "body"}
        assert isinstance(body["userId"], int)
        assert isinstance(body["id"], int)
        assert isinstance(body["title"], str)
        assert isinstance(body["body"], str)
        assert body["id"] == 1


class TestGetNonExistentPost:
    """Negative test case: requesting a resource that doesn't exist."""

    def test_get_nonexistent_post_returns_404(self):
        # Post IDs only go up to 100 on this API; 99999 is guaranteed absent.
        response = requests.get(f"{BASE_URL}/posts/99999")

        assert response.status_code == 404


class TestGetAllPosts:
    """Validates the full list endpoint and structural integrity of items within it."""

    def test_get_all_posts_returns_200_with_100_items(self):
        response = requests.get(f"{BASE_URL}/posts")

        assert response.status_code == 200

        body = response.json()
        assert isinstance(body, list)
        assert len(body) == 100

    @pytest.mark.parametrize("index", [0, 1, 50, 99])
    def test_each_post_in_list_has_expected_schema(self, index):
        """
        Parametrized across a spread of indices (first, second, middle, last)
        rather than checking every one of the 100 items individually —
        this keeps the test fast while still giving confidence that the
        schema is consistent across the full range of the list, not just
        the first entry.
        """
        response = requests.get(f"{BASE_URL}/posts")
        body = response.json()

        post = body[index]
        assert set(post.keys()) == {"userId", "id", "title", "body"}
        assert isinstance(post["title"], str) and len(post["title"]) > 0
        assert isinstance(post["body"], str) and len(post["body"]) > 0


class TestCreatePost:
    """Validates creating a new resource via POST."""

    def test_create_post_returns_201_and_echoes_submitted_data(self):
        payload = {
            "title": "AQA take-home assignment",
            "body": "Validating POST behavior on JSONPlaceholder.",
            "userId": 7,
        }

        response = requests.post(f"{BASE_URL}/posts", json=payload)

        assert response.status_code == 201

        body = response.json()
        # JSONPlaceholder echoes back submitted fields and assigns a new id
        assert body["title"] == payload["title"]
        assert body["body"] == payload["body"]
        assert body["userId"] == payload["userId"]
        assert "id" in body
        assert isinstance(body["id"], int)


class TestPostCommentsRelation:
    """
    Validates the relational endpoint /posts/{id}/comments, checking
    referential integrity: every comment returned must actually belong
    to the requested post.
    """

    @pytest.mark.parametrize("post_id", [1, 5, 10])
    def test_comments_for_post_all_reference_correct_post_id(self, post_id):
        response = requests.get(f"{BASE_URL}/posts/{post_id}/comments")

        assert response.status_code == 200

        comments = response.json()
        assert isinstance(comments, list)
        assert len(comments) > 0

        # Referential integrity: every comment must belong to the requested post
        for comment in comments:
            assert comment["postId"] == post_id
            assert "email" in comment
            assert "body" in comment