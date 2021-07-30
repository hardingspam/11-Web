var yearGroups = [2016, 2017, 2018]

  // add the options to the button
d3.select("#selectButton")
  .selectAll('myOptions')
 	.data(yearGroups)
  .enter()
	.append('option')
  .text(function (d) { return d; }) // text showed in the menu
  .attr("value", function (d) { return d; }) // corresponding value returned by the button

let margin = {top: 20, right: 0, bottom: 30, left: 10};
let svgWidth = 720, svgHeight = 300;
let height = svgHeight- margin.top- margin.bottom, width = svgWidth - margin.left - margin.right;

let svg = d3.select("#svg-area").append("svg");
svg.attr('height', svgHeight)
    .attr('width', svgWidth);

function updateBars(group) {

  if (group == 2016) {
    endpoint = "/percapita-2016"
  }
  if (group == 2017) {
    endpoint = "/percapita-2017"
  }
  if (group == 2018) {
    endpoint = "/percapita-2018"
  }

  d3.json(endpoint).then((data) => {

    console.log(data)
    service_lines = Object.keys(data)
    percapita = Object.values(data)

    d3.selectAll("svg > *").remove();

    let x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
        y = d3.scaleLinear().rangeRound([height, 0]);

    x.domain(service_lines);
    y.domain([0, d3.max(percapita, function(d) { return d; })]);

    let svg = d3.select("#svg-area").selectAll("svg");

    svg = svg.append("g")
             .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    svg.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y).ticks(5));

    // Create rectangles
    let bars = svg.selectAll('.bar')
        .data(service_lines)
        .enter()
        .append("g");

    bars.append('rect')
        .attr('class', 'bar')
        .attr("x", function(d) { return x(d); })
        .attr("y", function(d) { return y(data[d]); })
        .attr("width", x.bandwidth())
        .attr("height", function(d) { return height - y(data[d]); });

    bars.append("text")
        .text(function(d) {
            return data[d];
        })
        .attr("x", function(d){
            return x(d) + x.bandwidth()/2;
        })
        .attr("y", function(d){
            return y(data[d]) - 5;
        })
        .attr("font-family" , "sans-serif")
        .attr("font-size" , "9px")
        .attr("fill" , "black")
        .attr("text-anchor", "middle");
  });
};

d3.select("#selectButton").on("change", function(d) {
    // recover the option that has been chosen
    var selected = d3.select(this).property("value");
    // run the updateChart function with this selected option
    updateBars(selected);
});

updateBars(2016);
