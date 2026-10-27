from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models import Aluno, AlunoPublico
from core.security import cria_hash_senha

# ----------------------------------------------------------------------------
# LISTAR ALUNOS
# ----------------------------------------------------------------------------
def buscar_alunos(db: Session) -> list[Aluno]:
    try:
        return db.exec(select(Aluno)).all()
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# BUSCAR ALUNO PELO ID
# ----------------------------------------------------------------------------
def buscar_aluno_por_id(db: Session, aluno_id: int) -> Aluno:
    try:
        aluno = db.get(Aluno, aluno_id)
        if not aluno:
            raise KeyError(f"Aluno de ID {aluno_id} não encontrado.")
        return aluno
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# CADASTRAR ALUNO
# ----------------------------------------------------------------------------
def cadastrar_aluno(db: Session, dados_entrada: AlunoPublico, senha: str) -> Aluno:
    try:
        dados_dict = dados_entrada.model_dump(exclude={"aluno_id"})
        
        # Salvando com o campo correto 'aluno_senha' mapeado na Model
        novo_aluno = Aluno(**dados_dict, aluno_senha=cria_hash_senha(senha))
        
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        return novo_aluno
    except IntegrityError as e:
        db.rollback()
        raise ValueError("E-mail ou Matrícula já cadastrados.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# ATUALIZAR ALUNO
# ----------------------------------------------------------------------------
def atualizar_aluno(
    db: Session, aluno_id: int, dados_atualizados: AlunoPublico
) -> Aluno:
    try:
        aluno = db.get(Aluno, aluno_id)
        if not aluno:
            raise KeyError(f"Aluno de ID {aluno_id} não encontrado.")

        for key, value in dados_atualizados.model_dump(exclude_unset=True, exclude={"aluno_id"}).items():
            setattr(aluno, key, value)

        db.add(aluno)
        db.commit()
        db.refresh(aluno)
        return aluno
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade. Verifique se o e-mail ou matrícula já existe.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# DELETAR ALUNO
# ----------------------------------------------------------------------------
def deletar_aluno(db: Session, aluno_id: int) -> None:
    try:
        aluno = db.get(Aluno, aluno_id)
        if not aluno:
            raise KeyError(f"Aluno de ID {aluno_id} não encontrado.")

        db.delete(aluno)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Não é possível excluir: existem empréstimos vinculados a este aluno."
        ) from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e
