<template>
<div>
  <div id="buildOverlap">
    <div id="PolarChart"></div>
    <div id="Chord"></div>
  </div>
</div>
</template>

<script>

import { EventBus } from '../main.js'
import * as Plotly from 'plotly.js'
import * as tf from "@tensorflow/tfjs"

export default {
  name: 'Predictions',
  data () {
    return {
      probabilities: 0,
      k: 0,
      kValues: [5,6,7,8,9,10,11,12,13],
      sendExtra: [],
      sendHeatmap: [],
      step: 0,
      statusTypes: ['Outlier','Rare','Borderline','Safe'],
      gatherAllOccur: [],
      selectedPoints: [],
      storePreviousDistribution: [],
      flagContinue: true,
      deletedPoints: [],
      addedPoints: [],
      storeResults: [],
      called: 0
    }
  },
  methods: {
    reset () {
      Plotly.purge("PolarChart")
      var svg = d3.select("#Chord");
      svg.selectAll("*").remove();
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
    PolarChartView () {   
      Plotly.purge("PolarChart")
      this.sendExtra = []
      this.sendHeatmap = []
      var width = 615
      var height = 615

      var probabilitiesLocal = JSON.parse(this.probabilities[0])
      var categories = JSON.parse(this.probabilities[1])
      var groundTruth = this.probabilities[2]
      var yPredict = JSON.parse(this.probabilities[5])
      var XData = JSON.parse(JSON.parse(this.probabilities[6]))

      var underSamplInd = JSON.parse(this.probabilities[7])
      var percentage = this.probabilities[8]
      if (this.flagContinue) {
        this.storePreviousDistribution = [...groundTruth]
        this.storePreviousProba = [...percentage]
      }
      var overSamplInd = JSON.parse(this.probabilities[12])
      var unique = groundTruth.filter((v, i, a) => a.indexOf(v) === i);
      var stringParameters = []
      for (let i = 0; i < XData.length; i++) {
        this.clean(XData[i])
        stringParameters.push('ID: ' + JSON.stringify(i) + '<br> Probability (%): ' + parseInt(probabilitiesLocal[i][groundTruth[i]].toFixed(2) * 100) + '<br> Details: ' + JSON.stringify(XData[i]).replace(/,/gi, '<br>'))
      }
    
      var colorRange = ['rgba(255,127,0,1)','rgba(31,120,180,1)','rgba(223,101,176,1)','rgba(77,175,74,1)']
      var legendColors = ['rgba(255,127,0,1)','rgba(31,120,180,1)','rgba(223,101,176,1)','rgba(77,175,74,1)']
      var colorOutlines = ['rgba(240,240,240,1)','rgba(189,189,189,1)','rgba(115,115,115,1)','rgba(0,0,0,1)']

      var splitGroundTruth = []
      var splitPredictions = []
      var newSplitGroundTruth = []
      var newPredictionsSplit = []
      var newPredictionsSplitColors = []
      var splitStrings = []
      var stringParametersSplit = []

      var symbols = []
      var symbolsPerClass = []
      var colorMarkers = []
      var colorMarkersPerClass = []

      var summarizeSafe = 0
      var summarizeBorder = 0
      var summarizeRare = 0
      var summarizeOut = 0
      var summarizeSafePrevious = 0
      var summarizeBorderPrevious = 0
      var summarizeRarePrevious = 0
      var summarizeOutPrevious = 0
      var summarizeSafeSug = 0
      var summarizeBorderSug = 0
      var summarizeRareSug = 0
      var summarizeOutSug = 0
      var eachAllocation = []
      var eachAllocationSug = []
      var allocationPerClass = []
      var allocationPerClassPrevious = []
      var allocationPerClassSug = []

      var removedSafe = 0
      var removedBorder = 0
      var removedRare = 0
      var removedOut = 0
      var addedSafe = 0
      var addedBorder = 0
      var addedRare = 0
      var addedOut = 0
      var eachSankey = []
      var eachAllocationPrevious = []
      var eachSankeyAddition = []
      var removalPerClass = []
      var additionPerClass = []
      var storeIndices = []
      var storeIndicesHeat = []
      var storeIndicesSafe = []
      var storeIndicesBorder = []
      var storeIndicesRare = []
      var storeIndicesOut = []

      for (let m = 0; m < unique.length; m++) {
        symbols = []
        colorMarkers = []
        summarizeSafe = 0
        summarizeBorder = 0
        summarizeRare = 0
        summarizeOut = 0
        summarizeSafePrevious = 0
        summarizeBorderPrevious = 0
        summarizeRarePrevious = 0
        summarizeOutPrevious = 0
        summarizeSafeSug = 0
        summarizeBorderSug = 0
        summarizeRareSug = 0
        summarizeOutSug = 0
        removedSafe = 0
        removedBorder = 0
        removedRare = 0
        removedOut = 0
        addedSafe = 0
        addedBorder = 0
        addedRare = 0
        addedOut = 0
        eachAllocation = []
        eachAllocationPrevious = []
        eachAllocationSug = []
        eachSankey = []
        eachSankeyAddition = []
        splitGroundTruth = []
        splitPredictions = []
        splitStrings = []
        for (let h = 0; h < this.storePreviousDistribution.length; h++) {
          if (this.storePreviousDistribution[h] == unique[m]) {
            if (this.storePreviousProba[h] >= (0.8 * this.kValues[this.k])) {
                summarizeSafePrevious = summarizeSafePrevious + 1
                if (this.deletedPoints.includes(h)) {
                  removedSafe = removedSafe + 1
                }
            }
            else if (this.storePreviousProba[h] >= (0.5 * this.kValues[this.k])) {
                summarizeBorderPrevious = summarizeBorderPrevious + 1
                if (this.deletedPoints.includes(h)) {
                  removedBorder = removedBorder + 1
                }
            }
            else if (this.storePreviousProba[h] >= (0.2 * this.kValues[this.k])) {
                summarizeRarePrevious = summarizeRarePrevious + 1
                if (this.deletedPoints.includes(h)) {
                  removedRare = removedRare + 1
                }
            }
            else {
                summarizeOutPrevious = summarizeOutPrevious + 1
                if (this.deletedPoints.includes(h)) {
                  removedOut = removedOut + 1
                }
            }
          }
        }
        for (let h = 0; h < groundTruth.length; h++) {
          if (groundTruth[h] == unique[m]) {
            if (percentage[h] >= (0.8 * this.kValues[this.k])) {
                if (this.statusTypes.includes('Safe')) {
                  storeIndicesHeat.push(h)
                }
                splitPredictions.push(yPredict[h])
                splitGroundTruth.push(groundTruth[h])
                splitStrings.push(stringParameters[h])
                colorMarkers.push(colorOutlines[0])
                storeIndices.push(h)
                storeIndicesSafe.push(h)
                // if (this.deletedPoints.includes(h)) {
                //   removedSafe = removedSafe + 1
                // }
                if (this.addedPoints.includes(h)) {
                  addedSafe = addedSafe + 1
                }
                if (underSamplInd.includes(h)) {
                  summarizeSafe = summarizeSafe + 1
                  symbols.push('x')
                  if (this.selectedPoints.length != 0) {
                    if (this.selectedPoints.includes(h)) {
                      
                    } else {
                      summarizeSafeSug = summarizeSafeSug + 1
                    }
                  }
                } else if (overSamplInd.includes(h)) {
                  symbols.push('cross')
                  if (this.selectedPoints.length != 0) {
                    if (this.selectedPoints.includes(h)) {
                      summarizeSafeSug = summarizeSafeSug + 1
                    }
                  } else {
                    summarizeSafeSug = summarizeSafeSug + 1
                  }
                } else {
                  symbols.push('circle')
                  summarizeSafeSug = summarizeSafeSug + 1
                  summarizeSafe = summarizeSafe + 1
                }
            }
            else if (percentage[h] >= (0.5 * this.kValues[this.k])) {
                if (this.statusTypes.includes('Borderline')) {
                  storeIndicesHeat.push(h)
                }
                splitPredictions.push(yPredict[h])
                splitGroundTruth.push(groundTruth[h])
                splitStrings.push(stringParameters[h])
                colorMarkers.push(colorOutlines[1])
                storeIndices.push(h)
                storeIndicesBorder.push(h)
                // if (this.deletedPoints.includes(h)) {
                //   removedBorder = removedBorder + 1
                // }
                if (this.addedPoints.includes(h)) {
                  addedBorder = addedBorder + 1
                }
                if (underSamplInd.includes(h)) {
                  symbols.push('x')
                  summarizeBorder = summarizeBorder + 1
                  if (this.selectedPoints.length != 0) {
                    if (this.selectedPoints.includes(h)) {
                      
                    } else {
                      summarizeBorderSug = summarizeBorderSug + 1
                    }
                  }
                } else if (overSamplInd.includes(h)) {
                  symbols.push('cross')
                  if (this.selectedPoints.length != 0) {
                    if (this.selectedPoints.includes(h)) {
                      summarizeBorderSug = summarizeBorderSug + 1
                    }
                  } else {
                    summarizeBorderSug = summarizeBorderSug + 1
                  }
                } else {
                  symbols.push('circle')
                  summarizeBorderSug = summarizeBorderSug + 1
                  summarizeBorder = summarizeBorder + 1
                }
            }
            else if (percentage[h] >= (0.2 * this.kValues[this.k])) {
                if (this.statusTypes.includes('Rare')) {
                  storeIndicesHeat.push(h)
                }
                splitPredictions.push(yPredict[h])
                splitGroundTruth.push(groundTruth[h])
                splitStrings.push(stringParameters[h])
                colorMarkers.push(colorOutlines[2])
                storeIndices.push(h)
                storeIndicesRare.push(h)
                // if (this.deletedPoints.includes(h)) {
                //   removedRare = removedRare + 1
                // }
                if (this.addedPoints.includes(h)) {
                  addedRare = addedRare + 1
                }
                if (underSamplInd.includes(h)) {
                  summarizeRare = summarizeRare + 1
                  symbols.push('x')
                  if (this.selectedPoints.length != 0) {
                    if (this.selectedPoints.includes(h)) {
                      
                    } else {
                      summarizeRareSug = summarizeRareSug + 1
                    }
                  }
                } else if (overSamplInd.includes(h)) {
                  symbols.push('cross')
                  if (this.selectedPoints.length != 0) {
                    if (this.selectedPoints.includes(h)) {
                      summarizeRareSug = summarizeRareSug + 1
                    }
                  } else {
                    summarizeRareSug = summarizeRareSug + 1
                  }
                } else {
                  symbols.push('circle')
                  summarizeRareSug = summarizeRareSug + 1
                  summarizeRare = summarizeRare + 1
                }
            }
            else {
                if (this.statusTypes.includes('Outlier')) {
                  storeIndicesHeat.push(h)
                }
                splitPredictions.push(yPredict[h])
                splitGroundTruth.push(groundTruth[h])
                splitStrings.push(stringParameters[h])
                colorMarkers.push(colorOutlines[3])
                storeIndices.push(h)
                storeIndicesOut.push(h)
                // if (this.deletedPoints.includes(h)) {
                //   removedOut = removedOut + 1
                // }
                if (this.addedPoints.includes(h)) {
                  addedOut = addedOut + 1
                }
                if (underSamplInd.includes(h)) {
                  summarizeOut = summarizeOut + 1
                  symbols.push('x')
                  if (this.selectedPoints.length != 0) {
                    if (this.selectedPoints.includes(h)) {
                      
                    } else {
                      summarizeOutSug = summarizeOutSug + 1
                    }
                  }
                } else if (overSamplInd.includes(h)) {
                  symbols.push('cross')
                  if (this.selectedPoints.length != 0) {
                    if (this.selectedPoints.includes(h)) {
                      summarizeOutSug = summarizeOutSug + 1
                    }
                  } else {
                    summarizeOutSug = summarizeOutSug + 1
                  }
                } else {
                  symbols.push('circle')
                  summarizeOutSug = summarizeOutSug + 1
                  summarizeOut = summarizeOut + 1
                }
            }
          }
        }
        symbolsPerClass.push(symbols)  
        colorMarkersPerClass.push(colorMarkers)
        eachAllocation.push(summarizeSafe)
        eachAllocation.push(summarizeBorder)
        eachAllocation.push(summarizeRare)
        eachAllocation.push(summarizeOut)
        eachAllocationPrevious.push(summarizeSafePrevious)
        eachAllocationPrevious.push(summarizeBorderPrevious)
        eachAllocationPrevious.push(summarizeRarePrevious)
        eachAllocationPrevious.push(summarizeOutPrevious)
        eachAllocationSug.push(summarizeSafeSug)
        eachAllocationSug.push(summarizeBorderSug)
        eachAllocationSug.push(summarizeRareSug)
        eachAllocationSug.push(summarizeOutSug)
        eachSankey.push(removedSafe)
        eachSankey.push(removedBorder)
        eachSankey.push(removedRare)
        eachSankey.push(removedOut)
        eachSankeyAddition.push(addedSafe)
        eachSankeyAddition.push(addedBorder)
        eachSankeyAddition.push(addedRare)
        eachSankeyAddition.push(addedOut)
        allocationPerClass.push(eachAllocation)    
        allocationPerClassPrevious.push(eachAllocationPrevious)    
        allocationPerClassSug.push(eachAllocationSug)    
        removalPerClass.push(eachSankey)    
        additionPerClass.push(eachSankeyAddition)  
        newSplitGroundTruth.push(splitGroundTruth)
        newPredictionsSplit.push(splitPredictions)
        stringParametersSplit.push(splitStrings)
      }
      EventBus.$emit('SendSankey', removalPerClass)
      EventBus.$emit('SendSankeyAddition', additionPerClass)
      if (underSamplInd.length == 0 && overSamplInd.length == 0) {
        EventBus.$emit('VisualizeDistributionOfTypes', allocationPerClass)
        EventBus.$emit('VisualizeDistributionOfTypesPrevious', allocationPerClassPrevious)
        EventBus.$emit('VisualizeDistributionOfTypesSuggestion', [])
      } else if (underSamplInd.length != 0) {
        EventBus.$emit('VisualizeDistributionOfTypes', allocationPerClass)
        EventBus.$emit('VisualizeDistributionOfTypesPrevious', allocationPerClassPrevious)
        EventBus.$emit('VisualizeDistributionOfTypesSuggestion', allocationPerClassSug)
      } else {
        EventBus.$emit('VisualizeDistributionOfTypesSuggestion', allocationPerClassSug)
      }
      
      var tempArray = []
      var opacities = []
      var opacitiesSplit = []
      var total = 0
      for (var k = 0; k < newPredictionsSplit.length; k++) {
        tempArray = []
        opacities = []
        for (var el = 0; el < newPredictionsSplit[k].length; el++) {
            tempArray.push(colorRange[newPredictionsSplit[k][el]])
            if (this.selectedPoints.length == 0) {
              if (storeIndicesSafe.includes(storeIndices[total+el])) {
                if (this.statusTypes.includes('Safe')) {
                  opacities.push(0.7)
                } else {
                  opacities.push(0.05)
                }
              } else if (storeIndicesBorder.includes(storeIndices[total+el])) {
                if (this.statusTypes.includes('Borderline')) {
                  opacities.push(0.7)
                } else {
                  opacities.push(0.05)
                }
              } else if (storeIndicesRare.includes(storeIndices[total+el])) {
                if (this.statusTypes.includes('Rare')) {
                  opacities.push(0.7)
                } else {
                  opacities.push(0.05)
                }
              } else {
                if (this.statusTypes.includes('Outlier')) {
                  opacities.push(0.7)
                } else {
                  opacities.push(0.05)
                }
              }
            } else {
              if (this.selectedPoints.includes(storeIndices[total+el])) {
                if (storeIndicesSafe.includes(storeIndices[total+el])) {
                if (this.statusTypes.includes('Safe')) {
                  opacities.push(0.7)
                } else {
                  opacities.push(0.05)
                }
              } else if (storeIndicesBorder.includes(storeIndices[total+el])) {
                if (this.statusTypes.includes('Borderline')) {
                  opacities.push(0.7)
                } else {
                  opacities.push(0.05)
                }
              } else if (storeIndicesRare.includes(storeIndices[total+el])) {
                if (this.statusTypes.includes('Rare')) {
                  opacities.push(0.7)
                } else {
                  opacities.push(0.05)
                }
              } else {
                if (this.statusTypes.includes('Outlier')) {
                  opacities.push(0.7)
                } else {
                  opacities.push(0.05)
                }
              }
              } else {
                opacities.push(0.05)
              }
            }
          }
        opacitiesSplit.push(opacities)
        newPredictionsSplitColors.push(tempArray)
        total = total + newPredictionsSplit[k].length
      }

      this.sendHeatmap.push(storeIndicesSafe)
      this.sendHeatmap.push(storeIndicesBorder)
      this.sendHeatmap.push(storeIndicesRare)
      this.sendHeatmap.push(storeIndicesOut)
      this.sendHeatmap.push(storeIndicesHeat)
      this.sendHeatmap.push(underSamplInd)
      this.sendHeatmap.push(overSamplInd)
      EventBus.$emit('emittedEventCallingAdditionalDataHeatmap', this.sendHeatmap)
      EventBus.$emit('emittedEventCallingAdditionalDataOverview', this.sendHeatmap)

      this.sendExtra.push(symbolsPerClass)
      this.sendExtra.push(colorMarkersPerClass)
      this.sendExtra.push(storeIndices)
      this.sendExtra.push(stringParametersSplit)
      this.sendExtra.push(newSplitGroundTruth)
      this.sendExtra.push(opacitiesSplit)
      EventBus.$emit('emittedEventCallingAdditionalData', this.sendExtra)
      
      this.gatherAllOccur = []
      for (let looping=0; looping < newPredictionsSplit.length; looping++) {
        this.gatherAllOccur.push(newPredictionsSplit[looping].length)
      }
    
      var sum = this.gatherAllOccur.reduce((a, b) => a + b, 0)

      function indexOfMax(arr) {
          if (arr.length === 0) {
              return -1;
          }

          var max = arr[0];
          var maxIndex = 0;

          for (var i = 1; i < arr.length; i++) {
              if (arr[i] > max) {
                  maxIndex = i;
                  max = arr[i];
              }
          }

          return maxIndex;
      }

      var portions = []
      this.gatherAllOccur.forEach(element => {
        portions.push((element/sum) * 360)
      }); 

      const lab = tf.tensor1d(newSplitGroundTruth.flat(), 'int32');
      const pred = tf.tensor1d(newPredictionsSplit.flat(), 'int32');
      
      const num_Cls = categories.length;
        
      // Calling tf.confusionMatrix() method
      const output = tf.math.confusionMatrix(lab, pred, num_Cls);
        
      // Printing output
      var confusion = output.arraySync()

      var confusionPortion = []
      confusion.forEach(arrayCateg => {
        confusionPortion.push(arrayCateg.map(function(x) { return (x / sum) * 100; }))
      });

      var duplicConfusion = [...confusion]
      
      for (let i = 0; i < duplicConfusion.length; i++) {
        for (let j = 0; j < duplicConfusion[i].length; j++) {
          if (i == j) {
            duplicConfusion[i][j] = 0
          }
        }
      }

      var firstIndices = []
      var secondIndices = []
      for (let i = 0; i < duplicConfusion.length; i++) {
        var indexMax = indexOfMax(duplicConfusion[i])
        firstIndices.push(indexMax)
        duplicConfusion[i][indexMax] = 0
        var indexSecMax = indexOfMax(duplicConfusion[i])
        secondIndices.push(indexSecMax)
      }

      var predictions = []
      var data = []
      var r = []
      var theta = []
      for (var i = 0; i < probabilitiesLocal.length; i++) {
        if (storeIndices.includes(i)) {
        var tempData = {}
          for (var j = 0; j < probabilitiesLocal[i].length; j++) {
              tempData[categories[j]] = probabilitiesLocal[i][j] * 100
          }
          tempData["target"] = categories[groundTruth[i]]
          predictions.push(tempData)
        }
      }

      var storePrevious = 0
      var tickvalsArray = []
      tickvalsArray.push(storePrevious)

      for (var k = 0; k < categories.length; k++) {
        r = []
        theta = []
        if (categories.length == 2) {
          var scaleLin = d3.scale.linear().domain([0, 100]).range([(0+storePrevious)*(-1), (-1)*(storePrevious+portions[k])]);
        } else {
          var scaleLin = d3.scale.linear().domain([-100, 100]).range([(0+storePrevious)*(-1), (-1)*(storePrevious+portions[k])]);
        }
        for (var m =0; m < predictions.length; m++) {
          if (categories[k] == predictions[m].target) {
            r.push(predictions[m][categories[k]])
              if (categories.length == 3) {
                if (k == 0) {
                  if (predictions[m][categories[k+1]] >= predictions[m][categories[categories.length - 1]]) {
                    var scaled = scaleLin(predictions[m][categories[k+1]])
                  } else {
                    var scaled = scaleLin(predictions[m][categories[categories.length - 1]] * (-1))
                  }
                } else if (k == (categories.length - 1)) {
                  if (predictions[m][categories[k-1]] >= predictions[m][categories[0]]) {
                    var scaled = scaleLin(predictions[m][categories[k-1]] * (-1))
                  } else {
                    var scaled = scaleLin(predictions[m][categories[0]])
                  }
                } else {
                  if (predictions[m][categories[k+1]] >= predictions[m][categories[k-1]]) {
                    var scaled = scaleLin(predictions[m][categories[k+1]])
                  } else {
                    var scaled = scaleLin(predictions[m][categories[k-1]] * (-1))
                  }
                }
            } else if (categories.length == 2) {
              var scaled = scaleLin(predictions[m][categories[0]])
            } else {
              if (k == 0 || k == 1 || k == 2) {
                if ((predictions[m][categories[firstIndices[k]]]) >= (predictions[m][categories[secondIndices[k]]])) {
                  var scaled = scaleLin(predictions[m][categories[firstIndices[k]]])
                } else {
                  var scaled = scaleLin(predictions[m][categories[secondIndices[k]]] * (-1))
                }
              } else {
                if ((predictions[m][categories[firstIndices[k]]]) >= (predictions[m][categories[secondIndices[k]]])) {
                  var scaled = scaleLin(predictions[m][categories[firstIndices[k]]] * (-1))
                } else {
                  var scaled = scaleLin(predictions[m][categories[secondIndices[k]]])
                }                
              }
            }
            theta.push(scaled)
          }
        }

        data.push(
          {
            type: "scatterpolargl",
            r: r,
            theta: theta,
            mode: "markers",
            name: categories[k],
            hovertemplate: 
              "%{text}<br><br>" +
              "<extra></extra>",
            text: stringParametersSplit[k],
            marker: {
              color: newPredictionsSplitColors[k],
              symbol: symbolsPerClass[k],
              size: 10,
              line: {
                color: colorMarkersPerClass[k],
                width: 2
              },
              opacity: opacitiesSplit[k]
            },
            cliponaxis: false
          })

          storePrevious = storePrevious + portions[k]
          if (storePrevious != 360) {
            tickvalsArray.push(360 - storePrevious)
          }
        }
      var layout = {
          font: {
            size: 14
          },
          legend: {"orientation": "v", x: -0.03, y: 0.98},
          modebar: {"orientation": "v", x: 0, y: 0.7},
          showlegend: true,
          hoverlabel: { bgcolor: "#FFF" },
          hovermode: "closest",
          polar: {     
            hole: 0.35,
            sector: [0,360],
            angularaxis: {
              tickmode: 'array',
              tickvals: tickvalsArray
            },
            radialaxis: {
              side: "counterclockwise",
              showline: true,
              visible: true,
              range: [100, 0],
              linewidth: 2,
              tickwidth: 2,
              gridcolor: "#D3D3D3",
              gridwidth: 2,
              angle: 0
            },
          },
          margin: {
            l: 10,
            r: 2,
            b: 0,
            t: 0,
            pad: 0
          },
          width: width,
          height: height,
        }
      const OverviewPlotly = document.getElementById('PolarChart')
      var config = {displaylogo: false, responsive: true, displayModeBar: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'select2d', 'lasso2d', 'toggleHover', 'toggleSpikelines', 'hoverClosestGl2d','hoverCompareCartesian','hoverClosestCartesian', 'hoverClosestGl2d', 'hoverClosestPie']}
      Plotly.newPlot(OverviewPlotly, data, layout, config);
      
      var legendBoxes = OverviewPlotly.getElementsByClassName("scatterpts")
      for (let i = 0; i < legendBoxes.length; i++) {
        Plotly.d3.select(legendBoxes[i]).style("fill", legendColors[(legendBoxes.length-1) - i]);
        Plotly.d3.select(legendBoxes[i]).style("stroke", '#000000');
        Plotly.d3.select(legendBoxes[i]).attr("d", 'M7,0A7,7 0 1,1 0,-7A7,7 0 0,1 7,0Z');
      }
      this.flagContinue = true
      this.chordDiagramView(categories, confusionPortion, firstIndices, secondIndices)

    },
    chordDiagramView (categories, confusionPortion, firstIndices, secondIndices){



      var svg = d3.select("#Chord");
      svg.selectAll("*").remove();

      /*//////////////////////////////////////////////////////////
      ////////////////// Set up the Data /////////////////////////
      //////////////////////////////////////////////////////////*/

      // var matrix = [
      // [9.6899,0.8859,0.0554,0.443,2.5471,2.4363,0.5537,2.5471], /*Apple 19.1584*/
      // [0.1107,1.8272,0,0.4983,1.1074,1.052,0.2215,0.4983], /*HTC 5.3154*/
      // [0.0554,0.2769,0.2215,0.2215,0.3876,0.8306,0.0554,0.3322], /*Huawei 2.3811*/
      // [0.0554,0.1107,0.0554,1.2182,1.1628,0.6645,0.4983,1.052], /*LG 4.8173*/
      // [0.2215,0.443,0,0.2769,10.4097,1.2182,0.4983,2.8239], /*Nokia 15.8915*/
      // [1.1628,2.6024,0,1.3843,8.7486,16.8328,1.7165,5.5925], /*Samsung 38.0399*/
      // ];
      /*Sums up to exactly 100*/
      
      var colors = ["#ff7f00","#1f78b4","#df65b0	","#4daf4a"];

      /*Initiate the color scale*/
      var fill = d3.scale.ordinal()
          .domain(d3.range(categories.length))
          .range(colors);
        
      /*//////////////////////////////////////////////////////////
      /////////////// Initiate Chord Diagram /////////////////////
      //////////////////////////////////////////////////////////*/
      var margin = {top: 10, right: 10, bottom: 10, left: 10},
          width = 267 - margin.left - margin.right,
          height = 267 - margin.top - margin.bottom,
          innerRadius = Math.min(width, height) * .39,
          outerRadius = innerRadius * 1.04;

      /*Initiate the SVG*/
      var svg = d3.select("#Chord").append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + (margin.left + width/2) + "," + (margin.top + height/2) + ") rotate(90)");
      

      var chord = d3.layout.chord()
          .padding(.005)
          .sortSubgroups(d3.ascending) /*sort the chords inside an arc from high to low*/
          .sortChords(d3.descending) /*which chord should be shown on top when chords cross. Now the biggest chord is at the bottom*/
        .matrix(confusionPortion);

      /*//////////////////////////////////////////////////////////
      ////////////////// Draw outer Arcs /////////////////////////
      //////////////////////////////////////////////////////////*/

      var arc = d3.svg.arc()
          .innerRadius(innerRadius)
          .outerRadius(outerRadius);

      // creating the fill gradient
      function getGradID(d){ return "linkGrad-" + d.source.index + "-" + d.target.index; }


      var grads = svg.append("defs")
        .selectAll("linearGradient")
        .data(chord.chords)
        .enter()
        .append("linearGradient")
        .attr("id", getGradID)
        .attr("gradientUnits", "userSpaceOnUse")
        .attr("x1", function(d, i){ return innerRadius * Math.cos((d.source.endAngle-d.source.startAngle) / 2 + d.source.startAngle - Math.PI/2); })
        .attr("y1", function(d, i){ return innerRadius * Math.sin((d.source.endAngle-d.source.startAngle) / 2 + d.source.startAngle - Math.PI/2); })
        .attr("x2", function(d,i){ return innerRadius * Math.cos((d.target.endAngle-d.target.startAngle) / 2 + d.target.startAngle - Math.PI/2); })
        .attr("y2", function(d,i){ return innerRadius * Math.sin((d.target.endAngle-d.target.startAngle) / 2 + d.target.startAngle - Math.PI/2); })

        // set the starting color (at 0%)

        grads.append("stop")
          .attr("offset", "0%")
          .attr("stop-color", function(d){ return fill(d.source.index)})

          //set the ending color (at 100%)
        grads.append("stop")
          .attr("offset", "100%")
          .attr("stop-color", function(d){ return fill(d.target.index)})

      /*//////////////////////////////////////////////////////////
      //////////////// Initiate inner chords /////////////////////
      //////////////////////////////////////////////////////////*/

      var chords = svg.selectAll("path.chord")
        .data(chord.chords)
        .enter().append("svg:path")
        .attr("class", function(d) {
          return "chord chord-" + d.source.index + " chord-" + d.target.index // The first chord allows us to select all of them. The second chord allows us to select each individual one. 
        })
        .style("stroke", function(d) { return d3.rgb("#000000").darker(); })
        //.style("fill", function(d) { return fill(d.source.index); })
        .style("fill", function(d){ return "url(#" + getGradID(d) + ")"; })
        .attr("d", d3.svg.chord().radius(innerRadius))
        .attr('opacity', 0);

      var g = svg.selectAll("g.group")
        .data(chord.groups)
        .enter().append("svg:g")
        .attr("class", function(d) {return "group " + categories[d.index];});
        
      g.append("svg:path")
          .attr("class", "arc")
          .style("stroke", function(d) { return fill(d.index); })
          .style("fill", function(d) { return fill(d.index); })
          .attr("d", arc)
          .style("opacity", 0)
          .transition().duration(1000)
          .style("opacity", 0.4);

      /*//////////////////////////////////////////////////////////
      ////////////////// Initiate Ticks //////////////////////////
      //////////////////////////////////////////////////////////*/

      var ticks = svg.selectAll("g.group").append("svg:g")
        .attr("class", function(d) {return "ticks " + categories[d.index];})
        .selectAll("g.ticks")
        .attr("class", "ticks")
          .data(groupTicks)
        .enter().append("svg:g")
          .attr("transform", function(d) {
            return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
                + "translate(" + outerRadius+40 + ",0)";
          });

      /*Append the tick around the arcs*/
      ticks.append("svg:line")
        .attr("x1", 1)
        .attr("y1", 0)
        .attr("x2", 5)
        .attr("y2", 0)
        .attr("class", "ticks")
        .style("stroke", "#FFF");
        
      /*Add the labels for the %'s*/
      ticks.append("svg:text")
        .attr("x", 8)
        .attr("dy", ".35em")
        .attr("class", "tickLabels")
        .attr("transform", function(d) { return d.angle > Math.PI ? "rotate(180)translate(-16)" : null; })
        .style("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
        .text(function(d) { return d.label; })
        .attr('opacity', 0);
        
      /*//////////////////////////////////////////////////////////
      ////////////////// Initiate Names //////////////////////////
      //////////////////////////////////////////////////////////*/

      // g.append("svg:text")
      //   .each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })
      //   .attr("dy", ".35em")
      //   .attr("class", "titles")
      //   .attr("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
      //   .attr("transform", function(d) {
      //     return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
      //     + "translate(" + (innerRadius + 55) + ")"
      //     + (d.angle > Math.PI ? "rotate(180)" : "");
      //   })
      //   .attr('opacity', 0)
      //   .text(function(d,i) { return categories[i]; });  

        /*Create arcs or show them, depending on the point in the visual*/
        g.append("svg:path")
          .style("stroke", function(d) { return fill(d.index); })
          .style("fill", function(d) { return fill(d.index); })
          .attr("d", arc)
          .style("opacity", 0)
          .transition().duration(1000)
          .style("opacity", 1);

        /*Make mouse over and out possible*/
        d3.selectAll(".group")
          .on("click", fade(0))
          .on("dblclick", fade(.80));
          
        /*Show all chords*/
        chords.transition().duration(1000)
          .style("opacity", function(d) {
            if (d.source.index == d.target.index) {
              return 0
            }
            if ((firstIndices[d.source.index] == d.target.index) || (secondIndices[d.source.index] == d.target.index)) {
              return 0.6
            } else {
              return 0.15
            }
          });

        /*Show all the text*/
        d3.selectAll("g.group").selectAll("line")
          .transition().duration(100)
          .style("stroke","#000");
        /*Same for the %'s*/
        svg.selectAll("g.group")
          .transition().duration(100)
          .selectAll(".tickLabels").style("opacity",1);
        /*And the Names of each Arc*/	
        svg.selectAll("g.group")
          .transition().duration(100)
          .selectAll(".titles").style("opacity",1);		

      /*//////////////////////////////////////////////////////////
      ////////////////// Extra Functions /////////////////////////
      //////////////////////////////////////////////////////////*/

      /*Returns an event handler for fading a given chord group*/
      function fade(opacity) {
        return function(d, i) {
          svg.selectAll("path.chord")
              .filter(function(d) { return d.source.index != i && d.target.index != i; })
          .transition()
              .style("stroke-opacity", opacity)
              .style("fill-opacity", opacity);
        };
      };/*fade*/

      /*Returns an array of tick angles and labels, given a group*/
      function groupTicks(d) {
        var k = (d.endAngle - d.startAngle) / d.value;
        return d3.range(0, d.value, 1).map(function(v, i) {
          return {
            angle: v * k + d.startAngle,
            label: i % 5 ? null : v + "%"
          };
        });
      };/*groupTicks*/
    }
  },
  mounted () {

    EventBus.$on('Continue', data => { this.flagContinue = data })

    EventBus.$on('SendSelectedPointsUpdateIndicatorUn', data => { this.deletedPoints = data })
    EventBus.$on('SendSelectedPointsUpdateIndicatorOv', data => { this.addedPoints = data })

    EventBus.$on('limitPoints', data => { this.selectedPoints = data })
    EventBus.$on('limitPointsClear', data => { this.selectedPoints = data })
    EventBus.$on('limitPoints', this.PolarChartView)

    EventBus.$on('updateNeighborsGlobal', data => { this.k = data[0] })

    EventBus.$on('emittedEventCallingPerformanceProbPred', data => { this.probabilities = data })
    EventBus.$on('emittedEventCallingPerformanceProbPred', this.PolarChartView)

    EventBus.$on('ActivateType', data => {
      if (data == 0)
        this.statusTypes[data] = 'Outlier' 
      else if (data == 1)
        this.statusTypes[data] = 'Rare' 
      else if (data == 2)
        this.statusTypes[data] = 'Borderline' 
      else 
        this.statusTypes[data] = 'Safe' 
    })

    EventBus.$on('ActivateType', this.PolarChartView)

    EventBus.$on('deActivateType', data => {
      this.statusTypes[data] = '' 
    })

    EventBus.$on('clearSelections', data => {
      this.statusTypes = data 
    })

    EventBus.$on('deActivateType', this.PolarChartView)

    EventBus.$on('reset', this.reset)
  }
}
</script>

<style>

  #PolarChart .modebar{margin-top: 25px !important}

  #buildOverlap { position: relative }
  #PolarChart { position: absolute; top: 0; left: 0; z-index: 0}
  #Chord { position: absolute; top: 0; left: 0; z-index: 2}

  #Chord { 
    transform: translateX(179px) translateY(166px) !important
  }

  #PolarChart { 
    transform: translateX(-3px) translateY(-8px) !important
  }

  g.xtick {
    z-index: 3 !important;
    transform: translateX(12px) !important
  }

  .radial-line {
    z-index: 3 !important
  }

  .radial-axis {
    z-index: 3 !important
  }

  path.angularaxistick {
    display: none !important;
  }

  g.angularaxistick {
    display: none !important;
  }

	#clickerWrapper {
		  top: 0;
		  z-index: 1;
		  display: block;
		  position: relative;
		  width: 640px;
		  /*padding-top: 5px;*/
		  visibility: auto;
      text-align: center;
      margin: 0 auto;
		}

		#clicker {
		  z-index: 1;
		  display: block;
		  font-family: Oswald;
		  font-size: 36px;
		  font-weight: 300;
		  color: #363636;
		  position: relative;
		  /*width: 80px;*/
		  text-align: center;
		  width: 30%;
		  margin: 0 auto;
		  border: 1px solid;
		  border-color: #363636;
		  cursor: pointer;
		}

		#progress {
		  z-index: 1;
		  display: block;
		  position: relative;
		  width: 40%;
		  height: 6px;
		  margin: 10px auto;
		  visibility: hidden;
		}
		
		#buttonWrapper{
		  z-index: 1;
		  display: block;
		  font-family: Oswald;
		  font-size: 14px;
		  font-weight: 300;
		  color: #6B6B6B;
		  position: relative;
		  width: 640px;
		  text-align: center;	
		  overflow: hidden;	
      text-align: center;
      margin: 0 auto;
      margin-top: 30px;
		}
		
		#buttonWrapperInner{
			position: relative;
			width: 300px;
			height: 30px;
			margin: 0 auto;
		}
		
		
		#skip{
		  width: 90px;
		  cursor: pointer;	
		  float: left;	
		  text-align: left;
		}
		
		#reset{
		  width: 110px;
		  cursor: pointer;	
		  float: left;			  
		}

		#link{
		  width: 100px;
		  cursor: pointer;	
		  float: left;	
		  text-align: right;
		}
		
		line {
		  stroke: #000;
		  stroke-width: 1.px;
		}

		text {
		  font-size: 10px;
		}

		.titles{
		  font-size: 14px;
		}

		.explanation{
		  font-size: 20px;
		  font-weight: 300;
		  text-align: center;
		}
		
		path.chord {
		  fill-opacity: .80;
		}
		
		a {
			text-decoration: none;
			color: #6B6B6B;
		}
</style>