from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from uuid import UUID

from probe.repositories.user import UserRepository
from probe.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Generates a secure, salted bcrypt hash of the plain password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Securely verifies passwords using a constant-time algorithm to prevent timing attacks."""
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: UUID):
   
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def list_users(db: Session):
    return UserRepository.get_all(db)

def create_user(db: Session, data: UserCreate):
    clean_email = data.email.strip().lower() 
    
    if not clean_email or not data.password_hash.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Required authentication credentials cannot be empty."
        )
        
    if len(data.password_hash) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Security policy violation: Password must be at least 8 characters long."
        )

    clean_user_type = data.user_type.value.strip() if hasattr(data.user_type, 'value') else str(data.user_type).strip()
    if clean_user_type not in ["RECYCLER", "UPS COMPANY"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid system operational role requested."
        )
        
    existing_user = UserRepository.get_by_email(db, clean_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="A user profile with this email address is already registered."
        )
    
    user_dict = data.model_dump()
    user_dict["email"] = clean_email
    user_dict["user_type"] = clean_user_type
    user_dict["password_hash"] = get_password_hash(data.password_hash) 
    
    return UserRepository.create(db, user_dict)

def authenticate_user(db: Session, email: str, plain_password: str):
    if not email or not email.strip() or not plain_password or not plain_password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email and password strings cannot be empty."
        )

    clean_email = email.strip().lower()
    user = UserRepository.get_by_email(db, clean_email)
 
    generic_auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid email or password configuration."
    )
    
    if not user:
        raise generic_auth_error

    if not verify_password(plain_password, user.password_hash):
        raise generic_auth_error

    return user

def update_user(db: Session, user_id: UUID, data: UserUpdate):
    user = get_user(db, user_id)
    updated_fields = data.model_dump(exclude_unset=True)
    
    if "password_hash" in updated_fields and updated_fields["password_hash"]:
        if len(updated_fields["password_hash"]) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")
        updated_fields["password_hash"] = get_password_hash(updated_fields["password_hash"])
        
    if "email" in updated_fields and updated_fields["email"]:
        updated_fields["email"] = updated_fields["email"].strip().lower()
        
    if "user_type" in updated_fields and updated_fields["user_type"]:
        ut = updated_fields["user_type"]
        updated_fields["user_type"] = ut.value.strip() if hasattr(ut, 'value') else str(ut).strip()
        
    return UserRepository.update(db, user, updated_fields)

def delete_user(db: Session, user_id: UUID):
    user = get_user(db, user_id)
    return UserRepository.delete(db, user)
