// Establish var to store geoJSON link
const link = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";

// Create function that can take earthquake links from USGS and turn them into maps
function makeUSGSMap(link) {
	// Parse the link with d3
	d3.json(link, function(data) {
		// Create a function that binds a popup to each data point/circle
		function onEachFeature(feature, layer) {
			layer.bindPopup("<h3>Location: " + feature.properties.place + "</h3></hr><h3>Magnitude: " + feature.properties.mag +"</h3>");
		}
		
		// Create a function that will return the appropriate color for each bucket
		// (separate magnitude into buckets according to http://www.geo.mtu.edu/UPSeis/magnitude.html)
		function getColor(d) {
			if (d <= 2.5) {
				return "#2DFF57";
			} else if (d > 2.5 && d <= 5.4) {
				return "#03C229";
			} else if (d >= 5.5 && d <= 6.0) {
				return "#DCF92B";
			} else if (d >= 6.1 && d <= 6.9) {
				return "#B9D602";
			} else if (d >= 7.0 && d <= 7.9) {
				return "#F7B615";
			} else if (d >= 8.0) {
				return "#F61010";
			} else {
				return "black";
			}
		}

		// Create a function that returns an appropriate size for the radius of each circle
		function getSize(d) {
			if (d <= 2.5) {
				return 4;
			} else if (d > 2.5 && d <= 5.4) {
				return 6;
			} else if (d >= 5.5 && d <= 6.0) {
				return 8;
			} else if (d >= 6.1 && d <= 6.9) {
				return 10;
			} else if (d >= 7.0 && d <= 7.9) {
				return 12;
			} else if (d >= 8.0) {
				return 14;
			} else {
				return 0;
			}
		}

		// Create a var that stores the mapped out locations of each earthquake and its
		// corresponding data points, which are represented as circles
		var earthquakes = L.geoJSON(data.features, {
			pointToLayer: function(feature, latlng) {
				return L.circleMarker(latlng, {
					radius: getSize(feature.properties.mag),
					fillColor: getColor(feature.properties.mag),
					color: "black",
					weight: 1,
					opacity: 1,
					fillOpacity: 0.8
				})
			},
			onEachFeature: onEachFeature
		})

		// Create a background layer
		var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
			attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
			maxZoom: 18,
			id: "mapbox.streets",
			accessToken: API_KEY
		})

		// Use both layers to create a map
		var myMap = L.map("map", {
			center: [
				37.09, -95.71
			],
			zoom: 4,
			layers: [streetmap, earthquakes]
		})

		// Create a function that will return the appropriate color for each legend category
		function getLegendColor(category) {
			if (category === "2.5 or less") {
				return "#2DFF57";
			} else if (category === "2.5 to 5.4") {
				return "#03C229";
			} else if (category === "5.5 to 6.0") {
				return "#DCF92B";
			} else if (category === "6.1 to 6.9") {
				return "#B9D602";
			} else if (category === "7.0 to 7.9") {
				return "#F7B615";
			} else if (category === "8.0 or greater") {
				return "#F61010";
			} else {
				return "black";
			}
		}

		// Set up the legend and add the necessary information
		var legend = L.control({position: "bottomright"});
		legend.onAdd = function() {
			var div = L.DomUtil.create("div", "info legend"),
				categories = ["2.5 or less", "2.5 to 5.4", "5.5 to 6.0", "6.1 to 6.9", "7.0 to 7.9", "8.0 or greater"];
				labels = [];

			// Add the appropriate information into the legend space
			for (var i = 0; i < categories.length; i++) {
		        div.innerHTML +=
	            '<i style="background:' + getLegendColor(categories[i]) + '"></i> ' +
	            categories[i] + (categories[i] ? '&ndash;' + categories[i] + '<br>' : '+');
	        }
		    
		    // Return the legend (div) that was just made
		    return div;
		}
		// Add the legend to the map
		legend.addTo(myMap);
	})
}

// Call on the function to parse the given link
makeUSGSMap(link);
