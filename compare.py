from tinycss2 import parse_stylesheet_bytes, ast


def parse_file(fname):
    with open(fname, 'r') as f:
        content = f.read()
    f.close()
    content = content.encode('utf-8')
    rules, encoding = parse_stylesheet_bytes(
        css_bytes=content,
        protocol_encoding='utf-8',
        environment_encoding='utf-8',
    skip_comments=True,
    skip_whitespace=True
    )
    return rules


def get_font_map(rules):
    font_map = {}
    for rule in rules:
        # print('type of rule: {}'.format(rule.type))
        is_content_token = False
        for token in rule.content:
            if not isinstance(token, ast.WhitespaceToken):
                # print(token.value)
                if isinstance(token, ast.IdentToken) and token.value == 'content':
                    is_content_token = True
                if isinstance(token, ast.StringToken) and is_content_token:
                    for pt in rule.prelude:
                        if isinstance(pt, ast.IdentToken):
                            font_map[token.value] = pt.value
                            break
    return font_map


rules = parse_file('glyphicon.css')
font_map1 = get_font_map(rules)

rules = parse_file('font-awesome-src.css')
font_map2 = get_font_map(rules)

print('done')
