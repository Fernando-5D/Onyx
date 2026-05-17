from pydantic import BaseModel, EmailStr, Field

class UsuarioBase_Schema(BaseModel):
    email: EmailStr = Field(max_length=255)

class UsuarioSesion_Schema(UsuarioBase_Schema):
    passw: str = Field(min_length=8, max_length=255)

class UsuarioRegistro_Schema(UsuarioSesion_Schema):
    nombre: str = Field(min_length=3, max_length=25)