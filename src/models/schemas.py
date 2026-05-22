from pydantic import BaseModel, EmailStr, Field

class UsuarioBase_Schema(BaseModel):
    email: EmailStr = Field(max_length=255)

class UsuarioPassw_Schema(BaseModel):
    passw: str = Field(min_length=8, max_length=255)

class UsuarioSesion_Schema(UsuarioBase_Schema, UsuarioPassw_Schema):
    pass
    
class UsuarioRegistro_Schema(UsuarioSesion_Schema):
    nombre: str = Field(min_length=3, max_length=25)

class UsuarioRecuperarPassw_Schema(UsuarioPassw_Schema):
    codigo: int = Field(ge=100000, le=999999)