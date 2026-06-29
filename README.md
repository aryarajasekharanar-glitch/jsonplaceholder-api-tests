\# JSONPlaceholder API Tests



Automated API test suite for \[JSONPlaceholder](https://jsonplaceholder.typicode.com), a free, no-auth REST API for testing and prototyping (chosen from the \[public-apis](https://github.com/public-apis/public-apis) list).



\## Tech Stack



\- \*\*Python 3\*\*

\- \*\*Pytest\*\* (test runner, with `parametrize` used to cover multiple inputs per test case)

\- \*\*Requests\*\* (HTTP client)



\## Setup \& Installation



```bash

git clone <this-repo-url>

cd reqres-api-tests

python -m venv venv

venv\\Scripts\\activate        # Windows

\# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

```



\## Running the Tests



```bash

pytest -v test\_jsonplaceholder\_api.py

```



\## Test Cases



| # | Test Case | Endpoint | Method | What It Validates |

|---|-----------|----------|--------|---------------------|

| 1 | Get an existing post | `/posts/1` | GET | Status 200; response schema matches expected keys/types (`userId`, `id`, `title`, `body`) |

| 2 | Get a non-existent post | `/posts/99999` | GET | Status 404 (negative case — confirms the API correctly reports missing resources) |

| 3 | Get all posts | `/posts` | GET | Status 200; response is a list containing exactly 100 items |

| 4 | Schema check across the post list (parametrized: indices 0, 1, 50, 99) | `/posts` | GET | Each sampled post has the correct schema and non-empty `title`/`body` fields, confirming structural consistency isn't just true for the first item |

| 5 | Create a new post | `/posts` | POST | Status 201; response echoes back the submitted `title`, `body`, and `userId`, and includes a newly assigned `id` |

| 6 | Comments belong to the correct post (parametrized: post IDs 1, 5, 10) | `/posts/{id}/comments` | GET | Status 200; every returned comment's `postId` matches the requested post ID (referential integrity), and each comment has `email`/`body` fields |



\## Validation Approach \& Rationale



\- \*\*Status code checks\*\* are the first assertion in every test — confirming the API behaves as expected at the HTTP level before inspecting the payload.

\- \*\*Schema validation\*\* (checking exact key sets and field types) catches unexpected structural changes in the API's response shape, which is often a more meaningful regression signal than just checking individual values.

\- \*\*Negative testing\*\* (test case #2) is included deliberately — verifying correct 404 behavior is just as important as verifying success paths, and is a common gap in API test suites that only test the "happy path."

\- \*\*Referential integrity\*\* (test case #6) validates that relational data returned by the API is actually consistent (every comment really does belong to the post it claims to), rather than just checking the response is non-empty.

\- \*\*`pytest.mark.parametrize`\*\* is used for test cases #4 and #6 to validate behavior across multiple inputs (different post indices, different post IDs) without duplicating test code, keeping the suite concise while maintaining meaningful coverage breadth, per the assignment's recommendation.

