const API = "http://127.0.0.1:8000"



const loginForm = document.getElementById("loginForm")

if (loginForm) {
loginForm.addEventListener("submit", async (e) => {

e.preventDefault()

const email = document.getElementById("email").value
const password = document.getElementById("password").value

const res = await fetch(`${API}/auth/login`, {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({
email: email,
password: password
})
})

const data = await res.json()

if (data.access_token) {

localStorage.setItem("token", data.access_token)

window.location.href = "dashboard.html"

} else {

document.getElementById("message").innerText = "Login failed"

}

})
}

/* REGISTER */

const registerForm = document.getElementById("registerForm")

if (registerForm) {

registerForm.addEventListener("submit", async (e) => {

e.preventDefault()
const username = document.getElementById("reg_username").value
const email = document.getElementById("reg_email").value
const password = document.getElementById("reg_password").value

const res = await fetch(`${API}/api/v1/auth/register`, {

method: "POST",

headers: {

"Content-Type": "application/json"

},

body: JSON.stringify({

username: username,

email: email,

password: password

})

})

const data = await res.json()

document.getElementById("registerMessage").innerText = JSON.stringify(data)

})

}

/* CREATE TASK */

const taskForm = document.getElementById("taskForm")

if (taskForm) {

taskForm.addEventListener("submit", async (e) => {

e.preventDefault()

const token = localStorage.getItem("token")

const title = document.getElementById("taskTitle").value
const description = document.getElementById("taskDescription").value

const res = await fetch(`${API}/api/v1/tasks/create`, {

method: "POST",

headers: {

"Content-Type": "application/json",

"Authorization": `Bearer ${token}`

},

body: JSON.stringify({

title: title,
description: description

})

})

const data = await res.json()

document.getElementById("taskMessage").innerText = JSON.stringify(data)

loadTasks()

})

}

/* LOAD TASKS */

async function loadTasks() {

const token = localStorage.getItem("token")

const res = await fetch(`${API}/api/v1/tasks/get`, {
    method: "GET",

headers: {

"Authorization": `Bearer ${token}`

}

})

const tasks = await res.json()

const list = document.getElementById("taskList")

if (!list) return

list.innerHTML = ""

tasks.forEach(task => {

const li = document.createElement("li")

li.innerText = task.title

list.appendChild(li)

})

}

if (window.location.pathname.includes("dashboard")) {

loadTasks()

}

/* LOGOUT */

function logout() {

localStorage.removeItem("token")

window.location.href = "index.html"

}