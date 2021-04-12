validChars = ":-0123456789AÃÁÂÀBCÇDEÉÊFGHIÎÍJKLMNOÕÓÔPQRSTUÚÛVWXYZaãáâàbcçdeéêfghiíîjklmnoóôõpqrstuúûvwxyz\0"
moodId = ['FN', 'IP', 'PI', 'II', 'EI', 'MI', 'TI', 'FI', 'PS', 'IS', 'FS', 'IA', 'IN']
stopWords = ['paradigma', ':', moodId]

# FN - formas nominais: infinitivo, gerúndio e particípio
# IP - infinitivo pessoal
# PI - presente do indicativo
# II - imperfeito do indicativo
# EI - perfeito do indicativo
# MI - mais-que-perfeito do indicativo
# TI - futuro do pretérito do indicativo
# FI - futuro do presente do indicativo
# PS - presente do subjuntivo
# IS - imperfeito do subjuntivo
# FS - futuro do subjuntivo
# IA - imperativo afirmativo
# IN - imperativo negativo
# A lista de verbos foi aproveitada do projeto br.ispell:
# http://www.ime.usp.br/~ueda/br.ispell/beta.html


def parseParadigma(s):
    lenS = len(s)
    V = R = D = ''
    if lenS > 10 and s[0:10] == 'paradigma:':
        tail = s[10:lenS]
        idx = tail.find(':')
        if idx != -1:
            V = s[10:idx - 1]
        else:
            V = s[10:lenS - 1]
        if lenS > idx + 1:
            D = s[idx + 1:lenS - 1]
    return V, R, D


def extractTokens(s):
    lenS = len(s)
    if s[lenS - 1] == '\n':  # extract the last newline character, if any
        lenS = lenS - 1
    tokens = []
    tk = ''
    for n in range(lenS):
        c = s[n]
        if c in validChars:
            if c != ':':
                tk = tk + c
            else:
                tokens.append(tk)
                tokens.append(c)
                tk = ''
            if n == lenS - 1:
                tokens.append(tk)
    tokens.append('\0')
    return tokens


def processState5(tlist):
    verb = tlist[0]
    if tlist[2] != 'FN':
        v = {'verb': verb,
             tlist[2]: [tlist[4], tlist[6], tlist[8], tlist[10], tlist[12], tlist[14]]
             }
    else:
        v = {'verb': verb,
             tlist[2]: [verb, tlist[6], tlist[8]]
             }
    return v


def processState13(tlist):
    verb = tlist[0]
    paradigm = tlist[4]
    v = {'verb': verb,
         'isParadigm': False,
         'Paradigm': paradigm}
    return v


def processState17(tlist):
    verb = tlist[2]
    Suffix = tlist[4]
    idx = verb.find(Suffix)
    Radix = verb[0:idx]
    v = {'verb': verb,
         'isParadigm': True,
         'Paradigm': '',
         'Radix': Radix,
         'Suffix': Suffix}
    return v


def parseTokens(tlist):
    # Implments state transitions as seen in file "State Machine.png"
    v = {}
    tLen = len(tlist)
    n = 0
    errorMsg = ''
    lastState = state = '1'
    lastToken = currToken = ''
    while n <= tLen - 1:
        Break = 0
        if (Break == 0) and (state == '1'):
            lastToken = currToken
            currToken = tlist[n]
            if (Break == 0) and (currToken == '\0'):
                lastState = state
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '.'
                Break = 1
            if (Break == 0) and (currToken == ':'):
                lastState = state
                state = 'Error'
                errorMsg = 'Encontrado ":" onde não esperado'
                Break = 1
            if (Break == 0) and (currToken in moodId):
                lastState = state
                state = 'Error'
                errorMsg = currToken + ' encontrado no início da linha'
                Break = 1
            if (Break == 0) and (currToken == 'paradigma'):
                lastState = state
                state = '2'
                Break = 1
            if (Break == 0) and True:
                lastState = state
                state = '3'
                Break = 1
        if (Break == 0) and (state == '2'):
            lastToken = currToken
            currToken = tlist[n]
            if (Break == 0) and (currToken == '\0'):
                lastState = state
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '".'
                Break = 1
            if (Break == 0) and (currToken != ':'):
                lastState = state
                state = 'Error'
                errorMsg = 'Esperado ":" após "paradigma" mas encontrado "' + currToken + '"'
                Break = 1
            if (Break == 0) and (currToken == ':'):
                lastState = state
                state = '16'
                Break = 1
        if (Break == 0) and (state == '3'):
            lastToken = currToken
            currToken = tlist[n]
            if (Break == 0) and (currToken == ''):
                lastState = state
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '".'
                Break = 1
            if (Break == 0) and (currToken == '\0'):
                lastState = state
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '".'
                Break = 1
            if (Break == 0) and (currToken in moodId):
                lastState = state
                state = 'Error'
                errorMsg = 'Encontrado "' + currToken + '" em posição inválida.'
                Break = 1
            if (Break == 0) and (currToken == ':'):
                lastState = state
                state = '4'
                Break = 1
        if (Break == 0) and (state == '4'):
            lastToken = currToken
            currToken = tlist[n]
            if (Break == 0) and (currToken == ''):
                lastState = state
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '".'
                Break = 1
            if (Break == 0) and (currToken == '\0'):
                lastState = state
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '".'
                Break = 1
            if (Break == 0) and (currToken in moodId):
                lastState = state
                state = '5'
                Break = 1
            if (Break == 0) and (currToken == 'paradigma'):
                lastState = state
                state = '12'
                Break = 1
        if (Break == 0) and (state == '5'):
            lastToken = currToken
            currToken = tlist[n]
            if (Break == 0) and (currToken == '\0'):
                lastState = state
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '".'
                Break = 1
            if (Break == 0) and (lastToken == 'FN') and (len(tlist) < 10):
                lastState = state
                state = 'Error'
                errorMsg = 'Forma modal ' + lastToken + ' incompleta.'
                Break = 1
            if (Break == 0) and (lastToken != 'FN') and (len(tlist) < 16):
                lastState = state
                state = 'Error'
                errorMsg = 'Forma modal ' + lastToken + ' incompleta.'
                Break = 1
            if (Break == 0) and (currToken != ':'):
                lastState = state
                state = 'Error'
                errorMsg = 'Esperado ":" após ' + lastToken + ' mas encontrado "' + currToken + '"'
                Break = 1
            if (Break == 0) and (currToken == ':'):
                v = processState5(tlist)
                Break = 1
                lastState = state
                state = 'End'
        if (Break == 0) and (state == '12'):
            lastToken = currToken
            currToken = tlist[n]
            if (Break == 0) and (currToken in moodId):
                lastState = state
                state = 'Error'
                errorMsg = 'Encontrado "' + currToken + '" em posição inválida.'
                Break = 1
            if (Break == 0) and (currToken == '\0'):
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '".'
                Break = 1
            if (Break == 0) and (currToken == ':'):
                lastState = state
                state = '13'
                Break = 1
        if (Break == 0) and (state == '13'):
            lastToken = currToken
            currToken = tlist[n]
            if (Break == 0) and (currToken in stopWords):
                lastState = state
                state = 'Error'
                errorMsg = 'Encontrado "' + currToken + '" em posição inválida.'
                Break = 1
            if (Break == 0) and (currToken == '\0'):
                v = processState13(tlist)
                Break = 1
                lastState = state
                state = 'End'
        if (Break == 0) and (state == '16'):
            lastToken = currToken
            currToken = tlist[n]
            if (Break == 0) and (currToken == ''):
                lastState = state
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '".'
                Break = 1
            if (Break == 0) and (currToken == '\0'):
                lastState = state
                state = 'Error'
                errorMsg = 'Fim inesperado de linha após "' + lastToken + '".'
                Break = 1
            if (Break == 0) and (currToken in moodId):
                lastState = state
                state = 'Error'
                errorMsg = 'Encontrado "' + currToken + '" em posição inválida.'
                Break = 1
            if (Break == 0) and (currToken == ':'):
                lastState = state
                state = '17'
                Break = 1
        if (Break == 0) and (state == '17'):
            lastToken = currToken
            currToken = tlist[n]
            if (Break == 0) and (currToken in stopWords):
                lastState = state
                state = 'Error'
                errorMsg = 'Encontrado "' + currToken + '" em posição inválida.'
                Break = 1
            if (Break == 0) and (currToken == '\0'):
                v = processState17(tlist)
                Break = 1
                lastState = state
                state = 'End'
        if state == "Error'":
            break
        else:
            if state == "End":
                errorMsg = ''
                break
            else:
                n += 1

    return lastState, errorMsg, v


def includeInDict(vin, vout):
    d = vout
    verb = vin['verb']
    if not(verb in d):
        d[verb] = {}
        fields = {}
    else:
        fields = d[verb]
    if ('isParadigm' in vin) and not('isParadigm' in d[verb]):
        fields['isParadigm'] = vin['isParadigm']
    if ('Paradigm' in vin) and not('Paradigm' in d[verb]):
        fields['Paradigm'] = vin['Paradigm']
    if ('Radix' in vin) and not('Radix' in d[verb]):
        fields['Radix'] = vin['Radix']
    if ('Suffix' in vin) and not('Suffix' in d[verb]):
        fields['Suffix'] = vin['Suffix']
    if ('FN' in vin) and not('FN' in d[verb]):
        fields['FN'] = vin['FN']
    if ('IP' in vin) and not('IP' in d[verb]):
        fields['IP'] = vin['IP']
    if ('PI' in vin) and not('PI' in d[verb]):
        fields['PI'] = vin['PI']
    if ('II' in vin) and not('II' in d[verb]):
        fields['II'] = vin['II']
    if ('EI' in vin) and not('EI' in d[verb]):
        fields['EI'] = vin['EI']
    if ('MI' in vin) and not('MI' in d[verb]):
        fields['MI'] = vin['MI']
    if ('TI' in vin) and not('TI' in d[verb]):
        fields['TI'] = vin['TI']
    if ('FI' in vin) and not('FI' in d[verb]):
        fields['FI'] = vin['FI']
    if ('PS' in vin) and not('PS' in d[verb]):
        fields['PS'] = vin['PS']
    if ('IS' in vin) and not('IS' in d[verb]):
        fields['IS'] = vin['IS']
    if ('FS' in vin) and not('FS' in d[verb]):
        fields['FS'] = vin['FS']
    if 'IA' in vin and not('IA' in d[verb]):
        fields['IA'] = vin['IA']
    if 'IN' in vin and not('IN' in d[verb]):
        fields['IN'] = vin['IN']
    d[verb] = fields
    return d


def conjugate(verb, mood, paradigm, d):
    RadixIn = d[paradigm]['Radix']
    LenRIn = len(RadixIn)
    SuffixIn = d[paradigm]['Suffix']
    LenVV = len(verb)
    LenS = len(SuffixIn)
    RadixOut = verb[0:LenVV-LenS]
    Conjugation = d[paradigm][mood]
    N = len(Conjugation)
    FormOut = []
    for n in range(N):
        if Conjugation[n] != '':
            Tail = Conjugation[n][LenRIn:]
            FormOut.append(RadixOut + Tail)
        else:
            FormOut.append('')
    return FormOut


def printDict(d):
    f = open("conjugacoes.py", "w", encoding='utf8')
    f.write('# FN - formas nominais: infinitivo, gerúndio e particípio\n')
    f.write('# IP - infinitivo pessoal\n')
    f.write('# PI - presente do indicativo\n')
    f.write('# II - imperfeito do indicativo\n')
    f.write('# EI - perfeito do indicativo\n')
    f.write('# MI - mais-que-perfeito do indicativo\n')
    f.write('# TI - futuro do pretérito do indicativo\n')
    f.write('# FI - futuro do presente do indicativo\n')
    f.write('# PS - presente do subjuntivo\n')
    f.write('# IS - imperfeito do subjuntivo\n')
    f.write('# FS - futuro do subjuntivo\n')
    f.write('# IA - imperativo afirmativo\n')
    f.write('# IN - imperativo negativo\n')
    f.write('# A lista de verbos foi aproveitada do projeto br.ispell:\n')
    f.write('# http://www.ime.usp.br/~ueda/br.ispell/beta.html\n')
    f.write('#\n')
    f.write('verbos = {' + '\n')
    for verb in d.keys():
        f.write('\t' + verb + ':{' + '\n')
        for field in d[verb]:
            if type(d[verb][field]) == str:
                stripped = d[verb][field].strip()
            if (field == 'Paradigm') or (field == 'Radix') or (field == 'Suffix'):
                f.write("\t\t\t" + field + ":'" + stripped + "'," + "\n")
            else:
                f.write("\t\t\t" + field + ":" + str(d[verb][field]) + "," + "\n")
        f.write('\t' + '},' + '\n')
    f.write('}' + '\n')
    f.close()



