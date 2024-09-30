import deepl


def translate_deepl(txt: list, key, lang):
    print("[translator] Translating via deepl")
    translator = deepl.Translator(key)

    result = translator.translate_text(txt, target_lang=lang)
    return [x.text for x in result]


def translate_segments(segments,  agent):
    batch = []
    for i in segments:
        batch.append(i['text'])
    translation = translate_deepl(batch, agent.deepl, agent.lang)
    for i in range(len(segments)):
        segments[i]['text'] = translation[i]