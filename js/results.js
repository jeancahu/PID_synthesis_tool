import Plotly from 'plotly.js/lib/core'; // Chart lib
window.onresize = function() {
	Plotly.Plots.resize('step_response_graph');
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
	name: 'System response'
};


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


let min_y = Math.min.apply(
  Math,
  controllers.map(ctl =>
    Math.min.apply(
      Math,
      ctl.y_vect
    ))
);


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

		         //document.getElementById('servo_iae').innerHTML = 'IAE = '+error_indexes['IAE_R_'+key];
		         //document.getElementById('reg_iae').innerHTML = 'IAE = '+error_indexes['IAE_D_'+key];
		         //document.getElementById('total_iae').innerHTML = 'IAE = '+error_indexes['IAE_T_'+key];

	         step_input.x = [0, 0, max_time];
	         step_input.y = [0, 1, 1];

	         closed_loop_sys_response.x = controllers[element].t_vect;
	         closed_loop_sys_response.y = controllers[element].y_vect;

           let layout = {
             title: "Close-loop System Response",
             height: 700,
             xaxis: {title: "Time (s)"},
             yaxis: {title: "Magnitude"},
             yaxis: {range: [min_y, max_y*1.1]} // 0% 110%
           };
           let data = [step_input, closed_loop_sys_response];
           Plotly.newPlot('step_response_graph', data, layout);

		         break;
		     }
	   }
 }

 window.params_toggle = params_toggle;
 params_toggle(controllers[0].ctype, controllers[0].Ms);
