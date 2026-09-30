import os
import json
import re

PROBLEMS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'problems'))
if not os.path.exists(PROBLEMS_DIR):
    PROBLEMS_DIR = r"c:\Users\rishi\Downloads\Leetcode autocomplete\codepilot-data\problems"

all_files = sorted([f for f in os.listdir(PROBLEMS_DIR) if f.endswith('.json')])
p2_files = all_files[392:784]

print(f"==================================================")
print(f"DATASET QUALITY & CODE CONSISTENCY AUDITOR")
print(f"Partition 2: Problems 393 to 784 ({len(p2_files)} files)")
print(f"Range: {p2_files[0]} -> {p2_files[-1]}")
print(f"==================================================")

html_tag_re = re.compile(r'</?(?:p|div|span|code|sup|sub|font|strong|b|i|em|ul|ol|li|br|pre|table|thead|tbody|tr|th|td|a|h\d)\b[^>]*>', re.IGNORECASE)
html_entity_re = re.compile(r'&(?:[a-zA-Z0-9]+|#\d+|#x[0-9a-fA-F]+);')
chinese_re = re.compile(r'[\u4e00-\u9fff]')

issues = {
    'leaked_templates': [],
    'missing_placeholders': [],
    'unbalanced_braces': [],
    'cutoff_definitions': [],
    'raw_html_tags': [],
    'unescaped_html_entities': [],
    'chinese_artifacts': [],
    'malformed_examples': [],
}

def check_brace_balance(code):
    clean = re.sub(r'//.*', '', code)
    clean = re.sub(r'/\*.*?\*/', '', clean, flags=re.DOTALL)
    clean = re.sub(r'"(\\.|[^"])*"', '', clean)
    clean = re.sub(r"'(\\.|[^'])*'", '', clean)
    clean = re.sub(r'`(\\.|[^`])*`', '', clean)
    open_b = clean.count('{')
    close_b = clean.count('}')
    return open_b == close_b, open_b, close_b

for fname in p2_files:
    fpath = os.path.join(PROBLEMS_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as fp:
        d = json.load(fp)

    st = d.get('starterTemplates', {})
    sn = d.get('snippets', {})

    # 1. Verify starterTemplates
    for lang in ['python', 'cpp', 'java', 'javascript']:
        code = st.get(lang, '')
        if not code:
            continue

        # a) Placeholder check
        if lang == 'python':
            if 'pass' not in code and '...' not in code:
                issues['missing_placeholders'].append((fname, lang, 'no pass placeholder'))
        else:
            if '// Your code here' not in code:
                issues['missing_placeholders'].append((fname, lang, 'no // Your code here placeholder'))

        # b) Balanced braces check
        if lang in ['cpp', 'java', 'javascript']:
            balanced, ob, cb = check_brace_balance(code)
            if not balanced:
                issues['unbalanced_braces'].append((fname, lang, f"open={ob} close={cb}"))

        # c) Leaked solution check
        if lang == 'python':
            lines = [l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('#')]
            leaked = [l for l in lines if re.match(r'^(for |while |if |ans\s*=|res\s*=|primes =|mx =)', l)]
            if leaked:
                issues['leaked_templates'].append((fname, lang, leaked[0]))
        else:
            lines = [l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('//') and not l.strip().startswith('/*') and not l.strip().startswith('*')]
            # Exclude declarations like var solution = function() or declare global
            filtered = [l for l in lines if not re.match(r'^(?:var|let|const)\s+\w+\s*=\s*(?:function|\()', l) and \
                                             not l.startswith('declare ') and not l.startswith('interface ') and not l.startswith('type ') and not l.startswith('export ')]
            leaked = [l for l in filtered if re.match(r'^(for\s*\(|while\s*\(|let |const |var |int ans|int res|return (?!;))', l)]
            if leaked:
                issues['leaked_templates'].append((fname, lang, leaked[0]))

        # d) Cutoff definitions check
        last_non_empty = [l.strip() for l in code.split('\n') if l.strip()]
        if last_non_empty:
            last = last_non_empty[-1]
            if last.endswith(',') or last.endswith('(') or last.endswith('->'):
                issues['cutoff_definitions'].append((fname, lang, last))

    # 2. Verify Description & Content Quality
    desc = d.get('description', '')
    if html_tag_re.search(desc):
        issues['raw_html_tags'].append((fname, 'description', html_tag_re.findall(desc)[:3]))
    if html_entity_re.search(desc):
        issues['unescaped_html_entities'].append((fname, 'description', html_entity_re.findall(desc)[:3]))
    if chinese_re.search(desc):
        issues['chinese_artifacts'].append((fname, 'description', chinese_re.findall(desc)[:3]))

    # Constraints & Hints
    for idx, c in enumerate(d.get('constraints', [])):
        if html_tag_re.search(c):
            issues['raw_html_tags'].append((fname, f'constraints[{idx}]', html_tag_re.findall(c)[:3]))
        if html_entity_re.search(c):
            issues['unescaped_html_entities'].append((fname, f'constraints[{idx}]', html_entity_re.findall(c)[:3]))

    for idx, h in enumerate(d.get('hints', [])):
        if html_tag_re.search(h):
            issues['raw_html_tags'].append((fname, f'hints[{idx}]', html_tag_re.findall(h)[:3]))
        if html_entity_re.search(h):
            issues['unescaped_html_entities'].append((fname, f'hints[{idx}]', html_entity_re.findall(h)[:3]))

    # 3. Verify Examples
    for idx, ex in enumerate(d.get('examples', [])):
        inp = str(ex.get('input', ''))
        out = str(ex.get('output', ''))
        exp = str(ex.get('explanation', ''))
        for fld_name, text in [('input', inp), ('output', out), ('explanation', exp)]:
            if html_tag_re.search(text):
                issues['raw_html_tags'].append((fname, f'examples[{idx}].{fld_name}', html_tag_re.findall(text)[:3]))
            if html_entity_re.search(text):
                issues['unescaped_html_entities'].append((fname, f'examples[{idx}].{fld_name}', html_entity_re.findall(text)[:3]))
            if chinese_re.search(text):
                issues['chinese_artifacts'].append((fname, f'examples[{idx}].{fld_name}', chinese_re.findall(text)[:3]))
        if 'Explanation:' in out:
            issues['malformed_examples'].append((fname, idx, 'Explanation embedded in output'))
        if not inp and not out:
            issues['malformed_examples'].append((fname, idx, 'Both input and output empty'))

    # Verify Testcases
    for idx, tc in enumerate(d.get('testcases', [])):
        exp = str(tc.get('expected', ''))
        if 'Explanation:' in exp:
            issues['malformed_examples'].append((fname, idx, 'Explanation embedded in testcase expected'))

print("\n--- AUDIT SUMMARY BY CATEGORY ---")
all_passed = True
for cat, err_list in issues.items():
    status = "PASS [0 issues]" if len(err_list) == 0 else f"FAIL [{len(err_list)} issues]"
    print(f"  {cat.ljust(26)}: {status}")
    if err_list:
        all_passed = False
        for item in err_list[:5]:
            print(f"    -> {item}")

print("--------------------------------------------------")
if all_passed:
    print("STATUS: 100% COMPLIANT across all 392 files in Partition 2!")
else:
    print("STATUS: FAILED compliance check.")
print("==================================================")
