import json
import re

config_path = r"C:\Users\Administrator\.openclaw\openclaw.json"

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'models' in data and 'providers' in data['models']:
        providers = data['models']['providers']
        if 'cli-proxy' in providers:
            models = providers['cli-proxy'].get('models', [])
            
            # Filter out embedding models
            # Criteria: id contains "embed", "retriever", "bge", "nemo" (careful with nemo), "clip", "ranking", "reward"
            # And specific known non-chat models
            
            new_models = []
            removed = []
            
            for m in models:
                mid = m.get('id', '').lower()
                # Keywords that strongly suggest embedding/utility models, not chat
                if any(x in mid for x in ['embed', 'retriever', 'bge', 'clip', 'reward', 'rerank', 'ranking', 'guard']):
                    removed.append(mid)
                # Specific check for nemo-minitron if it's base
                elif 'base' in mid and 'instruct' not in mid: # Base models usually bad for chat
                    removed.append(mid)
                else:
                    new_models.append(m)
            
            providers['cli-proxy']['models'] = new_models
            print(f"Removed {len(removed)} embedding/utility models from cli-proxy config.")
            for r in removed[:5]:
                print(f" - {r}")
            if len(removed) > 5:
                print(f" ... and {len(removed)-5} more")

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print("Successfully updated openclaw.json")

except Exception as e:
    print(f"Error: {e}")
