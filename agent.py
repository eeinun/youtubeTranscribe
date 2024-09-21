import json
from os.path import isfile


class Agent:
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
                self.lang = input("Input ISO 639 language code.\nRefer to https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes\nNote that your language can be unsupported.\n-->").strip()
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