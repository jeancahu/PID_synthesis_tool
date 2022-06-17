import Plotly from 'plotly.js/lib/core'; // Chart lib

// Add listener for the form
let form = document.getElementsByTagName("form")[0];
let form_button = document.getElementById("submit_button");
let err_banner = document.getElementById("err_banner");
let model_as_input_box = document.getElementsByClassName("model_as_input_box")[0];

function resize_graph() {
	Plotly.Plots.resize('step_response_graph');

  if (model_as_input_box.clientWidth > 524) // From CSS
  {
    layout.width = model_as_input_box.clientWidth - form.clientWidth;
    layout.height = 700;
    Plotly.newPlot('step_response_graph', s_data, layout);
  } else {
    layout.width = model_as_input_box.clientWidth;
    layout.height = model_as_input_box.clientWidth;
    Plotly.newPlot('step_response_graph', s_data, layout);
  }
};

window.onresize = resize_graph

/* this script plots the file input when a file in the form Time,Step,PlantResponse is supplied*/
let step_input = {
	x: [1, 2, 2, 3, 4],
	y: [0, 0, 0.5, 0.5, 0.5],
	type: 'scatter',
	name: 'Step input'
};

let model_response = {
	x: [1, 2, 2.3, 2.5, 3, 4],
	y: [0, 0, 0, 0.4, 0.6, 0.7],
	type: 'scatter',
	name: 'Model response'
};

let layout = {
  title: "Open-loop Model Response",
  height: 700,
  width: model_as_input_box.clientWidth - form.clientWidth,
  xaxis: {title: "Time (s)"},
  yaxis: {title: "Magnitude"},
};

let s_data = [step_input, model_response];
Plotly.newPlot('step_response_graph', s_data, layout);

resize_graph();

function handleForm(event){
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
        let l_href = "/results_from_model_"+String(data.url_slug)
        let max_t = Math.max.apply(
          Math,
          data.simulation.time
        );

        console.log(data);
        step_input = {
	        x: [0, 0, max_t],
	        y: [0, 1, 1],
	        type: 'scatter',
	        name: 'Step input'
        };

        model_response = {
	        x: data.simulation.time,
	        y: data.simulation.m_respo,
	        type: 'scatter',
	        name: 'Model response'
        };

        s_data = [step_input, model_response];
        Plotly.newPlot('step_response_graph', s_data, layout);

        document.getElementById("show_results_btn").href=l_href;
      });
}

form_button.addEventListener("click", handleForm);
