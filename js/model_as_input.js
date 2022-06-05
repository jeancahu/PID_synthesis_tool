// Add listener for the form
let form = document.getElementsByTagName("form")[0];
form.addEventListener("click", function(event){
  event.preventDefault();

  fetch(form.action, {
    method: "POST",
    body: new FormData(form),
  }).catch(error => {
    console.log("Failed " + str(error));
  })
    .then(console.log("Done"));
});
