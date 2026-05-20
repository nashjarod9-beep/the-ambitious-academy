import re

transcript_path = r'C:\Users\user\.gemini\antigravity\brain\0d09ad13-fdc9-418b-a56d-115c819b763b\.system_generated\logs\transcript.jsonl'

lines = {}

with open(transcript_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We look for \n or " or \ followed by digits and a colon and space
# Better: unescape JSON first or just match the pattern
import json

for line in content.split('\n'):
    if not line.strip(): continue
    try:
        d = json.loads(line)
    except:
        continue
    
    # recursively search for the "Total Lines: 1176" and the formatted lines
    def search_dict(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and 'Total Lines: 1176' in v:
                    # found the output string
                    for out_line in v.split('\n'):
                        match = re.match(r'^(\d+): (.*)$', out_line)
                        if match:
                            lines[int(match.group(1))] = match.group(2)
                else:
                    search_dict(v)
        elif isinstance(obj, list):
            for item in obj:
                search_dict(item)

    search_dict(d)

if lines:
    sorted_lines = [lines[k] for k in sorted(lines.keys())]
    final_html = '\n'.join(sorted_lines)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Restored {len(sorted_lines)} lines directly to index.html")
else:
    print("Could not find the lines in transcript.")
