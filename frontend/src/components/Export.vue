<template>
  <div>
    <div id="ExportResults"></div>
    <div style="position: absolute; margin-top:-716px;">{{firstLabel}}</div>
    <div style="position: absolute; margin-top:-716px; margin-left: 348px">{{secondLabel}}</div>
    <div style="position: absolute; margin-top:-716px; margin-left: 695px">{{thirdLabel}}</div>
    <div style="position: absolute; margin-top:-370px">{{fourthLabel}}</div>
    <div style="position: absolute; margin-top:-370px; margin-left: 348px">{{fifthLabel}}</div>
    <div style="position: absolute; margin-top:-370px; margin-left: 695px">{{sixthLabel}}</div>
    <div style="position: absolute; margin-top:-22px">{{seventhLabel}}</div>
    <div style="position: absolute; margin-top:-22px; margin-left: 348px">{{eighthLabel}}</div>
    <div style="position: absolute; margin-top:-22px; margin-left: 695px">{{ninthLabel}}</div>
  </div>
</template>

<script>

import { EventBus } from '../main.js'
import * as Plotly from 'plotly.js'

export default {
  name: 'Space',
  data () {
    return {
      FinalResultsProject: 0,
      firstLabel: '',
      secondLabel: '',
      thirdLabel: '',
      fourthLabel: '',
      fifthLabel: '',
      sixthLabel: '',
      seventhLabel: '',
      eighthLabel: '',
      ninthLabel: '',
      kValues: [5,6,7,8,9,10,11,12,13],
      mDistValues: [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
    }
  },
  methods: {
      reset () {
        Plotly.purge('ExportResults')
      },
      ProjectionplotView() {

        Plotly.purge('ExportResults')

        var groundTruthOriginal = this.FinalResultsProject[2]
        var SDC = JSON.parse(this.FinalResultsProject[29])
        var indices = JSON.parse(this.FinalResultsProject[30])
        this.firstLabel = '' + SDC[0].toFixed(2) + '%, ' + this.kValues[0] + ', ' + this.mDistValues[indices[0]] + ''
        this.secondLabel = '' + SDC[1].toFixed(2) + '%, ' + this.kValues[1] + ', ' + this.mDistValues[indices[1]] + ''
        this.thirdLabel = '' + SDC[2].toFixed(2) + '%, ' + this.kValues[2] + ', ' + this.mDistValues[indices[2]] + ''
        this.fourthLabel = '' + SDC[3].toFixed(2) + '%, ' + this.kValues[3] + ', ' + this.mDistValues[indices[3]] + ''
        this.fifthLabel = '' + SDC[4].toFixed(2) + '%, ' + this.kValues[4] + ', ' + this.mDistValues[indices[4]] + ''
        this.sixthLabel = '' + SDC[5].toFixed(2) + '%, ' + this.kValues[5] + ', ' + this.mDistValues[indices[5]] + ''
        this.seventhLabel = '' + SDC[6].toFixed(2) + '%, ' + this.kValues[6] + ', ' + this.mDistValues[indices[6]] + ''
        this.eighthLabel = '' + SDC[7].toFixed(2) + '%, ' + this.kValues[7] + ', ' + this.mDistValues[indices[7]] + ''
        this.ninthLabel = '' + SDC[8].toFixed(2) + '%, ' + this.kValues[8] + ', ' + this.mDistValues[indices[8]] + ''
        var yData = this.FinalResultsProject[2]
        var colorRange = ['rgba(255,127,0,1)','rgba(31,120,180,1)','rgba(223,101,176,1)','rgba(77,175,74,1)']
        var colorOutlines = ['rgba(240,240,240,1)','rgba(189,189,189,1)','rgba(115,115,115,1)','rgba(0,0,0,1)']
        var data = []

        for (var j = 0; j < 9; j++) {
          var colors = []
          var colorMarkersPerClassMerg = []
          var opacities = []
          var UMAPDataY1 = []
          var UMAPDataX1 = []
          var UMAPDataY2 = []
          var UMAPDataX2 = []
          var UMAPDataY3 = []
          var UMAPDataX3 = []
          var safe = JSON.parse(this.FinalResultsProject[24])[j]
          var border = JSON.parse(this.FinalResultsProject[25])[j]
          var rare = JSON.parse(this.FinalResultsProject[26])[j]
          var outlier = JSON.parse(this.FinalResultsProject[27])[j]
          
          var UMAPDataOriginal = JSON.parse(this.FinalResultsProject[28])[j]
          var flag2Classes = true
          for (let k = 0; k < yData.length; k++) {
            opacities.push(0.7)
            colors.push(colorRange[groundTruthOriginal[k]])
            if (safe.includes(k)) {
              colorMarkersPerClassMerg.push(colorOutlines[0])
            } else if (border.includes(k)) {
              colorMarkersPerClassMerg.push(colorOutlines[1])
            } else if (rare.includes(k)) {
              colorMarkersPerClassMerg.push(colorOutlines[2])
            }
            else {
              colorMarkersPerClassMerg.push(colorOutlines[3])
            }
            if (groundTruthOriginal[k] == 0) {
              UMAPDataX1.push(UMAPDataOriginal[0][k])
              UMAPDataY1.push(UMAPDataOriginal[1][k])
            } else if (groundTruthOriginal[k] == 1) {
              UMAPDataX2.push(UMAPDataOriginal[0][k])
              UMAPDataY2.push(UMAPDataOriginal[1][k])
            } else {
              flag2Classes = false
              UMAPDataX3.push(UMAPDataOriginal[0][k])
              UMAPDataY3.push(UMAPDataOriginal[1][k])
            }
          }
          if (flag2Classes) {
            var UMAPDataX = UMAPDataX1.concat(UMAPDataX2);
            var UMAPDataY = UMAPDataY1.concat(UMAPDataY2);
          } else {
            var UMAPDataX = UMAPDataX1.concat(UMAPDataX2, UMAPDataX3);
            var UMAPDataY = UMAPDataY1.concat(UMAPDataY2, UMAPDataY3);
          }

          data.push(
            {
              type: 'scatter',
              mode: 'markers',
              x: UMAPDataX,
              y: UMAPDataY,
              hoverinfo: 'skip',
              marker: {
                color: colors,
                size: 8,
                line: {
                  color: colorMarkersPerClassMerg,
                  width: 2
                },
                opacity: opacities
              },
              xaxis: 'x'+parseInt(j+1),
              yaxis: 'y'+parseInt(j+1),
            })
          }

          var width = 1050
          var height = 1050

          var layout = {
            xaxis: {
                linecolor: 'black',
                linewidth: 1,
                mirror: true,
                showgrid: false,
                zeroline: false,
                anchor: 'y1',
                domain: [0, 0.33],
                showticklabels: false,
            },
            yaxis: {
                linecolor: 'black',
                linewidth: 1,
                mirror: true,
                showgrid: false,
                zeroline: false,
                anchor: 'x1',
                domain: [0.66, 1],
                showticklabels: false
            },
            xaxis2: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              anchor: 'y2',
              domain: [0.33, 0.66],
              zeroline: false,
              showticklabels: false
            },
            yaxis2: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              anchor: 'x2',
              domain: [0.66, 1],
              zeroline: false,
              showticklabels: false
            },
            xaxis3: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'y3',
              domain: [0.66, 1],
              showticklabels: false
            },
            yaxis3: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'x3',
              domain: [0.66, 1],
              showticklabels: false
            },
            xaxis4: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'y4',
              domain: [0, 0.33],
              showticklabels: false
            },
            yaxis4: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'x4',
              domain: [0.33, 0.66],
              showticklabels: false
            },
            xaxis5: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'y5',
              domain: [0.33, 0.66],
              showticklabels: false
            },
            yaxis5: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'x5',
              domain: [0.33, 0.66],
              showticklabels: false
            },
            xaxis6: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'y6',
              domain: [0.66, 1],
              showticklabels: false
            },
            yaxis6: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'x6',
              domain: [0.33, 0.66],
              showticklabels: false
            },
            xaxis7: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'y7',
              domain: [0, 0.33],
              showticklabels: false
            },
            yaxis7: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'x7',
              domain: [0, 0.33],
              showticklabels: false
            },
            xaxis8: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'y8',
              domain: [0.33, 0.66],
              showticklabels: false
            },
            yaxis8: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'x8',
              domain: [0, 0.33],
              showticklabels: false
            },
            xaxis9: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'y9',
              domain: [0.66, 1.0],
              showticklabels: false
            },
            yaxis9: {
              linecolor: 'black',
              linewidth: 1,
              mirror: true,
              showgrid: false,
              zeroline: false,
              anchor: 'x9',
              domain: [0, 0.33],
              showticklabels: false
            },
            font: { family: 'Helvetica', size: 14, color: '#000000' },
            autosize: true,
            width: width,
            height: height,
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
      
          var config = {scrollZoom: true, displaylogo: false, displayModeBar: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: true}

          var graphDiv = document.getElementById("ExportResults")
          Plotly.newPlot(graphDiv, data, layout, config)

      }
    },
  mounted () {    

    EventBus.$on('emittedEventCallingPerformanceProb', data => { this.FinalResultsProject = data })
    EventBus.$on('emittedEventCallingPerformanceProb', this.ProjectionplotView)

    EventBus.$on('reset', this.reset)
  }
}
</script>

<style scoped>
#ExportResults {
  word-break: break-all !important;
}
</style>