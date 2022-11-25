document.querySelector('#track-company').onsubmit = () => {
    const form = document.querySelector("#track-company")
    const companyCode = form.dataset.companycode

    const interval = document.querySelector('#check-interval').value
    const buy_value = document.querySelector('#buy-value').value
    const sell_value = document.querySelector('#sell-value').value

    addToWatchlist(companyCode, interval, buy_value, sell_value);
}

function addToWatchlist(companyCode, interval, buy_value, sell_value) {
    fetch('/watchlist', {
        method: 'POST',
        body: JSON.stringify({
            companyCode: companyCode,
            interval: interval,
            buy_value: buy_value,
            sell_value: sell_value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}
