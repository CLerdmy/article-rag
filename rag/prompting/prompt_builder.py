from typing import Optional

from db.dto import Chunk
from rag.prompting.templates import get_template


class PromptBuilder:
    
    def __init__(
        self,
        use_custom: bool = False,
        template_name: str = "default",
        system_prompt: Optional[str] = None,
        context_intro: Optional[str] = None,
        question_prefix: Optional[str] = None,
        answer_instruction: Optional[str] = None,
        include_title: bool = True,
        include_score: bool = True,
        score_precision: int = 3
    ):
        self.use_custom = use_custom
        self.template_name = template_name
        self.system_prompt = system_prompt
        self.context_intro = context_intro
        self.question_prefix = question_prefix
        self.answer_instruction = answer_instruction
        self.include_title = include_title
        self.include_score = include_score
        self.score_precision = score_precision
    
    def build(self, question: str, chunks: list[Chunk], title: Optional[str] = None) -> str:
        context = self._format_context(chunks, title)
        
        if not self.use_custom:
            template = get_template(self.template_name)
            return template.format(question=question, context=context)
        else:
            return self._custom_template(question, context)
    
    def _format_context(self, chunks: list[Chunk], title: Optional[str]) -> str:
        if not chunks:
            return "Нет доступного контекста."
        
        parts = []
        for chunk in chunks:
            meta_parts = []
            
            if self.include_title and title:
                meta_parts.append(f"Источник: {title}")
            
            if self.include_score and chunk.score is not None:
                score_str = f"{chunk.score:.{self.score_precision}f}"
                meta_parts.append(f"Релевантность: {score_str}")
            
            if meta_parts:
                meta = "[" + ", ".join(meta_parts) + "]\n"
            else:
                meta = ""
            
            parts.append(f"{meta}{chunk.text}")
        
        return "\n---\n".join(parts)
    
    def _custom_template(self, question: str, context: str) -> str:
        parts = []
        
        if self.system_prompt:
            parts.append(self.system_prompt)
        
        if self.context_intro:
            parts.append(self.context_intro)
        
        parts.append(context)
        
        if self.question_prefix:
            parts.append(f"{self.question_prefix} {question}")
        else:
            parts.append(f"Вопрос: {question}")
        
        if self.answer_instruction:
            parts.append(self.answer_instruction)
        
        return "\n---\n".join(parts)