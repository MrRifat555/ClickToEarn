const tg = window.Telegram.WebApp;

tg.ready();
tg.expand();

const balance = document.getElementById("balance");

let money = 0;

if (tg.initDataUnsafe.user) {

    const user = tg.initDataUnsafe.user;

    console.log("User ID:", user.id);
    console.log("Name:", user.first_name);

}

function dailyBonus() {

    money += 0.05;

    balance.innerHTML = "$" + money.toFixed(2);

    tg.showAlert("Daily Bonus Claimed!");

}

function watchAds() {

    tg.showAlert("Rewarded Ads Coming Soon");

}

function referral() {

    tg.showAlert("Referral System Coming Soon");

}

function withdraw() {

    tg.showAlert("Withdraw System Coming Soon");

}
