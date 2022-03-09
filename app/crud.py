from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas


# Refugees: READ
def get_refugees(db: Session, skip: int = 0, limit: int = 100):
    #return db.get(models.Refugee, refugee)
    return db.query(models.Refugee).offset(skip).limit(limit).all()

def get_refugees_by_id(db: Session, id: int = 0):
    return db.query(models.Refugee).filter(models.Refugee.id == id).all()

def get_refugees_by_family_name(db: Session, family_name: str):
    return db.query(models.Refugee).filter(models.Refugee.family_name == family_name).all()

def get_refugees_by_first_name(db: Session, first_name: str):
    return db.query(models.Refugee).filter(models.Refugee.first_name == first_name).all()

def get_refugees_by_first_and_family_name(db: Session, first_name: str, family_name: str):
    return (
        db.query(models.Refugee)
        .filter(models.Refugee.first_name == first_name, models.Refugee.family_name == family_name)
        .all()
    )
def get_refugees_by_birth_date(db: Session, birth_date: date):
    return db.query(models.Refugee).filter(models.Refugee.birth_date == birth_date).all()

def get_refugees_by_salary(db: Session, salary: int = 0):
    return db.query(models.Refugee).filter(models.Refugee.salary_targeted == salary).all()

def get_refugees_by_email(db: Session, email: str):
    return db.query(models.Refugee).filter(models.Refugee.email == email).all()

# def get_refugees_by_keyword(db: Session, keyword: str):
#     return (
#         db.query(models.Refugee, models.Keyword, models.EquivalentKeyword)
#         .filter(models.Refugee.keyword.contains(models.EquivalentKeyword.keyword))
#         .filter(models.EquivalentKeyword.keyword == models.Keyword.label)
#         .filter(models.Keyword.label == keyword)
#         .all()
#     )

# Refugees: CREATE
def create_refugee(db: Session, refugee: schemas.Refugee): # maybe put a keywords_id to link with equivalence table ? 
    db_refugee = models.Refugee(**refugee.dict())
    db.add(db_refugee)
    db.commit()
    db.refresh(db_refugee)
    return db_refugee

# Employers

# Keywords: CREATE
# def get_equikeywords_by_keyword(db: Session, keyword: str):

# OLD
def get_point_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PointEvent).offset(skip).limit(limit).all()


def get_points_by_player(db: Session, player: str):
    return db.query(models.PointEvent).filter(models.PointEvent.player == player).all()


def get_points_by_team(db: Session, team: str):
    return db.query(models.PointEvent).filter(models.PointEvent.team == team).all()


def get_points_by_season(db: Session, season: str):
    return db.query(models.PointEvent).filter(models.PointEvent.season == season).all()


def get_points_by_team_and_season(db: Session, team: str, season: str):
    return (
        db.query(models.PointEvent)
        .filter(models.PointEvent.team == team, models.PointEvent.season == season)
        .all()
    )


def get_points_by_player_and_season(db: Session, player: str, season: str):
    return (
        db.query(models.PointEvent)
        .filter(models.PointEvent.player == player, models.PointEvent.season == season)
        .all()
    )
