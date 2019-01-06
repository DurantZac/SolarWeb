/*
$(function(){
    $("#power_now").dxChart({
        dataSource: '/powergraphdata', 
        commonSeriesSettings: {
            argumentField: "time",
            type: "line",
            point: {
                visible: false
            },
            color: '#03a3d8'
        },
        series: [
            { valueField: "power_now", name: "Power Now" },
        ],
        argumentAxis: {
            tickInterval: { hours: 1 }
        }
    });
});

$(function(){
    $("#energy_by_day").dxChart({
        palette: "Violet",
        dataSource: '/energydaygraphdata', 
        series: {
            argumentField: "day",
            valueField: "energy_by_day",
            name: "Energy Produced By Day",
            type: "bar",
            color: '#03a3d8'
        }
    });
});

$(function(){
    $("#energy_by_month").dxChart({
        palette: "Violet",
        dataSource: '/energymonthgraphdata', 
        series: {
            argumentField: "month",
            valueField: "energy_by_month",
            name: "Energy Produced By Month",
            type: "bar",
            color: '#03a3d8'
        }
    });
});

*/




setInterval( function() {
				post();	
                $(function(){
                    $("#power_now").dxChart({
                        dataSource: '/powergraphdata', 
                        commonSeriesSettings: {
                            argumentField: "time",
                            type: "line",
                            point: {
                                visible: false
                            },
                            color: '#03a3d8'
                        },
                        series: [
                            { valueField: "power_now", name: "Power Now" },
                        ],
                        argumentAxis: {
                            tickInterval: { hours: 1 }
                        }
                    });
                });

                $(function(){
                    $("#energy_by_day").dxChart({
                        palette: "Violet",
                        dataSource: '/energydaygraphdata', 
                        series: {
                            argumentField: "day",
                            valueField: "energy_by_day",
                            name: "Energy Produced By Day",
                            type: "bar",
                            color: '#03a3d8'
                        }
                    });
                });

                $(function(){
                    $("#energy_by_month").dxChart({
                        palette: "Violet",
                        dataSource: '/energymonthgraphdata', 
                        series: {
                            argumentField: "month",
                            valueField: "energy_by_month",
                            name: "Energy Produced By Month",
                            type: "bar",
                            color: '#03a3d8'
                        }
                    });
                });
}
		, 60000)



function post(){
	$.post("/dialdata" ,function(){
		})
		.done(function(data) {
			var obj = JSON.parse(data);
			var value = obj.value;
			var gauge = $( "#gauge" ).dxCircularGauge("instance");
			gauge.option("value", obj.value);
		 })
}

$(function(){
    $("#gauge").dxCircularGauge({
        value: 1,
        scale: {
            startValue: 0,
            endValue: 20,
            tickInterval: 5,
        },
        tooltip: { enabled: true },
        title: {
            text: "Power Now",
            font: { size: 28 }
        },
        color: '#03a3d8'
    });
});


