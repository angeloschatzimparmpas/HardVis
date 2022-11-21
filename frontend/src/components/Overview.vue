<template>
  <div id="BoxPlot" class="BoxPlot"></div>
</template>

<script>
import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'

export default {
  name: 'Overview',
  data () {
    return {
      barchartmetrics: '',
      SelBarChartMetrics: [],
      SelBarChartUnder: [],
      SelBarChartOver: [],
      mode: 0,
      getProposals: [],
      AdditionalData: [],
      dataSet: 'VehicleC',
    }
  },
  methods: {
    BoxPlotView () {
        Plotly.purge('BoxPlot')

        var width = 1228
        var height = 255

        var rowsInit = JSON.parse(this.barchartmetrics[6])
        var metricsPerModel = []
        var metricsPerModelAll = JSON.parse(rowsInit)
        var columnsInit = this.barchartmetrics[10]

        var columns = []
        if (this.dataSet == 'VehicleC') {
          var length = 7;
          for (let k = 0; k < columnsInit.length; k++) {
            columns.push(columnsInit[k].substring(0, length))
          }
          var typeIndex = columnsInit.indexOf("SkewAbMinor");
          if (typeIndex != -1)
            columns[typeIndex] = "SkewAMi"
          var typeIndex = columnsInit.indexOf("SkewAbMajor");
          if (typeIndex != -1)
            columns[typeIndex] = "SkewAMa"
          var typeIndex = columnsInit.indexOf("ScalVarMinor");
          if (typeIndex != -1)
            columns[typeIndex] = "ScalVaMi"
          var typeIndex = columnsInit.indexOf("ScalVarMajor");
          if (typeIndex != -1)
            columns[typeIndex] = "ScalVaMa"
        } else {
          for (let k = 0; k < columnsInit.length; k++) {
            columns.push(columnsInit[k])
          }
        }
        
        var typeIndex = columns.indexOf("# Type #");
        if (typeIndex != -1)
          columns.splice(typeIndex, 1);

        var typeIndex = columns.indexOf("# Type ");
        if (typeIndex != -1)
          columns.splice(typeIndex, 1);

        metricsPerModel = [...metricsPerModelAll]
        var eachTypeGeneric = this.AdditionalData[4]
        // if (this.AdditionalData.length == 0) {
          
        // } else {
        //   for (let i = 0; i < metricsPerModelAll.length; i++) {
        //     if (eachTypeGeneric.includes(i)) {
        //       metricsPerModel.push(metricsPerModelAll[i])
        //     }
        //   }
        // }

        var perModelAllClear = []
        var perModelAllClearMiddle = []
        var perModelSelectedClear = []
        var x = []

        if (this.mode == 0) {
          for (let i = 0; i < metricsPerModel.length; i++) {
            for (let j = 0; j < Object.values(Object.values(metricsPerModel)[i]).length; j++) {
              perModelAllClear.push(Object.values(Object.values(metricsPerModel)[i])[j])
              x.push(columns[j])
            }
          }

          var metricsPerModelSel = []
          if (this.SelBarChartMetrics.length == 0) {
            for (let i = 0; i < metricsPerModelAll.length; i++) {
              if (eachTypeGeneric.includes(i)) {
                metricsPerModelSel.push(metricsPerModelAll[i])
              }
            }
            // metricsPerModelSel = metricsPerModel
          } else {
            for (let looping=0; looping < metricsPerModelAll.length; looping++) {
              if (eachTypeGeneric.includes(looping)) {
                if (this.SelBarChartMetrics.includes(looping)) {
                  metricsPerModelSel.push(metricsPerModelAll[looping])
                }
              }
              //metricsPerModelSel.push(metricsPerModel[looping])
            }
          }

          for (let i = 0; i < metricsPerModelSel.length; i++) {
            for (let j = 0; j < Object.values(Object.values(metricsPerModelSel)[i]).length; j++) {
              perModelSelectedClear.push(Object.values(Object.values(metricsPerModelSel)[i])[j])
              x.push(columns[j])
            }
          }

          var trace1 = {
            x: x,
            y: perModelAllClear, 
            name: 'All Points', 
            type: 'box',
            boxmean: true,
            marker: {
                color: 'rgb(64,0,75)'
            }
          };
          var trace2 = {
            x: x,
            y: perModelSelectedClear, 
            name: 'Selected Points', 
            type: 'box',
            boxmean: true,
            marker: {
                color: 'rgb(194,165,207)'
            }
          };
          EventBus.$emit('updateSelGlobal', (perModelSelectedClear.length/columns.length))
          EventBus.$emit('updateAllGlobal', (perModelAllClear.length/columns.length))
          EventBus.$emit('updateSelSuggestion', 0)
          EventBus.$emit('updateAllSuggestion', 0)
          var data = [trace1, trace2];
        } else if (this.mode == 1) {

          var metricsPerModelSel = []
          if ((this.SelBarChartMetrics.length == 0) && (eachTypeGeneric.length == metricsPerModelAll.length)) {
            var symbols = this.getProposals[5]

            for (let looping=0; looping < metricsPerModel.length; looping++) {
              if (symbols.includes(looping))
                metricsPerModelSel.push(metricsPerModel[looping])
            } 

            for (let i = 0; i < metricsPerModel.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModel)[i]).length; j++) {
                perModelAllClear.push(Object.values(Object.values(metricsPerModel)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSel.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSel)[i]).length; j++) {
                perModelSelectedClear.push(Object.values(Object.values(metricsPerModelSel)[i])[j])
                x.push(columns[j])
              }
            }

            var trace1 = {
              x: x,
              y: perModelAllClear, 
              name: 'All Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(64,0,75)'
              }
            };
            var trace2 = {
              x: x,
              y: perModelSelectedClear, 
              name: 'All Points in Undersampling Suggestion',
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(251,106,74)'
              }
            }; 
            EventBus.$emit('updateSelGlobal', (perModelAllClear.length/columns.length))
            EventBus.$emit('updateAllGlobal', (perModelAllClear.length/columns.length))
            EventBus.$emit('updateSelSuggestion', (perModelSelectedClear.length/columns.length))
            EventBus.$emit('updateAllSuggestion', (perModelSelectedClear.length/columns.length))
            var data = [trace1, trace2];
          } else if ((this.SelBarChartMetrics.length == 0) && (eachTypeGeneric.length != metricsPerModelAll.length)) {
            var symbols = this.getProposals[5]
            var metricsPerModelSelWithout = []
            for (let looping=0; looping < metricsPerModelAll.length; looping++) {
              if (eachTypeGeneric.includes(looping)) {
                //if (this.SelBarChartMetrics.includes(looping)) {
                if (symbols.includes(looping)) {
                  metricsPerModelSel.push(metricsPerModelAll[looping])
                  metricsPerModelSelWithout.push(metricsPerModelAll[looping])
                } else {
                  metricsPerModelSelWithout.push(metricsPerModelAll[looping])
                }
                //}
              }
            }  
          
            // var symbols = this.getProposals[5]
            // var symbolsMerge = [].concat.apply([], symbols);

            // var keepUnderPosition = []
            // for (let i=0; i<symbolsMerge.length; i++) {
            //   if (symbolsMerge[i] == "x") {
            //     keepUnderPosition.push(i)
            //   }
            // }
            
            // for (let looping=0; looping < metricsPerModel.length; looping++) {
            //   if (keepUnderPosition.includes(looping))
            //     metricsPerModelSel.push(metricsPerModel[looping])
            // } 

            for (let i = 0; i < metricsPerModelAll.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelAll)[i]).length; j++) {
                perModelAllClear.push(Object.values(Object.values(metricsPerModelAll)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSelWithout.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSelWithout)[i]).length; j++) {
                perModelAllClearMiddle.push(Object.values(Object.values(metricsPerModelSelWithout)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSel.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSel)[i]).length; j++) {
                perModelSelectedClear.push(Object.values(Object.values(metricsPerModelSel)[i])[j])
                x.push(columns[j])
              }
            }

            var trace1 = {
              x: x,
              y: perModelAllClear, 
              name: 'All Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(64,0,75)'
              }
            };
            var trace2 = {
              x: x,
              y: perModelAllClearMiddle, 
              name: 'Selected Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(194,165,207)'
              }
            };
            var trace3 = {
              x: x,
              y: perModelSelectedClear, 
              name: 'Selected Points in Undersampling Suggestion',
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(251,106,74)'
              }
            }; 
            EventBus.$emit('updateSelGlobal', (perModelAllClearMiddle.length/columns.length))
            EventBus.$emit('updateAllGlobal', (perModelAllClear.length/columns.length))
            EventBus.$emit('updateSelSuggestion', (perModelSelectedClear.length/columns.length))
            var data = [trace1, trace2, trace3];
          } else {
            var metricsPerModelSelWithout = []
            for (let looping=0; looping < metricsPerModelAll.length; looping++) {
              if (eachTypeGeneric.includes(looping)) {
                if (this.SelBarChartMetrics.includes(looping)) {
                  if (this.SelBarChartUnder.includes(looping)) {
                    metricsPerModelSel.push(metricsPerModelAll[looping])
                    metricsPerModelSelWithout.push(metricsPerModelAll[looping])
                  } else {
                    metricsPerModelSelWithout.push(metricsPerModelAll[looping])
                  }
                }
              }
            }

            for (let i = 0; i < metricsPerModelAll.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelAll)[i]).length; j++) {
                perModelAllClear.push(Object.values(Object.values(metricsPerModelAll)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSelWithout.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSelWithout)[i]).length; j++) {
                perModelAllClearMiddle.push(Object.values(Object.values(metricsPerModelSelWithout)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSel.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSel)[i]).length; j++) {
                perModelSelectedClear.push(Object.values(Object.values(metricsPerModelSel)[i])[j])
                x.push(columns[j])
              }
            }

            var trace1 = {
              x: x,
              y: perModelAllClear, 
              name: 'All Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(64,0,75)'
              }
            };

            var trace2 = {
              x: x,
              y: perModelAllClearMiddle, 
              name: 'Selected Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(194,165,207)'
              }
            };
            var trace3 = {
              x: x,
              y: perModelSelectedClear, 
              name: 'Selected Points in Undersampling Suggestion',
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(251,106,74)'
              }
            };
            EventBus.$emit('updateSelGlobal', (perModelAllClearMiddle.length/columns.length))
            EventBus.$emit('updateAllGlobal', (perModelAllClear.length/columns.length))
            EventBus.$emit('updateSelSuggestion', (perModelSelectedClear.length/columns.length))
            var data = [trace1, trace2, trace3];
          } 
        } else { // Oversample
          var metricsPerModelSel = []
          if ((this.SelBarChartMetrics.length == 0) && (eachTypeGeneric.length == metricsPerModelAll.length)) {
            var symbols = this.getProposals[6]
            for (let looping=0; looping < metricsPerModel.length; looping++) {
              if (symbols.includes(looping))
                metricsPerModelSel.push(metricsPerModel[looping])
            } 

            for (let i = 0; i < metricsPerModel.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModel)[i]).length; j++) {
                perModelAllClear.push(Object.values(Object.values(metricsPerModel)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSel.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSel)[i]).length; j++) {
                perModelSelectedClear.push(Object.values(Object.values(metricsPerModelSel)[i])[j])
                x.push(columns[j])
              }
            }

            var trace1 = {
              x: x,
              y: perModelAllClear, 
              name: 'All Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(64,0,75)'
              }
            };
            var trace2 = {
              x: x,
              y: perModelSelectedClear, 
              name: 'All Points in Oversampling Suggestion',
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(116,196,118)'
              }
            }; 
            EventBus.$emit('updateSelGlobal', (perModelAllClear.length/columns.length))
            EventBus.$emit('updateAllGlobal', (perModelAllClear.length/columns.length))
            EventBus.$emit('updateSelSuggestion', this.AdditionalData[6].length)
            EventBus.$emit('updateAllSuggestion', this.AdditionalData[6].length)
            var data = [trace1, trace2];
          } else if ((this.SelBarChartMetrics.length == 0) && (eachTypeGeneric.length != metricsPerModelAll.length)) {
            var symbols = this.getProposals[6]
            var metricsPerModelSelWithout = []
            for (let looping=0; looping < metricsPerModelAll.length; looping++) {
              if (eachTypeGeneric.includes(looping)) {
                //if (this.SelBarChartMetrics.includes(looping)) {
                if (symbols.includes(looping)) {
                  metricsPerModelSel.push(metricsPerModelAll[looping])
                  metricsPerModelSelWithout.push(metricsPerModelAll[looping])
                } else {
                  metricsPerModelSelWithout.push(metricsPerModelAll[looping])
                }
                //}
              }
            }  
          
            // var symbols = this.getProposals[5]
            // var symbolsMerge = [].concat.apply([], symbols);

            // var keepUnderPosition = []
            // for (let i=0; i<symbolsMerge.length; i++) {
            //   if (symbolsMerge[i] == "x") {
            //     keepUnderPosition.push(i)
            //   }
            // }
            
            // for (let looping=0; looping < metricsPerModel.length; looping++) {
            //   if (keepUnderPosition.includes(looping))
            //     metricsPerModelSel.push(metricsPerModel[looping])
            // } 

            for (let i = 0; i < metricsPerModelAll.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelAll)[i]).length; j++) {
                perModelAllClear.push(Object.values(Object.values(metricsPerModelAll)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSelWithout.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSelWithout)[i]).length; j++) {
                perModelAllClearMiddle.push(Object.values(Object.values(metricsPerModelSelWithout)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSel.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSel)[i]).length; j++) {
                perModelSelectedClear.push(Object.values(Object.values(metricsPerModelSel)[i])[j])
                x.push(columns[j])
              }
            }

            var trace1 = {
              x: x,
              y: perModelAllClear, 
              name: 'All Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(64,0,75)'
              }
            };
            var trace2 = {
              x: x,
              y: perModelAllClearMiddle, 
              name: 'Selected Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(194,165,207)'
              }
            };
            var trace3 = {
              x: x,
              y: perModelSelectedClear, 
              name: 'Selected Points in Oversampling Suggestion',
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(116,196,118)'
              }
            }; 
            EventBus.$emit('updateSelGlobal', (perModelAllClearMiddle.length/columns.length))
            EventBus.$emit('updateAllGlobal', (perModelAllClear.length/columns.length))
            EventBus.$emit('updateSelSuggestion', (perModelSelectedClear.length/columns.length))
            EventBus.$emit('updateAllSuggestion', this.AdditionalData[6].length)
            var data = [trace1, trace2, trace3];
          } else {
            var metricsPerModelSelWithout = []
            for (let looping=0; looping < metricsPerModelAll.length; looping++) {
              if (eachTypeGeneric.includes(looping)) {
                if (this.SelBarChartMetrics.includes(looping)) {
                  if (this.SelBarChartOver.includes(looping)) {
                    metricsPerModelSel.push(metricsPerModelAll[looping])
                    metricsPerModelSelWithout.push(metricsPerModelAll[looping])
                  } else {
                    metricsPerModelSelWithout.push(metricsPerModelAll[looping])
                  }
                }
              }
            }

            for (let i = 0; i < metricsPerModelAll.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelAll)[i]).length; j++) {
                perModelAllClear.push(Object.values(Object.values(metricsPerModelAll)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSelWithout.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSelWithout)[i]).length; j++) {
                perModelAllClearMiddle.push(Object.values(Object.values(metricsPerModelSelWithout)[i])[j])
                x.push(columns[j])
              }
            }

            for (let i = 0; i < metricsPerModelSel.length; i++) {
              for (let j = 0; j < Object.values(Object.values(metricsPerModelSel)[i]).length; j++) {
                perModelSelectedClear.push(Object.values(Object.values(metricsPerModelSel)[i])[j])
                x.push(columns[j])
              }
            }

            var trace1 = {
              x: x,
              y: perModelAllClear, 
              name: 'All Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(64,0,75)'
              }
            };

            var trace2 = {
              x: x,
              y: perModelAllClearMiddle, 
              name: 'Selected Points', 
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(194,165,207)'
              }
            };
            var trace3 = {
              x: x,
              y: perModelSelectedClear, 
              name: 'Selected Points in Oversampling Suggestion',
              type: 'box',
              boxmean: true,
              marker: {
                  color: 'rgb(116,196,118)'
              }
            };
            EventBus.$emit('updateSelGlobal', (perModelAllClearMiddle.length/columns.length))
            EventBus.$emit('updateAllGlobal', (perModelAllClear.length/columns.length))
            EventBus.$emit('updateSelSuggestion', (perModelSelectedClear.length/columns.length))
            var data = [trace1, trace2, trace3];
          }
        }

        var layout = {
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        boxmode: 'group',
        legend: {"orientation": "h", x:0.5,xanchor: "center",y:1.2,yanchor: "center"},
        autosize: true,
        width:  width,
        height: height,
        hovermode: 'x',
        margin: {
          l: 50,
          r: 0,
          b: 35,
          t: 0,
          pad: 0
        },
        xaxis: {
            title: 'Feature',
            titlefont: {
            size: 16,
            color: 'black'
            }},
        yaxis: {
            title: 'Normalized Values Distribution',
            titlefont: {
            size: 16,
            color: 'black'
            }}};

        var boxPlot = document.getElementById('BoxPlot');

        var config = {displayModeBar: false, scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
        
        Plotly.newPlot(boxPlot, data, layout, config);
      },
      reset () {
        Plotly.purge('BoxPlot')
      }
    },
    mounted () {
      EventBus.$on('SendToServerDataSetConfirmation', data => { this.dataSet = data })

      EventBus.$on('emittedEventCallingAdditionalDataHeatmap', data => {this.getProposals = data;})
      EventBus.$on('updateMode', data => {this.SelBarChartMetrics = [];})
      EventBus.$on('updateMode', data => {this.mode = data;})
      
      EventBus.$on('SendSelectedPointsUpdateIndicatorUn', data => {this.SelBarChartUnder = data;})
      EventBus.$on('SendSelectedPointsUpdateIndicatorOv', data => {this.SelBarChartOver = data;})

      EventBus.$on('emittedEventCallingPerformanceProb', data => {this.barchartmetrics = data;})
      EventBus.$on('emittedEventCallingPerformanceProb', this.BoxPlotView)

      EventBus.$on('limitPointsClear', data => {this.SelBarChartMetrics = data;})
      EventBus.$on('limitPoints', data => {this.SelBarChartMetrics = data;})
      EventBus.$on('emittedEventCallingAdditionalDataOverview', data => {this.AdditionalData = data;})
      EventBus.$on('emittedEventCallingPerformanceUpdate', this.BoxPlotView)
      EventBus.$on('emittedEventCallingPerformanceUpdateHeat', this.BoxPlotView)

      // reset view
      EventBus.$on('resetViews', this.reset)
    }
}
</script>