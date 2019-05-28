setInterval(
    updatePowerNow
, 20000);
setInterval(
    updateEnergyByDay
, 600000);
setInterval(
    updateEnergyByMonth
    , 600000);
setInterval(
    updateEnergyROI
    , 600000);
setInterval(
    updatePowerNowDial
, 30000);

//Set up the widgets
$(function(){
    $("#power_now").dxChart({
        dataSource: '/powergraphdata', 
        title: { text: "Watts over day", font: { family: "Calibri", weight: 400 } },
        commonSeriesSettings: {
            argumentField: "TimeStamp",
            type: "line",
            point: {
                visible: false
            },
            color: '#0092BC'
        },
        series: [
            { valueField: "Watts", name: "Watts", showInLegend: false }
        ],
        argumentAxis: {
            tickInterval: { hours: 1 }
        }
    });
});

$(function(){
    $("#energy_by_day").dxChart({
        title: { text: "KWH by day for last week", font: { family: "Calibri", weight: 400 } },
        dataSource: '/energydaygraphdata', 
        series: {
            argumentField: "DayofWeek",
            valueField: "KWH",
            showInLegend: false,
            type: "bar",
            color: '#0092BC'
        }
    });
});

$(function(){
    $("#energy_by_month").dxChart({
        title: { text: "KWH Per Month", font: { family: "Calibri", weight: 400 } },
        dataSource: '/energymonthgraphdata',
        series: {
            argumentField: "Month",
            showInLegend: false,
            valueField: "EnergyByMonth",
            type: "bar",
            color: '#0092BC'
        }
    });
});

$(function () {
    $("#return_on_investment").dxChart({
        dataSource: '/returnoninvestment',
        title: { text: "Return On Investment", font: { family: "Calibri", weight: 400 } },
        commonSeriesSettings: {
            argumentField: "Year",
            type: "stackedBar",
            hoverMode: "allArgumentPoints",
            selectionMode: "allArgumentPoints",
            label: {
                visible: true,
                format: {
                    type: "fixedPoint",
                    precision: 0
                }
            }
        },
        series: [
            {
            valueField: "EnergySavingByYear",
            color: '#008000',
            name: '$ Saving'
            },
            {
            valueField: "Depreciation",
                color: '#006400',
            name: 'Depreciation'
            }]
    });
});

$(function () {
    $("#gauge").dxCircularGauge({
        value: 0,
        scale: {
            startValue: 0,
            endValue: 20,
            tickInterval: 5,
            label: {
                customizeText: function (arg) {
                    return arg.valueText + " KW";
                }
            }
        },
        rangeContainer: {
            backgroundColor: "none",
            ranges: [
                {
                    startValue: 0,
                    endValue: 5,
                    color: "#E19094"
                },
                {
                    startValue: 5,
                    endValue: 10,
                    color: "#FCBB69"
                },
                {
                    startValue: 10,
                    endValue: 20,
                    color: "#A6C567"
                }
            ]
        },
        tooltip: { enabled: true },
        title: {
            text: "Power Now (KW)",
            font: { size: 28 }
        }       
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

function updateEnergyROI() {
    var chart = $("#return_on_investment").dxChart("instance");
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




