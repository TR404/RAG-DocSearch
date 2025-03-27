from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from ..models.user import User
from ..schemas.user import UserCreate
from ..settings.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..services.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", status_code=201)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Registers a new user if they are not already in the database."""
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return {"message": "User registered successfully"}


@router.post("/token", response_model=dict, include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(select(User).filter(User.email == form_data.username))
        db_user = result.scalars().first()

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}