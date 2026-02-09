@echo off
:: Embedding Proxy Startup Script
:: Runs the NVIDIA embedding proxy on port 8318

cd /d E:\PulsareonThinker\scripts\services
start /min "EmbeddingProxy" python embedding_proxy.py
