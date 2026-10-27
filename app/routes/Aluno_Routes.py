from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session

from entidades.models import alunoPublico
from controllers import AlunoController
from dependencies.dependencies import database

aluno_router = APIRouter()


# ----------------------------------------------------------------------------
# Schema específico do POST: recebe a senha além dos dados públicos.
# Aqui sim é o lugar de expor a senha (só na entrada; nunca na saída).
# ----------------------------------------------------------------------------
class AlunoCreate(AlunoPublico):
    usuario_senha: str = Field(min_length=6, max_length=255)


# GET — listar
@aluno_router.get("/alunos", status_code=status.HTTP_200_OK)
def buscar_alunos(db: Session = Depends(database.get_db)):
    try:
        return AlunoController.buscar_alunos(db)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# GET por id
@aluno_router.get("/alunos/{aluno_id}", status_code=status.HTTP_200_OK)
def buscar_aluno(aluno_id: int, db: Session = Depends(database.get_db)):
    try:
        return AlunoController.buscar_aluno_por_id(db, aluno_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# POST — criar (recebe senha)
@aluno_router.post("/alunos", status_code=status.HTTP_201_CREATED)
def criar_Aluno(dados: AlunoCreate, db: Session = Depends(database.get_db)):
    try:
        # Separa o schema público dos dados sensíveis
        dados_publicos = AlunoPublico(**dados.model_dump(exclude={"aluno_senha"}))
        return AlunoController.cadastrar_aluno(db, dados_publicos, dados.aluno_senha)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# PUT — atualizar (não mexe em senha)
@aluno_router.put("/alunos/{aluno_id}")
def atualizar_aluno(
    aluno_id: int, dados: AlunoPublico, db: Session = Depends(database.get_db)
):
    try:
        return AlunoController.atualizar_aluno(db, aluno_id, dados)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# DELETE — remover
@aluno_router.delete("/aluno/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_aluno(aluno_id: int, db: Session = Depends(database.get_db)):
    try:
        AlunoController.deletar_aluno(db, aluno_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )