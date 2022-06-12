// Add listener for the form
let form = document.getElementsByTagName("form")[0];
let form_button = document.getElementById("submit_button");

form_button.addEventListener("click", function(event){
  event.preventDefault();

  fetch(form.action, {
    method: "POST",
    body: new FormData(form),
  }).catch(error => {
    console.log("Failed " + str(error));
  })
    .then(response => response.json())
    .then(data => console.log(data));
});
