import jwt
from fastapi import HTTPException, Depends, status, Header
from sqlalchemy.orm import Session

from services.auth import JWT_SECRET_KEY, JWT_SECRET_ALGORITHM
from schemas.user import User as User_schema
from models import User


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
            "password": str(user.password),
            "role": int(user.category_id)
        },
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )

def generate_access_token(
    db: Session,
    user_login: User):
    
    user = (
        db.query(User).filter(
            User.username == user_login.username,
            User.password == user_login.password,
        ).first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    return _encode_jwt(user)

def get_current_user(access_token: str = Header(None)) -> tuple[str, int]:
    print("Checking user login")
    print(access_token)
    # Check if access_token is present and starts with "Bearer"
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not access_token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format. Expected 'Bearer <token>'.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        # Extract the actual token part
        token = access_token.split("Bearer ")[1]
        print("Token =", token)
        
        # Decode the JWT
        auth = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_SECRET_ALGORITHM])
        print(f"Decoded token: {auth}")
    
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get user information from the decoded token
    username = auth.get("username")
    role = auth.get("role")  # Make sure 'role' is an integer
    
    if not username or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing required user data.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return username, role

def allowed_roles(roles: list[int]):
    def role_checker(user_data: tuple[str, int] = Depends(get_current_user)):
        _, user_role = user_data 
        if user_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: Insufficient permissions"
            )
        return user_data
    return role_checker

