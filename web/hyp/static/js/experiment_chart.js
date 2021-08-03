function drawLine(chart, variantName, data, attributeName) {
  const series = new am4charts.LineSeries();
  series.dataFields.valueY = attributeName;
  series.dataFields.dateX = "date";
  series.name = variantName;

  const segment = series.segments.template;
  segment.interactionsEnabled = true;

  const hoverState = segment.states.create("hover");
  hoverState.properties.strokeWidth = 3;

  const dimmed = segment.states.create("dimmed");
  dimmed.properties.stroke = am4core.color("#dadada");

  segment.events.on("over", function(event) {
    accentHoveredLine(chart, event.target.parent.parent.parent);
  });

  segment.events.on("out", function(event) {
    applyDefaultLineStyles(chart, event.target.parent.parent.parent);
  });

  series.data = data;
  return series;
}

function accentHoveredLine(chart, hoveredLine) {
  hoveredLine.toFront();

  hoveredLine.segments.each(function(segment) {
    segment.setState("hover");
  });

  hoveredLine.legendDataItem.marker.setState("default");
  hoveredLine.legendDataItem.label.setState("default");

  chart.series.each(function(series) {
    if (series != hoveredLine) {
      series.segments.each(function(segment) {
        segment.setState("dimmed");
      });
      series.bulletsContainer.setState("dimmed");
      series.legendDataItem.marker.setState("dimmed");
      series.legendDataItem.label.setState("dimmed");
    }
  });
}

function applyDefaultLineStyles(chart) {
  chart.series.each(function(series) {
    series.segments.each(function(segment) {
      segment.setState("default");
    });
    series.bulletsContainer.setState("default");
    series.legendDataItem.marker.setState("default");
    series.legendDataItem.label.setState("default");
  });
}

am4core.ready(function() {
  am4core.useTheme(am4themes_animated);
  const chart = am4core.create("traffic-split-chart", am4charts.XYChart);
  chart.cursor = new am4charts.XYCursor();

  const title = chart.titles.create();
  title.text = "Traffic split by variant";
  title.fontSize = 25;
  title.marginBottom = 25;

  const splitsByVariant = JSON.parse(document.getElementById("traffic-split-data").textContent)

  const dateAxis = chart.xAxes.push(new am4charts.DateAxis());
  const valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

  Object.keys(splitsByVariant).forEach(function(variantName, i) {
    let line = drawLine(chart, variantName, splitsByVariant[variantName], "traffic_split");
    chart.series.push(line);
  });

  chart.legend = new am4charts.Legend();
  chart.legend.position = "right";
  chart.legend.scrollable = true;

  chart.legend.markers.template.states.create("dimmed").properties.opacity = 0.3;
  chart.legend.labels.template.states.create("dimmed").properties.opacity = 0.3;

  chart.legend.itemContainers.template.events.on("over", function(event) {
    accentHoveredLine(chart, event.target.dataItem.dataContext);
  });

  chart.legend.itemContainers.template.events.on("out", function(event) {
    applyDefaultLineStyles(chart, event.target.dataItem.dataContext);
  });
});
