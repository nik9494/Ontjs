document.addEventListener("DOMContentLoaded", () => {
    fetch("/female/profile/?telegram_id=12345") // Заменить на ID текущего пользователя
        .then(response => response.json())
        .then(data => {
            document.getElementById("profile-name").textContent = `Name: ${data.name}`;
            document.getElementById("unique-code").textContent = `Code: ${data.unique_code}`;
        });
});
