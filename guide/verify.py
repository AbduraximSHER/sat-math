"""Recompute every keyed answer. The prose is not the source of truth."""

from __future__ import annotations

import re

import sympy as sp

from guide.model import Check, Lesson, MiniItem, Unit

SYMPY_LOCALS = {
    "sqrt": sp.sqrt,
    "log": sp.log,
    "pi": sp.pi,
    "Rational": sp.Rational,
    "Abs": sp.Abs,
}


def sym(expr: str):
    return sp.simplify(sp.sympify(expr, locals=SYMPY_LOCALS))


def normalize(text: str) -> str:
    return (
        text.replace("\u2212", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2264", "<=")
        .replace("\u2265", ">=")
        .replace("\u00d7", "*")
        .replace("\u00f7", "/")
    )


def number_forms(expected: str) -> list[str]:
    value = sym(expected)
    if not value.is_rational:
        raise ValueError(f"not a rational value: {expected}")
    num, den = sp.fraction(sp.together(value))
    num = int(num)
    den = int(den)
    if den < 0:
        num, den = -num, -den
    forms = [str(num) if den == 1 else f"{num}/{den}"]
    den2 = den
    while den2 % 2 == 0:
        den2 //= 2
    while den2 % 5 == 0:
        den2 //= 5
    if den2 == 1 and den != 1:
        sign = "-" if num < 0 else ""
        n = abs(num)
        # exact decimal from integer division
        scale = 1
        d = den
        while d % 2 == 0:
            d //= 2
            scale *= 10
        while d % 5 == 0:
            d //= 5
            scale *= 10
        # n/den = (n * scale/den) / scale, but scale/den may not be int if we counted wrong
        scaled = n * scale // den
        digits = str(scaled).zfill(len(str(scale)) - 1)
        # place the decimal point `len(str(scale))-1` from the right? scale is 10**k
        k = 0
        s = scale
        while s > 1:
            s //= 10
            k += 1
        digits = str(n * (10**k) // den).zfill(k + 1)
        whole, frac = digits[:-k], digits[-k:]
        if k == 0:
            dec = whole
        else:
            dec = f"{whole}.{frac}".rstrip("0").rstrip(".")
        forms.append(sign + dec)
    return forms


def contains_number(answer: str, form: str) -> bool:
    text = normalize(answer)
    token = normalize(form)
    if "/" in token:
        pattern = r"(?<![0-9/])" + re.escape(token) + r"(?![0-9/])"
    else:
        pattern = r"(?<![0-9./-])" + re.escape(token) + r"(?![0-9/])"
    return re.search(pattern, text) is not None


def answer_has_value(answer: str, expected: str) -> bool:
    return any(contains_number(answer, form) for form in number_forms(expected))


def _require_shows(answer: str, check: Check, errors: list[str], where: str) -> None:
    for snippet in check.shows:
        if snippet not in answer:
            errors.append(f"{where}: answer does not show {snippet!r}")


def checked_solutions(equation: str, var: str) -> sp.FiniteSet:
    symbol = sp.symbols(var, real=True)
    local = dict(SYMPY_LOCALS)
    local[var] = symbol
    expr = sp.sympify(equation, locals=local)
    good = []
    for candidate in sp.solve(expr, symbol):
        if not getattr(candidate, "is_real", False):
            continue
        plugged = sp.simplify(expr.subs(symbol, candidate))
        if plugged == 0 or (getattr(plugged, "is_number", False) and abs(complex(plugged)) < 1e-8):
            good.append(sp.simplify(candidate))
    return sp.FiniteSet(*good)


def _parse_solution_list(expected: str) -> sp.FiniteSet:
    if expected.strip() == "NONE":
        return sp.FiniteSet()
    parts = [sym(part) for part in expected.split(",")]
    return sp.FiniteSet(*parts)


def _statistic(kind: str, data: tuple[str, ...]):
    values = [sym(item) for item in data]
    if kind == "mean":
        return sp.simplify(sum(values) / len(values))
    if kind == "median":
        ordered = sorted(values, key=lambda item: float(item))
        n = len(ordered)
        if n % 2 == 1:
            return ordered[n // 2]
        return sp.simplify((ordered[n // 2 - 1] + ordered[n // 2]) / 2)
    if kind == "range":
        return sp.simplify(max(values) - min(values))
    if kind == "mode":
        counts: dict = {}
        for item in values:
            counts[item] = counts.get(item, 0) + 1
        top = max(counts.values())
        winners = [item for item, count in counts.items() if count == top]
        if len(winners) != 1 or top < 2:
            raise ValueError(f"data has no unique mode: {data}")
        return winners[0]
    raise ValueError(kind)


def check_item(answer: str, checks: tuple[Check, ...], where: str, errors: list[str]) -> None:
    if not checks:
        errors.append(f"{where}: missing check")
        return
    for check in checks:
        try:
            _one(answer, check, where, errors)
        except Exception as exc:  # noqa: BLE001 — surface the item, then keep going
            errors.append(f"{where}: checker crashed ({check.kind}): {exc}")


def _one(answer: str, check: Check, where: str, errors: list[str]) -> None:
    if check.kind == "value":
        got = sym(check.expr)
        expected = sym(check.expected)
        if sp.simplify(got - expected) != 0:
            errors.append(f"{where}: {check.expr} = {got}, expected {expected}")
        if not answer_has_value(answer, check.expected):
            errors.append(
                f"{where}: answer {answer!r} does not contain {number_forms(check.expected)}"
            )
        _require_shows(answer, check, errors, where)
        return

    if check.kind == "eq":
        if not check.shows:
            errors.append(f"{where}: eq check needs a shown form")
        difference = sym(f"({check.left}) - ({check.right})")
        if difference != 0:
            errors.append(f"{where}: {check.left} is not equal to {check.right}")
        _require_shows(answer, check, errors, where)
        return

    if check.kind == "solve":
        got = checked_solutions(check.equation, check.var)
        expected = _parse_solution_list(check.expected)
        if got != expected:
            errors.append(f"{where}: solutions {got} != {expected}")
        if expected == sp.FiniteSet():
            if "no solution" not in answer.lower():
                errors.append(f"{where}: empty solution set not named in the answer")
        else:
            for part in expected.args:
                if part.is_rational:
                    if not answer_has_value(answer, str(part)):
                        errors.append(f"{where}: answer missing solution {part}")
                elif not check.shows:
                    errors.append(f"{where}: non-rational solution {part} needs shows")
        _require_shows(answer, check, errors, where)
        return

    if check.kind == "system2":
        x, y = sp.symbols("x y", real=True)
        local = dict(SYMPY_LOCALS)
        local["x"] = x
        local["y"] = y
        equations = [
            sp.sympify(check.eq1, locals=local),
            sp.sympify(check.eq2, locals=local),
        ]
        solutions = sp.solve(equations, [x, y], dict=True)
        unique = [
            sol
            for sol in solutions
            if sol.get(x) is not None
            and sol.get(y) is not None
            and sol[x].free_symbols == set()
            and sol[y].free_symbols == set()
        ]
        if check.empty:
            if unique:
                errors.append(f"{where}: expected no solution, got {unique}")
            lowered = answer.lower()
            if "no solution" not in lowered or "yechim yo'q" not in lowered:
                errors.append(f"{where}: no-solution answer must say it in both languages")
            return
        if len(unique) != 1:
            errors.append(f"{where}: expected one solution, got {solutions}")
            return
        got_x = sp.simplify(unique[0][x])
        got_y = sp.simplify(unique[0][y])
        if got_x != sym(check.x) or got_y != sym(check.y):
            errors.append(f"{where}: system gave {(got_x, got_y)} != {(check.x, check.y)}")
        if not answer_has_value(answer, check.x) or not answer_has_value(answer, check.y):
            errors.append(f"{where}: answer {answer!r} missing x or y")
        _require_shows(answer, check, errors, where)
        return

    if check.kind == "ineq":
        if sym(check.expr) != sym(check.expected):
            errors.append(f"{where}: boundary {check.expr} != {check.expected}")
        if normalize(check.relation) not in normalize(answer):
            errors.append(f"{where}: answer missing relation {check.relation!r}")
        _require_shows(answer, check, errors, where)
        return

    if check.kind == "order":
        values = [sym(item) for item in check.data]
        for left, right in zip(values, values[1:]):
            if not left < right:
                errors.append(f"{where}: order is not strict: {check.data}")
                break
        cursor = 0
        raw = answer
        for snippet in check.shows:
            found = raw.find(snippet, cursor)
            if found < 0:
                errors.append(f"{where}: {snippet!r} is out of order or missing")
                break
            cursor = found + len(snippet)
        return

    if check.kind == "stat":
        got = _statistic(check.stat, check.data)
        if sp.simplify(got - sym(check.expected)) != 0:
            errors.append(f"{where}: {check.stat} is {got}, expected {check.expected}")
        if not answer_has_value(answer, check.expected):
            errors.append(f"{where}: answer missing statistic {check.expected}")
        _require_shows(answer, check, errors, where)
        return

    if check.kind == "vertical":
        lowered = answer.lower()
        if "undefined" not in lowered or "qiyalik yo'q" not in lowered:
            errors.append(f"{where}: vertical slope must be named in both languages")
        return

    if check.kind == "manual":
        if len(check.note.strip()) < 80:
            errors.append(f"{where}: manual note is too thin")
        _require_shows(answer, check, errors, where)
        return

    errors.append(f"{where}: unknown check kind {check.kind}")


def _joined(parts: tuple[str, ...]) -> str:
    return "\n\n".join(parts).strip()


def _lesson_shape(lesson: Lesson, errors: list[str]) -> None:
    where = f"lesson {lesson.code}"
    if len(lesson.examples) < 2:
        errors.append(f"{where}: need at least 2 examples")
    if len(lesson.mistakes) < 3:
        errors.append(f"{where}: need at least 3 mistakes")
    if len(lesson.practice) < 5:
        errors.append(f"{where}: need at least 5 practice items")
    kinds = {example.kind for example in lesson.examples}
    if not {"foundation", "sat"}.issubset(kinds):
        errors.append(f"{where}: examples must include foundation and sat")
    for label, text in (
        ("goal_en", lesson.goal_en),
        ("goal_uz", lesson.goal_uz),
    ):
        if len(text.strip()) < 80:
            errors.append(f"{where}: {label} is short")
    if len(lesson.prereq_en.strip()) < 40 or len(lesson.prereq_uz.strip()) < 40:
        errors.append(f"{where}: prerequisites are short")
    if len(_joined(lesson.teacher_en)) < 280 or len(_joined(lesson.teacher_uz)) < 280:
        errors.append(f"{where}: teacher path is short")
    explain_en = _joined(lesson.explain_en)
    explain_uz = _joined(lesson.explain_uz)
    if len(explain_en) < 1500 or len(explain_uz) < 1500:
        errors.append(
            f"{where}: explanation is short (en {len(explain_en)}, uz {len(explain_uz)})"
        )
    ratio = len(explain_uz) / max(len(explain_en), 1)
    if not 0.6 <= ratio <= 1.65:
        errors.append(f"{where}: Uzbek/English length ratio is {ratio:.2f}")
    if lesson.figure and (not lesson.figure_caption_en or not lesson.figure_caption_uz):
        errors.append(f"{where}: figure needs two captions")
    for index, example in enumerate(lesson.examples, start=1):
        item = f"{where} example {index}"
        if len(example.steps) < 3:
            errors.append(f"{item}: need at least 3 steps")
        for step_en, step_uz in example.steps:
            if len(step_en.strip()) < 22 or len(step_uz.strip()) < 22:
                errors.append(f"{item}: a step is too short")
        if len(example.prompt_en) < 12 or len(example.prompt_uz) < 12:
            errors.append(f"{item}: prompt is short")
        check_item(example.answer, example.checks, item, errors)
    for index, mistake in enumerate(lesson.mistakes, start=1):
        if len(mistake.en) < 50 or len(mistake.uz) < 50:
            errors.append(f"{where} mistake {index} is short")
    for index, practice in enumerate(lesson.practice, start=1):
        item = f"{where} practice {index}"
        if len(practice.prompt_en) < 12 or len(practice.prompt_uz) < 12:
            errors.append(f"{item}: prompt is short")
        if len(practice.solution_en) < 32 or len(practice.solution_uz) < 32:
            errors.append(f"{item}: solution is short")
        check_item(practice.answer, practice.checks, item, errors)


def verify_book(units: tuple[Unit, ...], mini: tuple[MiniItem, ...]) -> list[str]:
    errors: list[str] = []
    lessons = [lesson for unit in units for lesson in unit.lessons]
    codes = [lesson.code for lesson in lessons]
    if len(lessons) != 44:
        errors.append(f"expected 44 lessons, found {len(lessons)}")
    if len(codes) != len(set(codes)):
        errors.append(f"duplicate lesson codes: {codes}")
    expected_codes = (
        ["0.1"]
        + [f"1.{i}" for i in range(1, 11)]
        + [f"2.{i}" for i in range(1, 9)]
        + [f"3.{i}" for i in range(1, 9)]
        + [f"4.{i}" for i in range(1, 7)]
        + [f"5.{i}" for i in range(1, 8)]
        + [f"6.{i}" for i in range(1, 5)]
    )
    if codes != expected_codes:
        errors.append(f"lesson order mismatch:\n got {codes}\n want {expected_codes}")
    manuals = 0
    for lesson in lessons:
        _lesson_shape(lesson, errors)
        for example in lesson.examples:
            manuals += sum(1 for check in example.checks if check.kind == "manual")
        for practice in lesson.practice:
            manuals += sum(1 for check in practice.checks if check.kind == "manual")
    if len(mini) != 20:
        errors.append(f"mini-test needs 20 items, found {len(mini)}")
    for item in mini:
        where = f"mini {item.number}"
        if len(item.analysis_en) < 55 or len(item.analysis_uz) < 55:
            errors.append(f"{where}: analysis is short")
        check_item(item.answer, item.checks, where, errors)
        manuals += sum(1 for check in item.checks if check.kind == "manual")
    if manuals > 10:
        errors.append(f"too many manual checks: {manuals}")
    _spot_recompute(lessons, mini, errors)
    return errors


def _find(lessons: list[Lesson], code: str) -> Lesson:
    for lesson in lessons:
        if lesson.code == code:
            return lesson
    raise KeyError(code)


def _spot_recompute(lessons: list[Lesson], mini: tuple[MiniItem, ...], errors: list[str]) -> None:
    """Hand arithmetic written a second way, then matched to the printed answer."""

    def need(code: str, which: str, index: int, hand: str, label: str) -> None:
        lesson = _find(lessons, code)
        pool = lesson.examples if which == "example" else lesson.practice
        answer = pool[index].answer
        if not answer_has_value(answer, hand):
            errors.append(f"spot {label}: answer {answer!r} != recomputed {hand}")

    # 15% of 80 is 12. 25% off $40 leaves 30.
    if sym("80*15/100") != 12:
        errors.append("spot percent arithmetic failed")
    need("1.4", "example", 0, "12", "15 percent of 80")
    if sym("40*3/4") != 30:
        errors.append("spot sale price failed")
    need("1.4", "example", 1, "30", "25 percent off 40")

    # 20% up then 20% down on 100 leaves 96, a 4% loss.
    if sym("100*6/5*4/5") != 96:
        errors.append("spot successive percent failed")
    need("1.5", "example", 1, "96", "successive percent level")

    # (x/2) + (x/4) = 9 → x = 12
    if sym("9 / (1/2 + 1/4)") != 12:
        errors.append("spot fraction equation failed")
    need("2.3", "example", 1, "12", "fraction equation")

    # 2x + 3y = 12 and x - y = 1 → (3, 2)
    x, y = sp.symbols("x y")
    solved = sp.solve([2 * x + 3 * y - 12, x - y - 1], [x, y], dict=True)[0]
    if solved[x] != 3 or solved[y] != 2:
        errors.append("spot system failed")
    answer = _find(lessons, "2.7").examples[1].answer
    if not (answer_has_value(answer, "3") and answer_has_value(answer, "2")):
        errors.append(f"spot system answer {answer!r}")

    # y = x**2 - 4x + 3 at x = 2 is -1. Roots 1 and 3.
    if sym("2**2 - 4*2 + 3") != -1:
        errors.append("spot vertex failed")
    vertex_answer = _find(lessons, "3.4").examples[0].answer
    if not answer_has_value(vertex_answer, "-1"):
        errors.append(f"spot vertex answer {vertex_answer!r}")

    # 3-4-5 sine is 3/5. Ramp tan is 3/4.
    if sym("3/5") != sp.Rational(3, 5):
        errors.append("spot sine failed")
    need("5.4", "example", 0, "3/5", "sine")
    need("5.4", "example", 1, "3/4", "tangent")

    # Quarter circle r = 6 has area 9π. Checked as an equality show in the lesson.
    sector = _find(lessons, "5.7").examples[1].answer
    if "9π" not in sector:
        errors.append(f"spot sector answer {sector!r}")

    # Extraneous root: sqrt(2x+3) = x rejects -1 and keeps 3.
    radical = sp.sqrt(2 * x + 3) - x
    if sp.simplify(radical.subs(x, 3)) != 0:
        errors.append("spot radical root 3 failed")
    if sp.simplify(radical.subs(x, -1)) == 0:
        errors.append("spot radical root -1 should be extraneous")
    need("3.7", "example", 1, "3", "checked radical root")

    # Mini-test items 2, 8, and 19: 25% of 64, the system, the cylinder.
    by_number = {item.number: item for item in mini}
    if not answer_has_value(by_number[2].answer, str(sym("64/4"))):
        errors.append("spot mini percent")
    if not answer_has_value(by_number[8].answer, "3"):
        errors.append("spot mini system")
    if "48π" not in by_number[19].answer:
        errors.append("spot mini cylinder")


def self_test_matcher() -> None:
    assert contains_number("B. 12", "12")
    assert not contains_number("B. 12", "1")
    assert not contains_number("B. 12", "2")
    assert not contains_number("112", "12")
    assert not contains_number("1/2", "1")
    assert not contains_number("29/12", "12")
    assert contains_number("29/12 (2 5/12)", "29/12")
    assert contains_number("x = \u22121/10", "-1/10")
    assert not contains_number("x = 1/2", "2")
    assert contains_number("25%", "25")
    assert not contains_number("80", "8")
    assert contains_number("x \u2264 2", "2")
    assert number_forms("29/12")[0] == "29/12"
    assert "0.375" in number_forms("3/8")
    assert number_forms("-4") == ["-4"]
    assert sym("(9/4)+(1/6)") == sym("29/12")
