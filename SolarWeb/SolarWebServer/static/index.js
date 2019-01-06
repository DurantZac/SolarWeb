setInterval(
    updatePowerNow
, 30000);
setInterval(
    updateEnergyByDay
, 60000);
setInterval(
    updateEnergyByMonth
, 300000);
setInterval(
    updatePowerNowDial
, 30000);

//Set up the widgets
$(function(){
    $("#power_now").dxChart({
        dataSource: '/powergraphdata', 
        commonSeriesSettings: {
            argumentField: "TimeStamp",
            type: "line",
            point: {
                visible: false
            },
            color: '#03a3d8'
        },
        series: [
            { valueField: "Watts", name: "Power Now" }
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
            argumentField: "DayofWeek",
            valueField: "Watts",
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
            argumentField: "Month",
            valueField: "EnergyByMonth",
            name: "Energy Produced By Month",
            type: "bar",
            color: '#03a3d8'
        }
    });
});

$(function () {
    $("#gauge").dxCircularGauge({
        value: 1,
        scale: {
            startValue: 0,
            endValue: 20,
            tickInterval: 5
        },
        tooltip: { enabled: true },
        title: {
            text: "Power Now",
            font: { size: 28 }
        },
        color: '#03a3d8'
    });
});


//Update the data based on setinterval above

function updatePowerNow() {
    var chart = $("#power_now").dxChart("instance");
    var ds = chart.option('dataSource');
    chart.option('dataSource', "");
    chart.option('dataSource', ds);
}

function updateEnergyByDay() {
    var chart = $("#energy_by_day").dxChart("instance");
    var ds = chart.option('dataSource');
    chart.option('dataSource', "");
    chart.option('dataSource', ds);
}

function updateEnergyByMonth() {
    var chart = $("#energy_by_month").dxChart("instance");
    var ds = chart.option('dataSource');
    chart.option('dataSource', "");
    chart.option('dataSource', ds);
    chart._render();
}


function updatePowerNowDial(){
    $.post("/dialdata", function () {
    })
    .done(function (data) {
            var obj = JSON.parse(data);
            var value = obj.value;
            var gauge = $("#gauge").dxCircularGauge("instance");
            gauge.option("value", value);
    });
}




