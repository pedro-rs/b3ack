document.querySelector('#track-company').onclick = () => {
    const btn = document.querySelector("#track-company")
    const companyCode = btn.dataset.companycode
    addToWatchlist(companyCode);
}

function addToWatchlist(companyCode) {
    fetch('/watchlist', {
        method: 'POST',
        body: JSON.stringify({
            companyCode: companyCode
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}
