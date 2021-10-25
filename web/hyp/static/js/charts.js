function renderDateLineChart(options) {
  am4core.useTheme(am4themes_hypTheme);
  am4core.options.autoSetClassName = true;

  const chart = am4core.create(options.containerId, am4charts.XYChart);
  chart.numberFormatter.numberFormat = "##%";

  const title = chart.titles.create();
  title.text = options.title;
  title.fontSize = 25;
  title.marginBottom = 25;

  const dateAxis = chart.xAxes.push(new am4charts.DateAxis({ baseInterval: { timeUnit: "day", count: 1 }}));
  const valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

  Object.keys(options.data).forEach(function(lineName) {
    let line = drawLine(chart, lineName, options.data[lineName], options.dataKey);
    chart.series.push(line);
  });

  const cursor = new am4charts.XYCursor();
  chart.cursor = cursor;

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

  const firstSeriesDataCount = Object.values(options.data)[0];

  if (firstSeriesDataCount == null || firstSeriesDataCount.length < 5) {
    const noDataLabel = chart.createChild(am4core.Label);
    noDataLabel.text = "Not enough data 😭";
    noDataLabel.fontSize = 20;
    noDataLabel.isMeasured = false;
    noDataLabel.y = am4core.percent(50);
    noDataLabel.x = am4core.percent(50);
    noDataLabel.horizontalCenter = "middle";

    const xAxisLabel = chart.chartContainer.createChild(am4core.Label);
    xAxisLabel.text = "Date";
    xAxisLabel.align = "center";
  }

  return chart;
}

function drawLine(chart, lineName, data, attributeName) {
  const series = new am4charts.LineSeries();
  series.dataFields.valueY = attributeName;
  series.dataFields.dateX = "date";
  series.name = lineName;

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

const purple = am4core.color("#8138FE");
const tang = am4core.color("#FF8F37");
const green = am4core.color("#46C25C");
const smoke = am4core.color("#202020");
const black = am4core.color("#131313");
const white = am4core.color("#FFFFFF");

function am4themes_hypTheme(target) {
  if (target instanceof am4core.ColorSet) {
    target.list = [
      tang,
      green,
      purple,
      white
    ];
  } else if (target instanceof am4core.InterfaceColorSet) {
    target.setFor("stroke", tang);
    target.setFor("background", black);
    target.setFor("grid", white);
    target.setFor("text", white);
    target.setFor("alternativeText", white);
    target.setFor("positive", white);
    target.setFor("neeative", white);
  }
}
