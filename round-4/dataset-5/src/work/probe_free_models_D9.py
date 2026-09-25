import sys, os, json, time, asyncio, httpx
sys.path.insert(0, 'src'); import common, gloss
P = gloss.load_prompt()
pairs = [("Attends(x, conference)", "x attends the conference"), ("Bufaz(x, python)", "x is written in Python"),
         ("Food(x)", "x is not food"), ("CanGetRhythmsRight(x)", "x is an employee in James's town"),
         ("HasBody(x, wooden)", "x has a wooden body"), ("Heavy(x)", "x is heavy and x has a flat surface")]
msgs = gloss.build_messages(P, "If a chef is cool and attends the conference, then the chef can get the rhythms right.", pairs)
async def one(c, m):
    t = time.time()
    r = await c.post(os.environ["OPENROUTER_BASE_URL"].rstrip("/") + "/chat/completions", headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                     json={"model": m, "messages": msgs, "temperature": 0, "max_tokens": 1500, "usage": {"include": True}})
    d = r.json()
    try:
        txt = d["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        txt = None
    print(m, r.status_code, f"{time.time()-t:.1f}s", repr(txt)[:200] if txt else str(d)[:300], (d.get("usage") or {}).get("cost"), (d.get("usage") or {}).get("completion_tokens"))
async def main():
    async with httpx.AsyncClient(timeout=300) as c:
        await asyncio.gather(*[one(c, m) for m in sys.argv[1:]])
asyncio.run(main())
