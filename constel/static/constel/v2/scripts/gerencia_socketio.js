$(document).ready(function () {
  const socket = io("ws://sentinelawe2.herokuapp.com")
  const button_activate = document.querySelector("#activate_sentinel")
  const button_deactivate = document.querySelector("#deactivate_sentinel")

  socket.on("connect", response => {
    socket.emit("is_on");
  });

  socket.on("disconnect", response => {
    button_activate.disabled = true
    button_deactivate.disabled = true
  });

  socket.on("send_data", response => {
    loadBoard(response)
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
        <h1 class="card-header">${activityTypeKey}</h1>
        <div class="card-body ${activityTypeKey}">
        </div>
      </div>
    `
  }

  const activityStatusCard = (activityStatusKey, activityStatusValue) => {
    return `
      <div class="col">
        <div class="card m-auto bg-info ${activityStatusKey}">
          <h1 class="card-header text-center" style="font-size: 8em;">${activityStatusValue}</h1>
          <div class="card-body">
            <h5 class="card-title">${activityStatusKey.toUpperCase()}</h5>
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
