function bubbleChart() {
    var width = 480,
        height = 480,
        ncomps = "value";

    function chart(selection) {
        var data = selection.enter().data();
        var div = selection,
            svg = div.selectAll('svg');
        svg.attr('width', width).attr('height', height);

        var tooltip = selection
            .append("div")
            .style("position", "absolute")
            .style("visibility", "hidden")
            .style("color", "white")
            .style("padding", "4px")
            .style("background-color", "black")
            .style("text-align", "center")
            .text("");

        var simulation = d3.forceSimulation(data)
            .force("x", d3.forceX(480).strength(0.05))
            .force("y", d3.forceY(480).strength(0.05))
            .force("charge", d3.forceManyBody(100));

        var scaleRadius = d3.scaleLinear().domain([d3.min(data, function(d) {
            return +d[ncomps];
        }), d3.max(data, function(d) {
            return +d[ncomps];
        })]).range([2, 20])

        var node = svg.selectAll(".circles")
            .data(data)
            .enter()
            .append("circle")
            .attr('r', function(d) {
                return scaleRadius(d[ncomps])
            })
            .on("mouseover", function(d) {
                tooltip.html(d.name + "<br>" + d[ncomps] + " competitions");
                return tooltip.style("visibility", "visible");
            })
            .on("mousemove", function() {
                return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px");
            })
            .on("mouseout", function() {
                return tooltip.style("visibility", "hidden");
            });

        node.transition().duration(400).attr('r', function(d) {
            return scaleRadius(d[ncomps])
        })

        simulation.nodes(data)
            .on("tick", d => {
                node.attr("cx", d => d.x).attr("cy", d => d.y);
            });
    }

    chart.width = function(value) {
        if (!arguments.length) {
            return width;
        }
        width = value;
        return chart;
    };

    chart.height = function(value) {
        if (!arguments.length) {
            return height;
        }
        height = value;
        return chart;
    };

    chart.ncomps = function(value) {
        if (!arguments.ncomps) {
            return ncomps;
        }
        ncomps = value;
        return chart;
    };

    return chart;
}
