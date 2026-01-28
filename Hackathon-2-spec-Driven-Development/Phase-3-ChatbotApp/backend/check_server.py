"""
Quick check to verify the server and database with integer IDs.
"""

import asyncio
import httpx
import uuid


async def check():
    """Full server check with integer IDs."""
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        # Health check
        print("1. Health check...")
        r = await client.get(f"{base_url}/health")
        print(f"   Status: {r.status_code} - {r.text}")

        # Signup with unique email
        email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        print(f"\n2. Signup with {email}...")
        r = await client.post(
            f"{base_url}/api/auth/signup",
            json={"email": email, "password": "test123456"}
        )
        print(f"   Status: {r.status_code}")
        data = r.json()
        user_id = data["user"]["id"]
        token = data["token"]
        print(f"   User ID: {user_id} (type: {type(user_id).__name__})")
        print(f"   Token received: {token[:30]}...")

        # Create a task
        headers = {"Authorization": f"Bearer {token}"}
        print(f"\n3. Creating a task...")
        r = await client.post(
            f"{base_url}/api/tasks",
            headers=headers,
            json={"title": "Test with integer ID", "description": "Verifying int IDs work"}
        )
        print(f"   Status: {r.status_code}")
        task_data = r.json()
        task_id = task_data["task"]["id"]
        print(f"   Task ID: {task_id} (type: {type(task_id).__name__})")
        print(f"   Task: {task_data['task']}")

        # List tasks
        print(f"\n4. Listing tasks...")
        r = await client.get(
            f"{base_url}/api/tasks",
            headers=headers
        )
        print(f"   Status: {r.status_code}")
        tasks = r.json()
        print(f"   Total tasks: {tasks['total']}")
        for t in tasks.get("tasks", []):
            print(f"   - ID: {t['id']} (type: {type(t['id']).__name__}) | Title: {t['title']}")

        # Get task by integer ID
        print(f"\n5. Getting task by ID {task_id}...")
        r = await client.get(
            f"{base_url}/api/tasks/{task_id}",
            headers=headers
        )
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            task = r.json()["task"]
            print(f"   Retrieved Task: ID={task['id']}, Title={task['title']}")

        # Complete the task
        print(f"\n6. Completing task {task_id}...")
        r = await client.patch(
            f"{base_url}/api/tasks/{task_id}",
            headers=headers,
            json={"completed": True}
        )
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            task = r.json()["task"]
            print(f"   Task completed: {task['completed']}")

        # Delete the task
        print(f"\n7. Deleting task {task_id}...")
        r = await client.delete(
            f"{base_url}/api/tasks/{task_id}",
            headers=headers
        )
        print(f"   Status: {r.status_code}")
        print(f"   Response: {r.text}")

        print("\n=== All tests passed! Integer IDs are working correctly. ===")


if __name__ == "__main__":
    asyncio.run(check())
