import Plotly from 'plotly.js/lib/core'; // Chart lib

let step_response_graph = document.getElementById("step_response_graph");
function resize_graph() {
  if (step_response_graph.clientWidth < 700){
    layout.height = step_response_graph.clientWidth;

    s_data[0].name = "R";
    s_data[1].name = "Ser";
    s_data[2].name = "Reg";


    Plotly.newPlot('step_response_graph', s_data, layout);
  } else {
    layout.height = 700;

    s_data[0].name = "Set-point value";
    s_data[1].name = "Servo response";
    s_data[2].name = "Regulatory response";

    Plotly.newPlot('step_response_graph', s_data, layout);
  }

  Plotly.Plots.resize('step_response_graph');
};

window.onresize = resize_graph;

let layout = {
  title: "Close-loop System Response",
  height: 700,
  margin: {l: 60, r: 60, b: 60},
  xaxis: {title: "Time (s)", range: [0, 0]},
  yaxis: {title: "Magnitude", range: [0, 0]} // 0% 110%
};


// /* this script plots the file input when a file in the form Time,Step,PlantResponse is supplied*/
let step_input = {
	x: [1, 2, 2, 3, 4],
	y: [0, 0, 0.5, 0.5, 0.5],
	type: 'scatter',
	name: 'Set-point value'
};

let closed_loop_sys_response = {
	x: [1, 2, 2.3, 2.5, 3, 4],
	y: [0, 0, 0, 0.4, 0.6, 0.7],
	type: 'scatter',
	name: 'Servo response'
};

let closed_loop_reg_response = {
	x: [1, 2, 2.3, 2.5, 3, 4],
	y: [0, 0, 0, 0.4, 0.6, 0.7],
	type: 'scatter',
	name: 'Regulatory response'
};

let s_data = [step_input, closed_loop_sys_response, closed_loop_reg_response];

// Max simulation time
let max_time = Math.max.apply(
  Math,
  controllers.map(ctl => ctl.t_vect[ ctl.t_vect.length -1 ])
);

let max_y = Math.max.apply(
  Math,
  controllers.map(ctl =>
    Math.max.apply(
      Math,
      ctl.y_vect
    ))
);


let min_y = Math.min(Math.min.apply(
  Math,
  controllers.map(ctl =>
    Math.min.apply(
      Math,
      ctl.y_vect
    ))
),
Math.min.apply(
  Math,
  controllers.map(ctl =>
    Math.min.apply(
      Math,
      ctl.y_vect_reg
    ))
));


resize_graph();
function params_toggle(cnt, ms)
 {
   let key;
	   for ( var element = 0; element<controllers.length; element++ ){
		     if ( controllers[element].ctype == cnt && controllers[element].Ms == ms )
		     {
		         key = cnt+'_'+ms.replace('.','_'); //TODO

		         document.getElementById('controller_name').innerHTML = cnt+', Ms = '+ms;
		         document.getElementById('kp_const').innerHTML = controllers[element].kp;
		         document.getElementById('ti_const').innerHTML = controllers[element].ti;
		         document.getElementById('td_const').innerHTML = controllers[element].td;

		       document.getElementById('servo_iae').innerHTML = 'IAE = '+controllers[element].IAE;
		       document.getElementById('reg_iae').innerHTML = 'IAE = '+controllers[element].IAE_reg;
		       document.getElementById('total_iae').innerHTML = 'IAE = ' + (parseFloat(controllers[element].IAE) + parseFloat(controllers[element].IAE_reg));

	         step_input.x = [0, 0, max_time];
	         step_input.y = [0, 1, 1];

	         closed_loop_sys_response.x = controllers[element].t_vect;
	         closed_loop_sys_response.y = controllers[element].y_vect;

           closed_loop_reg_response.x = controllers[element].t_vect;
           closed_loop_reg_response.y = controllers[element].y_vect_reg;

           layout.xaxis = {title: "Time (s)", range: [0, max_time]};
           layout.yaxis = {title: "Magnitude", range: [min_y*1.1, max_y*1.1]}; // 0% 110%

           s_data = [step_input, closed_loop_sys_response, closed_loop_reg_response];
           Plotly.newPlot('step_response_graph', s_data, layout);

		         break;
		     }
	   }
 }

 window.params_toggle = params_toggle;
 params_toggle(controllers[0].ctype, controllers[0].Ms);
