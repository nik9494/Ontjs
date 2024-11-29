document.addEventListener("DOMContentLoaded", () => {
    const content = document.getElementById("content");

    fetch("/lead/overview/")
        .then(response => response.json())
        .then(data => {
            let overviewHTML = "<ul>";
            data.overview.forEach(item => {
                overviewHTML += `<li>ID: ${item.female_id}, Name: ${item.name}, Earnings Today: ${item.earnings_today}</li>`;
            });
            overviewHTML += "</ul>";
            content.innerHTML = `<h2>Team Overview</h2>${overviewHTML}`;
        });
});
