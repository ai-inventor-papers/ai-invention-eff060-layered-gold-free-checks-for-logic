"""Gloss rule (prereg f + D8), verdict parsing and the async client (HTTP mocked in-test only; no network)."""
import asyncio
import json

import httpx

import gloss
from freelab import gloss_decision

PU = [("A(x)", "x is a"), ("B(x)", "x is b"), ("A(x)", "x is b"), ("B(x)", "x is a")]


def test_gloss_decision_rules():
    maps = [{"reading": "weak", "pair_ids": [0, 1]}, {"reading": "weak", "pair_ids": [2, 3]}]
    yes = {p: ("YES", "YES") for p in PU}
    v = dict(yes)
    v[PU[2]] = ("NO", "NO")
    assert gloss_decision(maps, PU, v) == ("CORRECT", 0)
    v = {PU[0]: ("NO", "NO"), PU[1]: ("YES", "YES"), PU[2]: ("YES", "YES"), PU[3]: ("NO", "NO")}
    assert gloss_decision(maps, PU, v) == ("ERROR_GLOSS", None)
    v = {PU[0]: ("YES", "NO"), PU[1]: ("YES", "YES"), PU[2]: ("NO", "NO"), PU[3]: ("YES", "YES")}
    assert gloss_decision(maps, PU, v)[0] == "UNRESOLVED_GLOSS"
    conv = [{"reading": "weak", "pair_ids": [2, 3]}, {"reading": "converse", "pair_ids": [0, 1]}]
    v = {PU[0]: ("YES", "YES"), PU[1]: ("YES", "YES"), PU[2]: ("NO", "NO"), PU[3]: ("NO", "NO")}
    assert gloss_decision(conv, PU, v) == ("READING_CHOICE", 1)


def test_parse_verdicts():
    assert gloss.parse_verdicts('```json\n{"1": "YES", "2": "no"}\n```', 2) == {1: "YES", 2: "NO"}
    assert gloss.parse_verdicts('{"1": "YES"}', 2) is None
    assert gloss.parse_verdicts(None, 1) is None


def test_rate_pairs_with_mock_transport(tmp_path, monkeypatch):
    monkeypatch.setattr(gloss, "CACHE", tmp_path / "cache.jsonl")
    monkeypatch.setattr(gloss, "LEDGER", tmp_path / "ledger.jsonl")
    monkeypatch.setenv("OPENROUTER_BASE_URL", "http://mock/api/v1")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")

    def handler(req: httpx.Request) -> httpx.Response:
        body = json.loads(req.content)
        n = body["messages"][1]["content"].count("SYMBOL USE:")
        ans = {str(i + 1): ("YES" if i % 2 == 0 else "NO") for i in range(n)}
        return httpx.Response(200, json={"choices": [{"message": {"content": json.dumps(ans)}}],
                                         "usage": {"cost": 0.001, "prompt_tokens": 10, "completion_tokens": 5}})

    async def go():
        c = gloss.Client(phase="test")
        c.http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        try:
            return await gloss.rate_pairs(c, [{"sentence_id": "s1", "sentence": "S.", "pairs": [("A(x)", "x is a"), ("B(x)", "x is b")]}])
        finally:
            await c.close()
    v = asyncio.run(go())
    assert len(v) == 4 and set(v.values()) <= {"YES", "NO"}
    assert len((tmp_path / "ledger.jsonl").read_text().splitlines()) == 2  # one call per checker
    v2 = asyncio.run(go())  # fully cached: no new calls
    assert v2 == v and len((tmp_path / "ledger.jsonl").read_text().splitlines()) == 2
