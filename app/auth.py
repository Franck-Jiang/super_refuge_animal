import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from services.auth import JWT_SECRET_KEY, JWT_SECRET_ALGORITHM
from schemas.user import User


def verify_autorization_header(access_token: str):
    if not access_token or not access_token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No auth provided.")

    try:
        token = access_token.split("Bearer ")[1]
        print("Token =", token)
        auth = jwt.decode(token, JWT_SECRET_KEY, JWT_SECRET_ALGORITHM)
        print(f"{auth}")
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail=f"Invalid token.")

    return auth

def _encode_jwt(user: User) -> str:
    return jwt.encode(
        {
            "username": str(user.username),
            "password": str(user.password)
        },
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )

# def generate_access_token(
#     db: Session,
#     user_login: User,
# ):
#     user = (
#         db.query(models.User)
#         .filter(
#             models.User.username == user_login.username,
#             models.User.password == user_login.password,
#         )
#         .first()
#     )

#     if not user:
#         raise HTTPException(status_code=404, detail="Incorrect username or password")

#     return _encode_jwt(user)