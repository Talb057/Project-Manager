const addBtn = document.querySelector("#add")

const group = document.querySelector(".group")

function removeInput(){
    this.parentElement.remove();
}

function addInput(){
    const task = document.createElement("input");
    task.type = "text";
    task.className = "form-control me-5 my-1";
    task.name = "task[]";
    task.placeholder = "Add Task";

    const form = document.createElement("div");
    form.className = "form-group d-flex justify-content-between align-items-start";

    const del = document.createElement("a");
    del.innerHTML = "Remove";
    del.className = "btn btn-danger";

    del.addEventListener("click", removeInput);

    group.appendChild(form);
    form.appendChild(task);
    form.appendChild(del);
}

addBtn.addEventListener("click", addInput);