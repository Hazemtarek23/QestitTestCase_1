from pydantic import BaseModel
from typing import List, Dict

class ExpertStepResult(BaseModel):
    step_id: str
    description: str
    output_key: str
    output_value: str

class ExpertReviewResult(BaseModel):
    run_id: str
    user_input: str
    chunk_data: Dict[str, str]
    step_results: List[ExpertStepResult]
