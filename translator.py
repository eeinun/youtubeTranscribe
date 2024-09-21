import deepl


def translate_deepl(txt: list, key):
    print("[translator] Translating via deepl")
    translator = deepl.Translator(key)

    result = translator.translate_text(txt, target_lang="ko")
    return [x.text for x in result]