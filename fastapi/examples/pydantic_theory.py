from decimal import Decimal
import re
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, HttpUrl, RootModel, ValidationError, field_validator


class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    is_active: bool = True
    created_at: datetime = None
    tags: List[str] = []

#кастомные валидаторы
class UserWithValidation(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    
    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v
    
    @field_validator('age')
    def validate_age(cls, v):
        if v is not None and (v < 0 or v > 150):
            raise ValueError('Age must be between 0 and 150')
        return v

#наследование моделей
class BaseUser(BaseModel):
    name: str
    email: str

class AdminUser(BaseUser):
    role: str = "admin"
    permissions: List[str] = ["read", "write", "delete"]
    is_super_admin: bool = False

class RegularUser(BaseUser):
    role: str = "user"
    subscription_tier: str = "basic"


#вложенные модели
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class UserWithAddress(BaseModel):
    id: int
    name: str
    email: str
    address: Address
    shipping_addresses: List[Address] = []
    
    
#Конфигурация моделей
class StrictUser(BaseModel):
    model_config = {
        'str_strip_whitespace': True,
        'validate_assignment': True,
        'frozen': True,  # делает объекты неизменяемыми
        'extra': 'forbid'  # запрещает дополнительные поля
    }
    
    id: int
    name: str
    email: str


user_data = {
    "id": 1,
    "name": "John Doe",
    "email": "johne@xample.com",
    "age": 25,
    "is_active": True,
    "created_at": "2023-01-15T10:30:00",
    "tags": ["python", "developer"]
}

try:
    user = User(**user_data)
    print(user)
except ValidationError:
    print("Ошибка валидации")



# Сериализация и десериализация
user_dict = user.model_dump()
print(type(user_dict).__name__)


user_json = user.model_dump_json()
print(type(user_json).__name__)


user_dict_exclude = user.model_dump(exclude={'email'})
print(user_dict_exclude)

#Работа с датами и специальными типами
# class AdvancedUser(BaseModel):
#     user_id: UUID = uuid4()
#     email: EmailStr
#     website: Optional[HttpUrl] = None
#     salary: Decimal
#     metadata: Dict[str, Any] = {}  


# advanced_user_data = {
#     "email": "john@example.com",
#     "website": "https://johndoe.info",
#     "salary": 2000.50
# }

# try:
#     advanced_user = AdvancedUser(**advanced_user_data)
#     print("Успешно создан:", advanced_user.model_dump())
# except ValidationError as e:
#     print("Ошибки валидации:")
#     for error in e.errors():
#         print(f"- {error['loc']}: {error['msg']}")



#Валидация корневых типов
class IntList(RootModel):
    root: List[int]

# Позволяет валидировать списки напрямую
int_list = IntList([1, 2, 3])


#Generic модели
T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    success: bool
    data: T
    message: str = ""

# Использование
user_response = Response[User](success=True, data=user, message="бебра")
print(user_response)