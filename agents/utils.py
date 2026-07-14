import json
import re

def clean_and_parse_json(raw: str) -> dict:
    raw = raw.strip()
    
    # 1. Try to parse directly first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
        
    # 2. Extract content from markdown code blocks (e.g. ```json ... ``` or ``` ... ```)
    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw)
    if code_block_match:
        content = code_block_match.group(1).strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raw = content # Fall back to parsing the extracted content
            
    # 3. Find the first '{' and last '}' to extract just the JSON object
    start = raw.find('{')
    end = raw.rfind('}')
    if start != -1 and end != -1:
        json_str = raw[start:end+1].strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Remove trailing commas before a closing bracket or brace
            fixed_json = re.sub(r',\s*([\]}])', r'\1', json_str)
            try:
                return json.loads(fixed_json)
            except json.JSONDecodeError:
                pass
                
            # If still failing, let's raise the error with the raw text for debugging
            raise json.JSONDecodeError(
                f"JSON decode failed. Raw string: {raw}",
                doc="", pos=0
            )
            
    raise ValueError(f"No JSON object found in response: {raw}")
