"""Conservative Pine source evidence recovery; never interprets a strategy."""
import re

MAX_LINES = 400
MAX_ROUNDS = 80
WARNING = '片段未恢复完整控制流，不可顺序执行'


def _masked(code):
    # Keep every newline/column: source offsets remain authoritative.
    pattern = r'/\*[\s\S]*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    return re.sub(pattern, lambda m: re.sub(r'[^\n]', ' ', m.group()), code)


def _statements(lines):
    result = []
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        start = i
        depth = 0
        while i < len(lines):
            text = lines[i]
            depth += sum(text.count(c) for c in '([') - sum(text.count(c) for c in ')]')
            i += 1
            if depth <= 0:
                break
        text = '\n'.join(lines[start:i])
        result.append(dict(start=start, end=i, indent=len(lines[start].expandtabs(4)) - len(lines[start].expandtabs(4).lstrip()), text=text))
    return result


def enrich_rule(base: dict, rule: dict) -> str:
    """Recover literal lines plus ancestor blocks and preceding definitions.

    Whole if/else chains are atomic: a cap never returns a newly orphaned else.
    This lexical closure is evidence, not an executable or complete program.
    """
    original = str(rule.get('code') or '')
    code = str(base.get('code') or '')
    start = base.get('code_start_line')
    language = str(base.get('language') or '').lower()
    if language and language not in ('pine', 'pinescript', 'pine script'):
        return WARNING + '（非 Pine 源码，保留原片段）。\n' + original
    if not re.search(r'//@version\s*=|\bstrategy\s*\(|\bstudy\s*\(|\bindicator\s*\(', code):
        return WARNING + '（无法确认 Pine 语法，保留原片段）。\n' + original
    try:
        start = int(start)
    except (ValueError, TypeError):
        return WARNING + '（缺少原文起始行号，保留原片段）。\n' + original
    lines = code.splitlines()
    selected = {int(n) - start for n in re.findall(r'^\s*L(\d+):', original, re.M)}
    if not selected or min(selected) < 0 or max(selected) >= len(lines):
        return WARNING + '（原文行号无法定位，保留原片段）。\n' + original
    masked = _masked(code).splitlines()
    statements = _statements(masked)
    blocks = []
    for index, statement in enumerate(statements):
        if not re.match(r'\s*(?:if|for|while)\b', statement['text']):
            continue
        end = statement['end']
        for following in statements[index + 1:]:
            if following['indent'] < statement['indent']:
                break
            if following['indent'] == statement['indent'] and not re.match(r'\s*else\b', following['text']):
                break
            end = following['end']
        blocks.append((statement['start'], end))
    definitions = []
    for statement in statements:
        match = re.match(r'\s*(?:(?:var|varip|const|simple|series)\s+)?(?:(?:float|int|bool|string|color)\s+)?(\[[\s\S]*?\]|[A-Za-z_]\w*)\s*(?::=|=(?!=|>))', statement['text'])
        if match:
            names = set(re.findall(r'\b[A-Za-z_]\w*\b', match.group(1)))
            definitions.append((statement, names))
    truncated = False
    for _ in range(MAX_ROUNDS):
        expanded = set(selected)
        for statement in statements:
            if any(i in selected for i in range(statement['start'], statement['end'])):
                expanded.update(range(statement['start'], statement['end']))
                names = set(re.findall(r'(?<![\w.])[A-Za-z_]\w*', statement['text']))
                for definition, defined in definitions:
                    if definition['start'] < statement['start'] and names & defined:
                        expanded.update(range(definition['start'], definition['end']))
        # Enclose all selected dependencies as well as original order lines.
        for lo, hi in reversed(blocks):
            if any(i in expanded for i in range(lo, hi)):
                expanded.update(range(lo, hi))
        if len(expanded) > MAX_LINES:
            truncated = True
            break
        if expanded == selected:
            break
        selected = expanded
    else:
        truncated = True
    if truncated:
        # The original slice may itself omit context, so explicitly fall back
        # rather than publishing a partly expanded chain as balanced evidence.
        return WARNING + f'（依赖闭包达到上限：{MAX_LINES} 行/{MAX_ROUNDS} 轮，已截断；保留原片段）。\n' + original
    evidence = '\n'.join(f'L{i + start}: {lines[i]}' for i in sorted(selected))
    return '源码证据切片（保留原行号与缩进；补充控制块及前置定义）。\n' + evidence + '\n' + WARNING + '（静态切片不证明函数、状态及跨柱执行语义）。'
