import re


def tokenize(code):
    token_specification = [
        ('KW_SELECT', r'\bselect\b'),
        ('KW_WHERE', r'\bwhere\b'),
        ('KW_LIMIT', r'\bLIMIT\b'),
        ('KW_A', r'\ba\b'),
        ('ID', r'\?[a-zA-Z_]\w*'),
        ('PREFIX_ID', r'[a-zA-Z_]\w*:[a-zA-Z_]\w*'),
        ('DPONTOS', r':'),
        ('STRING', r'"[^"\r\n]*"(?:@[a-zA-Z]+)?'),
        ('NUM', r'\b\d+\b'),
        ('PA', r'\{'),
        ('PF', r'\}'),
        ('PONTO', r'\.'),
        ('OP', r'[=><!]'),
        ('SKIP', r'[ \t\n\r]+'),
        ('ERROR', r'.')
    ]

    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    linha = 1
    tokens = []

    it = re.finditer(tok_regex, code)
    while True:
        try:
            m = next(it)
        except StopIteration:
            break
        dic = m.groupdict()
        tipo, valor = None, None

        if dic['NUM']:
            tipo, valor = "NUM", int(dic['NUM'])
        elif dic['KW_SELECT']:
            tipo, valor = "KW_SELECT", dic['KW_SELECT']
        elif dic['KW_WHERE']:
            tipo, valor = "KW_WHERE", dic['KW_WHERE']
        elif dic['KW_LIMIT']:
            tipo, valor = "KW_LIMIT", dic['KW_LIMIT']
        elif dic['KW_A']:
            tipo, valor = "KW_A", dic['KW_A']
        elif dic['PREFIX_ID']:
            prefix, suffix = dic['PREFIX_ID'].split(":", 1)
            tokens.append(("ID", prefix, linha, m.span()))
            tokens.append(("DPONTOS", ":", linha, (m.span()[0] + len(prefix), m.span()[0] + len(prefix) + 1)))
            tokens.append(("ID", suffix, linha, (m.span()[0] + len(prefix) + 1, m.span()[1])))
            continue
        elif dic['ID']:
            tipo, valor = "ID", dic['ID']
        elif dic['STRING']:
            tipo, valor = "STRING", dic['STRING']
        elif dic['PA']:
            tipo, valor = "PA", dic['PA']
        elif dic['PF']:
            tipo, valor = "PF", dic['PF']
        elif dic['PONTO']:
            tipo, valor = "PONTO", dic['PONTO']
        elif dic['DPONTOS']:
            tipo, valor = "DPONTOS", dic['DPONTOS']
        elif dic['OP']:
            tipo, valor = "OP", dic['OP']
        elif dic['SKIP']:
            continue
        else:
            tipo, valor = "ERRO", m.group(0)

        tokens.append((tipo, valor, linha, m.span()))

    return tokens


code = '''
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
'''

tokens = tokenize(code)
for token in tokens:
    print(token)