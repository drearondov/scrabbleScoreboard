let update_avatar = () => {
    avatar_id = document.querySelector("#avatar").innerText
    document.querySelector("#avatar").innerHTML = `<img src="static/img/avatar-${avatar_id}.png" alt="player avatar">`;
}

update_avatar();
