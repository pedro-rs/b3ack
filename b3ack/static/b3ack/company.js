document.querySelector('#track-company').onsubmit = () => {
    const form = document.querySelector("#track-company")
    const companyCode = form.dataset.companycode

    const intervalInput = document.querySelector('#check-interval')
    const interval = intervalInput.value

    console.log(interval)
    addToWatchlist(companyCode, interval);
}

function addToWatchlist(companyCode, interval) {
    fetch('/watchlist', {
        method: 'POST',
        body: JSON.stringify({
            companyCode: companyCode,
            interval: interval
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}
