"""
Firebase ID token verification using the Firebase Auth REST API.
No external dependencies required — uses only Python's built-in urllib.
"""
import json
import urllib.request
import urllib.error

FIREBASE_API_KEY = "AIzaSyAom58-XFC4yvjYiaIiPYpoilRVgB5E29g"
FIREBASE_VERIFY_URL = (
    "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo"
    f"?key={FIREBASE_API_KEY}"
)


def verify_firebase_token(id_token):
    """
    Verify a Firebase ID token by calling the Firebase Auth REST API.
    Returns a dict with user info (email, displayName, localId, etc.).
    Raises an exception on failure.
    """
    payload = json.dumps({"idToken": id_token}).encode("utf-8")

    req = urllib.request.Request(
        FIREBASE_VERIFY_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise ValueError(f"Firebase token verification failed: {error_body}") from e
    except urllib.error.URLError as e:
        raise ValueError(f"Firebase connection error: {str(e)}") from e

    users = data.get("users", [])
    if not users:
        raise ValueError("No user found for the provided token")

    user_info = users[0]
    return {
        "uid": user_info.get("localId", ""),
        "email": user_info.get("email", ""),
        "name": user_info.get("displayName", ""),
        "email_verified": user_info.get("emailVerified", False),
    }
