from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dependencies import get_db
from models import User, Female

api_router = APIRouter()

# Admin Routes
@api_router.get("/admin/dashboard/")
async def admin_dashboard(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Female))
    females = result.scalars().all()
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {
        "total_females": len(females),
        "total_users": len(users),
        "total_earnings": sum(f.earnings_today for f in females),
    }

# Female Routes
@api_router.get("/female/profile/")
async def female_profile(telegram_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Female).where(Female.telegram_id == telegram_id))
    female = result.scalar_one_or_none()
    if not female:
        return {"error": "Profile not found"}
    return {"name": female.name, "earnings_today": female.earnings_today}

# Lead Routes
@api_router.get("/lead/overview/")
async def lead_overview(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Female))
    females = result.scalars().all()
    return {"overview": [{"id": f.id, "name": f.name, "earnings_today": f.earnings_today} for f in females]}

# User Routes
@api_router.post("/user/create/")
async def create_user(telegram_id: str, name: str, db: AsyncSession = Depends(get_db)):
    new_user = User(telegram_id=telegram_id, name=name)
    db.add(new_user)
    await db.commit()
    return {"message": "User created", "user": {"id": new_user.id, "name": new_user.name}}
