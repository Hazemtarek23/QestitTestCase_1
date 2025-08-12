from typing import Protocol, Dict, Any


class TextGenerator(Protocol):
    async def generate_text(self, system_prompt: str, user_prompt: str, max_length: int = 1024) -> str:
        ...

    def get_model_info(self) -> Dict[str, Any]:
        ...


