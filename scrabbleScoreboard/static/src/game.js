let clock = () => {
    let date = new Date();
    let hrs = date.getHours();
    let mins = date.getMinutes();
    
    let period = "AM";
    if (hrs == 0) {
        hrs = 12;
    } else if (hrs >= 12) {
        hrs = hrs -12;
        period = "PM"
    }
    
    hrs = hrs < 10 ? "0" +  hrs : hrs;
    mins = mins < 10 ? "0" + mins : mins;

    const time = `${hrs}:${mins}`;
    document.querySelector("#clock").innerText = time;
    document.querySelector("#period").innerText = period;
    setTimeout(clock, 60000);
};

let weekday = () => {
    let date = new Date();
    const days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    document.querySelector("#weekday").innerText = days[date.getDay()];
};

let day = () => {
    let date = new Date();
    let year = date.getFullYear();
    let day = date.getDate();
    let month = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ];
    let formatted_date = `${day} ${month[date.getMonth()]} ${year}`;
    document.querySelector("#date").innerText = formatted_date;
};

clock();
weekday();
day();

