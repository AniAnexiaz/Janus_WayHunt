import json
import os
import requests

from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import SUBPATHS


def generate_llm_analysis(findings, llm_config, run_dir: str):

    if not llm_config:
        return

    prompt = build_prompt(findings)

    if llm_config.get("url"):

        response = call_local_llm(
            llm_config["url"],
            prompt
        )

    elif llm_config.get("api_key"):

        response = call_api_llm(
            llm_config["api_key"],
            llm_config.get("model"),
            prompt
        )

    else:
        return

    path = os.path.join(run_dir, SUBPATHS["llm_analysis"])
    ensure_directory(os.path.dirname(path))

    with open(path, "w", encoding="utf-8") as f:
        f.write(response)


def build_prompt(findings):

    findings_json = json.dumps(findings[:50], indent=2)

    return f"""
Analyze the following historical security exposures.

Provide:

1 severity assessment
2 exploit scenarios
3 remediation recommendations
4 prioritized vulnerabilities

Findings:
{findings_json}
"""


def call_local_llm(endpoint, prompt):

    try:

        r = requests.post(
            endpoint,
            json={"prompt": prompt},
            timeout=60
        )

        if r.status_code == 200:

            data = r.json()

            return data.get("response", "")

    except Exception:
        pass

    return "LLM analysis failed."


def call_api_llm(api_key, model, prompt):

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model or "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        r = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if r.status_code == 200:

            data = r.json()

            return data["choices"][0]["message"]["content"]

    except Exception:
        pass

    return "LLM analysis failed."
