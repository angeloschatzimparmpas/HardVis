<template>
  <div id="Scatterplot"></div>
</template>

<script>

import { EventBus } from '../main.js'
import * as Plotly from 'plotly.js'

export default {
  name: 'Space',
  data () {
    return {
      FinalResultsScatter: 0,
      FinalResultsExtra: 0,
      selectionStatusHeat: -1,
      keyOnce: true
    }
  },
  methods: {
      reset () {
        Plotly.purge('Scatterplot')
      },
      ScatterplotView() {

        Plotly.purge('Scatterplot')

        var XDataNorm = JSON.parse(JSON.parse(this.FinalResultsScatter[11]))
        if (this.keyOnce) {
          EventBus.$emit('emittedEventUpdateSlider', this.FinalResultsScatter)
        }
        var groundTruthOriginal = this.FinalResultsScatter[2]
        var UMAPDataOriginal = this.FinalResultsScatter[9]
        var symbolsPerClass = this.FinalResultsExtra[0]
        var colorMarkersPerClass = this.FinalResultsExtra[1]
        var limitInstances = this.FinalResultsExtra[2]
        var stringParameters = this.FinalResultsExtra[3]
        var groundTruth = this.FinalResultsExtra[4]
        var opacities = this.FinalResultsExtra[5]
        var colorRange = ['rgba(255,127,0,1)','rgba(31,120,180,1)','rgba(223,101,176,1)','rgba(77,175,74,1)']
        var colorRangeAlternative = ['rgba(84,48,5,1)', 'rgba(140,81,10,1)', 'rgba(191,129,45,1)', 'rgba(223,194,125,1)', 'rgba(246,232,195,1)', 'rgba(199,234,229,1)', 'rgba(128,205,193,1)', 'rgba(53,151,143,1),', 'rgba(1,102,94,1)', 'rgba(0,60,48,1)']
        var colors = []

        var UMAPDataY1 = []
        var UMAPDataX1 = []
        var UMAPDataY2 = []
        var UMAPDataX2 = []
        var UMAPDataY3 = []
        var UMAPDataX3 = []

        var symbolsPerClassMerg = [].concat.apply([], symbolsPerClass);
        var colorMarkersPerClassMerg = [].concat.apply([], colorMarkersPerClass);
        var stringParametersMerg = [].concat.apply([], stringParameters);
        var groundTruthMerg = [].concat.apply([], groundTruth);
        var opacitiesMerg = [].concat.apply([], opacities);

        var flag2Classes = true
        for (let k = 0; k < limitInstances.length; k++) {
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

        var data = []

        if (this.selectionStatusHeat == -1) {
          for (let i = 0; i < groundTruthMerg.length; i++) {
            colors.push(colorRange[groundTruthMerg[i]])
          }
        } else {
          for (let i = 0; i < XDataNorm.length; i++) {
            if ((Object.values(XDataNorm[i])[this.selectionStatusHeat]) >= 0.9)
              colors.push(colorRangeAlternative[9])
            else if ((Object.values(XDataNorm[i])[this.selectionStatusHeat]) >= 0.8)
              colors.push(colorRangeAlternative[8])
            else if ((Object.values(XDataNorm[i])[this.selectionStatusHeat]) >= 0.7)
              colors.push(colorRangeAlternative[7])
            else if ((Object.values(XDataNorm[i])[this.selectionStatusHeat]) >= 0.6)
              colors.push(colorRangeAlternative[6])
            else if ((Object.values(XDataNorm[i])[this.selectionStatusHeat]) >= 0.5)
              colors.push(colorRangeAlternative[5])
            else if ((Object.values(XDataNorm[i])[this.selectionStatusHeat]) >= 0.4)
              colors.push(colorRangeAlternative[4])
            else if ((Object.values(XDataNorm[i])[this.selectionStatusHeat]) >= 0.3)
              colors.push(colorRangeAlternative[3])
            else if ((Object.values(XDataNorm[i])[this.selectionStatusHeat]) >= 0.2)
              colors.push(colorRangeAlternative[2])
            else if ((Object.values(XDataNorm[i])[this.selectionStatusHeat]) >= 0.1)
              colors.push(colorRangeAlternative[1])
            else
              colors.push(colorRangeAlternative[0])
          }
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
            text: stringParametersMerg,
            marker: {
              color: colors,
              symbol: symbolsPerClassMerg,
              size: 16,
              line: {
                color: colorMarkersPerClassMerg,
                width: 3
              },
              opacity: opacitiesMerg
            },
          })

          var width = 1228
          var height = 1025

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
            dragmode: 'lasso',
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
      
          var config = {scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: true}

          var graphDiv = document.getElementById("Scatterplot")
          Plotly.newPlot(graphDiv, data, layout, config)

          graphDiv.on('plotly_selected', function(evt) {
            if (typeof evt !== 'undefined') {
              var ClassifierIDsListCleared = []
              var ClassifierIDsListOv = []
              var ClassifierIDsListUn = []
              for (let i = 0; evt.points.length; i++) {
                if (evt.points[i] === undefined) {
                  break
                } else {
                  var splittedHover = evt.points[i].text.split(/[ ,]+/)
                  var symbol = evt.points[i]["marker.symbol"]
                  var ID = parseInt(splittedHover[1])
                  if (symbol == "x")
                    ClassifierIDsListUn.push(ID)
                  if (symbol == "cross")
                    ClassifierIDsListOv.push(ID)
                  ClassifierIDsListCleared.push(ID)
                }
              }
              EventBus.$emit('limitPoints', ClassifierIDsListCleared)
              EventBus.$emit('SendSelectedPointsUpdateIndicatorUn', ClassifierIDsListUn)
              EventBus.$emit('SendSelectedPointsUpdateIndicatorOv', ClassifierIDsListOv)
              EventBus.$emit('emittedEventCallingPerformanceUpdateHeat')
            }
          });

      }
    },
  mounted () {    
    EventBus.$on('emittedEventCallingAdditionalData', data => { this.FinalResultsExtra = data })
    EventBus.$on('emittedEventCallingPerformanceUpdate', this.ScatterplotView)
    EventBus.$on('emittedEventCallingPerformanceProb', data => { this.FinalResultsScatter = data })
    EventBus.$on('emittedEventCallingPerformanceProb', this.ScatterplotView)
    EventBus.$on('updateClickedHeat', data => { this.selectionStatusHeat = data })
    EventBus.$on('updateClickedHeat', this.ScatterplotView)

    EventBus.$on('reset', this.reset)
  }
}
</script>