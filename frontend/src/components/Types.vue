<template>
  <div id="BarChart"></div>
</template>

<script>

import { EventBus } from '../main.js'
import * as Plotly from 'plotly.js'

export default {
  name: 'Types',
  data () {
    return {
      FinalResultsBar: [],
      FinalResultsBarPrevious: [],
      FinalResultsBarSuggestion: [],
      FinalGeneralResults: [],
      removalSankey: [],
      additionSankey: [],
      modeOvUn: 0,
    }
  },
  methods: {
      reset () {
        Plotly.purge('BarChart')
      },
      BarChartView() {
        var modeOvOrUn = this.modeOvUn
        
        Plotly.purge('BarChart')
        
        var categories = JSON.parse(this.FinalGeneralResults[1]).reverse()
        var distribution = this.FinalResultsBar
        var distributionPrevious = this.FinalResultsBarPrevious
        var distributionSuggestion = this.FinalResultsBarSuggestion
        var removal = this.removalSankey
        var addition = this.additionSankey
        var colorOutlines = ['rgba(217,217,217,1)','rgba(150,150,150,1)','rgba(82,82,82,1)','rgba(0,0,0,1)']
        var types = ['Safe (S)','Borderline (B)','Rare (R)','Outlier (O)']

        var traverseArray = []
        var resultingArray = []
        var traverseArraySuggestion = []
        var resultingArraySuggestion = []
        var differenceArray = []
        var differenceArrayStore= []
        var removalArray = []
        var removalArrayStore = []
        var additionArray = []
        var additionArrayStore = []

        for (let k = 0; k < types.length; k++) {
          traverseArray = []
          traverseArraySuggestion = []
          differenceArray = []
          removalArray = []
          additionArray = []
          for (let m = 0; m < distribution.length; m++) {
            traverseArray.push(distribution[m][k])
            if (distributionSuggestion.length == 0) {
              traverseArraySuggestion.push(0)
            } else {
              traverseArraySuggestion.push(distributionSuggestion[m][k])
            }
            additionArray.push(addition[m][k])
          }
          for (let m = 0; m < distributionPrevious.length; m++) {
            differenceArray.push(distributionPrevious[m][k])
            removalArray.push(removal[m][k])
          }
          resultingArray.push(traverseArray)
          resultingArraySuggestion.push(traverseArraySuggestion)
          differenceArrayStore.push(differenceArray)
          removalArrayStore.push(removalArray)
          additionArrayStore.push(additionArray)
        }
        
        var combineArrays = []
        combineArrays.push(differenceArrayStore)
        combineArrays.push(removalArrayStore)
        combineArrays.push(additionArrayStore)
        EventBus.$emit('HistoryCall', combineArrays)

        var data = []
        if (modeOvOrUn == 2) {
          for (var i = (types.length-1); i >= 0; i--) {
            data.push({
              type: 'bar',
              name: types[i],
              x: categories,
              y: resultingArraySuggestion[i],
              xaxis: 'x2',
              barmode: 'stack', 
              marker: {
                color: colorOutlines[i]
              },
              showlegend:true,
            })  
          }

          for (var i = (types.length-1); i >= 0; i--) {
            data.push({
              type: 'bar',
              name: types[i],
              x: categories,
              y: resultingArray[i],
              xaxis: 'x1',
              barmode: 'stack', 
              marker: {
                color: colorOutlines[i]
              },
              showlegend:false
            })  
          }
        } else {
          for (var i = (types.length-1); i >= 0; i--) {
            data.push({
              type: 'bar',
              name: types[i],
              x: categories,
              y: resultingArraySuggestion[i],
              xaxis: 'x2',
              barmode: 'stack', 
              marker: {
                color: colorOutlines[i]
              },
              showlegend:false,
            })  
          }

          for (var i = (types.length-1); i >= 0; i--) {
            data.push({
              type: 'bar',
              name: types[i],
              x: categories,
              y: resultingArray[i],
              xaxis: 'x1',
              barmode: 'stack', 
              marker: {
                color: colorOutlines[i]
              },
              showlegend:true
            })  
          }
        }

          var width = 615
          var height = 300

          var layout = {
            yaxis: {
              title: 'Number of Instances'
            },
            xaxis: {
              domain: [0, 0.50],
              anchor: 'x1', 
              title: 'Base'
            },
            xaxis2: {
              domain: [0.50, 1],
              anchor: 'x2', 
              title: 'Suggestion'
            },
            barmode: 'stack',
            font: { family: 'Helvetica', size: 14, color: '#000000' },
            autosize: false,
            width: width,
            height: height,
            // showlegend: true,
            // legend: {"orientation": "h", x: 0.08, y: 1.1},
            legend: {"orientation": "h", x:0.08, y: 1.1},
            margin: {
              l: 50,
              r: 0,
              b: 40,
              t: 0,
              pad: 0
            },
          }
      
          var myPlot = document.getElementById('BarChart')

          var config = {scrollZoom: false, displaylogo: false, displayModeBar: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: true}

          Plotly.newPlot(myPlot, data, layout, config)

          myPlot.on('plotly_legendclick', function(data){
            var specificLegend = data.data[data.curveNumber]
            if (specificLegend.visible == "legendonly") {
              EventBus.$emit('limitPoints', [])
              if (modeOvOrUn == 2) {
                EventBus.$emit('ActivateType', data.curveNumber)
              } else {
                EventBus.$emit('ActivateType', data.curveNumber-4)
              }
              EventBus.$emit('emittedEventCallingPerformanceUpdate')
            }
            else {
              EventBus.$emit('limitPoints', [])
              if (modeOvOrUn == 2) {
                EventBus.$emit('deActivateType', data.curveNumber)
              } else {
                EventBus.$emit('deActivateType', data.curveNumber-4)
              }
              EventBus.$emit('emittedEventCallingPerformanceUpdate')
            }
          });
          
      }
    },
  mounted () {  
    EventBus.$on('updateMode', data => { this.modeOvUn = data })
    EventBus.$on('SendSelectedPointsUpdateIndicatorOver', data => { this.FinalResultsBar = this.FinalResultsBarSuggestion })
      
    EventBus.$on('SendSankey', data => { this.removalSankey = data })
    EventBus.$on('SendSankeyAddition', data => { this.additionSankey = data })
    EventBus.$on('VisualizeDistributionOfTypes', data => { this.FinalResultsBar = data })
    EventBus.$on('VisualizeDistributionOfTypesPrevious', data => { this.FinalResultsBarPrevious = data })
    EventBus.$on('VisualizeDistributionOfTypesSuggestion', data => { this.FinalResultsBarSuggestion = data })
    EventBus.$on('emittedEventCallingPerformanceUpdateHeat', this.BarChartView)
    EventBus.$on('emittedEventCallingPerformanceProb', data => { this.FinalGeneralResults = data })
    EventBus.$on('emittedEventCallingPerformanceProb', this.BarChartView)

    EventBus.$on('reset', this.reset)
  }
}
</script>