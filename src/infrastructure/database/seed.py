import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from dotenv import load_dotenv

from src.infrastructure.database.tables import UserModel, MonitoredAccountModel, SubscriptionModel

load_dotenv()

async def seed_data():
    # 1. Setup Connection
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        print("🌱 Starting Seed Process...")

        # 2. Create Default User (If not exists)
        # We assume YOU are the user.
        user_email = "binhnam1505@gmail.com"
        result = await session.execute(select(UserModel).where(UserModel.email == user_email))
        user = result.scalar_one_or_none()

        if not user:
            user = UserModel(email=user_email, is_active=True)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"✅ Created User: {user.email} (ID: {user.id})")
        else:
            print(f"ℹ️ User {user_email} already exists (ID: {user.id})")

        # 3. Create a Target Account (MrBeast)
        target_username = "mrbeast"
        result = await session.execute(select(MonitoredAccountModel).where(MonitoredAccountModel.username == target_username))
        account = result.scalar_one_or_none()

        if not account:
            account = MonitoredAccountModel(username=target_username, platform="tiktok")
            session.add(account)
            await session.commit()
            await session.refresh(account)
            print(f"✅ Created Account: @{account.username}")
        else:
            print(f"ℹ️ Account @{target_username} already exists")

        # 4. Create Subscription (Link User <-> Account)
        # This is the "Fan-Out" logic: User subscribes to Account
        result = await session.execute(
            select(SubscriptionModel).where(
                SubscriptionModel.user_id == user.id,
                SubscriptionModel.account_id == account.id
            )
        )
        subscription = result.scalar_one_or_none()

        if not subscription:
            sub = SubscriptionModel(user_id=user.id, account_id=account.id)
            session.add(sub)
            await session.commit()
            print(f"🔗 Linked {user.email} to @{account.username}")
        else:
            print(f"ℹ️ Subscription already active")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_data())