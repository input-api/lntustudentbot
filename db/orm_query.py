from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import pytz

from db.models import UserData, UserStatus, WhiteList, Structure, Position, GovernmentAlbum, ProposeIdea, Question, \
    Answer, PositionStatus, ScheduledEvents, EventAlbum, LNTUCapability


#/////////////////////// ORM QUERIES FOR MODEL WhiteList ///////////////////////#
async def orm_add_to_white_list(session: AsyncSession, id):
    query = select(WhiteList.superadmin_id)
    result = await session.execute(query)

    existing_superadmin = result.scalars().first()

    if not existing_superadmin:
        su = WhiteList(superadmin_id=id)
        session.add(su)
        await session.commit()
    else:
        pass

#/////////////////////// ORM QUERIES FOR MODEL UserData ///////////////////////#
async def orm_add_user_data(session: AsyncSession, data: dict):
    user = UserData(
        tg_id=data["tg_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        username=data["username"]
    )
    session.add(user)
    await session.flush()

    user_status = UserStatus(
        user_id=user.tg_id
    )

    session.add(user_status)
    await session.commit()

async def orm_get_users_data(session: AsyncSession()):
    query = select(UserData)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_users_data_count(session: AsyncSession()):
    query = select(func.count(UserData.tg_id))
    result = await session.execute(query)
    count = result.scalar()
    return count

async def orm_get_user_data(session: AsyncSession(), user_id: int):
    query = select(UserData).where(UserData.tg_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_get_banned_users(session: AsyncSession(), user_id: int):
    query = select(UserData).join(UserStatus).where(UserStatus.banned == True)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_update_user_data(session: AsyncSession(), user_id: int, data):
    query = update(UserData).where(UserData.tg_id == user_id).values(
        first_name=data["first_name"],
        last_name=data["last_name"],
        username=data["username"]
    )
    await session.execute(query)
    await session.commit()


#/////////////////////// ORM QUERIES FOR MODEL UserStatus ///////////////////////#
async def orm_update_status_warning(session: AsyncSession(), user_id):
    query = update(UserStatus).where(UserStatus.user_id == user_id).values(
        warning=True
    )
    await session.execute(query)
    await session.commit()

async def orm_update_status_banned(session: AsyncSession(), user_id):
    query = update(UserStatus).where(UserStatus.user_id == user_id).values(
        banned=True
    )
    await session.execute(query)
    await session.commit()

async def orm_update_status_unban(session: AsyncSession(), user_id):
    query = update(UserStatus).where(UserStatus.user_id == user_id).values(
        banned=False
    )
    await session.execute(query)
    await session.commit()

async def orm_update_status_event_notifications(session: AsyncSession, user_id: int, status: bool):
    query = update(UserStatus).where(UserStatus.user_id == user_id).values(
        event_notifications=status
    )
    await session.execute(query)
    await session.commit()

async def orm_get_status(session: AsyncSession(), user_id):
    query = select(UserStatus).where(UserStatus.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_get_status_warning(session: AsyncSession(), user_id):
    query = select(UserStatus.warning).where(UserStatus.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_get_status_banned(session: AsyncSession(), user_id):
    query = select(UserStatus.banned).where(UserStatus.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_get_status_event_notifications(session: AsyncSession(), user_id):
    query = select(UserStatus.event_notifications).where(UserStatus.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_get_all_user_with_event_notification(session: AsyncSession):
    query = select(UserData.tg_id).join(UserStatus, UserData.tg_id == UserStatus.user_id).where(UserStatus.event_notifications == True)
    result = await session.execute(query)
    return result.scalars().all()

#/////////////////////// ORM QUERIES FOR MODEL Structure ///////////////////////#
async def orm_add_structure(session: AsyncSession(), data: dict):
    structure = Structure(
        full_name=data["full_name"],
        short_name=data["short_name"],
    )
    session.add(structure)
    await session.commit()

async def orm_get_structure(session: AsyncSession(), structure):
    query = select(Structure).where(Structure.short_name == structure)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_get_all_structures(session: AsyncSession()):
    query = select(Structure)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_structure_by_tg_id_position(session: AsyncSession(), tg_id: int):
    query = select(Structure).join(Position, Structure.id == Position.structure_id).where(Position.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalars().first()


#/////////////////////// ORM QUERIES FOR MODEL Position ///////////////////////#
async def orm_add_position(session: AsyncSession(), data: dict):
    query = select(Structure.id).where(Structure.short_name == data["structure"])
    structure_obj = await session.execute(query)
    structure_id = structure_obj.scalars().first()

    position = Position(
        position_title=data["position_title"],
        tg_id=data["tg_id"],
        name=data["name"],
        surname=data["surname"],
        phone=data["phone"],
        instagram=data["instagram"],
        telegram=data["telegram"],
        email=data["email"],
        is_admin=data["is_admin"],
        quote=data["quote"],
        structure_id=structure_id,
    )
    session.add(position)
    await session.flush()

    gov_photo = GovernmentAlbum(
        image=data["photo_file_id"],
        position_id=position.id,
    )
    session.add(gov_photo)
    await session.flush()

    position_status = PositionStatus(
        position_id=position.id
    )
    session.add(position_status)
    await session.commit()

async def orm_get_positions(session: AsyncSession, structure: str):
    query = select(Position).join(Structure, Position.structure_id == Structure.id).where(Structure.short_name == structure)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_all_positions(session: AsyncSession):
    query = select(Position)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_positions_id_list(session: AsyncSession):
    query = select(Position.id)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_update_position(session: AsyncSession, position_id, **kwargs):
    query = update(Position).where(Position.id == position_id).values(
        **kwargs
    )
    await session.execute(query)
    await session.commit()

#/////////////////////// ORM QUERIES FOR MODEL GovernmentAlbum ///////////////////////#
async def orm_get_image_by_position_id(session: AsyncSession, position: int):
    query = select(GovernmentAlbum).join(Position, Position.id == GovernmentAlbum.position_id).where(GovernmentAlbum.position_id == position)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_update_position_photo(session: AsyncSession, position_id: int, image):
    query = update(GovernmentAlbum).where(GovernmentAlbum.position_id == position_id).values(
        image=image
    )
    await session.execute(query)
    await session.commit()

#/////////////////////// ORM QUERIES FOR MODEL ProposeIdea ///////////////////////#
async def orm_add_propose_idea(session: AsyncSession(), data: dict):
    idea = ProposeIdea(
        idea = data["idea"],
        from_whom_id=data["from_whom_id"],
        proposed_at=data["proposed_at"],
    )
    session.add(idea)
    await session.commit()


#/////////////////////// ORM QUERIES FOR MODEL Question ///////////////////////#
async def orm_add_question(session: AsyncSession(), data):
    question = Question(
        for_whom=data["for_whom"],
        content=data["content"],
        message_id=data["message_id"],
        from_whom_id=data["from_whom_id"]
    )
    session.add(question)
    await session.commit()

async def orm_update_question(session: AsyncSession(), id):
    query = update(Question).where(Question.id == id).values(
        answered=True
    )
    await session.execute(query)
    await session.commit()

async def orm_get_questions(session: AsyncSession(), structure: str):
    query = select(Question).join(Structure, Question.for_whom == Structure.short_name).where(Question.answered == False, Structure.short_name == structure)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_from_whom_id(session: AsyncSession(), question_id):
    query = select(Question.from_whom_id, Question.content).where(Question.id == question_id)
    result = await session.execute(query)
    return result.first()

#/////////////////////// ORM QUERIES FOR MODEL Answer ///////////////////////#
async def orm_add_answer(session: AsyncSession(), data):
    answer = Answer(
        answer_text=data["answer_text"],
        who_answered_id=data["who_answered_id"],
        question_id=data["question_id"],
    )
    session.add(answer)
    await session.flush()

    question_id = data["question_id"]

    await orm_update_question(session, question_id)


#/////////////////////// ORM QUERIES FOR MODEL ScheduledEvents ///////////////////////#
async def orm_add_scheduled_event(session: AsyncSession(), data):
    query = select(Position.id).where(Position.tg_id == data["created_by"])
    admin_obj = await session.execute(query)
    admin = admin_obj.scalars().first()

    event = ScheduledEvents(
        title=data["title"],
        description=data["description"],
        date_time_start=data["date_time"],
        location=data["location"],
        organizer=data["organizer"],
        created_by=admin
    )
    session.add(event)
    await session.flush()

    event_photo = EventAlbum(
        image=data["image"],
        album_event_id=event.id
    )
    session.add(event_photo)
    await session.commit()

async def orm_get_scheduled_event_by_id(session: AsyncSession, event_id):
    query = select(ScheduledEvents).where(ScheduledEvents.id == event_id)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_get_admins_events(session: AsyncSession, admin_tg_id, public: bool):
    creator_obj = await session.execute(select(Position.id).where(Position.tg_id == admin_tg_id))
    creator = creator_obj.scalars().first()

    kyiv_tz = pytz.timezone("Europe/Kiev")
    now_kyiv = datetime.now(kyiv_tz).replace(tzinfo=None)

    query = select(ScheduledEvents).where(ScheduledEvents.created_by == creator, ScheduledEvents.published == public, ScheduledEvents.date_time_start > now_kyiv)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_admins_events_id_list(session: AsyncSession, admin_tg_id: int, publish: bool, publish_status: bool):
    creator_obj = await session.execute(select(Position.id).where(Position.tg_id == admin_tg_id))
    creator = creator_obj.scalars().first()

    kyiv_tz = pytz.timezone("Europe/Kiev")
    now_kyiv = datetime.now(kyiv_tz).replace(tzinfo=None)

    if publish:
        query = select(ScheduledEvents.id).where(
            ScheduledEvents.created_by == creator,
            ScheduledEvents.published == publish_status,
            ScheduledEvents.date_time_start > now_kyiv)
    else:
        query = select(ScheduledEvents.id).where(
            ScheduledEvents.created_by == creator,
            ScheduledEvents.date_time_start > now_kyiv)

    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_date_time_start_event(session: AsyncSession, event_id):
    query = select(ScheduledEvents.date_time_start).where(ScheduledEvents.id == event_id)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_get_published_events(session: AsyncSession):
    query = select(ScheduledEvents).where(ScheduledEvents.published == True)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_update_event(session: AsyncSession, event_id, **kwargs):
    query = update(ScheduledEvents).where(ScheduledEvents.id == event_id).values(
        **kwargs
    )
    await session.execute(query)
    await session.commit()

async def orm_delete_event_by_id(session: AsyncSession, event_id):
    await session.execute(
        delete(EventAlbum).where(EventAlbum.album_event_id == event_id)
    )
    await session.execute(
        delete(ScheduledEvents).where(ScheduledEvents.id == event_id)
    )
    await session.commit()

#/////////////////////// ORM QUERIES FOR MODEL EventAlbum ///////////////////////#
async def orm_get_poster_by_event_id(session: AsyncSession, event_id: int):
    query = select(EventAlbum.image).where(EventAlbum.album_event_id == event_id)
    result = await session.execute(query)
    return result.scalars().first()

async def orm_update_event_poster(session: AsyncSession, event_id: int, image):
    query = update(EventAlbum).where(EventAlbum.album_event_id == event_id).values(
        image=image
    )
    await session.execute(query)
    await session.commit()

#/////////////////////// ORM QUERIES FOR MODEL LNTUCapability ///////////////////////#
async def orm_add_lntu_telent(session: AsyncSession, capability, from_whom_id):
    capability_obj = LNTUCapability(
        capability=capability,
        from_whom_id=from_whom_id
    )
    session.add(capability_obj)
    await session.commit()