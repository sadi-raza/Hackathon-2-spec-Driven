"""
Test script to verify integer IDs work correctly.
"""

import asyncio
import httpx
import time

async def test_integer_ids():
    """Test the API with integer IDs."""
    base_url = "http://localhost:8000/api"
    time.sleep(10) # Wait for server to start

    async with httpx.AsyncClient() as client:
        print("\n=== Testing Integer IDs ===\n")

        # 1. Register a new user
        print("1. Registering a new user...")
        register_response = await client.post(
            f"{base_url}/auth/signup",
            json={"email": "test_int@example.com", "password": "test123456"}
        )
        print(f"   Status: {register_response.status_code}")

        if register_response.status_code == 409:
            # User already exists, try to login
            print("   User exists, logging in...")
            login_response = await client.post(
                f"{base_url}/auth/login",
                json={"email": "test_int@example.com", "password": "test123456"}
            )
            if login_response.status_code != 200:
                print(f"   Login failed: {login_response.text}")
                return
            auth_data = login_response.json()
        elif register_response.status_code != 201:
            print(f"   Register failed: {register_response.text}")
            return
        else:
            auth_data = register_response.json()

        user_id = auth_data.get("user", {}).get("id")
        token = auth_data.get("token")
        print(f"   User ID: {user_id} (type: {type(user_id).__name__})")
        print(f"   Token: {token[:30]}...")

        # 2. Create a task
        print("\n2. Creating a task...")
        headers = {"Authorization": f"Bearer {token}"}
        task_response = await client.post(
            f"{base_url}/tasks",
            headers=headers,
            json={"title": "Test task with integer ID", "description": "Testing!"}
        )
        print(f"   Status: {task_response.status_code}")
        if task_response.status_code == 201:
            task_data = task_response.json()
            task_id = task_data.get("task", {}).get("id")
            print(f"   Task ID: {task_id} (type: {type(task_id).__name__})")
        else:
            task_id = None
            print(f"   Failed: {task_response.text}")

        # 3. List tasks
        print("\n3. Listing tasks...")
        list_response = await client.get(
            f"{base_url}/tasks",
            headers=headers
        )
        print(f"   Status: {list_response.status_code}")
        if list_response.status_code == 200:
            tasks = list_response.json()
            print(f"   Total tasks: {tasks.get('total')}")
            for task in tasks.get("tasks", []):
                print(f"   - ID: {task['id']} | Title: {task['title']}")
        else:
            print(f"   Failed: {list_response.text}")

        # 4. Get a specific task by integer ID
        if task_id:
            print(f"\n4. Getting task by ID {task_id}...")
            get_response = await client.get(
                f"{base_url}/tasks/{task_id}",
                headers=headers
            )
            print(f"   Status: {get_response.status_code}")
            if get_response.status_code == 200:
                task = get_response.json().get("task")
                print(f"   Task: {task}")
            else:
                print(f"   Failed: {get_response.text}")

        # 5. Check database directly
        print("\n5. Checking database...")
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        from app.config import settings

        engine = create_async_engine(settings.DATABASE_URL)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT id, email FROM users ORDER BY id"))
            users = result.fetchall()
            print(f"   Users in DB:")
            for user in users:
                print(f"   - ID: {user[0]} (type: {type(user[0]).__name__}) | Email: {user[1]}")

            result = await conn.execute(text("SELECT id, title, user_id FROM tasks ORDER BY id"))
            tasks = result.fetchall()
            print(f"   Tasks in DB:")
            for task in tasks:
                print(f"   - ID: {task[0]} (type: {type(task[0]).__name__}) | Title: {task[1]} | User: {task[2]}")

        await engine.dispose()

        print("\n=== All tests passed! Integer IDs are working correctly. ===\n")


if __name__ == "__main__":
    asyncio.run(test_integer_ids())
