// Set up SVG width and height
var svgWidth = 900;
var svgHeight = 500;

//Set up margins
var margin = {
	top: 20,
	right: 40,
	bottom: 80,
	left: 100
};

// Set up chart width and height
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Connect to appropriate div and append SVG
var svg = d3.select("#scatter")
	.append("svg")
	.attr("height", svgHeight)
	.attr("width", svgWidth);

// Append SVG group to SVG
var chartGroup = svg.append("g")
	.attr("transform", `translate(${margin.left}, ${margin.top})`);

// Initial Params
var chosenXAxis = "poverty";
var chosenYAxis = "smokes";

// Function used for updating x-scale var
function xScale(medData, chosenXAxis) {
	var xLinearScale = d3.scaleLinear()
		.domain([d3.min(medData, d => d[chosenXAxis]) * 0.8, d3.max(medData, d => d[chosenXAxis]) * 1.2])
		.range([0, width]);

	return xLinearScale;
}

// Create updatable y scale function
function yScale(medData, chosenYAxis) {
	var yLinearScale = d3.scaleLinear()
		.domain([d3.min(medData, d => d[chosenYAxis]) * 0.6, d3.max(medData, d => d[chosenYAxis]) * 1.2])
		.range([height, 0]);

	return yLinearScale;
}

function updateToolTip(chosenXAxis, chosenYAxis, circlesGroup, ctext) {

	var xlabel = "";
	var ylabel = "";

	if (chosenXAxis === "poverty") {
		xlabel = "Poverty";
	}
	else {
		xlabel = "Income";
	}

	if (chosenYAxis === "smokes") {
		ylabel = "Smokes";
	}
	else {
		ylabel = "Healthcare";
	}

	if (xlabel !== "Income") {
		var toolTip = d3.tip()
		.attr("class", "tooltip")
		.offset([80, -60])
		.html(function(d) {
			return (`${d.state}<br/>${xlabel}: ${d[chosenXAxis]}%<br/>${ylabel}: ${d[chosenYAxis]}%`);
		});
	}
	else {
		var toolTip = d3.tip()
		.attr("class", "tooltip")
		.offset([80, -60])
		.html(function(d) {
			return (`${d.state}<br/>${xlabel}: $${d[chosenXAxis]}<br/>${ylabel}: ${d[chosenYAxis]}%`);
		});
	}
	

	circlesGroup.call(toolTip);

	circlesGroup.on("mouseover", function(data) {
		toolTip.show(data);
	})
		.on("mouseout", function(data) {
			toolTip.hide(data);
		});

	ctext.call(toolTip);
	ctext.on("mouseover", function(data) {
		toolTip.show(data);
	})
		.on("mouseout", function(data) {
			toolTip.hide(data);
		})

	return circlesGroup;
	return ctext;
}

function renderxAxis(newXscale, xAxis) {
	var bottomAxis = d3.axisBottom(newXscale);

	xAxis.transition()
		.duration(1000)
		.call(bottomAxis);

	return xAxis;
}

function renderyAxis(newYscale, yAxis) {
	var leftAxis = d3.axisLeft(newYscale);

	yAxis.transition()
		.duration(100)
		.call(leftAxis);

	return yAxis;
}

function rendercx(circlesGroup, newXscale, chosenXAxis) {
	circlesGroup.transition()
		.duration(1000)
		.attr("cx", d => newXscale(d[chosenXAxis]));

	return circlesGroup;
}

function rendercy(circlesGroup, newYscale, chosenYAxis) {
	circlesGroup.transition()
		.duration(1000)
		.attr("cy", d => newYscale(d[chosenYAxis]));

	return circlesGroup;
}

// Retrieve data from CSV
d3.csv("data.csv", function(error, medData) {
	if (error) throw error;

	// Parse numerical data
	medData.forEach(function(data) {
		data.poverty = +data.poverty;
		data.smokes = +data.smokes;
		data.healthcare = +data.healthcare;
		data.income = +data.income;
	});
	
	// xLinearScale function
	var xLinearScale = xScale(medData, chosenXAxis);

	// yLinearScale function
	var yLinearScale = yScale(medData, chosenYAxis);

	// Create initial axis functions
	var bottomAxis = d3.axisBottom(xLinearScale);
	var leftAxis = d3.axisLeft(yLinearScale);

	// append x-axis
	var xAxis = chartGroup.append("g")
		.classed("x-axis", true)
		.attr("transform", `translate(0, ${height})`)
		.call(bottomAxis);

	// append y-axis
	var yAxis = chartGroup.append("g")
		.classed("y-axis", true)
		.call(leftAxis);

	// append initial circles
	var circlesGroup = chartGroup.selectAll("circle")
		.data(medData)
		.enter()
		.append("circle")
		.attr("cx", d => xLinearScale(d[chosenXAxis]))
		.attr("cy", d => yLinearScale(d[chosenYAxis]))
		.attr("r", 15)
		.attr("fill", "#002aff")
		.attr("opacity", ".8");

	// append text to the same xy coords of circles and adjust for smoothness
	var ctext = svg.append("g")
		.attr("transform", `translate(${margin.left}, ${margin.top})`)
		.selectAll("text")
		.data(medData)
		.enter()
		.append("text")
		.attr("dx", d => xLinearScale(d[chosenXAxis]) - 11)
		.attr("dy", d => yLinearScale(d[chosenYAxis]) + 6)
		.text(d => d.abbr)
		.style("fill", "white")
		.style("font-size", "15px");

	// append to the svg the location of the x-axis labels
	var xlabelsGroup = chartGroup.append("g")
		.attr("transform", `translate(${width / 2}, ${height + 20})`);

	// append actual text to x-axis
	var povertyLabel = xlabelsGroup.append("text")
		.attr("x", 16)
		.attr("y", 57)
		.attr("value", "poverty")
		.classed("active", true)
		.text("Poverty");

	// append actual text to x-axis
	var incomeLabel = xlabelsGroup.append("text")
		.attr("x", 16)
		.attr("y", 28)
		.attr("value", "income")
		.classed("inactive", true)
		.text("Income");

	// append to the svg the location of the y-axis labels
	var ylabelsGroup = chartGroup.append("g")
		.attr("transform", "rotate(-90)");

	// append actual text to y-axis
	var smokesLabel = ylabelsGroup
		.append("text")
		.attr("y", 0 - margin.left)
		.attr("x", 0 - (height / 2))
		.attr("dy", "1em")
		.attr("value", "smokes")
		.classed("active", true)
		.text("Smokes");

	// append actual text to y-axis
	var healthcareLabel = ylabelsGroup
		.append("text")
		.attr("y", 35 - margin.left)
		.attr("x", 0 - (height / 2))
		.attr("dy", "1em")
		.attr("value", "healthcare")
		.classed("inactive", true)
		.text("Healthcare");

	// create toolTips for chosen x and y axes and call the functions upon the circlesGroup
	var circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup, ctext);

	// select all of the xlabels and listen for a click
	xlabelsGroup.selectAll("text")
		.on("click", function() {
			// get value of selection
			var value = d3.select(this).attr("value");
			if (value !== chosenXAxis) {
				// replaces the chosenXAxis with value
				chosenXAxis = value;
				// updates scale to new data
				xLinearScale = xScale(medData, chosenXAxis);
				// updates x axis to new scale
				xAxis = renderxAxis(xLinearScale, xAxis);
				// renders new x coords of circles to the new scale for the chosen x-axis
				circlesGroup = rendercx(circlesGroup, xLinearScale, chosenXAxis);
				// renders new tooltips to chosen axis
				circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup, ctext);

			// transition the x coords for state abbr
			ctext.transition()
				.duration(1000)
				.attr("dx", d => xLinearScale(d[chosenXAxis]) - 10);

			// change classes based on whether an axis is active or inactive
				if (chosenXAxis === "poverty") {
					povertyLabel
						.classed("active", true)
						.classed("inactive", false)
					incomeLabel
						.classed("active", false)
						.classed("inactive", true)
				}
				else {
					povertyLabel
						.classed("active", false)
						.classed("inactive", true)
					incomeLabel
						.classed("active", true)
						.classed("inactive", false)
				}
			}
		})

	// select all of the ylabels and listen for a click
	ylabelsGroup.selectAll("text")
		.on("click", function() {
			// get value of selection
			var value = d3.select(this).attr("value");
			if (chosenYAxis !== value) {
				// replaces the chosenYAxis with value
				chosenYAxis = value;
				// updates scale to new data
				yLinearScale = yScale(medData, chosenYAxis);
				// updates y axis to new scale
				yAxis = renderyAxis(yLinearScale, yAxis);
				// renders new y coords of circles to the new scale for the chosen x-axis
				circlesGroup = rendercy(circlesGroup, yLinearScale, chosenYAxis);
				// renders new tooltips to chosen axis
				circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup, ctext);

			// transition the y coords for state abbr
			ctext.transition()
				.duration(1000)
				.attr("dy", d => yLinearScale(d[chosenYAxis]) + 4);

			// change classes based on whether an axis is active or inactive
				if (chosenYAxis === "smokes") {
					smokesLabel
						.classed("active", true)
						.classed("inactive", false)
					healthcareLabel
						.classed("active", false)
						.classed("inactive", true)
				}
				else {
					smokesLabel
						.classed("active", false)
						.classed("inactive", true)
					healthcareLabel
						.classed("active", true)
						.classed("inactive", false)
				}

			};
		});

});






















