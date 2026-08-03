const tg = window.Telegram.WebApp;

tg.ready();
tg.expand();

const balance = document.getElementById("balance");

let user = null;

if (tg.initDataUnsafe.user) {
    user = tg.initDataUnsafe.user;
    loginUser();
}

async function loginUser() {

    await fetch("https://clicktoearn.onrender.com/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: user.id,
            username: user.username || "",
            first_name: user.first_name || ""
        })
    });

    loadBalance();
}

async function loadBalance() {

    const res = await fetch(
        `https://clicktoearn.onrender.com/balance/${user.id}`
    );

    const data = await res.json();

    balance.innerHTML = "$" + Number(data.balance).toFixed(2);
}

async function dailyBonus(){

    await fetch(
        `https://clicktoearn.onrender.com/daily/${user.id}`,
        {
            method:"POST"
        }
    );

    alert("🎉 Daily Bonus +$1");

    loadBalance();
}

async function watchAds() {

    show_11491413('pop')
    .then(async () => {

        await fetch(
            `https://clicktoearn.onrender.com/reward/${user.id}`,
            {
                method: "POST"
            }
        );

        alert("🎉 Reward +$1");

        loadBalance();

    })
    .catch((e) => {

        console.log(e);
        alert("❌ Ad failed: " + JSON.stringify(e));

    });

}


function referral() {
    alert("👥 Referral System Coming Soon");
}

function withdraw() {
    alert("💸 Withdraw System Coming Soon");
}
