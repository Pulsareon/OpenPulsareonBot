
import json
import os

account_files = [
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-ferryarlene2791990@gmail.com-sturdy-chimera-486321-n3.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-gorczanydonna28121996@gmail.com-rosy-slate-486321-d2.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-johnspauline3111993@gmail.com-fabled-mystery-486321-n0.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-mayerdebra2331992@gmail.com-totemic-gravity-486322-t2.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-naderviolet30111990@gmail.com-powerful-anchor-486321-e2.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-sauerbryant18111999@gmail.com-trim-bot-486322-e3.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-stantonkristen1062003@gmail.com-qualified-acre-486322-s3.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-stiedemannblake431995@gmail.com-axial-canto-486322-f9.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-uptonalice611991@gmail.com-dogwood-site-486321-e9.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\gemini-wehnerroman26121996@gmail.com-red-bruin-486322-r1.json",
    "E:\\PulsareonThinker\\data\\secrets\\api_credentials\\AuthenticationFiles\\okonsean31101991@gmail.com-pulsareonthinker1.json"
]

all_profiles = {}
found_files_locations = []

for file_path in account_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            account_data = json.load(f)

        email = account_data.get('email')
        if not email:
            print(f"Skipping {file_path}: 'email' field not found.")
            continue

        token_info = account_data.get('token', {})
        expiry_date = token_info.pop('expiry', None) # Extract and remove 'expiry'

        # Create a new structure for the profile
        profile_entry = {
            "type": "google",
            "email": email,
            "data": {
                "token": token_info
            }
        }
        if expiry_date:
            profile_entry["data"]["expiry_date"] = expiry_date

        profile_name = email.split('@')[0] # Use the part before @ as a simple profile name
        all_profiles[profile_name] = profile_entry
        found_files_locations.append(file_path)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred with file {file_path}: {e}")

output_json_snippet = json.dumps({"google": all_profiles}, indent=2)

print("JSON Snippet for auth.profiles:")
print(output_json_snippet)
print("\nFile Locations:")
for loc in found_files_locations:
    print(loc)

print("[WORKER_COMPLETE]")
