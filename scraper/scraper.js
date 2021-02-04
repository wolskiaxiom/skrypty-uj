const request = require('request');
const cheerio = require('cheerio');
const fs = require('fs');

class Offer {
    constructor(id, title, urlToOffer, urlToImage, price) {
        this.id = id
        this.title = title
        this.urlToOffer = urlToOffer
        this.urlToImage = urlToImage
        this.price = price
    }

    getCsvLine() {
        return this.id + ';' + this.title + ';' + this.urlToOffer + ';' + this.urlToImage + ';' + this.price +'\n'
    }

}

function getExecutionId() {
    return new Date().getTime();
}

function getWriteStream(name) {
    const writeStream = fs.createWriteStream('data/posts/posts_' + name + '.csv');
    writeStream.write(`Id;Title;UrlToOffer;UrlToImage;Price\n`);
    return writeStream
}


const download = function (uri, filename, callback) {
    request.head(uri, function (err, res, body) {
        request(uri).pipe(fs.createWriteStream(filename)).on('close', callback);
    });
};


function getOffersHtmlFromOlx() {
    let url = 'https://www.olx.pl/oferty'
    return new Promise((resolve, reject) => {
        request(url, (error, response, body) => {
            if (error) reject(error);
            if (response.statusCode !== 200) {
                reject('Invalid status code <' + response.statusCode + '>');
            }
            resolve(body);
        });
    });
}

function extractOffersFromHtml(html) {
    let offers = []

    const $ = cheerio.load(html);

    $('#offers_table').find('.offer-wrapper').each(((index, element) => {
        let id = $(element).children('table').attr('data-id')
        let urlToOffer = $(element).find('.detailsLink').attr('href')
        let notStrippedUrlToImage = $(element).find('.detailsLink').children('img').attr('src')
        let urlToImage = notStrippedUrlToImage && notStrippedUrlToImage.substring(0, notStrippedUrlToImage.lastIndexOf('/image') + 6)
        let title = $(element).find('.detailsLink strong').html()
        let price = $(element).find('.price strong').html()

        if (id && urlToOffer && urlToImage && title && price) {
            offers.push(new Offer(id, title, urlToOffer, urlToImage, price))
        }
    }))
    return offers
}

async function performWork() {
    try {
        const executionId = getExecutionId()
        const writer = getWriteStream(executionId)
        fs.mkdirSync('data/images/' + executionId)

        const html = await getOffersHtmlFromOlx()

        let offers = extractOffersFromHtml(html)
        offers.forEach(offer => {
            writer.write(offer.getCsvLine())
            download(offer.urlToImage, 'data/images/' + executionId + '/' + offer.id + '.png', () => {
                console.log(offer.id+'.png downloaded!')
            })
        })

    } catch (error) {
        console.log('something went wrong')
        console.log(error)
    }

}
module.exports = {
    performWork
}