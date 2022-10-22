import React, {useState, useEffect} from "react";
import * as Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import axios from "axios";
import $ from 'jquery';
import "./timeChart.css";
import {enabled} from "glamor";
import useInterval from "../../../useInterval";

const TimeChart = (props) => {

    var chart;

    function requestData() {
        $.ajax({
            url: ``,
            success: function (point) {
                var series = chart.series[0],
                    shift = series.data.length > 30; // shift if the series is

                // add the point
                chart.series[0].addPoint(point, true, shift);
                console.log(series.data);
            },
            xhrFields: {
                withCredentials: false
            },
            cache: false
        });
    }

    useInterval(() => {
        requestData();
    }, 3000);

    $(document).ready(function () {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'time-chart',
                defaultSeriesType: 'spline',
                height: 650,
                width: 1390,
                backgroundColor: 'white',
                events: {
                    load: requestData
                }
            },
            credits: {enabled: false},
            title: {text: ''},
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 100,
                maxZoom: 20 * 1000,
            },
            yAxis: {
                minPadding: 0.2,
                maxPadding: 0.2,
                labels: {
                    enabled: false,
                    style: {
                        fontSize: 16,
                    }
                },
                title: {
                    text: '',
                    margin: 80
                },
            },
            plotOptions: {
                series:{
                    colorByPoint : true,
                    dataLabels:{
                        // enabled : true, //각각의 데이터 값을 나타낼 것인지
                        color:'black', // 데이터 값을 나타낼 때 색
                        style: {
                            // fontSize: 15
                        }
                    }
                },
            },
            time: {
                useUTC: false
            },
            series: [{
                showInLegend: false,
                name: '',
                data: []
            }]
        });

        // setInterval(requestData, 3000);
        // return () => {
        //     clearInterval(requestData);
        // }
    });

    return (
        <>
            <div className="container-two">
                <div id="time-chart"></div>
            </div>
        </>
    );
}

export default TimeChart;