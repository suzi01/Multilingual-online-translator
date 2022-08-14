import requests, sys
from bs4 import BeautifulSoup

class ConnectionError(Exception):
    def __str__(self):
        return 'Something wrong with your internet connection'


def connection_check(page):
    try:
        if page.status_code not in [200, 404]:
            raise ConnectionError
    except ConnectionError as err:
        print(err)


class WordError(Exception):
    pass
    # def __str__(self, word):
    #     return "Sorry, unable to find %s" % str(word)

class LanguageError(Exception):
    pass
    # def __str__(self, lang):
    #     return f'Sorry, the program doesn\'t support %s' %str(lang)



args = sys.argv  # we get the list of arguments

languages = {1:'Arabic', 2:'German', 3:'English', 4:'Spanish', 5:'French', 6:'Hebrew',
             7: 'Japanese', 8: 'Dutch', 9:'Polish', 10: 'Portuguese', 11:'Romanian',
             12:'Russian', 13:'Turkish'}

# print('Hello, welcome to the translator. Translator supports:')
# for k,v in languages.items():
#     print("{}. {}".format(k,v))


headers = {'User-Agent': 'Mozilla/5.0'}

# print("Type the number of your language:")
# from_lang = int(input())
#
# print("Type the number of a language you want to translate to or '0' to translate to all languages:")
# to_lang = int(input())
#
# print('Type the word you want to translate:')
# word = input()

from_lang = args[1]


if len(args) != 4:
    print("The script should be called with 3 arguments: source language, target language(s) and word")


if args[2] == 'all':
    to_lang = 0
else:
    to_lang = args[2]

word = args[3]

if to_lang == 0:
    lang_list = list(languages.values())
    lang_list.remove(from_lang.capitalize())
else:
    lang_list = [to_lang]


with open(f'{word}.txt', 'w', encoding='utf-8') as f:
    for lang in lang_list:
        url = "https://context.reverso.net/translation/{}-{}/{}".format(from_lang.lower(), lang.lower(), word)
        s = requests.Session()
        page = s.get(url, headers=headers)
        connection_check(page)

        try:

            if page.status_code == 404:
                raise WordError(word)
            if (to_lang != 0) and (to_lang.capitalize() not in list(languages.values())):
                print('it works')
                raise LanguageError(to_lang)
                sys.exit()

            else:

                soup = BeautifulSoup(page.content, 'html.parser')

                print(f'{lang} Translations:', file=f)
                print(f'{lang} Translations:')

                related_words = soup.find(id='translations-content').find_all('a', {'class': 'translation'})
                [print(wrd.text.strip(), file=f) for wrd in related_words[:1]]
                [print(wrd.text.strip()) for wrd in related_words[:1]]

                print(f'{lang} Examples:', file=f)
                print(f'{lang} Examples:')

                related_phrases = soup.find(id='examples-content').find_all('span',{'class':'text'})
                for original, translated in zip(related_phrases[0:1:2], related_phrases[1:2:2]):
                    print(original.text.strip(), file=f)
                    print(original.text.strip())
                    print(translated.text.strip(), file=f)
                    print(translated.text.strip())
                    print('', file=f)
                    print('')

        except WordError:
            print("Sorry, unable to find %s" % str(word))
        except LanguageError:
            print('Sorry, the program doesn\'t support %s' %str(lang))