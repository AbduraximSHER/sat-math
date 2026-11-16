"""Data shape for one bilingual teacher lesson."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Check:
    """Independent arithmetic check. The displayed answer is not trusted alone."""

    kind: str
    expr: str = ""
    expected: str = ""
    left: str = ""
    right: str = ""
    relation: str = ""
    equation: str = ""
    var: str = "x"
    eq1: str = ""
    eq2: str = ""
    x: str = ""
    y: str = ""
    data: tuple[str, ...] = ()
    stat: str = ""
    shows: tuple[str, ...] = ()
    note: str = ""
    empty: bool = False


def value(expr: str, expected: str, *shows: str) -> Check:
    return Check("value", expr=expr, expected=str(expected), shows=shows)


def eq(left: str, right: str, *shows: str) -> Check:
    return Check("eq", left=left, right=right, shows=shows)


def solve(equation: str, expected: str, *shows: str, var: str = "x") -> Check:
    return Check("solve", equation=equation, expected=expected, shows=shows, var=var)


def system(eq1: str, eq2: str, x: str, y: str) -> Check:
    return Check("system2", eq1=eq1, eq2=eq2, x=str(x), y=str(y))


def nosol(eq1: str, eq2: str) -> Check:
    return Check("system2", eq1=eq1, eq2=eq2, empty=True)


def ineq(expr: str, expected: str, relation: str) -> Check:
    return Check("ineq", expr=expr, expected=str(expected), relation=relation)


def order(data: tuple[str, ...] | list[str], shows: tuple[str, ...] | list[str]) -> Check:
    return Check("order", data=tuple(data), shows=tuple(shows))


def stat(kind: str, data: tuple[str, ...] | list[str], expected: str) -> Check:
    return Check("stat", stat=kind, data=tuple(str(d) for d in data), expected=str(expected))


def vertical() -> Check:
    return Check("vertical")


def manual(note: str, *shows: str) -> Check:
    return Check("manual", note=note, shows=shows)


def _as_checks(checks: Check | tuple[Check, ...] | list[Check]) -> tuple[Check, ...]:
    if isinstance(checks, Check):
        return (checks,)
    return tuple(checks)


@dataclass(frozen=True)
class Example:
    kind: str  # foundation or sat
    prompt_en: str
    prompt_uz: str
    steps: tuple[tuple[str, str], ...]
    answer: str
    checks: tuple[Check, ...]
    choices: tuple[tuple[str, str, str], ...] = ()
    gloss: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "steps", tuple(self.steps))
        object.__setattr__(self, "checks", _as_checks(self.checks))
        object.__setattr__(self, "choices", tuple(self.choices))


@dataclass(frozen=True)
class Practice:
    prompt_en: str
    prompt_uz: str
    answer: str
    solution_en: str
    solution_uz: str
    checks: tuple[Check, ...]
    gloss: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", _as_checks(self.checks))


@dataclass(frozen=True)
class Mistake:
    en: str
    uz: str


@dataclass(frozen=True)
class Lesson:
    code: str
    title_en: str
    title_uz: str
    goal_en: str
    goal_uz: str
    prereq_en: str
    prereq_uz: str
    teacher_en: tuple[str, ...]
    teacher_uz: tuple[str, ...]
    explain_en: tuple[str, ...]
    explain_uz: tuple[str, ...]
    examples: tuple[Example, ...]
    mistakes: tuple[Mistake, ...]
    practice: tuple[Practice, ...]
    figure: str = ""
    figure_caption_en: str = ""
    figure_caption_uz: str = ""
    figure_width_cm: float = 15.2
    extras: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "teacher_en",
            "teacher_uz",
            "explain_en",
            "explain_uz",
            "examples",
            "mistakes",
            "practice",
            "extras",
        ):
            object.__setattr__(self, name, tuple(getattr(self, name)))


@dataclass(frozen=True)
class Unit:
    code: str
    title_en: str
    title_uz: str
    intro_en: tuple[str, ...]
    intro_uz: tuple[str, ...]
    lessons: tuple[Lesson, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "intro_en", tuple(self.intro_en))
        object.__setattr__(self, "intro_uz", tuple(self.intro_uz))
        object.__setattr__(self, "lessons", tuple(self.lessons))


@dataclass(frozen=True)
class MiniItem:
    number: int
    domain: str
    prompt_en: str
    prompt_uz: str
    answer: str
    analysis_en: str
    analysis_uz: str
    checks: tuple[Check, ...]
    choices: tuple[tuple[str, str, str], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", _as_checks(self.checks))
        object.__setattr__(self, "choices", tuple(self.choices))


@dataclass(frozen=True)
class Prose:
    kind: str
    text: str = ""
    text_uz: str = ""
    items: tuple[tuple[str, str], ...] = ()
    headers: tuple[str, ...] = ()
    rows: tuple[tuple[str, ...], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        object.__setattr__(self, "headers", tuple(self.headers))
        object.__setattr__(self, "rows", tuple(self.rows))
