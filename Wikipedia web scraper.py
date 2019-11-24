from requests_html import HTML, HTMLSession
import sys


def info():
    content_box = r.html.find("div.toc", first=True)
    contents = content_box.find("li")
    bullets = [x.find(".toctext", first=True).text for x in contents]

    try:
        cutoff = bullets.index("See also")
    except ValueError:
        cutoff = bullets.index("References")

    bullets = bullets[0:cutoff]
    inputs = []

    for i, bullet in enumerate(bullets, start=1):
        print("{}: {}".format(i, bullet))
        inputs.append(str(i))

    option = input("Please enter the number of the section you would like to read: ")

    while option not in inputs:
        option = input("please enter a valid number: ")

    body = r.html.find("div.mw-parser-output", first=True)
    selected = bullets[int(option) - 1]
    header = r.html.find("h2", containing=selected, first=True)

    if not header:
        header = r.html.find("h3", containing=selected, first=True)

    start = body.element.index(header.element) + 1

    while body.element[start].tag != "h2":
        para = body.element[start]

        if para.tag == "p":
            text = "".join([i for i in para.itertext()]).strip()
            print(text)

        else:
            pass

        start += 1


session = HTMLSession()

search_term = input("Please enter the name of the Wikipedia page you are looking for: ").split()
search_term = [x.title() for x in search_term]
search_term = "_".join(search_term)

r = session.get("https://en.wikipedia.org/wiki/{}".format(search_term))
error_text = "Wikipedia does not have an article with this exact name."

try:
    if r.html.find("b")[1].text == error_text:
        print("There is no Wikipedia page with this name.")
        sys.exit()
except IndexError:
    print("The name that you entered is not a valid pagename.")
    sys.exit()

title = r.html.find("h1", first=True).text
print(title)

intro = r.html.find("p", first=True).text
print(intro)

while 1:
    choice = input("Would you like to find out more? y/n: ").lower()

    while choice not in ("y", "n"):
        choice = input("Please enter 'y' or 'n': ").lower()

    if choice == "n":
        sys.exit()

    else:
        info()
