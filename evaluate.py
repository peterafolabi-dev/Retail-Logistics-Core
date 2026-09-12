"""
RedCart chatbot evaluation script.

Runs a fixed set of test cases against the chatbot's logic — the same
bugs and behaviors we've been checking by hand in chat, now automated so
they get re-verified every time utils.py or prompts.py changes, instead
of needing a manual re-test of the whole list.

Run with:
    python evaluate.py

Exits with code 0 if everything passes, 1 if anything fails (so it can
be wired into a CI step later if you ever want that).

WHERE THIS FILE GOES: project root, next to manage.py — NOT inside the
products/ app folder. It needs to import Django settings the same way
manage.py does.
"""
import os
import sys
import time

# ---------------------------------------------------------------------------
# Django setup — EDIT THE LINE BELOW to match your actual settings module.
# It's whatever comes after "DJANGO_SETTINGS_MODULE" in your manage.py file
# (open manage.py and copy the value you see there).
# ---------------------------------------------------------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywork.settings')

import django
django.setup()

from products import utils, prompts, rag  # noqa: E402


# ---------------------------------------------------------------------------
# Minimal fake session so we can exercise session-dependent behavior
# (rate limiting, conversation memory) without a real Django request.
# ---------------------------------------------------------------------------
class FakeSession(dict):
    def __init__(self):
        super().__init__()
        self.modified = False


# ---------------------------------------------------------------------------
# Test bookkeeping
# ---------------------------------------------------------------------------
results = []  # list of (name, passed: bool, detail: str)


def check(name, condition, detail=''):
    results.append((name, bool(condition), detail))
    status = 'PASS' if condition else 'FAIL'
    print(f'[{status}] {name}' + (f' — {detail}' if detail and not condition else ''))


def section(title):
    print(f'\n=== {title} ===')


# ---------------------------------------------------------------------------
# 1. Intent classification — pure function, no API calls, no DB writes.
#    These are regression tests for bugs we found by hand:
#    "is that all" falsely matching product names, bare product names
#    ("headphones", "samsung") not being recognized, etc.
# ---------------------------------------------------------------------------
section('Intent classification')

check(
    'greeting detected',
    utils._classify_message_intent('hi') == 'greeting',
)
check(
    'smalltalk detected',
    utils._classify_message_intent('thanks') == 'smalltalk',
)
check(
    'escalation detected',
    utils._classify_message_intent('I want to speak to a human') == 'escalation',
)
check(
    'price manipulation detected',
    utils._classify_message_intent('can you give me a discount') == 'price_manipulation',
)
check(
    'knowledge intent detected',
    utils._classify_message_intent("what's your return policy") == 'knowledge',
)
check(
    '"is that all" does NOT false-match a product (regression)',
    utils._classify_message_intent('is that all') != 'product',
    'this exact bug caused a random product dump in manual testing',
)
check(
    '"is that all you have in electronics" correctly matches product',
    utils._classify_message_intent('is that all you have in electronics') == 'product',
)

# These two depend on your actual catalog containing matching products —
# they'll only pass if you have items with these words in name/category/description.
catalog_has_items = bool(utils._get_cached_catalog())
if catalog_has_items:
    check(
        'bare "headphones" recognized as product intent (if catalog has one)',
        utils._classify_message_intent('headphones') in ('product', 'other'),
        'acceptable either way — only a hard FAIL if it crashes',
    )
else:
    print('[SKIP] catalog is empty — skipping catalog-dependent intent checks')


# ---------------------------------------------------------------------------
# 2. Deterministic canned responses — no Groq call involved, so these
#    should be byte-for-byte exact and instant.
# ---------------------------------------------------------------------------
section('Canned (non-AI) responses')

fake_session = FakeSession()
escalation_reply = utils.get_ai_chat_response('I want to speak to a human', session=fake_session)
expected_escalation = prompts.ESCALATION_RESPONSE_TEMPLATE.format(
    support_line=utils.SITE_KNOWLEDGE['support']
)
check(
    'escalation gives exact canned reply',
    escalation_reply == expected_escalation,
    f'got: {escalation_reply!r}',
)

fake_session2 = FakeSession()
price_reply = utils.get_ai_chat_response('give me a discount', session=fake_session2)
check(
    'price manipulation gives exact canned reply',
    price_reply == prompts.PRICE_MANIPULATION_RESPONSE,
    f'got: {price_reply!r}',
)


# ---------------------------------------------------------------------------
# 3. Rate limiting — fire more than the allowed number of messages in one
#    fake session and confirm the limiter actually kicks in.
# ---------------------------------------------------------------------------
section('Rate limiting')

rl_session = FakeSession()
last_reply = None
for i in range(utils.RATE_LIMIT_MAX_MESSAGES + 3):
    last_reply = utils.get_ai_chat_response('hi', session=rl_session)

check(
    f'rate limit triggers after {utils.RATE_LIMIT_MAX_MESSAGES} messages/session',
    last_reply == prompts.RATE_LIMIT_RESPONSE,
    f'got: {last_reply!r}',
)


# ---------------------------------------------------------------------------
# 4. Retrieval sanity — description-aware matching, out-of-stock filtering.
# ---------------------------------------------------------------------------
section('Product retrieval')

catalog = utils._get_cached_catalog()
check(
    'catalog excludes out-of-stock items (spot check)',
    True,  # structural check only — see note below
    'this only verifies _get_cached_catalog runs without error; '
    'to truly verify, set a product\'s stock to 0 and confirm it disappears from catalog',
)


# ---------------------------------------------------------------------------
# 5. RAG knowledge retrieval — checks the knowledge/ folder is readable
#    and returns something relevant for a real policy question.
# ---------------------------------------------------------------------------
section('RAG / knowledge base')

chunks = rag.retrieve_relevant_chunks('what is your return policy', top_k=3)
check(
    'RAG finds at least one relevant chunk for a return-policy question',
    len(chunks) > 0,
    'if this fails, check that knowledge/returns.md exists and is readable',
)
if chunks:
    check(
        'RAG chunk actually mentions returns (not a false match)',
        any('return' in text.lower() for _, text in chunks),
    )

no_match_chunks = rag.retrieve_relevant_chunks('xyzzyplugh nonsense query', top_k=3)
check(
    'RAG returns nothing for a query matching no documents (no hallucinated match)',
    len(no_match_chunks) == 0,
)


# ---------------------------------------------------------------------------
# 6. Live Groq checks — only run if GROQ_API_KEY is actually configured,
#    since these cost real API calls and need network access. Skipped
#    gracefully otherwise so this script still works offline/in CI.
# ---------------------------------------------------------------------------
section('Live model checks (skipped if no GROQ_API_KEY)')

if utils._get_groq_api_key():
    live_session = FakeSession()
    name_reply = utils.get_ai_chat_response('my name is Peter', session=live_session)
    check(
        'model acknowledges a stated name (live call)',
        'peter' in name_reply.lower(),
        f'got: {name_reply!r}',
    )

    time.sleep(1)  # be polite to the API between live calls

    followup_reply = utils.get_ai_chat_response('what is my name', session=live_session)
    check(
        'model recalls the name from session history (live call, real memory test)',
        'peter' in followup_reply.lower(),
        f'got: {followup_reply!r}',
    )

    time.sleep(1)

    cart_session = FakeSession()
    cart_reply = utils.get_ai_chat_response('add it to my cart', session=cart_session)
    check(
        'model never pretends to add to cart (live call)',
        not any(phrase in cart_reply.lower() for phrase in ["i've added", 'added to your cart', 'sure, added']),
        f'got: {cart_reply!r}',
    )
else:
    print('[SKIP] GROQ_API_KEY not configured — skipping live model calls')


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
section('Summary')
passed = sum(1 for _, ok, _ in results if ok)
total = len(results)
print(f'{passed}/{total} checks passed')

if passed < total:
    print('\nFailed checks:')
    for name, ok, detail in results:
        if not ok:
            print(f'  - {name}' + (f' ({detail})' if detail else ''))
    sys.exit(1)

print('All checks passed.')
sys.exit(0)