// from data.js
var tableData = data;

// select the button
var filter_btn = d3.select("#filter-btn");

// function that removes duplicates from an array
function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}

// listen for event
filter_btn.on("click", function() {
	
	// prevent the page from refreshing once activated
	d3.event.preventDefault();
	
	// remove our tbody so that our info doesn't stack
	d3.select("tbody").remove();
	
	// append a new tbody to replace the once we just removed
	var tbody = d3.select("#ufo-table").append("tbody");
	
	// select our inputs
	var dt_input_f = d3.select("#datetime");
	var city_input_f = d3.select("#city");
	var state_input_f = d3.select("#state");
	var country_input_f = d3.select("#country");
	var shape_input_f = d3.select("#shape");
	
	// grab the values within our tags
	var dt_input_val = dt_input_f.property("value");
	var city_input_val = city_input_f.property("value");
	var state_input_val = state_input_f.property("value");
	var country_input_val = country_input_f.property("value");
	var shape_input_val = shape_input_f.property("value");
	
	// take all of the inputs and turn them into an array
	var inputs = [dt_input_val, city_input_val, state_input_val, country_input_val, shape_input_val];
	
	// create a list of every feature to be used for ref later
	var data_index = ["datetime", "city", "state", "country", "shape"];

	// create an iter item that attaches an index number with each input
	var input_iter = inputs.entries();

	// create an empty arr to store inputs with data
	var input_filtered = [];

	// remove inputs that are left blank
	for (let e of input_iter) {
		if (e[1] != "") {
			input_filtered.push(e);
		}
	}

	// grab the appropriate endpoints for each of our inputs
	var endpoints = [];
	for (let e of input_filtered) {
		for (i=0; i<data_index.length; i++) {
			if (e[0] === data_index.indexOf(data_index[i])) {
				endpoints.push(data_index[i]);
			}
		}
	}

	// create an empty array that will store our matches
	var matches = [];

	// query our db and push objs that match at least one of the criteria
	for (i=0; i<endpoints.length; i++) {
		matches.push(tableData.filter(inst => inst[endpoints[i]] === input_filtered[i][1]));
	}

	// flatten our array to make it smoothly iterable again
	one_d_matches = matches.flat();

	// grab our one dimensional arr and clean/update it accordingly
	// (due to the nature of our data, the order in which we filter our features does not effect the output)
	for (i=0; i<endpoints.length; i++) {
		one_d_matches = one_d_matches.filter(inst => inst[endpoints[i]] === input_filtered[i][1]);
	}

	// grab only the unique values
	unique_arr = one_d_matches.filter(onlyUnique);

	// once found the matches, grab the values and push them to tbody
	var tbody = d3.select("tbody");
	var values_array = unique_arr.map(inst => Object.values(inst));
	values_array.forEach(function(obj_val_arr) {
		var tr = tbody.append("tr");
		obj_val_arr.forEach(function(val) {
			var cell = tr.append("td");
			cell.text(val);
		})
	})
})