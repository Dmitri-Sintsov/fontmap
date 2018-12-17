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
                            content = token.value
                            font_css = pt.value
                            if not content.startswith('\\u'):
                                content = '\\u{:04x}'.format(ord(token.value))
                            font_map[content] = font_css
                            break
    return font_map


def add_to_content_map(content_map, font_map):
    for content, font_css in font_map.items():
        font_family, glyph_name = font_css.split('-', 1)
        if content not in content_map:
            content_map[content] = {}
        content_map[content][font_family] = glyph_name


def add_to_name_map(name_map, font_map):
    for content, font_css in font_map.items():
        font_family, glyph_name = font_css.split('-', 1)
        if glyph_name not in name_map:
            name_map[glyph_name] = {}
        name_map[glyph_name][font_family] = content


rules = parse_file('glyphicon.css')
font_map1 = get_font_map(rules)

rules = parse_file('font-awesome-src.css')
font_map2 = get_font_map(rules)

content_map = {}
add_to_content_map(content_map, font_map1)
add_to_content_map(content_map, font_map2)

name_map = {}
add_to_name_map(name_map, font_map1)
add_to_name_map(name_map, font_map2)

print('done')
