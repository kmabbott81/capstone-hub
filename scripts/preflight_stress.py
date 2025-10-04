import os, asyncio, json, time, random, string
import aiohttp

BASE = os.environ.get("BASE_URL", "https://mabbottmbacapstone.up.railway.app")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")  # set this in env
DEBUG_KEY = os.environ.get("DEBUG_KEY")  # same as on server for debug routes
HEADERS = {"Accept": "application/json"}

def rnd(n=6): return ''.join(random.choices(string.ascii_letters+string.digits, k=n))

async def get_csrf(session):
    async with session.get(f"{BASE}/api/csrf-token") as r:
        j = await r.json()
        return j.get("csrf_token","")

async def login(session):
    # login is CSRF-exempt per Phase 1; rate-limited separately
    async with session.post(f"{BASE}/api/auth/login",
                            json={"password": ADMIN_PASSWORD},
                            headers=HEADERS) as r:
        return r.status

async def create_deliverable(session, token):
    payload = {
        "title": f"LoadTest-{rnd()}",
        "description": "preflight",
        "status": "Not Started"
    }
    h = dict(HEADERS); h["X-CSRFToken"] = token
    async with session.post(f"{BASE}/api/deliverables", json=payload, headers=h) as r:
        try: j = await r.json()
        except: j = {}
        return r.status, j.get("id")

async def update_deliverable(session, token, did):
    payload = {"status":"In Progress"}
    h = dict(HEADERS); h["X-CSRFToken"] = token
    async with session.put(f"{BASE}/api/deliverables/{did}", json=payload, headers=h) as r:
        return r.status

async def delete_deliverable(session, token, did):
    h = dict(HEADERS); h["X-CSRFToken"] = token
    async with session.delete(f"{BASE}/api/deliverables/{did}", headers=h) as r:
        return r.status

async def burst_login_rate_limit(session):
    codes = []
    for _ in range(6):
        async with session.post(f"{BASE}/api/auth/login",
                                json={"password": "definitely-wrong"},
                                headers=HEADERS) as r:
            codes.append(r.status)
    return codes  # expect last one 429

async def csrf_negative(session):
    # should fail 400/403 without token
    async with session.post(f"{BASE}/api/deliverables",
                            json={"title":"NoToken"}, headers=HEADERS) as r:
        return r.status

async def idle_timeout(session, token):
    # requires debug route to set _last_seen artificially old
    h = {"X-Debug-Key": DEBUG_KEY}
    async with session.post(f"{BASE}/api/_debug/set_last_seen",
                            json={"ago_seconds": 1900}, headers=h) as r:
        if r.status == 200:
            _ = await r.json()
        else:
            print(f"   Debug endpoint returned {r.status}")
    # now attempt a write -> should 401
    h2 = dict(HEADERS); h2["X-CSRFToken"] = token
    async with session.post(f"{BASE}/api/deliverables",
                            json={"title":"Should401"}, headers=h2) as r:
        return r.status

async def do_backup(session, token):
    h = dict(HEADERS); h["X-CSRFToken"] = token
    async with session.post(f"{BASE}/api/admin/backup", headers=h) as r:
        return r.status

async def read_burst(session, n=100):
    tasks = [session.get(f"{BASE}/api/deliverables") for _ in range(n)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [getattr(r, "status", 0) for r in results]

async def main():
    # Test CSRF without affecting rate limits
    async with aiohttp.ClientSession() as temp_session:
        print(">> CSRF negative:", await csrf_negative(temp_session))

    if not ADMIN_PASSWORD:
        print("!! ADMIN_PASSWORD not set; skipping admin-only tests")
        return

    # Test rate limiting with throwaway session
    async with aiohttp.ClientSession() as temp_session:
        codes = await burst_login_rate_limit(temp_session)
        print(">> Login burst:", codes)

    # Use fresh session for actual admin work
    cookies = aiohttp.CookieJar()
    async with aiohttp.ClientSession(cookie_jar=cookies) as session:
        # Login as admin
        ok = await login(session)
        print(">> Admin login status:", ok)

        token = await get_csrf(session)

        # Concurrency: create/update/delete 20 items in parallel
        created = await asyncio.gather(*[create_deliverable(session, token) for _ in range(20)])
        ids = [i for (code, i) in created if code in (200,201) and i]
        print(f">> Created: {len(ids)}")

        upd = await asyncio.gather(*[update_deliverable(session, token, i) for i in ids])
        print(f">> Updated OK:", sum(1 for c in upd if c==200))

        # Backup under load
        rb = await read_burst(session, 50)
        bk = await do_backup(session, token)
        print(">> Read burst 50 avg status:", sum(rb)/len(rb), " backup:", bk)

        # Idle timeout via debug hook (staging only)
        if DEBUG_KEY:
            idle = await idle_timeout(session, token)
            print(">> Idle-timeout write status (expect 401):", idle)

        # Cleanup
        dele = await asyncio.gather(*[delete_deliverable(session, token, i) for i in ids])
        print(">> Deleted OK:", sum(1 for c in dele if c in (200,204)))

if __name__ == "__main__":
    asyncio.run(main())
