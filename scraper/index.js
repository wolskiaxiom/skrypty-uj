const scraper = require('./scraper')

function performTask() {
    scraper.performWork()
}

setInterval(performTask, 30000);
