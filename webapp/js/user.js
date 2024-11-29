document.addEventListener("DOMContentLoaded", () => {
    const content = document.getElementById("content");

    fetch("/user/profile/")
        .then(response => response.json())
        .then(data => {
            content.innerHTML = `
                <h2>Welcome, ${data.name}!</h2>
                <p>Stars Balance: ${data.stars_balance}</p>
                <button id="add-stars">Add Stars</button>
            `;

            document.getElementById("add-stars").addEventListener("click", () => {
                fetch("/user/add-stars/", { method: "POST" })
                    .then(response => response.json())
                    .then(result => {
                        alert(`Stars added: ${result.added}`);
                    });
            });
        });
});
