// Add listener for the form
let form = document.getElementsByTagName("form")[0];
form.addEventListener("click", function(event){
  if(event.target.id == "in_file")
    return;

  event.preventDefault(); // avoid default behavior

  if(event.target.id == "clear_button" ){
    document.getElementById("textcontent").value="";
    return;
  }

  fetch(form.action, {
    method: "POST",
    body: new FormData(form),
  }).catch(error => {
    // No connection - server down
    console.log("Failed " + error);
  })
    .then(console.log("Done"));
});
