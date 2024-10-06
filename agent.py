import json
from os.path import isfile


class Agent:
    iso639 = { # https://community.openai.com/t/whisper-transcribe-api-verbose-json-results-format-of-language-property/646014/4
        'afrikaans': 'af', 'arabic': 'ar', 'armenian': 'hy',
        'azerbaijani': 'az', 'belarusian': 'be', 'bosnian': 'bs',
        'bulgarian': 'bg', 'catalan': 'ca', 'chinese': 'zh',
        'croatian': 'hr', 'czech': 'cs', 'danish': 'da',
        'dutch': 'nl', 'english': 'en', 'estonian': 'et',
        'finnish': 'fi', 'french': 'fr', 'galician': 'gl',
        'german': 'de', 'greek': 'el', 'hebrew': 'he',
        'hindi': 'hi', 'hungarian': 'hu', 'icelandic': 'is',
        'indonesian': 'id', 'italian': 'it', 'japanese': 'ja',
        'kannada': 'kn', 'kazakh': 'kk', 'korean': 'ko',
        'latvian': 'lv', 'lithuanian': 'lt', 'macedonian': 'mk',
        'malay': 'ms', 'maori': 'mi', 'marathi': 'mr',
        'nepali': 'ne', 'norwegian': 'no', 'persian': 'fa',
        'polish': 'pl', 'portuguese': 'pt', 'romanian': 'ro',
        'russian': 'ru', 'serbian': 'sr', 'slovak': 'sk',
        'slovenian': 'sl', 'spanish': 'es', 'swahili': 'sw',
        'swedish': 'sv', 'tagalog': 'tl', 'tamil': 'ta',
        'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk',
        'urdu': 'ur', 'vietnamese': 'vi', 'welsh': 'cy'
    }
    def __init__(self):
        if not isfile("secrets.json"):
            with open("secrets.json", "w", encoding="utf-8") as f:
                json.dump({"updated": 0, "language": "ko", "openai": "", "deepl": ""}, f)
        with open("secrets.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if data['updated'] == 0:
            print("API keys are needed.")
            data['openai'] = input("Input OpenAI secret key: ").strip()
            data['deepl'] = input("Input DeepL secret key: ").strip()
            with open("secrets.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
            print("Keys are registered to secrets.json\n")
        self.openai = data['openai']
        self.deepl = data['deepl']
        self.lang = data['language']

    def modify(self):
        while True:
            print("Configuration menu.")
            print("1. OpenAI api secret")
            print("2. DeepL api secret")
            print("3. Language")
            print("4. Finish")
            while True:
                print("Input number: ", end='')
                num = input().strip()
                if num not in '1234':
                    print('\r' + ' ' * len(num) + '\r')
                else:
                    break
            if num == '1':
                self.openai = input("Input OpenAI secret key: ").strip()
            elif num == '2':
                self.deepl = input("Input DeepL secret key: ").strip()
            elif num == '3':
                print("Input ISO 639 language code.\n"
                      "Refer to 'Set 1' column of https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes.\n"
                      "To see on shell input [iso]\n"
                      "Note that your language can be unsupported.\n")
                print(f"Your country is currently set to {self.lang}({([None] + [x for x in self.iso639 if self.iso639[x] == self.lang])[-1]})")
                tmp = input("--> ").strip()
                if tmp == "iso":
                    alpha = "a"
                    print(f"- {alpha} ----------------")
                    for k in self.iso639:
                        if alpha != k[0]:
                            alpha = k[0]
                            print(f"- {alpha} ----------------")
                        print(f"    {k:<12}: {self.iso639[k]}")
                    self.lang = input("\n--> ").strip()
                else:
                    self.lang = tmp
            elif num == '4':
                with open("secrets.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["updated"] += 1
                data["language"] = self.lang
                data["openai"] = self.openai
                data["deepl"] = self.deepl
                with open("secrets.json", "w", encoding="utf-8") as f:
                    json.dump(data, f)
                break

if __name__ == "__main__":
    agent = Agent()
    agent.modify()