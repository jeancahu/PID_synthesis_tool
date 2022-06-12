// Add listener for the form
let form = document.getElementsByTagName("form")[0];
let form_button = document.getElementById("submit_button");
let clear_button = document.getElementById("clear_button");

clear_button.addEventListener("click", function(event){
  event.preventDefault();
  document.getElementById("textcontent").value="";
});

form_button.addEventListener("click", function(event){
  event.preventDefault(); // avoid default behavior

  form_button.disabled = true;
  form_button.innerText = 'Calculating...';

  fetch(form.action, {
    method: "POST",
    body: new FormData(form),
  }).catch(error => {
    // No connection - server down
    console.log("Failed " + str(error));
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      form_button.disabled = false;
      form_button.innerText = 'Compute';
      });
});
