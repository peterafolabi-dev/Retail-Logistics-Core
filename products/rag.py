"""
Lightweight Retrieval-Augmented Generation (RAG) for RedCart.

This is deliberately NOT a vector database with embeddings. At the scale
of a handful of policy documents, keyword-scored retrieval is faster,
free (no embeddings API calls), and just as accurate as semantic search —
vector search earns its cost at hundreds/thousands of documents, not five
or six markdown files.

The interface (retrieve_relevant_chunks) is kept small and self-contained
on purpose: if this ever needs to become a real vector-DB pipeline later,
only this file changes — nothing in utils.py or prompts.py needs to know
the difference.

Add documents by dropping .md or .txt files into the knowledge/ folder
next to this file. No code changes needed to pick up new files.
"""
import os
import re
import time
import logging

from django.conf import settings

logger = logging.getLogger(__name__)

_CHUNK_CACHE = None
_CHUNK_CACHE_TIME = 0
CHUNK_CACHE_TTL = 300  # 5 minutes — matches the product catalog cache in utils.py

_STOPWORDS = {
    'the', 'a', 'an', 'is', 'are', 'do', 'does', 'you', 'your', 'i', 'me', 'my',
    'have', 'has', 'want', 'need', 'for', 'of', 'to', 'in', 'on', 'with', 'and',
    'or', 'what', 'which', 'show', 'find', 'looking', 'please', 'can', 'could',
    'all', 'any', 'some', 'yes', 'no', 'not', 'that', 'this', 'these', 'those',
    'was', 'were', 'been', 'will', 'would', 'should', 'about', 'just', 'only',
    'more', 'most', 'than', 'then', 'there', 'here', 'how', 'why', 'it', 'its',
    'am', 'be', 'so', 'if', 'but', 'as', 'at', 'by', 'we', 'us', 'ok', 'okay',
}


def _knowledge_dir():
    """
    Directory containing knowledge base documents. Configurable via
    settings.KNOWLEDGE_BASE_DIR; defaults to a 'knowledge' folder placed
    next to this file.
    """
    configured = getattr(settings, 'KNOWLEDGE_BASE_DIR', None)
    if configured:
        return configured
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'knowledge')


def _tokenize(text):
    return {w for w in re.findall(r'[a-z0-9]+', text.lower()) if w not in _STOPWORDS and len(w) >= 3}


def _chunk_text(text, max_chunk_chars=600):
    """
    Split a document into paragraph-sized chunks. Keeps related sentences
    together (better retrieval quality) without chunks growing so large
    that irrelevant parts of a long document get dragged into the prompt.
    """
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    chunks = []
    current = ''
    for para in paragraphs:
        if len(current) + len(para) > max_chunk_chars and current:
            chunks.append(current.strip())
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current:
        chunks.append(current.strip())
    return chunks


def _load_and_chunk_documents():
    """Read every .md/.txt file in the knowledge directory and chunk it."""
    directory = _knowledge_dir()
    chunks = []  # list of dicts: {'source': filename, 'text': chunk, 'tokens': set}

    if not os.path.isdir(directory):
        logger.warning('Knowledge base directory not found: %s', directory)
        return chunks

    for filename in sorted(os.listdir(directory)):
        if not filename.lower().endswith(('.md', '.txt')):
            continue
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except OSError as exc:
            logger.error('Could not read knowledge file %s: %s', filepath, exc)
            continue

        source_name = os.path.splitext(filename)[0].replace('-', ' ').replace('_', ' ').title()
        for chunk in _chunk_text(content):
            chunks.append({
                'source': source_name,
                'text': chunk,
                'tokens': _tokenize(chunk),
            })

    return chunks


def _get_cached_chunks():
    global _CHUNK_CACHE, _CHUNK_CACHE_TIME
    now = time.time()
    if _CHUNK_CACHE is not None and (now - _CHUNK_CACHE_TIME) < CHUNK_CACHE_TTL:
        return _CHUNK_CACHE

    _CHUNK_CACHE = _load_and_chunk_documents()
    _CHUNK_CACHE_TIME = now
    return _CHUNK_CACHE


def retrieve_relevant_chunks(query, top_k=3, min_overlap=1):
    """
    Return the top_k most relevant (source, chunk_text) tuples for the
    given query, based on keyword token overlap.

    Returns an empty list if nothing meets min_overlap — callers should
    treat that as "no relevant documents found" and say so honestly
    rather than guessing (see prompts.rag_prompt).
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    chunks = _get_cached_chunks()
    scored = []
    for chunk in chunks:
        overlap = len(query_tokens & chunk['tokens'])
        if overlap >= min_overlap:
            scored.append((overlap, chunk['source'], chunk['text']))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [(source, text) for _, source, text in scored[:top_k]]


def reload_knowledge_base():
    """Force a re-read of the knowledge directory on the next retrieval call.
    Call this after editing/adding documents if you don't want to wait for
    the cache TTL to expire."""
    global _CHUNK_CACHE, _CHUNK_CACHE_TIME
    _CHUNK_CACHE = None
    _CHUNK_CACHE_TIME = 0