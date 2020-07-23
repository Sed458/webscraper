const puppeteer = require('puppeteer');

const url = 'https://www.amazon.in/s?k=Shirts&ref=nb_sb_noss_2';

async function fetchProductList(url) {
    const browser = await puppeteer.launch({
        headless: true,
        defaultViewport: null
    });
    const page = await browser.newPage();

    await page.goto(url, { waitUntil: 'networkidle2' });
    await page.waitFor('div[data-cel-widget^="search_result_"]');

    const result = await page.evaluate(() => {
        let totalSearchResults = Array.from(document.querySelectorAll('div[data-cel-widget^="search_result_"]')).length;

        let productsList = [];

        for (let i = 1; i < totalSearchResults - 1; i++) {
            let product = {
                brand: '',
                product: ''
            };
            let onlyProduct = false;
            let emptyProductMeta = false;

            let productNodes = Array.from(document.querySelectorAll(`div[data-cel-widget="search_result_${i}"] .a-size-base-plus.a-color-base`));

            if (productNodes.length === 0) {
                productNodes = Array.from(document.querySelectorAll(`div[data-cel-widget="search_result_${i}"] .a-size-medium.a-color-base.a-text-normal`));
                productNodes.length > 0 ? onlyProduct = true : emptyProductMeta = true;
            }

            let productDetails = productNodes.map(el => el.innerText);

            if (!emptyProductMeta) {
                product.brand = onlyProduct ? '' : productDetails[0];
                product.product = onlyProduct? productDetails[0] : productDetails[1];
            }

            let rawImage = document.querySelector(`div[data-cel-widget="search_result_${i}"] .s-image`);
            product.image = rawImage ? rawImage.src : '';

            let rawUrl = document.querySelector(`div[data-cel-widget="search_result_${i}"] a[target="_blank"].a-link-normal`);
            product.url = rawUrl ? rawUrl.href : '';

            let rawPrice = document.querySelector(`div[data-cel-widget="search_result_${i}"] span.a-offscreen`);
            product.price = rawPrice ? rawPrice.innerText : '';

            if (typeof product.product !== 'undefined') {
                !product.product.trim() ? null : productsList = productsList.concat(product);
            }
        }
        return productsList;
    });
}

fetchProductList(url);