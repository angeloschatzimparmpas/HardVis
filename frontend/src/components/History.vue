<template>
  <div id="SankeyDiagram" style="overflow: auto; width: 615px"></div>
</template>

<script>

import { EventBus } from '../main.js'
import * as Plotly from 'plotly.js'
import $ from 'jquery'; // <-to import jquery

export default {
  name: 'History',
  data () {
    return {
      FinalResultsSankey: 0,
      FinalResultsGlob: 0,
      storeTypes: [],
      storeSources: [],
      storeTargets: [],
      storeRemoval: [],
      storeAddition: [],
      layers: 0,
      each: 5,
      Execute: true,
      Mode: -1,
      firstTime: true,
      labels: [],
      colors: [],
      sources: [],
      targets: [],
      values: [],
      colorLinks: [],
      widthGlobal: 0
    }
  },
  methods: {
      reset () {
        Plotly.purge('SankeyDiagram')
      },
      SankeyDiagramView () {
        if (this.Execute) {
          this.Execute = false
          Plotly.purge('SankeyDiagram')
    
        if (this.firstTime) {
            this.storeTypes = []
            this.storeRemoval = []
            this.storeAddition = []
            this.labels = []
            this.colors = []
            this.sources = []
            this.targets = []
            this.values = []
            this.colorLinks = []
            this.storeSources = []
            this.storeTargets = []
            this.layers = 0
            this.widthGlobal = 0
            this.Mode = -1

            var categories = JSON.parse(this.FinalResultsGlob[1])
            var types = this.FinalResultsSankey[0]
            this.storeTypes.push(types)
            var removal = this.FinalResultsSankey[1]
            this.storeRemoval.push(removal)
            var addition = this.FinalResultsSankey[2]
            this.storeAddition.push(addition)

            var sourceNodes = []
            var targetNodes = []  
            var labelsLegend = ['All Data', 'S','B','R','O','US','OS']
            var colorsLegend = ["#ffffff","#d9d9d9","#969696","#525252","#000000","#67000d","#00441b"] 
            var colorRange = ['rgba(255,127,0,0.5)','rgba(31,120,180,0.5)','rgba(223,101,176,0.5)','rgba(77,175,74,0.5)']
            sourceNodes.push(0)
            targetNodes.push(1)
            targetNodes.push(2)
            targetNodes.push(3)
            targetNodes.push(4)
            this.storeSources.push(targetNodes)
              this.labels.push(labelsLegend[this.layers])
              this.colors.push(colorsLegend[this.layers])
              for (var i = 0; i < targetNodes.length; i++) {
                for (var j = 0; j < categories.length; j++) {
                  this.sources.push(sourceNodes[this.layers])
                  this.targets.push(targetNodes[i])
                  this.values.push(this.storeTypes[this.layers][i][j])
                  this.colorLinks.push(colorRange[j])
                }
                this.labels.push(labelsLegend[i+1])
                this.colors.push(colorsLegend[i+1])
              }
            this.layers = this.layers + 1
            this.firstTime = false
          } else {
            if (this.Mode == 0) {
              var labelsLegend = ['S','B','R','O','US']
              var colorsLegend = ["#d9d9d9","#969696","#525252","#000000","#67000d"] 
              var colorRange = ['rgba(255,127,0,0.5)','rgba(31,120,180,0.5)','rgba(223,101,176,0.5)','rgba(77,175,74,0.5)']

              var categories = JSON.parse(this.FinalResultsGlob[1])
              var types = this.FinalResultsSankey[0]
              this.storeTypes.push(types)
              var removal = this.FinalResultsSankey[1]
              this.storeRemoval.push(removal)
              var addition = this.FinalResultsSankey[2]
              this.storeAddition.push(addition)

              var targetNodes = []
              targetNodes.push(0+(this.layers*this.each))
              targetNodes.push(1+(this.layers*this.each))
              targetNodes.push(2+(this.layers*this.each))
              targetNodes.push(3+(this.layers*this.each))
              targetNodes.push(4+(this.layers*this.each))
              for (var i = 0; i < this.storeSources[this.layers-1].length; i++) {
                for (var j = 0; j < categories.length; j++) {
                  this.sources.push(this.storeSources[this.layers-1][i])
                  this.targets.push(targetNodes[i])
                  if (i >= this.storeTypes[this.layers].length) {
                    this.values.push(0.01)
                    this.colorLinks.push('rgba(255,255,255,0)')
                  } else{
                    this.values.push(this.storeTypes[this.layers][i][j] - this.storeRemoval[this.layers][i][j])
                    this.colorLinks.push(colorRange[j])
                  }
                }
                this.labels.push(labelsLegend[i])
                this.colors.push(colorsLegend[i])
              }
              // for (var i = 0; i < this.storeSources[k].length; i++) {
              //   labels.push(labelsLegend[i])
              //   colors.push(colorsLegend[i])
              // }
              for (var i = 0; i < this.storeSources[this.layers-1].length; i++) {
                for (var j = 0; j < categories.length; j++) {
                  this.sources.push(this.storeSources[this.layers-1][i])
                  this.targets.push(targetNodes[targetNodes.length-1])
                  if (i >= this.storeTypes[this.layers].length) {
                    this.values.push(0.01)
                    this.colorLinks.push('rgba(255,255,255,0)')
                  } else{
                    this.values.push(this.storeRemoval[this.layers][i][j])
                    this.colorLinks.push(colorRange[j])
                  }
                }
              }
              if (this.layers <= 1) {
                this.labels.push(labelsLegend[targetNodes.length-1])
                this.colors.push(colorsLegend[targetNodes.length-1])
              }
              // }
              // for (var i = 0; i < targetNodes[5].length; i++) {
              //   for (var j = 0; j < categories.length; j++) {
              //     sources.push(this.storeSources[k][i])
              //     targets.push(this.storeTargets[k][4])
              //     values.push(this.storeRemoval[k][i][j])
              //     colorLinks.push(colorRange[j])

              //   }
              // }
              // labels.push(labelsLegend[4])
              // colors.push(colorsLegend[4])
              // for (var i = 0; i < sourceNodes.length; i++) {
              //   for (var j = 0; j < categories.length; j++) {
              //     sources.push(sourceNodes[i])
              //     targets.push(targetNodes[5])
              //     values.push(addition[i][j])
              //     colorLinks.push(colorRange[j])

              //   }
              // }
              // labels.push(labelsLegend[5])
              // colors.push(colorsLegend[5])
              //targetNodes.pop()
              this.storeSources.push(targetNodes)
              this.layers = this.layers + 1
            } else {
              var labelsLegend = ['S','B','R','O','OS']
              var colorsLegend = ["#d9d9d9","#969696","#525252","#000000","#00441b"] 
              var colorRange = ['rgba(255,127,0,0.5)','rgba(31,120,180,0.5)','rgba(228,26,28,0.5)','rgba(77,175,74,0.5)']

              var categories = JSON.parse(this.FinalResultsGlob[1])
              var types = this.FinalResultsSankey[0]
              this.storeTypes.push(types)
              var removal = this.FinalResultsSankey[1]
              this.storeRemoval.push(removal)
              var addition = this.FinalResultsSankey[2]
              this.storeAddition.push(addition)

              var targetNodes = []
              targetNodes.push(0+(this.layers*this.each))
              targetNodes.push(1+(this.layers*this.each))
              targetNodes.push(2+(this.layers*this.each))
              targetNodes.push(3+(this.layers*this.each))
              targetNodes.push(4+(this.layers*this.each))
              for (var i = 0; i < this.storeSources[this.layers-1].length; i++) {
                for (var j = 0; j < categories.length; j++) {
                  this.sources.push(this.storeSources[this.layers-1][i])
                  this.targets.push(targetNodes[i])
                  if (i >= this.storeTypes[this.layers].length) {
                    this.values.push(0.01)
                    this.colorLinks.push('rgba(255,255,255,0)')
                  } else{
                    this.values.push(this.storeTypes[this.layers][i][j] - this.storeAddition[this.layers][i][j])
                    this.colorLinks.push(colorRange[j])
                  }
                }
                this.labels.push(labelsLegend[i])
                this.colors.push(colorsLegend[i])
              }
              // for (var i = 0; i < this.storeSources[k].length; i++) {
              //   labels.push(labelsLegend[i])
              //   colors.push(colorsLegend[i])
              // }
              for (var i = 0; i < this.storeSources[this.layers-1].length; i++) {
                for (var j = 0; j < categories.length; j++) {
                  this.sources.push(this.storeSources[this.layers-1][i])
                  this.targets.push(targetNodes[targetNodes.length-1])
                  if (i >= this.storeTypes[this.layers].length) {
                    this.values.push(0.01)
                    this.colorLinks.push('rgba(255,255,255,0)')
                  } else{
                    this.values.push(this.storeAddition[this.layers][i][j])
                    this.colorLinks.push(colorRange[j])
                  }
                }
              }
              if (this.layers <= 1) {
                this.labels.push(labelsLegend[targetNodes.length-1])
                this.colors.push(colorsLegend[targetNodes.length-1])
              }
              // }
              // for (var i = 0; i < targetNodes[5].length; i++) {
              //   for (var j = 0; j < categories.length; j++) {
              //     sources.push(this.storeSources[k][i])
              //     targets.push(this.storeTargets[k][4])
              //     values.push(this.storeRemoval[k][i][j])
              //     colorLinks.push(colorRange[j])

              //   }
              // }
              // labels.push(labelsLegend[4])
              // colors.push(colorsLegend[4])
              // for (var i = 0; i < sourceNodes.length; i++) {
              //   for (var j = 0; j < categories.length; j++) {
              //     sources.push(sourceNodes[i])
              //     targets.push(targetNodes[5])
              //     values.push(addition[i][j])
              //     colorLinks.push(colorRange[j])

              //   }
              // }
              // labels.push(labelsLegend[5])
              // colors.push(colorsLegend[5])
              //targetNodes.pop()
              this.storeSources.push(targetNodes)
              this.layers = this.layers + 1
            }
          }
          
          if ((this.layers == 1) || (this.layers % 6 == 0)) {
            this.widthGlobal = 615 + this.widthGlobal
          }
          
          var height = 300
          var data = []
          data.push({
            type: "sankey",
            orientation: "h",
            node: {
              arrangement: "snap",
              pad: 15,
              thickness: 30,
              line: {
                color: "black",
                width: 0.5,
              },
              label: this.labels,
              color: this.colors,
            },
            link: {
              source: this.sources,
              target: this.targets,
              value: this.values,
              color: this.colorLinks,
            }
          })

          var layout = {
            showlegend: false,
            font: { family: 'Helvetica', size: 14, color: '#000000' },
            autosize: false,
            width: this.widthGlobal,
            height: height,
            margin: {
              l: 5,
              r: 5,
              b: 5,
              t: 5,
              pad: 0
            },
          }
          var config = {displayModeBar: false, scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
          Plotly.react('SankeyDiagram', data, layout, config)
          document.getElementById('SankeyDiagram').scrollLeft = this.widthGlobal;
        }
      },
    },
  mounted () {    
    EventBus.$on('sendNewK', data => {
      this.firstTime = true
      this.Execute = true
    })
    EventBus.$on('SendSelectedPointsUpdateIndicatorUnder', data => {
      this.Mode = 0
      this.Execute = true
    })
    EventBus.$on('SendSelectedPointsUpdateIndicatorOver', data => { 
      this.Mode = 1
      this.Execute = true
    })
    EventBus.$on('emittedEventCallingPerformanceProb', data => { this.FinalResultsGlob = data })
    EventBus.$on('HistoryCall', data => { this.FinalResultsSankey = data })
    EventBus.$on('HistoryCall', this.SankeyDiagramView)

    EventBus.$on('reset', this.reset)
  }
}
</script>