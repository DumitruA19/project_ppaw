# app/models/sql_models.py
import uuid
from sqlalchemy import (
    Column, String, Text, ForeignKey, BigInteger, 
    Boolean, Index, Integer, Date, Numeric
)
# IMPORT CRITIC PENTRU COMPATIBILITATE MYSQL 8.0+
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from app.core.db import Base

def generate_uuid():
    return str(uuid.uuid4())

# =============================================================================
# 1-3. USERS, ACCOUNT, ADMIN (Modulele: Auth, Account, Admin)
# =============================================================================
class User(Base):
    """Gerează datele de identitate și profil."""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid) 
    email = Column(String(320), nullable=False, unique=True, index=True)
    name = Column(String(200), nullable=True)
    password_hash = Column(String(255), nullable=False) #
    role = Column(String(50), nullable=False, server_default=text("'user'")) #
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

    # Relatii catre toate modulele
    conversations = relationship("Conversation", back_populates="user", cascade="all,delete")
    favorites = relationship("Favorite", back_populates="user", cascade="all,delete")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all,delete")
    payments = relationship("Payment", back_populates="user")

# =============================================================================
# 4-7. CHAT & RAG (Modulele: Chat, Conversations, Messages, Recommendations)
# =============================================================================
class Conversation(Base):
    """Sesiuni de chat individuale între utilizator și AI."""
    __tablename__ = "conversations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=True)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))
    updated_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)"))

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all,delete")
    recommendations = relationship("Recommendation", back_populates="conversation", cascade="all,delete")

class Message(Base):
    """Istoricul replicilor dintr-o conversație."""
    __tablename__ = "messages"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False) # 'user' sau 'assistant'
    content = Column(Text, nullable=False) 
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))
    
    conversation = relationship("Conversation", back_populates="messages")

class Recommendation(Base):
    """Cărțile sugerate de AI pe baza contextului RAG."""
    __tablename__ = "recommendations"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    book_title = Column(String(400), nullable=False)
    chroma_doc_id = Column(String(200), nullable=True)
    reason = Column(Text, nullable=True) 
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

    conversation = relationship("Conversation", back_populates="recommendations")

# =============================================================================
# 8-10. BILLING & USAGE (Modulele: Subscriptions, Billing, Usage)
# =============================================================================
class BillingPlan(Base):
    """Definițiile planurilor tarifare."""
    __tablename__ = "billing_plans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    monthly_price = Column(Numeric(10, 2), nullable=False)
    message_limit = Column(Integer, nullable=True)

class Subscription(Base):
    """Statusul abonamentului activ al unui utilizator."""
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_name = Column(String(50), nullable=False) 
    status = Column(String(50), nullable=False) 
    current_period_start = Column(DATETIME(fsp=3), nullable=False)
    current_period_end = Column(DATETIME(fsp=3), nullable=False)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))
    
    user = relationship("User", back_populates="subscriptions")

class Payment(Base):
    """Istoricul tranzacțiilor financiare."""
    __tablename__ = "payments"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="RON")
    status = Column(String(50), default="succeeded")
    created_at = Column(DATETIME(fsp=3), server_default=text("CURRENT_TIMESTAMP(3)"))

    user = relationship("User", back_populates="payments")

class UsageCounter(Base):
    """Monitorizarea consumului de mesaje AI."""
    __tablename__ = "usage_counters"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    messages_used = Column(Integer, default=0)
    last_update = Column(DATETIME(fsp=3), server_default=text("CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)"))

# =============================================================================
# 11-12. SYSTEM & FAVORITES (Modulele: Favorites, Logs, Auth Extras)
# =============================================================================
class Favorite(Base):
    """Cărțile salvate de utilizator."""
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_title = Column(String(400), nullable=False)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

    user = relationship("User", back_populates="favorites")

class Log(Base):
    """Audit de sistem."""
    __tablename__ = "logs"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(36), nullable=True)
    action = Column(String(255), nullable=False) 
    metadata_json = Column(Text, nullable=True) 
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

class PasswordReset(Base):
    """Token-uri pentru resetarea parolelor."""
    __tablename__ = "password_resets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DATETIME(fsp=3), nullable=False)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

    user = relationship("User", backref="password_resets")

# =============================================================================
# INDEXURI FINALE
# =============================================================================
Index("IX_subscriptions_user_status", Subscription.user_id, Subscription.status)


# Adăugați în app/models/sql_models.py
class ActionLog(Base):
    __tablename__ = "action_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    action_type = Column(String(50), nullable=False)  # ex: CHAT, LOGIN, BILLING, INGEST
    endpoint = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="SUCCESS") # SUCCESS sau ERROR
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))