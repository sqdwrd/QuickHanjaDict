import requests
import os
import webbrowser


browser_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                "like Gecko) Chrome/88.0.4324.190 Safari/537.36"}


def get_index(search: str):
    divider = list()
    if search[0] == ";" or search[0] == ":":
        open_in_web_browser = True
    else:
        open_in_web_browser = False
    search = search.replace(";", "").replace(":", "")
    for i in range(os.get_terminal_size().columns):
        divider.append("─")
    json = requests.get("https://hanja.dict.naver.com/api3/ccko/search?query=" + search +
                        "&range=word&page=1&shouldSearchOpen=false", headers=browser_header).json()
    word_json = json['searchResultMap']['searchResultListMap']['WORD']['items'][0]
    if open_in_web_browser:
        webbrowser.open("https://hanja.dict.naver.com/" + word_json["destinationLink"])
    print(word_json['expEntry'])
    word_char_list = list()
    for i in word_json['expEntry']:
        word_char_list.append(i)
    comma_word = ','.join(word_char_list)
    index = requests.get("https://hanja.dict.naver.com/api3/ccko/search/letter?query=" + comma_word, headers=browser_header)
    chars = list()
    for i in index.json()["searchResult"]:
        chars.append("[" + i['expKoreanPron'] + "]")
    print(" / ".join(chars))
    print("".join(divider))


if __name__ == '__main__':
    try:
        while True:
            try:
                get_index(input("검색어 입력\n>>"))
            except IndexError:
                print('찾을 수 없는 단어')
    except KeyboardInterrupt:
        print("\n종료")
