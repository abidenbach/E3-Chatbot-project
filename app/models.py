from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, Enum, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from database import Base
import enum

class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id_utilisateur = Column(Integer, primary_key=True)
    nom = Column(String(191), nullable=False)
    prenom = Column(String(191), nullable=False)
    mail = Column(String(191), unique=True, nullable=False)
    motdepasse_hash = Column(String(255), nullable=False)

class StyleMusical(Base):
    __tablename__ = "style_musical"

    id_style = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False)

class Salle(Base):
    __tablename__ = "salle"

    id_salle = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False)
    chemin = Column(String(255))

class Contact(Base):
    __tablename__ = "contact"

    id_contact = Column(Integer, primary_key=True)
    tel = Column(String(20), nullable=False)
    adresse = Column(Text, nullable=False)
    mail = Column(String(255), nullable=False)

class Prompt(Base):
    __tablename__ = "prompt"

    id_prompt = Column(Integer, primary_key=True)
    contexte = Column(Text, nullable=False)
    label = Column(String(255), nullable=False)

class Menu(Base):
    __tablename__ = "menu"

    id_menu = Column(Integer, primary_key=True)
    actif = Column(Boolean, nullable=False, default=False)
    chemin = Column(String(255), nullable=False)
    date_ = Column(DateTime, nullable=False)

class MenuProduit(Base):
    __tablename__ = "menu_produit"

    id_produit = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False)
    prix = Column(Numeric(10, 2), nullable=False)
    id_menu = Column(Integer, ForeignKey("menu.id_menu"), nullable=False)

class Artiste(Base):
    __tablename__ = "artiste"

    id_artiste = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    prenom = Column(String(255), nullable=False)
    nom_scene = Column(String(255), nullable=False)
    id_style = Column(Integer, ForeignKey("style_musical.id_style"), nullable=False)

class Concert(Base):
    __tablename__ = "concert"

    id_concert = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    id_salle = Column(Integer, ForeignKey("salle.id_salle"), nullable=False)
    id_artiste = Column(Integer, ForeignKey("artiste.id_artiste"), nullable=False)

class Billet(Base):
    __tablename__ = "billet"

    id_billet = Column(Integer, primary_key=True)
    date_achat = Column(DateTime, nullable=False)
    date_valide = Column(DateTime)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=False)
    id_concert = Column(Integer, ForeignKey("concert.id_concert"), nullable=False)

class RoleEnum(enum.Enum):
    user = "user"
    assistant = "assistant"

class Chat(Base):
    __tablename__ = "chat"

    uuid_chat = Column(CHAR(36), primary_key=True)
    created_at = Column(DateTime, nullable=False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=False)
    id_prompt = Column(Integer, ForeignKey("prompt.id_prompt"), nullable=False)

class Message(Base):
    __tablename__ = "message"

    uuid_message = Column(CHAR(36), primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    contenu = Column(Text, nullable=False)
    date_creation = Column(DateTime, nullable=False)
    uuid_chat = Column(CHAR(36), ForeignKey("chat.uuid_chat"), nullable=False)