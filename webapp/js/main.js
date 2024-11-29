document.addEventListener("DOMContentLoaded", () => {
    const content = document.getElementById("content");

    document.getElementById("dashboard-link").addEventListener("click", () => {
        content.innerHTML = `<h2>Dashboard</h2><p>Loading...</p>`;
        fetch("/admin/dashboard/")
            .then(response => response.json())
            .then(data => {
                content.innerHTML = `
                    <h2>Dashboard</h2>
                    <p>Total Earnings: ${data.total_earnings}</p>
                    <p>Total Users: ${data.total_users}</p>
                `;
            });
    });

    document.getElementById("reports-link").addEventListener("click", () => {
        content.innerHTML = `<h2>Reports</h2><p>Loading...</p>`;
        fetch("/admin/reports/")
            .then(response => response.json())
            .then(data => {
                let reportHTML = "<ul>";
                data.reports.forEach(report => {
                    reportHTML += `<li>Chat ID: ${report.chat_id}, Earnings: ${report.messages_count}</li>`;
                });
                reportHTML += "</ul>";
                content.innerHTML = `<h2>Reports</h2>${reportHTML}`;
            });
    });

    document.getElementById("chats-link").addEventListener("click", () => {
        content.innerHTML = `<h2>Active Chats</h2><p>Loading...</p>`;
        fetch("/admin/active-chats/")
            .then(response => response.json())
            .then(data => {
                let chatHTML = "<ul>";
                data.active_chats.forEach(chat => {
                    chatHTML += `<li>Chat ID: ${chat.chat_id}, User ID: ${chat.user_id}, Female ID: ${chat.female_id}</li>`;
                });
                chatHTML += "</ul>";
                content.innerHTML = `<h2>Active Chats</h2>${chatHTML}`;
            });
    });

    document.getElementById("users-link").addEventListener("click", () => {
        content.innerHTML = `<h2>Users</h2><p>Loading...</p>`;
        fetch("/admin/females/")
            .then(response => response.json())
            .then(data => {
                let userHTML = "<ul>";
                data.females.forEach(female => {
                    userHTML += `<li>ID: ${female.id}, Name: ${female.name}, Earnings Today: ${female.earnings_today}</li>`;
                });
                userHTML += "</ul>";
                content.innerHTML = `<h2>Users</h2>${userHTML}`;
            });
    });
});
