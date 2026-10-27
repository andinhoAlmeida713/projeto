from typing import Optional
from sqlmodel import Field, SQLModel

# ----------------------------------------------------------------------------
# 1. Base Model: Campos compartilhados (Padrão para rotas e banco)
# ----------------------------------------------------------------------------
class AlunoBase(SQLModel):
    aluno_nome: str = Field(max_length=100, nullable=False)
    aluno_email: str = Field(max_length=100, unique=True, nullable=False)
    aluno_matricula: str = Field(max_length=20, unique=True, nullable=False)


# ----------------------------------------------------------------------------
# 2. Table Model: Representa a tabela "aluno" exatamente no MySQL
# ----------------------------------------------------------------------------
class Aluno(AlunoBase, table=True):
    __tablename__: str = "aluno"

    aluno_id: Optional[int] = Field(default=None, primary_key=True)
    aluno_senha: str = Field(max_length=255, nullable=False)


# ----------------------------------------------------------------------------
# 3. Public Model: O que é retornado nas listagens/consultas (Sem a senha)
# ----------------------------------------------------------------------------
class AlunoPublico(AlunoBase):
    aluno_id: int
