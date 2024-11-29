document.addEventListener("DOMContentLoaded", () => {
    fetch("/admin/dashboard/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("total-earnings").textContent = `Total Earnings: ${data.total_earnings}`;
            document.getElementById("total-users").textContent = `Total Users: ${data.total_users}`;
        });
});
