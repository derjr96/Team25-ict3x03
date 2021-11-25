let donutChart = (dataColumns, colorArray, ctitle) => {
	if (dataColumns.length === 0) {
		ctitle = "No active\ninvestments";
        colorArray = ["#6D6D6D"];
        dataColumns = [["Not invested",100]];
	}

	let chart = bb.generate({
		data: {
			columns: dataColumns,
			type:"donut",
		},
		color: { pattern: colorArray },
		donut: { title:ctitle },
        bindto: "#chart"
	});
};

let candleChart = (chart_date, chart_data) => {

    let chart = bb.generate({
        data: {
          x: "Date",
          xFormat: "%d/%m/%Y",
          columns: [
            chart_date,
            chart_data
          ],
          type: "candlestick",
          colors: {
            data1: "#00d1b2"
          },
          labels: true
        },
        candlestick: {
          color: {
            down: "#ff3860"
          },
          width: {
            ratio: 0.5
          }
        },
        axis: {
          x: {
            type: "timeseries",
            tick: {
              format: "%d/%m",
              culling: true,
              fit: true,
              rotate: 45
            },
            padding: {
              left: 1000*60*60*24,
              right: 1000*60*60*24
            }
          }
        },
        zoom: {
            enabled: true,
        },
        resize:{
            auto: true
        },
        bindto: "#cchart"
      });    
}