document.querySelector('#track-company').onclick = () => {
    const btn = document.querySelector("#track-company")
    const companyId = btn.dataset.companyid
    addToWatchlist(companyId);
}

function addToWatchlist(companyId) {
    fetch('/watchlist', {
        method: 'POST',
        body: JSON.stringify({
            companyId: companyId
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}
