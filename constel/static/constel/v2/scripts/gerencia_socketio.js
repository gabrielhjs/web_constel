$(document).ready(function () {
  const socket = io("wss://sentinelawe2.herokuapp.com")
  const button_activate = document.querySelector("#activate_sentinel")
  const button_deactivate = document.querySelector("#deactivate_sentinel")
  const updatedHour = document.querySelector("#updatedHour")

  socket.on("connect", _ => {
    socket.emit("is_on");
  });

  socket.on("disconnect", _ => {
    button_activate.disabled = true
    button_deactivate.disabled = true
  });

  socket.on("send_data", response => {
    loadBoard(response)
    updatedHour.innerHTML = new Date().toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo" })
  });

  socket.on("is_on", response => {

    if (response.response) {
      button_activate.disabled = true;
      button_deactivate.disabled = false;
    }
    else {
      button_activate.disabled = false
      button_deactivate.disabled = true
    }

  })

  button_activate.onclick = () => {
    button_activate.blur()
    socket.emit("turn_on")
  };

  button_deactivate.onclick = () => {
    button_deactivate.blur()
    socket.emit("turn_off")
  };
});

function loadBoard(result) {
  const activityTypeCard = (activityTypeKey) => {
    return `
      <div class="card w-100 bg-dark text-white mb-2">
        <h2 class="card-header">${activityTypeKey}</h2>
        <div class="card-body pb-0">
          <div class="container-fluit">
            <div class="row row-cols-auto ${activityTypeKey}">
            </div>
          </div>
        </div>
      </div>
    `
  }

  const activityStatusCard = (activityStatusKey, activityStatusValue) => {
    const cardColor = {
      STARTED: "rgb(93,190,63)",
      COMPLETED: "rgb(121,182,235)",
      NOTDONE: "rgb(96,206,206)",
      PENDING: "rgb(255,222,0)",
      SUSPENDED: "rgb(153,255,255)",
      CANCELLED: "rgb(119,233,118)",
    }
    return `
      <div class="col mb-3 text-dark">
        <div class="card m-auto ${activityStatusKey}" style="background-color: ${cardColor[activityStatusKey.toUpperCase()]};">
          <h1 class="card-header text-center p-2" style="font-size: 5em;">${activityStatusValue}</h1>
          <div class="card-body p-2">
            <h5 class="card-title m-auto">${activityStatusKey.toUpperCase()}</h5>
          </div>
        </div>
      </div>
    `
  }

  for (let [activityTypeKey, activityTypeValue] of Object.entries(result)) {
    if (!board.find(`.${activityTypeKey}`).length) {
      board.append(activityTypeCard(activityTypeKey))
    }
    let activityType = board.find(`.${activityTypeKey}`)

    for (let [activityStatusKey, activityStatusValue] of Object.entries(activityTypeValue)) {
      if (!activityType.find(`.${activityStatusKey}`).length) {
        activityType.append(activityStatusCard(activityStatusKey, activityStatusValue))
      }
      else {
        activityType.find(`.${activityStatusKey}`).children("h1").text(`${activityStatusValue}`)
      }
    }
  }
}
