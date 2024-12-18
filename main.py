from datetime import datetime, timedelta
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

JWT_SECRET = "123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory user database
users_db = {
    "user1": dict(username="user1", password="password1", spending=5000.0),
    "user2": dict(username="user2", password="password2", spending=15000.0),
}

# Bonus levels sorted by min_spending
bonus_levels = [
    dict(level="Silver", min_spending=0, cashback=0.01),
    dict(level="Gold", min_spending=10000, cashback=0.02),
    dict(level="Platinum", min_spending=20000, cashback=0.03),
]

# Pydantic models
class User(BaseModel):
    username: str
    password: str
    spending: float

class BonusLevel(BaseModel):
    level: str
    min_spending: float
    cashback: float

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users_db.get(form_data.username)
    if not user_dict or user_dict["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_dict["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user_dict = users_db.get(username)
    if user_dict is None:
        raise credentials_exception
    return User(**user_dict)

@app.get("/bonus", response_model=dict)
async def read_bonus_data(current_user: User = Depends(get_current_user)):
    user_spending = current_user.spending
    # Determine current and next bonus levels
    sorted_levels = sorted(bonus_levels, key=lambda x: x["min_spending"])
    current_level = None
    next_level = None
    for level in sorted_levels:
        if user_spending >= level["min_spending"]:
            current_level = level
        else:
            if current_level:
                next_level = level
            break
    if not next_level:
        next_level = "No higher level"
    return {
        "current_level": current_level,
        "next_level": next_level
    }