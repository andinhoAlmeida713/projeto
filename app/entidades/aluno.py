from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import Field
from sqlmodel import Session

from entidades.models import AlunoPublico
from controllers import AlunoController
from dependencies.dependencies import database

aluno_router = APIRouter()


# ----------------------------------------------------------------------------
# Schema específico do POST: recebe a senha além dos dados públicos.
# ----------------------------------------------------------------------------
class AlunoCreate(AlunoPublico):
    aluno_senha: str = Field(min_length=6, max_length=255)


# GET — listar todos os alunos
@aluno_router.get("/alunos", status_code=status.HTTP_200_OK)
def buscar_alunos(db: Session = Depends(database.get_db)):
    try:
        return AlunoController.buscar_alunos(db)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# GET — buscar por id
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


# POST — criar aluno (recebe senha)
@aluno_router.post("/alunos", status_code=status.HTTP_201_CREATED)
def criar_Aluno(dados: AlunoCreate, db: Session = Depends(database.get_db)):
    try:
        # Remove a senha antes de repassar os dados de perfil público ao Controller
        dados_publicos = AlunoPublico(**dados.model_dump(exclude={"aluno_senha"}))
        return AlunoController.cadastrar_aluno(db, dados_publicos, dados.aluno_senha)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# PUT — atualizar (não altera a senha)
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


# DELETE — remover aluno
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
