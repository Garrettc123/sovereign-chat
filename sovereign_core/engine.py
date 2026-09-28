from __future__ import annotations
import math, re
from dataclasses import dataclass, field

MODES = {
    'architect':  ('Architect',  'Here is the strongest architectural solution:'),
    'strategist': ('Strategist', 'Here is the highest-leverage strategic move:'),
    'visionary':  ('Visionary',  'Here is the boldest version of this idea:'),
    'analyst':    ('Analyst',    'Here is the clearest reading of this problem:'),
    'sovereign':  ('Sovereign',  'Full-strength sovereign response:'),
}

BODIES = {
    'architect':  'Design the system in distinct layers with explicit contracts. Every boundary is a module. Every dependency is named.',
    'strategist': 'Turn assets into three-layer income: flagship offer, recurring subscription, internal automation that compounds.',
    'visionary':  'Make the experience feel impossible to ignore. One feature so unusual there is no existing category for it.',
    'analyst':    'Separate verified facts from assumptions. Instrument the strongest system. Convert that into undeniable evidence.',
    'sovereign':  'Pick the strongest system. Prove it works. Deploy it for one real customer at full price. That converts belief into evidence.',
}

NEXT_MOVES = {
    'architect':  'Ship a walking skeleton this week: intake → decision → fulfillment → receipt. No extra modules until that loop closes.',
    'strategist': 'Price one outcome offer, put a live checkout on it, and run 20 conversations toward one paid close.',
    'visionary':  'Name the product in language only this company can use. Lead with the feeling, then prove the mechanism.',
    'analyst':    'Instrument one metric that a customer would pay to move. Publish that number weekly.',
    'sovereign':  'Collapse the portfolio to one flagship. Sell it. Fulfill it same day. Ledger the proof.',
}

MEMORY_RE = [
    r"my name is ([A-Za-z\s']+)",
    r"i(?:'m| am) building ([A-Za-z0-9 ,\-']+)",
    r"i want (?:to )?([A-Za-z0-9 ,\-']+)",
    r"i(?:'ve| have) built ([A-Za-z0-9 ,\-']+)",
    r"my goal (?:is )?([A-Za-z0-9 ,\-']+)",
]

OFFER = {
    'sku': 'contractor-lead-leak-audit',
    'price': 47,
    'url': 'https://buy.stripe.com/dRm8wPbb72pY2Mz8BR43S1D',
    'storefront': 'https://garrettc123.github.io/',
    'line': 'Live SKU: $47 Contractor Lead Leak Audit — 48-hour map of where Texas trades shops lose jobs after the lead hits.',
}


def _detect_mode(text: str, current: str) -> str:
    t = text.lower()
    if re.search(r'sovereign|unprecedented|full.?strength|maximum|no.?limit', t): return 'sovereign'
    if re.search(r'build|code|system|architect|deploy|module|api|function', t): return 'architect'
    if re.search(r'strategy|revenue|business|wealth|sell|market|customer|money|leverage', t): return 'strategist'
    if re.search(r'vision|creative|design|brand|story|imagine|bold', t): return 'visionary'
    if re.search(r'analyz|debug|compare|tradeoff|data|metric|audit', t): return 'analyst'
    return current


def _extract_memories(text: str) -> list[str]:
    out = []
    for pat in MEMORY_RE:
        for m in re.finditer(pat, text, re.I):
            val = m.group(1).strip().rstrip('.!?')
            if len(val) > 3:
                out.append(val)
    return out


def _intensity(text: str) -> int:
    words = len(text.split())
    return min(100, int(30 + math.sqrt(max(words, 1)) * 14))


def _clip(text: str, n: int = 140) -> str:
    t = ' '.join(text.split())
    return t if len(t) <= n else t[: n - 1].rstrip() + '…'


def _synthesize(text: str, mode: str, memories: list[str]) -> str:
    label, lead = MODES[mode]
    body = BODIES[mode]
    nxt = NEXT_MOVES[mode]
    mem_ctx = '; '.join(memories[-2:])
    mem_clause = f' Drawing on context: {mem_ctx}.' if mem_ctx else ''
    asked = _clip(text)
    offer = OFFER['line']
    return (
        f'{lead}{mem_clause}\n\n'
        f'{body}\n\n'
        f'Against what you just asked — “{asked}” — lock the next move: {nxt}\n\n'
        f'{offer}'
    )


@dataclass(slots=True)
class Message:
    role: str
    text: str


@dataclass(slots=True)
class SovereignChatEngine:
    history: list[Message] = field(default_factory=list)
    memories: list[str] = field(default_factory=list)
    mode: str = 'architect'

    def chat(self, text: str) -> dict:
        self.history.append(Message('user', text))
        new_mems = _extract_memories(text)
        for m in new_mems:
            if m not in self.memories:
                self.memories.append(m)
        self.mode = _detect_mode(text, self.mode)
        intensity = _intensity(text)
        label, _lead = MODES[self.mode]
        answer = _synthesize(text, self.mode, self.memories)
        self.history.append(Message('assistant', answer))
        return {
            'mode': self.mode,
            'label': label,
            'intensity': intensity,
            'answer': answer,
            'memories': list(self.memories),
            'offer': dict(OFFER),
        }

    def reset(self) -> None:
        self.history.clear()
        self.memories.clear()
        self.mode = 'architect'
