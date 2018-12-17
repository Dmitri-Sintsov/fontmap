import re

from tinycss2 import parse_stylesheet_bytes, ast


def parse_css_file(fname):
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


def parse_rule(rule):
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
                        content_token = token
                        font_css_token = pt
                        return font_css_token, content_token
    return None, None


def get_font_map(rules):
    font_map = {}
    for rule in rules:
        font_css_token, content_token = parse_rule(rule)
        if font_css_token is not None:
            # Convert char to entity. Commented out.
            # if not content_token.value.startswith('\\u'):
            #     content = '\\u{:04x}'.format(ord(token.value))
            # font_family, glyph_name = font_css.split('-', 1)
            font_map[font_css_token.value] = rule
    return font_map


def parse_gi_to_fa_map(fname):
    gi_to_fa_map = {}
    with open(fname, 'r') as f:
        source_glyphicon = None
        for line in f:
            result = re.findall(r"\s*&\.(.+?)\s*\{", line, re.UNICODE)
            if len(result) > 0:
                source_glyphicon = result[0]
            else:
                result = re.findall(r"\s*@extend\s*\.(.*?);\s*", line, re.UNICODE)
                if len(result) > 0:
                    if source_glyphicon != None:
                        gi_to_fa_map[source_glyphicon] = result[0]
                        source_glyphicon = None
    f.close()
    return gi_to_fa_map


def generate_css(css_fname, gi_to_fa_map, font_map_fa):
    with open(css_fname, 'w+') as f:
        for glyph_name, fa_name in gi_to_fa_map.items():
            if fa_name in font_map_fa:
                rule = font_map_fa[fa_name]
                font_css_token, content_token = parse_rule(rule)
                if font_css_token is not None:
                    font_css_token.value = glyph_name
                    print(rule.serialize(), file=f)
            else:
                print('Warning: mapping fa name "{}" is not found for glyphicon: "{}"'.format(glyph_name, fa_name))
    f.close()


rules = parse_css_file('glyphicon.css')
font_map_glyphicon = get_font_map(rules)

rules = parse_css_file('font-awesome-src.css')
font_map_fa = get_font_map(rules)

# https://gist.githubusercontent.com/blowsie/15f8fe303383e361958bd53ecb7294f9/raw/89495bbd533e7e05cc0d551557b4fbf882ed9369/glyphicon_font-awesome_convert.scss
gi_to_fa_map = parse_gi_to_fa_map('glyphicon_font-awesome_convert.scss')

generate_css('map.css', gi_to_fa_map, font_map_fa)

print('done')
