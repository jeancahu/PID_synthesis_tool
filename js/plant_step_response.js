/* this script plots the file input when a file in the form Time,Step,PlantResponse is supplied*/

window.onresize = function() {
	  Plotly.Plots.resize('step_response_graph');
      };

      var step_input = {
	  x: [1, 2, 2, 3, 4],
	  y: [0, 0, 0.5, 0.5, 0.5],
	  type: 'scatter',
	  name: 'Step input'
      };

      var sys_response = {
	  x: [1, 2, 2.3, 2.5, 3, 4],
	  y: [0, 0, 0, 0.4, 0.6, 0.7],
	  type: 'scatter',
	  name: 'System response'
      };

      var data = [step_input, sys_response];

      Plotly.newPlot('step_response_graph', data);

      var file_content = "";
      var v = 1;
      var T = 1;
      var L = 1;
      var K = 1;

      document.getElementById('in_file').addEventListener('change', readFileAsString)

      function readFileAsString() {
	  var files = this.files;
	  if (files.length === 0) {
              console.log('No file is selected');
              return;
	  }

	  var reader = new FileReader();
	  reader.onload = function(event) {
	      file_content = event.target.result;
	      //var content = event.target.result.replace(/\n/g, 'NL');
	      //content = content.replace(/\t/g, 'TB');
	      //file_content = content.replace(/ /g, 'SP');
	      document.getElementById('textcontent').value = file_content


	      var content_matrix = file_content.replace(/\r/g, '');
	      content_matrix = content_matrix.replace(/[,; ]/g, '\t');
	      content_matrix = content_matrix.replace(/\t*\t/g, '\t');
	      content_matrix = content_matrix.replace(/^\t/, '');
	      content_matrix = content_matrix.replace(/\n\t/g, '\n');
	      content_matrix = content_matrix.replace(/\t\n/g, '\n');
	      content_matrix = content_matrix.split('\n');

	      //console.log(content_matrix);

	      var counter = 0;
	      var number = 0.0;
	      var temp = 0.0;
	      var step_input_array = [];
	      var sys_resp_array = [];
	      var time_array = [];

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

	      step_input = {
		  x: time_array,
		  y: step_input_array,
		  type: 'scatter',
		  name: 'Step input'
	      };

	      sys_response = {
		  x: time_array,
		  y: sys_resp_array,
		  type: 'scatter',
		  name: 'System response'
	      };

	      data = [step_input, sys_response];
	      Plotly.newPlot('step_response_graph', data);

	      console.log(step_input_array);

	  };
	  reader.readAsText(files[0]);
      }

      function compute_params ()
      {
          console.log("compute_params running");
	  v = document.getElementById('in_frac').value;
	  T = document.getElementById('in_time').value;
	  L = document.getElementById('in_dtime').value;
	  K = document.getElementById('in_prop').value;
	  if ( file_content == "" )
	  {
	      window.location.href = '/interactive/client_cgi_python.py?v='+v+'&T='+T+'&L='+L+'&K='+K;
	  }
	  else
	  {
	      window.location.href = '/interactive/client_cgi_python.py?step_resp='+file_content;
	  }
      }
