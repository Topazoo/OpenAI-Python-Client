from .base import BaseStrEnum

class GPT_4_CHAT_MODELS(BaseStrEnum):
    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_32K = "gpt-4-32k"
    GPT_4_32K_0314 = "gpt-4-32k-0314"

class GPT_3_5_CHAT_MODELS(BaseStrEnum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"

class GPT_3_5_COMPLETION_MODELS(BaseStrEnum):
    TEXT_DAVINCI_003 = "text-davinci-003"
    TEXT_DAVINCI_002 = "text-davinci-002"

class GPT_3_COMPLETION_MODELS(BaseStrEnum):
    TEXT_CURIE_001 = "text-curie-001"
    TEXT_BABBAGE_001 = "text-babbage-001"
    TEXT_ADA_001 = "text-ada-001"
    
class GPT_3_BASE_MODELS(BaseStrEnum):
    DAVINCI = "davinci"
    CURIE = "curie"
    BABBAGE = "babbage"
    ADA = "ada"

class GPT_3_EDIT_MODELS(BaseStrEnum):
    TEXT_DAVINCI_EDIT_001 = "text-davinci-edit-001"
    CODE_DAVINCI_EDIT_001 = "code-davinci-edit-001"

class GPT_3_EMBEDDING_MODELS(BaseStrEnum):
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"
    TEXT_SEARCH_ADA_DOC_001 = "text-search-ada-doc-001"

class WHISPER_TRANSLATION_MODELS(BaseStrEnum):
    WHISPER_1 = "whisper-1"

class GPT_3_CODEX_MODELS(BaseStrEnum):
    CODE_DAVINCI_002 = "code-davinci-002"
    CODE_CUSHMAN_001 = "code-cushman-001"

class MODERATION_MODELS(BaseStrEnum):
    TEXT_MODERATION_LATEST = "text-moderation-latest"
    TEXT_MODERATION_STABLE = "text-moderation-stable"

class CHAT_MODELS(GPT_4_CHAT_MODELS, GPT_3_5_CHAT_MODELS): pass
class COMPLETION_MODELS(GPT_3_5_COMPLETION_MODELS, GPT_3_COMPLETION_MODELS, GPT_3_BASE_MODELS): pass
class EDIT_MODELS(GPT_3_EDIT_MODELS): pass
class EMBEDDING_MODELS(GPT_3_EMBEDDING_MODELS): pass
class TRANSLATION_MODELS(WHISPER_TRANSLATION_MODELS): pass
class FINE_TUNING_MODELS(GPT_3_BASE_MODELS): pass
class CODEX_MODELS(GPT_3_CODEX_MODELS): pass

class MODELS(CHAT_MODELS, COMPLETION_MODELS, EDIT_MODELS, TRANSLATION_MODELS, EMBEDDING_MODELS, CODEX_MODELS, MODERATION_MODELS): pass
