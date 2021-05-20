$(document).ready(function() {
    const socket = io("ws://localhost:3333/");
    const button_activate = document.querySelector("#activate_sentinel");
    const button_deactivate = document.querySelector("#deactivate_sentinel");
    const light = document.querySelector("#sentinel_is_active_light");

    socket.on("connect", response => {
        socket.emit("is_on");
    });

    socket.on("disconnect", response => {
        light.style.backgroundColor = "grey";
        button_activate.disabled = true;
        button_deactivate.disabled =  true;
    });

    socket.on("send_data", response => {
        console.log(response)

        loadBoard(response)
    });

    socket.on("is_on", response => {

        if (response.response) {
            light.style.backgroundColor = "green";
            button_activate.disabled = true;
            button_deactivate.disabled =  false;
        }
        else {
            light.style.backgroundColor = "red";
            button_activate.disabled = false;
            button_deactivate.disabled =  true;
        }
        
    })

    button_activate.onclick = () => {
        button_activate.blur();
        socket.emit("turn_on");
    };

    button_deactivate.onclick = () => {
        button_deactivate.blur();
        socket.emit("turn_off");
    };
});

function loadBoard(result) {
    for (let [activityTypeKey, activityTypeValue] of Object.entries(result)) {
        for (let [activityStatusKey, activityStatusValue] of Object.entries(activityTypeValue)) {
            if (!board.find(`.${activityStatusKey}`).length) {
                board.append(`
                    <div class="${activityStatusKey}"><h1>${activityTypeKey}</h1><h2>${activityStatusKey}: ${activityStatusValue}</h2></div>
                `)
            }
            else {
                board.find(`.${activityStatusKey}`).children("h2").text(`${activityStatusKey}: ${activityStatusValue}`)
            }
        }
    }
}
