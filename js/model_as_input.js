// Add listener for the form
let form = document.getElementsByTagName("form")[0];
let form_button = document.getElementById("submit_button");
let err_banner = document.getElementById("err_banner");

form_button.addEventListener("click", function(event){
  event.preventDefault();
  err_banner.classList.add("d-none");
  fetch(form.action, {
    method: "POST",
    body: new FormData(form),
  }).catch(error => {
    console.log("Failed " + str(error));
    err_banner.classList.remove("d-none");
  })
    .then(response => {
      if (response.status != 200){
        response.json().then(data => {
          err_banner.getElementsByTagName("div")[0].innerText=data.message;
          err_banner.classList.remove("d-none");
        });
        throw "Bad response from the server.";
      }
      return response.json();
    })
    .then(
      data => {
        document.location.href='/results_from_model_'+data['url_slug'];
      });
});
