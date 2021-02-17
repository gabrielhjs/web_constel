$(document).ready(function() {
    const socket = io("ws://sentinela-web.herokuapp.com/");
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

        for (const i in response.response) {
            table.append(`
            <tr>
                <td>${response.response[i][0]}</td>
                <td>${response.response[i][1]}</td>
                <td>${response.response[i][2]}</td>
            </tr>
        `)
        }
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
