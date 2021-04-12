import utils


def main():
    file = open("verbs.txt", "r", encoding='utf-8')
    Dict = {}
    for line in file:
        tokens = utils.extractTokens(line)
        t, e, v = utils.parseTokens(tokens)
        if e != '':
            print(line)
            print(tokens)
            print(t)
            print(e)
            print(v)
        else:
            Dict = utils.includeInDict(v, Dict)
    file.close()
    for Verb in Dict.keys():
        Paradigm = Dict[Verb]['Paradigm']
        if Paradigm != '':
            for Mood in utils.moodId:
                if Mood in Dict[Paradigm]:
                    Dict[Verb][Mood] = utils.conjugate(Verb, Mood, Paradigm, Dict)
    utils.printDict(Dict)


main()