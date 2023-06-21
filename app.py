from flask import Flask, render_template, request, redirect, url_for
import requests
import random
from bs4 import BeautifulSoup

random.seed()


def randomgif():
    url = "https://tenor.com/tr/"
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    url_list = []
    step1 = soup.find("div", attrs={'class': 'homepage'})
    step2 = step1.find("div", attrs={'class': 'center-container featured'})
    step3 = step2.findAll("div", attrs={'class': 'GifList'})
    for x in step3:
        gif_url = x.find_all("img")
        for y in gif_url:
            gif = y["src"]
            url_list.append(gif)
    return random.choice(url_list)


def specialgif(index):
    special_urls = []
    search_url = f"https://tenor.com/tr/search/{index}-gifs"
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    url_list = []
    step1 = soup.find("div", attrs={'class': 'search'})
    step2 = step1.findAll("div", attrs={'class': 'GifList'})
    for x in step2:
        gif_url = x.find_all("img")
        for y in gif_url:
            gif = y["src"]
            special_urls.append(gif)
    return random.choice(special_urls)


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['keyword']:
            return redirect(url_for("special"))
        else:
            return redirect(url_for("random"))

    return render_template("index.html")


@app.route('/random')
def random_gif():
    return render_template("random.html", gif=randomgif())


@app.route('/special', methods=['GET', 'POST'])
def special_gif():
    if request.method == 'POST':
        keyword = request.form['keyword']
        if keyword:
            filtered = ""
            for character in keyword:
                if character.isalnum():
                    filtered += character
            gif = specialgif(filtered)
            return render_template("special.html", gif=gif)
        else:
            return render_template("random.html", gif=randomgif())


if __name__ == '__main__':
    app.run(debug=True)
