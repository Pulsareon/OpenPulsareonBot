#!/usr/bin/env python3
"""
Embedding Proxy Server
Provides OpenAI-compatible /v1/embeddings endpoint using NVIDIA NIM embedding API.
Runs on port 8318 to complement CLI Proxy API on 8317.
"""

import json
import time
import asyncio
from aiohttp import web, ClientSession, ClientTimeout

# NVIDIA embedding config
NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"
NVIDIA_EMBEDDING_MODEL = "nvidia/nv-embedqa-e5-v5"  # Good general-purpose embedding model

# NVIDIA API Keys (from cli-proxy config)
NVIDIA_API_KEYS = [
    "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",
    "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"
]

key_index = 0

def get_next_key() -> str:
    global key_index
    key = NVIDIA_API_KEYS[key_index % len(NVIDIA_API_KEYS)]
    key_index += 1
    return key

async def get_nvidia_embedding(session: ClientSession, texts: list[str], api_key: str) -> list[list[float]]:
    """Call NVIDIA NIM embedding API."""
    url = f"{NVIDIA_API_BASE}/embeddings"
    
    payload = {
        "input": texts,
        "model": NVIDIA_EMBEDDING_MODEL,
        "input_type": "query",  # or "passage" for documents
        "encoding_format": "float",
        "truncate": "END"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    async with session.post(
        url,
        json=payload,
        headers=headers,
        timeout=ClientTimeout(total=60)
    ) as resp:
        if resp.status != 200:
            error_text = await resp.text()
            raise Exception(f"NVIDIA API error {resp.status}: {error_text}")
        
        data = await resp.json()
        # Extract embeddings in order
        return [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]

async def handle_embeddings(request: web.Request) -> web.Response:
    """Handle /v1/embeddings requests (OpenAI-compatible)."""
    try:
        body = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON"}, status=400)
    
    # Parse input - can be string or list of strings
    input_data = body.get("input", [])
    if isinstance(input_data, str):
        input_data = [input_data]
    
    if not input_data:
        return web.json_response({"error": "No input provided"}, status=400)
    
    model = body.get("model", "text-embedding-3-small")
    
    try:
        api_key = get_next_key()
        async with ClientSession() as session:
            # NVIDIA supports batching - process in chunks of 50
            batch_size = 50
            all_embeddings = []
            
            for i in range(0, len(input_data), batch_size):
                batch = input_data[i:i+batch_size]
                embeddings = await get_nvidia_embedding(session, batch, api_key)
                all_embeddings.extend(embeddings)
                
                # Small delay between batches
                if i + batch_size < len(input_data):
                    await asyncio.sleep(0.1)
        
        response = {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "index": i,
                    "embedding": emb
                }
                for i, emb in enumerate(all_embeddings)
            ],
            "model": model,
            "usage": {
                "prompt_tokens": sum(len(t.split()) for t in input_data),
                "total_tokens": sum(len(t.split()) for t in input_data)
            }
        }
        return web.json_response(response)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return web.json_response({"error": str(e)}, status=500)

async def handle_models(request: web.Request) -> web.Response:
    """Handle /v1/models requests."""
    return web.json_response({
        "object": "list",
        "data": [
            {
                "id": "text-embedding-3-small",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "openclaw-embedding-proxy"
            },
            {
                "id": "text-embedding-3-large", 
                "object": "model",
                "created": int(time.time()),
                "owned_by": "openclaw-embedding-proxy"
            },
            {
                "id": NVIDIA_EMBEDDING_MODEL,
                "object": "model", 
                "created": int(time.time()),
                "owned_by": "nvidia"
            }
        ]
    })

async def handle_health(request: web.Request) -> web.Response:
    """Health check endpoint."""
    return web.json_response({
        "status": "ok",
        "backend": "nvidia",
        "model": NVIDIA_EMBEDDING_MODEL,
        "api_keys": len(NVIDIA_API_KEYS),
        "timestamp": time.time()
    })

def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/v1/embeddings", handle_embeddings)
    app.router.add_get("/v1/models", handle_models)
    app.router.add_get("/health", handle_health)
    app.router.add_get("/", handle_health)
    return app

if __name__ == "__main__":
    print(f"🚀 Embedding Proxy (NVIDIA NIM) starting on http://127.0.0.1:8318")
    print(f"📦 Using model: {NVIDIA_EMBEDDING_MODEL}")
    print(f"🔑 API keys loaded: {len(NVIDIA_API_KEYS)}")
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=8318, print=lambda x: print(f"  {x}"))
