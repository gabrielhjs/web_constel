$(document).ready(function() {
    const socket = io("ws://127.0.0.1:5000");
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
        console.log(table)

        const html = `
            <tr>
                <td>${response.response["contrato"]}</td>
                <td>${response.response["ok"]}</td>
                <td>${response.response["logoff"]}</td>
                <td>${response.response["sinal_ont"]}</td>
                <td>${response.response["sinal_olt"]}</td>
            </tr>
        `

        if (table.children().length == 0) {
            table.append(html)
        }
        else {
            table.children().first().before(html)
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
