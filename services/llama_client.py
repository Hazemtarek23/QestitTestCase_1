import os
import logging
import requests
from typing import Dict
from services.ports import TextGenerator


class LlamaClient(TextGenerator):
    """Local llama.cpp server client (OpenAI-compatible chat API)."""

    def __init__(self, model_name: str = None):
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.base_url = os.getenv("LLAMA_SERVER_BASE_URL", "http://127.0.0.1:8080").rstrip('/')
        self.api_key = os.getenv("LLAMA_API_KEY", "")
        self.verify_ssl = os.getenv("LLAMA_VERIFY_SSL", "true").lower() not in ("0", "false", "no")
        self.model_name = model_name or os.getenv("LLAMA_MODEL", "unsloth.Q4_K_M.gguf")

        # Endpoint
        self.chat_url = f"{self.base_url}/v1/chat/completions"

        self.logger.info("✅ Llama client initialized")
        self.logger.info(f"✅ Base URL: {self.base_url}")
        self.logger.info(f"✅ Model: {self.model_name}")

    async def generate_text(self, system_prompt: str, user_prompt: str, max_length: int = 1024) -> str:
        try:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "top_p": 0.8,
                "max_tokens": max(1, min(int(max_length), 4096)),
                "n_predict": max(1, min(int(max_length), 4096)),
                "stream": False
            }

            try:
                response = requests.post(
                    self.chat_url,
                    headers=headers,
                    json=payload,
                    timeout=120,
                    verify=self.verify_ssl
                )
            except requests.exceptions.ReadTimeout:
                self.logger.warning("Read timeout from llama server, retrying once with extended timeout...")
                response = requests.post(
                    self.chat_url,
                    headers=headers,
                    json=payload,
                    timeout=180,
                    verify=self.verify_ssl
                )

            if response.status_code == 200:
                data = response.json()
                if data.get("choices"):
                    return (data["choices"][0]["message"]["content"] or "").strip()
                raise Exception("No choices in llama server response")
            raise Exception(f"Llama server error {response.status_code}: {response.text}")
        except Exception as e:
            self.logger.error(f"Llama generation failed: {e}")
            return ""

    def get_model_info(self) -> Dict[str, str]:
        return {
            "provider": "Local Llama Server",
            "endpoint": self.base_url,
            "model_name": self.model_name,
            "deployment_url": self.chat_url,
        }

    def test_connection(self) -> bool:
        try:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5,
                "n_predict": 5,
            }
            r = requests.post(self.chat_url, headers=headers, json=payload, timeout=10, verify=self.verify_ssl)
            return r.status_code == 200
        except Exception:
            return False

