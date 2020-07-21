const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrape(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);

    var movies = await page.evaluate(() => {
        var titlesList = document.querySelectorAll('h2');
        var movieArr = [];

        for (var i = 0; i < titlesList.length; i++) {
            if (titlesList[i].innerText.trim() !== "") {
                movieArr[i] = {
                    title: titlesList[i].innerText.trim(),
                    summary: titlesList[i].nextElementSibling.innerText.trim()
                };
            }
        }
        return movieArr;
    })

    movies = movies.filter((movie) => movie !== null);

    fs.writeFile("./netflixscrape.json", JSON.stringify(movies, null, 3), (err) => {
        if (err) {
            console.error(err);
            return;
        };
        console.log("Great Success");
    });

    browser.closer();
}

scrape("https://www.digitaltrends.com/movies/best-movies-on-netflix/")