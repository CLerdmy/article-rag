DEFAULT = """Ты - ассистент, который отвечает на вопросы, используя только представленный контекст.

Контекст:
{context}

Вопрос:
{question}

Ответ (если информации нет в контексте, честно скажи об этом):"""

TEMPLATES = {
    "default": DEFAULT
}

def get_template(name: str = "default") -> str:
    return TEMPLATES.get(name, DEFAULT)