from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Integer, BigInteger, String, DateTime, Text, ForeignKey, func


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class UserData(Base):
    __tablename__ = "user_data"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)

class UserStatus(Base):
    __tablename__ = "user_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    banned: Mapped[bool] = mapped_column(Boolean, default=False)
    warning: Mapped[bool] = mapped_column(Boolean, default=False)
    event_notifications: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id = mapped_column(ForeignKey("user_data.tg_id"), unique=True)

class Structure(Base):
    __tablename__ = "structure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    short_name: Mapped[str] = mapped_column(String(10), nullable=False)

class Position(Base):
    __tablename__ = "position"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    position_title: Mapped[str] = mapped_column(String(100), nullable=False)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(15), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(13), nullable=False)
    instagram: Mapped[str] = mapped_column(String(50))
    telegram: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    quote: Mapped[str] = mapped_column(String(200))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    structure_id: Mapped[int] = mapped_column(ForeignKey("structure.id"))

    structure = relationship("Structure", backref="positions")

class PositionStatus(Base):
    __tablename__ = "position_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    questions_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    hostels_notifications: Mapped[bool] = mapped_column(Boolean, default=False)
    ideas_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    talents_notifications: Mapped[bool] = mapped_column(Boolean, default=True)

    position_id = mapped_column(ForeignKey("position.id"), unique=True)


class PositionShowInfo(Base):
    __tablename__ = "position_show_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    show_phone: Mapped[bool] = mapped_column(Boolean, default=True)
    show_instagram: Mapped[bool] = mapped_column(Boolean, default=True)
    show_telegram: Mapped[bool] = mapped_column(Boolean, default=True)
    show_email: Mapped[bool] = mapped_column(Boolean, default=True)

    position_id: Mapped[int] = mapped_column(ForeignKey("position.id"))

    position = relationship("Position", backref="position_show_info")


class GovernmentAlbum(Base):
    __tablename__ = "government_album"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    position_id: Mapped[int] = mapped_column(ForeignKey("position.id"))

    position = relationship("Position", backref="government_album", lazy='selectin')

class ScheduledEvents(Base):
    __tablename__ = "scheduled_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    date_time_start: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    organizer: Mapped[str] = mapped_column(String(100), nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by = mapped_column(ForeignKey("position.id"))

class EventAlbum(Base):
    __tablename__ = "event_album"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    album_event_id: Mapped[int] = mapped_column(ForeignKey("scheduled_events.id"), nullable=False)

class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    for_whom: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    answered: Mapped[bool] = mapped_column(Boolean, default=False)
    from_whom_id: Mapped[int] = mapped_column(ForeignKey("user_data.tg_id"), nullable=False)

class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    who_answered_id: Mapped[int] = mapped_column(ForeignKey("user_data.tg_id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), unique=True, nullable=False)

class ProposeIdea(Base):
    __tablename__ = "propose_idea"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    idea: Mapped[str] = mapped_column(Text, nullable=False)
    from_whom_id: Mapped[int] = mapped_column(ForeignKey("user_data.tg_id"), nullable=False)
    proposed_at: Mapped[str] = mapped_column(String(20), nullable=False)

class JoinGovernment(Base):
    __tablename__ = "join_government"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    join_to: Mapped[str] = mapped_column(String(20), nullable=False)
    user_info: Mapped[str] = mapped_column(String(100), nullable=False)
    structure: Mapped[str] = mapped_column(String(5), nullable=False)
    group: Mapped[str] = mapped_column(String(20), nullable=False)
    motivation: Mapped[str] = mapped_column(Text, nullable=False)
    own_idea: Mapped[str] = mapped_column(Text, nullable=False)
    from_whom_id: Mapped[int] = mapped_column(ForeignKey("user_data.tg_id"), nullable=False)

class Hostel(Base):
    __tablename__ = "hostel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(30), nullable=False)

class HostelDisadvantages(Base):
    __tablename__ = "hostel_disadvantages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    from_whom_id: Mapped[int] = mapped_column(ForeignKey("user_data.tg_id"), nullable=False)
    hostel_id: Mapped[int] = mapped_column(ForeignKey("hostel.id"), nullable=False)

class HostelDisadvantagesAlbum(Base):
    __tablename__ = "hostel_disadvantages_album"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    album_disadvantages_id: Mapped[int] = mapped_column(ForeignKey("hostel_disadvantages.id"), nullable=False)

class HostelComplaint(Base):
    __tablename__ = "hostel_complaint"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    from_whom_id: Mapped[int] = mapped_column(ForeignKey("user_data.tg_id"), nullable=False)
    hostel_id: Mapped[int] = mapped_column(ForeignKey("hostel.id"), nullable=False)

class LNTUCapability(Base):
    __tablename__ = "lntu_capability"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    capability: Mapped[str] = mapped_column(Text, nullable=False)
    from_whom_id: Mapped[int] = mapped_column(ForeignKey("user_data.tg_id"), nullable=False)

class WhiteList(Base):
    __tablename__ = "white_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    superadmin_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

# class Chats(Base):
#     __tablename__ = "bot_chat"
