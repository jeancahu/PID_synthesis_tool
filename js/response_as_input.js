import Plotly from 'plotly.js/lib/core'; // Chart lib

window.onresize = function() {
	Plotly.Plots.resize('step_response_graph');
};

// Clear text box
document.getElementById("textcontent").value="";

/* this script plots the file input when a file in the form Time,Step,PlantResponse is supplied*/
let step_input = {
	x: [1, 2, 2, 3, 4],
	y: [0, 0, 0.5, 0.5, 0.5],
	type: 'scatter',
	name: 'Step input'
};

let sys_response = {
	x: [1, 2, 2.3, 2.5, 3, 4],
	y: [0, 0, 0, 0.4, 0.6, 0.7],
	type: 'scatter',
	name: 'Plant response'
};

let model_response = {
	x: [1, 2, 2.3, 2.5, 3, 4],
	y: [0, 0, 0, 0.4, 0.6, 0.7],
	type: 'scatter',
	name: 'Model response'
};

let layout = {
  title: "Open-loop Plant Response",
  font: {
    //family: 'Courier New, monospace',
    size: 14,
    //color: '#7f7f7f'
  },
  xaxis: {title: "Time (s)"},
  yaxis: {title: "Magnitude"},
  height: 700,
};


let data = [step_input, sys_response];
Plotly.newPlot('step_response_graph', data, layout);

var file_content = "";

function updatePlot(file_content) {
	  var content_matrix = file_content.replace(/\r/g, '');
	  content_matrix = content_matrix.replace(/[,; ]/g, '\t');
	  content_matrix = content_matrix.replace(/\t*\t/g, '\t');
	  content_matrix = content_matrix.replace(/^\t/, '');
	  content_matrix = content_matrix.replace(/\n\t/g, '\n');
	  content_matrix = content_matrix.replace(/\t\n/g, '\n');
	  content_matrix = content_matrix.split('\n');

	  //console.log(content_matrix);

	  let counter = 0;
	  let number = 0.0;
	  let temp = 0.0;
	  let step_input_array = [];
	  let sys_resp_array = [];
	  let time_array = [];

	  for ( counter = 0 ; counter < content_matrix.length ; counter++){

		  //console.log(content_matrix[counter]);
		  content_matrix[counter] = content_matrix[counter].split('\t');

		  time_array.push(
		    parseFloat(content_matrix[counter][0]));
		  step_input_array.push(
		    parseFloat(content_matrix[counter][1]));
		  sys_resp_array.push(
		    parseFloat(content_matrix[counter][2]));
	  }

	step_input["x"] = time_array;
  step_input["y"] = step_input_array;

	sys_response["x"] = time_array;
	sys_response["y"] = sys_resp_array;

	  data = [step_input, sys_response];
	  Plotly.newPlot('step_response_graph', data);
}

function readFileAsString() {
	var files = this.files;
	if (files.length === 0) {
    console.log('No file is selected');
    return;
	}

	var reader = new FileReader();
	reader.onload = function(event) {
	  file_content = event.target.result;
	  document.getElementById('textcontent').value = file_content;
    updatePlot(file_content);
	};
	reader.readAsText(files[0]);
}
document.getElementById('in_file').addEventListener('change', readFileAsString);

function updatePlotFromTextbox(event) {
  updatePlot(event.target.value);
}

document.getElementById('textcontent').addEventListener('change', updatePlotFromTextbox);


// Add listener for the form
let form = document.getElementsByTagName("form")[0];
let form_button = document.getElementById("submit_button");
let clear_button = document.getElementById("clear_button");
let continue_a = document.getElementById("continue");
let err_banner = document.getElementById("err_banner");

clear_button.addEventListener("click", function(event){
  event.preventDefault();
  document.getElementById("textcontent").value="";
  Plotly.newPlot('step_response_graph', [], layout);
});

form_button.addEventListener("click", function(event){
  event.preventDefault(); // avoid default behavior

  form_button.disabled = true;
  continue_a.classList.add("disabled");
  err_banner.classList.add("d-none");
  form_button.innerText = 'Calculating...';

  fetch(form.action, {
    method: "POST",
    body: new FormData(form),
  }).catch(error => {
    // No connection - server down
    console.log("Failed " + str(error));
  })
    .then(response => {
      form_button.disabled = false;
      form_button.innerText = 'Compute';

      if (response.status != 200){
        response.json().then(data => {
          err_banner.getElementsByTagName("div")[0].innerText=data.message;
          err_banner.classList.remove("d-none");
        });
        throw "Bad response from the server.";
      }

      return response.json();
    })
    .then(data => {
      continue_a.href='/results_from_response_'+data['url_slug'];
      continue_a.classList.remove("disabled");

      step_input["x"] = data.simulation.time;
      step_input["y"] = data.simulation.step;

	    sys_response["x"] = data.simulation.time;
	    sys_response["y"] = data.simulation.respo;

      model_response["x"] = data.simulation.time;
	    model_response["y"] = data.simulation.m_respo;

	    data = [step_input, sys_response, model_response];
	    Plotly.newPlot('step_response_graph', data);
      });
});
