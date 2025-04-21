from dataclasses import dataclass

@dataclass
class ContextInfo:
    name: str
    cluster: str
    user: str
    current: bool
