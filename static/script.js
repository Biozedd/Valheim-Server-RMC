// api token here
const API_TOKEN = "your_super_secret_password";


async function checkStatus() {
    const badge = document.getElementById("live-badge");
    try {
        const res = await fetch("/api/status");
        const data = await res.json();
        if (data.online) {
            badge.innerText = "وضعیت سرور: روشن (Online)";
            badge.style.backgroundColor = "#059669";
        } else {
            badge.innerText = "وضعیت سرور: خاموش (Offline)";
            badge.style.backgroundColor = "#dc2626";
        }
    } catch (err) {
        badge.innerText = "عدم ارتباط با API";
        badge.style.backgroundColor = "#475569";
    }
}


async function controlServer(action) {
    const statusDiv = document.getElementById("status-msg");
    statusDiv.style.color = "#fbbf24";
    statusDiv.innerText = "در حال ارسال درخواست...";

    try {
        const response = await fetch(`/api/${action}`, {
            method: "POST",
            headers: {
                "Authorization": API_TOKEN
            }
        });

        const result = await response.json();

        if (response.ok) {
            statusDiv.style.color = "#10b981";
            statusDiv.innerText = result.message;
            setTimeout(checkStatus, 2000);
        } else {
            statusDiv.style.color = "#ef4444";
            statusDiv.innerText = `Error: ${result.detail}`;
        }
    } catch (error) {
        statusDiv.style.color = "#ef4444";
        statusDiv.innerText = "خطا: ارتباط با سرور برقرار نشد!";
    }
}

checkStatus();
setInterval(checkStatus, 5000);