<template>
<div style="width: 100%; display: table;">
    <div style="display: table-row">
        <div id="ScatterplotTest" style="width: 365px; display: table-cell;"></div>
        <div id="BarChartTest" style="display: table-cell; outline: 2px dashed black;"></div>
    </div>
</div>
</template>

<script>

import { EventBus } from '../main.js'
import * as Plotly from 'plotly.js'

export default {
  name: 'Confusion',
  data () {
    return {
      FinalResultsConf: 0,
      step: 0,
      xAxisBA: [],
      xAxisFS: [],
      yAxis: [],
      previousBA: [],
      previousFM: [],
      previousBATrain: [],
      previousFMTrain: [],
      WidthBar: [],
      firstTime: 0,
    }
  },
  methods: {
      reset () {
        // var svg = d3.select("#container");
        // svg.selectAll("*").remove();
        // var svg = d3.select("#legend");
        // svg.selectAll("*").remove();
        Plotly.purge('ScatterplotTest')
        Plotly.purge('LineChart')
      },
      clean(obj) {
        var propNames = Object.getOwnPropertyNames(obj);
        for (var i = 0; i < propNames.length; i++) {
          var propName = propNames[i];
          if (obj[propName] === null || obj[propName] === undefined) {
            delete obj[propName];
          }
        }
      },
      FinalResultsConfView () {

        Plotly.purge('ScatterplotTest')

        var UMAPDataOriginal = this.FinalResultsConf[17]
        var y_Values = this.FinalResultsConf[18]
        var y_Predict = JSON.parse(this.FinalResultsConf[19])
        var XTest = JSON.parse(JSON.parse(this.FinalResultsConf[20]))
        var probabilitiesLocal = JSON.parse(this.FinalResultsConf[21])
        var colorRange = ['rgba(255,127,0,0.7)','rgba(31,120,180,0.7)','rgba(223,101,176,0.7)','rgba(77,175,74,0.7)']
        var colorRangeAlter = ['rgba(255,127,0,0.05)','rgba(31,120,180,0.05)','rgba(223,101,176,0.05)','rgba(77,175,74,0.05)']

        var stringParameters = []
        for (let i = 0; i < XTest.length; i++) {
          this.clean(XTest[i])
          stringParameters.push('ID: ' + JSON.stringify(i) + '<br> Probability (%): ' + parseInt(probabilitiesLocal[i][y_Values[i]].toFixed(2) * 100) + '<br> Details: ' + JSON.stringify(XTest[i]).replace(/,/gi, '<br>'))
        }

        var UMAPDataY = []
        var UMAPDataX = []
        for (let k = 0; k < y_Values.length; k++) {
          UMAPDataX.push(UMAPDataOriginal[0][k])
          UMAPDataY.push(UMAPDataOriginal[1][k])
        }

        var data = []
        var colors = []
        var symbols = []
        var outlines = []

        for (let i = 0; i < y_Values.length; i++) {
          if (y_Values[i] == y_Predict[i]) {
            colors.push(colorRangeAlter[y_Values[i]])
            if (y_Predict[i] == 0)
              outlines.push(colorRangeAlter[0])
            else if (y_Predict[i] == 1)
              outlines.push(colorRangeAlter[1])
            else
              outlines.push(colorRangeAlter[2])
          } else {
            colors.push(colorRange[y_Values[i]])
            if (y_Predict[i] == 0)
              outlines.push(colorRange[0])
            else if (y_Predict[i] == 1)
              outlines.push(colorRange[1])
            else
              outlines.push(colorRange[2])
          }

          symbols.push('star')
        }

        data.push(
          {
            type: 'scatter',
            mode: 'markers',
            x: UMAPDataX,
            y: UMAPDataY,
            hovertemplate: 
              "%{text}<br><br>" +
              "<extra></extra>",
            text: stringParameters,
            marker: {
              color: colors,
              symbol: symbols,
              line: {
                color: outlines,
                width: 2
              },
              size: 12,
            },
          })

          var width = 360
          var height = 300

          var layout = {
            xaxis: {
                visible: false,
                autorange: true
            },
            yaxis: {
                visible: false,
                autorange: true
            },
            font: { family: 'Helvetica', size: 14, color: '#000000' },
            autosize: true,
            width: width,
            height: height,
            dragmode: 'zoom',
            hovermode: "closest",
            hoverlabel: { bgcolor: "#FFF" },
            showlegend: false,
            margin: {
              l: 0,
              r: 0,
              b: 0,
              t: 0,
              pad: 0
            },
          }
      
          var config = {scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'select2d', 'lasso2d', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: true}

          var graphDiv = document.getElementById("ScatterplotTest")
          Plotly.newPlot(graphDiv, data, layout, config)

      },
      BarChartView () {
        Plotly.purge('BarChartTest')

        var BACur = parseFloat((JSON.parse(this.FinalResultsConf[22]) * 100).toFixed(2))
        var FMCur = parseFloat((JSON.parse(this.FinalResultsConf[23]) * 100).toFixed(2))
        var BACurTrain = parseFloat((JSON.parse(this.FinalResultsConf[31]) * 100).toFixed(2))
        var FMCurTrain = parseFloat((JSON.parse(this.FinalResultsConf[32]) * 100).toFixed(2))

        if (this.firstTime == 0) {
          this.previousBA.push(BACur)
          this.previousFM.push(FMCur)
          this.previousBATrain.push(BACurTrain)
          this.previousFMTrain.push(FMCurTrain)
          EventBus.$emit('updateBA', BACur)
          EventBus.$emit('updateFM', FMCur)
          EventBus.$emit('updateBACur', BACur)
          EventBus.$emit('updateFMCur', FMCur)

          EventBus.$emit('updateBATrain', BACurTrain)
          EventBus.$emit('updateFMTrain', FMCurTrain)
          EventBus.$emit('updateBACurTrain', BACurTrain)
          EventBus.$emit('updateFMCurTrain', FMCurTrain)
          this.firstTime = 1
        } else if (this.firstTime == 1) {
          this.step = this.step + 1        
          this.yAxis.push(this.step)
          this.previousBA.push(BACur)
          this.previousFM.push(FMCur)
          this.previousBATrain.push(BACurTrain)
          this.previousFMTrain.push(FMCurTrain)
          var diffBA = BACur - this.previousBA[this.step-1]
          var diffFM = FMCur - this.previousFM[this.step-1]
          this.xAxisBA.push(diffBA)
          this.xAxisFS.push(diffFM)
          //this.WidthBar.push(2)
          EventBus.$emit('updateBACur', BACur)
          EventBus.$emit('updateFMCur', FMCur)

          EventBus.$emit('updateBACurTrain', BACurTrain)
          EventBus.$emit('updateFMCurTrain', FMCurTrain)

          var trace1 = {
            x: this.xAxisBA,
            y: this.yAxis,
            //width: this.WidthBar,
            name: 'Bal. Acc.',
            type: 'bar',
            orientation: 'h',
            marker: {
              color: 'rgb(0,225,225)'
            }
          };

          var trace2 = {
            x: this.xAxisFS,
            y: this.yAxis,
            //width: this.WidthBar,
            name: 'F1-Score',
            type: 'bar',
            orientation: 'h',
            marker: {
              color: 'rgb(225,0,225)'
            }
          };

          var data = [trace1, trace2];
          var height = 300
          var width = 255

          var layout = {
            yaxis: {
              autorange: 'reversed',
              title: 'Step of the Process',
              tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
              tickvals: this.yAxis
            },
            xaxis: {
              title: 'Performance Difference (%)',
              fixedrange: true
              // tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
              // tickvals: [0,20,40,60,80,100],
              // ticktext: ['0    ','20    ','40    ','60    ','80    ','100    '],
            },
            legend: {"orientation": "h", x: 0, y: 1.1},
            font: { family: 'Helvetica', size: 14, color: '#000000' },
            autosize: false,
            //bargap: 0.1,
            //bargroupgap: 0,
            width: width,
            height: height,
            dragmode: 'pan',
            barmode: 'group',
            hovermode: "closest",
            showlegend: true,
            margin: {
              l: 30,
              r: 12,
              b: 35,
              t: 0,
              pad: 0
            },
          }
        
            var config = {scrollZoom: true, displaylogo: false, displayModeBar: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'select2d', 'lasso2d', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: false}

            var graphDiv = document.getElementById("BarChartTest")
            Plotly.newPlot(graphDiv, data, layout, config)
          } else if (this.firstTime == 3) {
            this.step = this.step + 1        
            this.yAxis.push(this.step)
            this.previousBA.push(this.previousBA[this.step-1])
            this.previousFM.push(this.previousFM[this.step-1])
            this.previousBATrain.push(this.previousBATrain[this.step-1])
            this.previousFMTrain.push(this.previousFMTrain[this.step-1])
            var diffBA = this.previousBA[this.step-1] - this.previousBA[this.step-1]
            var diffFM = this.previousFM[this.step-1] - this.previousFM[this.step-1]
            this.xAxisBA.push(diffBA)
            this.xAxisFS.push(diffFM)
            //this.WidthBar.push(2)
            EventBus.$emit('updateBACur', this.previousBA[this.step-1])
            EventBus.$emit('updateFMCur', this.previousFM[this.step-1])

            EventBus.$emit('updateBACurTrain', this.previousBATrain[this.step-1])
            EventBus.$emit('updateFMCurTrain', this.previousFMTrain[this.step-1])

            var trace1 = {
              x: this.xAxisBA,
              y: this.yAxis,
              //width: this.WidthBar,
              name: 'Bal. Acc.',
              type: 'bar',
              orientation: 'h',
              marker: {
                color: 'rgb(0,225,225)'
              }
            };

            var trace2 = {
              x: this.xAxisFS,
              y: this.yAxis,
              //width: this.WidthBar,
              name: 'F1-Score',
              type: 'bar',
              orientation: 'h',
              marker: {
                color: 'rgb(225,0,225)'
              }
            };

            var data = [trace1, trace2];
            var height = 300
            var width = 255

            var layout = {
              yaxis: {
                autorange: 'reversed',
                title: 'Step of the Process',
                tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
                tickvals: this.yAxis
              },
              xaxis: {
                title: 'Performance Difference (%)',
                fixedrange: true
                // tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
                // tickvals: [0,20,40,60,80,100],
                // ticktext: ['0    ','20    ','40    ','60    ','80    ','100    '],
              },
              legend: {"orientation": "h", x: 0, y: 1.1},
              font: { family: 'Helvetica', size: 14, color: '#000000' },
              autosize: false,
              //bargap: 0.1,
              //bargroupgap: 0,
              width: width,
              height: height,
              dragmode: 'pan',
              barmode: 'group',
              hovermode: "closest",
              showlegend: true,
              margin: {
                l: 30,
                r: 12,
                b: 35,
                t: 0,
                pad: 0
              },
            }
        
            var config = {scrollZoom: true, displaylogo: false, displayModeBar: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'select2d', 'lasso2d', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: false}

            var graphDiv = document.getElementById("BarChartTest")
            Plotly.newPlot(graphDiv, data, layout, config)
            this.firstTime = 1
          } else if (this.firstTime == 4) {
            this.step = this.step + 1        
            this.yAxis.push(this.step)
            this.previousBA.push(this.previousBA[this.step-2])
            this.previousFM.push(this.previousFM[this.step-2])
            this.previousBATrain.push(this.previousBATrain[this.step-2])
            this.previousFMTrain.push(this.previousFMTrain[this.step-2])
            var diffBA = this.previousBA[this.step-2] - this.previousBA[this.step-1]
            var diffFM = this.previousFM[this.step-2] - this.previousFM[this.step-1]
            this.xAxisBA.push(diffBA)
            this.xAxisFS.push(diffFM)
            //this.WidthBar.push(2)
            EventBus.$emit('updateBACur', this.previousBA[this.step-2])
            EventBus.$emit('updateFMCur', this.previousFM[this.step-2])

            EventBus.$emit('updateBACurTrain', this.previousBATrain[this.step-2])
            EventBus.$emit('updateFMCurTrain', this.previousFMTrain[this.step-2])

            var trace1 = {
              x: this.xAxisBA,
              y: this.yAxis,
              //width: this.WidthBar,
              name: 'Bal. Acc.',
              type: 'bar',
              orientation: 'h',
              marker: {
                color: 'rgb(0,225,225)'
              }
            };

            var trace2 = {
              x: this.xAxisFS,
              y: this.yAxis,
              //width: this.WidthBar,
              name: 'F1-Score',
              type: 'bar',
              orientation: 'h',
              marker: {
                color: 'rgb(225,0,225)'
              }
            };

            var data = [trace1, trace2];
            var height = 300
            var width = 255

            var layout = {
              yaxis: {
                autorange: 'reversed',
                title: 'Step of the Process',
                tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
                tickvals: this.yAxis
              },
              xaxis: {
                title: 'Performance Difference (%)',
                fixedrange: true
                // tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
                // tickvals: [0,20,40,60,80,100],
                // ticktext: ['0    ','20    ','40    ','60    ','80    ','100    '],
              },
              legend: {"orientation": "h", x: 0, y: 1.1},
              font: { family: 'Helvetica', size: 14, color: '#000000' },
              autosize: false,
              //bargap: 0.1,
              //bargroupgap: 0,
              width: width,
              height: height,
              dragmode: 'pan',
              barmode: 'group',
              hovermode: "closest",
              showlegend: true,
              margin: {
                l: 30,
                r: 12,
                b: 35,
                t: 0,
                pad: 0
              },
            }
          
            var config = {scrollZoom: true, displaylogo: false, displayModeBar: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'select2d', 'lasso2d', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: false}

            var graphDiv = document.getElementById("BarChartTest")
            Plotly.newPlot(graphDiv, data, layout, config)
            this.firstTime = 1
          } else {
            this.firstTime = 1
          }
      },
    },
  mounted () {    
    EventBus.$on('firstTimeConfusion', data => { this.firstTime = data })
    EventBus.$on('emittedEventCallingPerformanceProb', data => { this.FinalResultsConf = data })
    EventBus.$on('emittedEventCallingPerformanceProb', this.FinalResultsConfView)
    EventBus.$on('emittedEventCallingPerformanceProb', this.BarChartView)

    EventBus.$on('reset', this.reset)
  }
}
</script>
