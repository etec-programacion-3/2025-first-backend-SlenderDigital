from fastapi import APIRouter, HTTPException, Depends, status
from tortoise.exceptions import IntegrityError, DoesNotExist
from app.database.db_models import User
from app.schemas import UserCreate, UserOut
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from datetime import datetime, timedelta
from pydantic import EmailStr

SECRET_KEY = "supersecretkey"  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await User.get_or_none(id=user_id)
    if user is None or not user.active:
        raise credentials_exception
    return user

def admin_required(user=Depends(get_current_user)):
    if user.rol != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

# Endpoints
@router.post("/auth/registro", response_model=UserOut)
async def register(user_in: UserCreate):
    hashed_password = get_password_hash(user_in.password)
    try:
        user = await User.create(
            name=user_in.name,
            last_name=user_in.last_name,
            email=user_in.email,
            password=hashed_password,
            rol=user_in.rol,
            active=user_in.active
        )
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.active:
        raise HTTPException(status_code=403, detail="Inactive user")
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/usuarios", response_model=List[UserOut])
async def list_users(current_user=Depends(admin_required)):
    return await User.all()

@router.get("/usuarios/{user_id}", response_model=UserOut)
async def get_user_profile(user_id: int, current_user=Depends(get_current_user)):
    if current_user.rol != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/usuarios/{user_id}", response_model=UserOut)
async def update_user_profile(user_id: int, user_in: UserCreate, current_user=Depends(get_current_user)):
    if current_user.rol != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_in.name
    user.last_name = user_in.last_name
    user.email = user_in.email
    if user_in.password:
        user.password = get_password_hash(user_in.password)
    user.rol = user_in.rol if current_user.rol == "admin" else user.rol
    user.active = user_in.active if current_user.rol == "admin" else user.active
    await user.save()
    return user
