<template>
  <div>
    <div id="Heatmap"></div>
    <div id="LegendHeat"></div>
  </div>
</template>

<script>
import * as d3Base from 'd3'
import { EventBus } from '../main.js'
import * as colorbr from 'colorbrewer'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)
const colorbrewer = Object.assign(colorbr)

export default {
  name: "Heatmap",
  data () {
    return {
      GetResultsAll: '',
      Toggles: '',
      limitation: 0,
      flag: false,
      classesNumber: 10,
      cellSize: 16,
      ModelsIDHeatStack: [],
      highlighted: [],
      responsiveWidthHeight: [],
      FeaturesAccuracyStore: [],
      FeaturesStore: [],
      PermImpEliStore: [],
      featureUniStore: [],
      modelIdsStore: [],
      keyLocal: 0,
      activeModels: 0,
      flagLocal: false,
      smallScreenMode: '0px',
      dataFI: [],
      featureData: [],
      generKey: [],
      featureGenGlobal: [],
      keepMainRemovedFeatures: [],
      ColorEachType: [],
      limitCompletelyPoints: [],
    }
  },
  methods: {
    reset () {
      var svg = d3.select("#Heatmap");
      svg.selectAll("*").remove();
      var svgLeg = d3.select("#LegendHeat");
      svgLeg.selectAll("*").remove();
    },
    HeatmapView () {
      // Clear Heatmap first
      var svg = d3.select("#Heatmap");
      svg.selectAll("*").remove();

      var rowsInit = JSON.parse(this.dataFI[11])
      var rows = JSON.parse(rowsInit)
      
      var columns = this.dataFI[10]

      if (columns.includes("# Type #")) {
      } else {
        columns.push("# Type #")
      }

      var eachTypeSafe = this.ColorEachType[0]
      var eachTypeBorder = this.ColorEachType[1]
      var eachTypeRare = this.ColorEachType[2]
      var eachTypeOutlier = this.ColorEachType[3]
      var eachTypeGeneric = this.ColorEachType[4]

      var eachType = []
      if (this.limitCompletelyPoints.length == 0) {
        eachType = [... eachTypeGeneric]
      } else {
        for (let i = 0; i < eachTypeGeneric.length; i++) {
          if (this.limitCompletelyPoints.includes(eachTypeGeneric[i])) {
            eachType.push(eachTypeGeneric[i])
          }
        }
      }

      var len = eachType.length
      let indicesYAxis = []
      for (let i = 0; i < len; i++) {
        indicesYAxis[i] = eachType[i]
      } 

      let indicesXAxis = []
      var temp = []
      var len2 = columns.length
      for (let i = 0; i < len2; i++) {
        temp = []
        temp.push("R")
        temp.push(columns[i].toString())
        indicesXAxis[i] = temp
      }

        var values = []
        var modelData = []
        for (let j = 0; j <len2; j++) {
          var data = []
          eachType.forEach(i => {
            values[j] = rows[i][j]
            if (columns[j] == "# Type #")
            if (eachTypeSafe.includes(i))
              values[j] = -4
            else if (eachTypeBorder.includes(i))
              values[j] = -3
            else if (eachTypeRare.includes(i))
              values[j] = -2
            else
              values[j] = -1
            data.push(values[j])
          })
          modelData.push(data)
        }
      var transposedArray = []
      transposedArray = modelData[0].map((col, i) => modelData.map(row => row[i]))

      var dataAll = {"columns":indicesXAxis,"index":indicesYAxis,"data":transposedArray}
      this.heatmap_display(dataAll, "#Heatmap");

    },
    heatmap_display(data, heatmapId) {
    var columns = this.dataFI[10]
    var len = columns.length

    var lenData = data.data.length

    var eachType = this.ColorEachType
    var colorTypes = ['#d9d9d9',"#969696","#525252","#000000"]

    var symbolsUnder = this.ColorEachType[5]
    var symbolsOver = this.ColorEachType[6]

    var featuresAddRem = []
    var featuresGen = this.featureGenGlobal
    var cellSize = this.cellSize
    //##########################################################################
    // Patrick.Brockmann@lsce.ipsl.fr
    //##########################################################################
    
    //==================================================
    // References
    // http://bl.ocks.org/Soylent/bbff6cc507dca2f48792
    // http://bost.ocks.org/mike/selection/
    // http://bost.ocks.org/mike/join/
    // http://stackoverflow.com/questions/9481497/understanding-how-d3-js-binds-data-to-nodes
    // http://bost.ocks.org/mike/miserables/
    // http://bl.ocks.org/ianyfchang/8119685

    //==================================================
    var tooltip = d3.select(heatmapId)
        .append("div")
        .style("position", "absolute")
        .style("visibility", "hidden");
    // define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
    const zoom = d3.zoom()
                        .scaleExtent([0.4, 3]) //zoom limit
                        .on('zoom', () => {
                            svg.attr('transform', d3.event.transform) // updated for d3 v4
                        })

    //==================================================
    

    var viewerHeight = 530
    var widthHeatmap = 615

    var viewerPosTop = 20;
    var viewerPosTopHeat = 70;
    var viewerPosLeft = 50;

    var legendElementWidth = cellSize * 2.5;

    // http://bl.ocks.org/mbostock/5577023
    var colors = colorbrewer.BrBG[this.classesNumber];

    // http://bl.ocks.org/mbostock/3680999
    var svg;

    //==================================================
      var arr = data.data;
      var row_number = arr.length;
      var col_number = arr[0].length;

      var colorScale = d3.scaleQuantize()
          .domain([0.0, 1.0])
          .range(colors);

      svg = d3.select(heatmapId).append("svg")
          .attr("width", widthHeatmap)
          .attr("height", viewerHeight)
          .call(zoom)
            //.call(zoom.transform, d3.zoomIdentity.translate(200, 20).scale(0.25)) //initial size
            .append('svg:g')
            .attr("transform", "scale(1.35,1.35) translate(" + viewerPosLeft + "," + viewerPosTopHeat + ")");

      svg.append('defs')
          .append('pattern')
          .attr('id', 'diagonalHatch')
          .attr('patternUnits', 'userSpaceOnUse')
          .attr('width', 4)
          .attr('height', 4)
          .append('path')
          .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
          .attr('stroke', '#000000')
          .attr('stroke-width', 1);

      var rowSortOrder = false;
      var colSortOrder = false;
 
      var rowLabels = svg.append("g")
          .attr("class", "rowLabels")
          .selectAll(".rowLabel")
          .data(data.index)
          .enter().append("text")
          .text(function(d) {
            return d
          })
          .style('font-weight', function(d) {
            // console.log(d)
            // if (d[0] === "# Action #" || d[0] === "Average") {
            //     return "bold"
            // }
          })
          .attr("x", 0)
          .attr("y", function(d, i) {
            return (i * cellSize);
          })
          .style("text-anchor", "end")
          .attr("transform", function(d, i) {
              return "translate(-3," + cellSize / 1.8 + ")";
          })
          .attr("class", "rowLabel mono")
          .attr("id", function(d, i) {
              return "rowLabel_" + i;
          })
          .on('mouseover', function(d, i) {
              d3.select('#rowLabel_' + i).classed("hover", true);
          })
          .on('mouseout', function(d, i) {
              d3.select('#rowLabel_' + i).classed("hover", false);
          })
          .style("fill", function(d, i) {
            if (symbolsUnder.includes(d)) {
              return "#fb6a4a"
            } else if (symbolsOver.includes(d)) {
              return "#74c476"
            } else {
              return "#000000"
            }
          })
          // .on("click", function(d, i) {
          //     rowSortOrder = !rowSortOrder;
          //     sortByValues("r", i, rowSortOrder);
          //     d3.select("#order").property("selectedIndex", 0);
          //     //$("#order").jqxComboBox({selectedIndex: 0});
          // });

      var colLabels = svg.append("g")
          .attr("class", "colLabels")
          .selectAll(".colLabel")
          .data(data.columns)
          .enter().append("text")
          .text(function(d) {
              d.shift();
              return d.count > 1 ? d.reverse().join("/") : d.reverse();
          })
          .attr("x", 0)
          .attr("y", function(d, i) {
              return (i * 20);
          })
          .style("text-anchor", "left")
          .style('font-weight',function(d,i){
            if (d[0] === "# Clustering #") {
                return "bold"
            }
          })
          .attr("transform", function(d, i) {
              return "translate(" + cellSize / 1.8 + ", -3) rotate(-90) rotate(45, 0, " + (i * 20) + ")";
          })
          .attr("class", "colLabel mono")
          .attr("id", function(d, i) {
              return "colLabel_" + i;
          })
          .on('mouseover', function(d, i) {
              d3.select('#colLabel_' + i).classed("hover", true);
          })
          .on('mouseout', function(d, i) {
              d3.select('#colLabel_' + i).classed("hover", false);
          })
          .on("click", function(d, i) {
            if (i == (len-1)) {
              EventBus.$emit('updateClickedHeat', -1)
            } else {
              EventBus.$emit('updateClickedHeat', i)
            }
            colSortOrder = !colSortOrder;
            sortByValues("c", i, colSortOrder);
            d3.select("#order").property("selectedIndex", len);
          });

      var row = svg.selectAll(".row")
          .data(data.data)
          .enter().append("g")
          .attr("id", function(d) {
            return d.idx;
          })
          .attr("class", "row");
          svg.append("text").attr("x", (cellSize*(len/2))).attr("y", -55).text("Feature").style("font-size", "14px").attr("alignment-baseline","top")
          svg.append("text").attr("transform", "rotate(-90)").attr("x", (-1)*(cellSize*(lenData/2))).attr("y", -30).style("text-anchor", "middle").style("font-size", "14px").text("Instance"); // -130 before for HeartC
          var heatMap = row.selectAll(".cell")
          .data(function(d) {
              return d;
          })
          .enter().append("svg:rect")
          .attr("id", function(d, i, j){
              var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              return k.toString()+i.toString();
          })
          .attr("x", function(d, i) {
              return ((i * 20));
          })
          .attr("y", function(d, i, j) {
            var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              return ((k * 12));
          })
          .attr("rx", 4)
          .attr("ry", 4)
          .attr("class", function(d, i, j) {
              var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              return "cell cr" + k + " cc" + i;
          })
          .attr("row", function(d, i, j) {
              var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
              return k;
          })
          .attr("col", function(d, i, j) {
              return i;
          })
          .attr("width", cellSize)
          .attr("height", 12)
          .attr('stroke-width', 1.5)
          .attr("stroke", function(d, i, j) {
            var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
            if (eachType[0].length != 0) 
              if (eachType[0].includes(data.index[k]))
                return colorTypes[0]
            if (eachType[1].length != 0) 
              if (eachType[1].includes(data.index[k]))
                return colorTypes[1]
            if (eachType[2].length != 0) 
              if (eachType[2].includes(data.index[k]))
                return colorTypes[2]
            if (eachType[3].length != 0) 
              if (eachType[3].includes(data.index[k]))
                return colorTypes[3]
          })
          .style("fill", function(d) {
              if (d == -1) return colorTypes[3]
              else if (d == -2) return colorTypes[2]
              else if (d == -3) return colorTypes[1]
              else if (d == -4) return colorTypes[0]
              else return colorScale(d)
          })
          .on('mouseover', function(d, i, j) {
              if (i == (len-1)) {

              } else {
                var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
                d3.select('#colLabel_' + i).classed("hover", true);
                d3.select('#rowLabel_' + k).classed("hover", true);
                if (d != null) {
                    tooltip.style("visibility", "visible");
                    tooltip.html('<div class="heatmap_tooltip">' + d.toFixed(2) + '</div>');
                } else
                    tooltip.style("visibility", "hidden");
              }
          })
          .on('mouseout', function(d, i, j) {
              if (i == (len-1)) {

              } else {
                var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
                d3.select('#colLabel_' + i).classed("hover", false);
                d3.select('#rowLabel_' + k).classed("hover", false);
                tooltip.style("visibility", "hidden");
              }
          })
          .on("mousemove", function(d, i) {
              tooltip.style("top", 70 + "px").style("left", 25 + "px");
          })
          // .on('click', function(d, i, j) {
          //   var rowsExtracted = svg.selectAll(".row")._groups[0]
          //   var k = Array.prototype.indexOf.call(j[i].parentNode.parentNode.childNodes,j[i].parentNode) - 3;
          //   d3.select(this).style("fill", function(d) {
          //     if (d3.select(this).style("fill") === "yellow" || d3.select(this).style("fill") === "url(\"#diagonalHatch\")") {
          //       if (d3.select(this).style("fill") === "url(\"#diagonalHatch\")"){
          //         if (d == -2) {
          //           const index = featuresAddRem.indexOf(k);
          //           if (index > -1) {
          //             featuresAddRem.splice(index, 1);
          //           }
          //           if (status.includes(Features[k])) {
          //             var outputArray = [];
          //             for (let i = 0; i < status.length; i++) {
          //               if (status[i] !== Features[k]) {
          //                 outputArray.push(status[i]);
          //               }
          //             }
          //             EventBus.$emit('updateRemovedFeaturesBack', outputArray)
          //           }
          //           EventBus.$emit('updateHistoryKey', 0)
          //           EventBus.$emit('updateValuesofHistory', k)
          //           EventBus.$emit('addFeature', featuresAddRem)
          //           return 'yellow'
          //         } else if (d == -3) {
          //           return '#969696'
          //         } else if (d == -4) {
          //           // svg.selectAll("rect").each(function(d){
          //           //   if (d == -4) {
          //           //     d3.select(this).style("fill", "url(#diagonalHatch)")
          //           //   }
          //           // })
          //           featuresGen.push(k)
          //           EventBus.$emit('updateHistoryKey', 3)
          //           EventBus.$emit('addFeatureGen', featuresGen)
          //           return 'yellow'
          //         } else {
          //           return colorScale(d)
          //         }
          //       } else {
          //         if (d == -4) {
          //           const index = featuresGen.indexOf(k);

          //           if (index > -1) {
          //             featuresGen.splice(index, 1);
          //           }
          //           EventBus.$emit('updateHistoryKey', 4)
          //           EventBus.$emit('removeFeaturesGen', featuresGen)
          //           return "url(#diagonalHatch)"
          //         } else {
          //           status.push(Features[k])
          //           featuresAddRem.push(k)
          //           EventBus.$emit('updateRemovedFeatures', status)
          //           EventBus.$emit('updateHistoryKey', 1)
          //           EventBus.$emit('updateValuesofHistory', k)
          //           EventBus.$emit('removeFeatures', featuresAddRem)
          //           return "url(#diagonalHatch)"
          //         }  
          //       }
          //     } else {
          //       if (d == -3) {
          //         return '#969696'
          //       } else {
          //         return colorScale(d)
          //       }
          //     }
          //   })
          // });

      var svgLeg = d3.select("#LegendHeat");
      svgLeg.selectAll("*").remove();
        
      var svgLeg = d3.select("#LegendHeat").append("svg")
        .attr("width", widthHeatmap)
        .attr("height", viewerHeight*0.12)

      var legend = svgLeg.append('g')
          .attr("class", "legend")
          .attr("transform", "translate(100,0)")
          .selectAll(".legendElement")
          .data([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
          .enter().append("g")
          .attr("class", "legendElement");

      legend.append("svg:rect")
          .attr("x", function(d, i) {
              return legendElementWidth * i;
          })
          .attr("y", viewerPosTop)
          .attr("class", "cellLegend bordered")
          .attr("width", legendElementWidth)
          .attr("height", cellSize / 2)
          .style("fill", function(d, i) {
              return colors[i];
          });

      legend.append("text")
          .attr("class", "mono legendElement")
          .text(function(d) {
              return "≥" + Math.round(d * 100) / 100;
          })
          .attr("x", function(d, i) {
              return legendElementWidth * i;
          })
          .attr("y", viewerPosTop + cellSize);

      svgLeg.append("text").attr("x", 235).attr("y", 60).text("Normalized Values").style("font-size", "16px").attr("alignment-baseline","top")

      //==================================================
      // Change ordering of cells
      function sortByValues(rORc, i, sortOrder) {
          var t = svg.transition().duration(1000);
          var values = [];
          var sorted;
          d3.selectAll(".c" + rORc + i)
              .filter(function(d) {
                  if (d != null) values.push(d);
                  else values.push(-999); // to handle NaN
              });
          if (rORc == "r") { // sort on cols
              sorted = d3.range(col_number).sort(function(a, b) {
                  if (sortOrder) {
                      return values[b] - values[a];
                  } else {
                      return values[a] - values[b];
                  }
              });
              t.selectAll(".cell")
                  .attr("x", function(d) {
                      var col = parseInt(d3.select(this).attr("col"));
                      return sorted.indexOf(col) * cellSize;
                  });
              t.selectAll(".colLabel")
                  .attr("y", function(d, i) {
                      return sorted.indexOf(i) * cellSize;
                  })
                  .attr("transform", function(d, i) {
                      return "translate(" + cellSize / 2 + ", -3) rotate(-90) rotate(45, 0, " + (sorted.indexOf(i) * cellSize) + ")";
                  });
              t.selectAll(".rowLabel")
               .style('font-weight',function(d, loop){
                 if (loop == i) {
                   return "bold"
                 } else {
                   return "normal"
                 }
                  
                });
          } else { // sort on rows
              sorted = d3.range(row_number).sort(function(a, b) {
                  if (sortOrder) {
                      return values[b] - values[a];
                  } else {
                      return values[a] - values[b];
                  }
              });
              t.selectAll(".cell")
                  .attr("y", function(d) {
                      var row = parseInt(d3.select(this).attr("row"));
                      return sorted.indexOf(row) * cellSize;
                  });
              t.selectAll(".rowLabel")
                  .attr("y", function(d, i) {
                      return sorted.indexOf(i) * cellSize;
                  })
                  .attr("transform", function(d, i) {
                      return "translate(-3," + cellSize / 1.8 + ")";
                  });
              t.selectAll(".colLabel")
               .style('font-weight',function(d, loop){
                 if (loop == i) {
                   return "bold"
                 } else {
                   return "normal"
                 }
                  
                });
              }
          }

          //==================================================
          d3.select("#order").on("change", function() {
            var newOrder = d3.select("#order").property("value");	
            this.changeOrder(newOrder, heatmapId);
          });

          //==================================================
          d3.select("#palette")
            .on("keyup", function() {
              var newPalette = d3.select("#palette").property("value");
              if (newPalette != null)						// when interfaced with jQwidget, the ComboBox handles keyup event but value is then not available ?
                this.changePalette(newPalette, heatmapId);
            })
            .on("change", function() {
            var newPalette = d3.select("#palette").property("value");
              this.changePalette(newPalette, heatmapId);
            });

        //==================================================
      d3.select('#colLabel_'+(len-1)).dispatch('click');
    },
    changeOrder(newOrder, heatmapId) {
  var svg = d3.select(heatmapId);
  var cellSize = this.cellSize
  var t = svg.transition().duration(1000);
  if (newOrder == "sortinit_col") { // initial sort on cols (alphabetically if produced like this)
      t.selectAll(".cell")
          .attr("x", function(d) {
              var col = parseInt(d3.select(this).attr("col"));
              return col * cellSize;
          });
      t.selectAll(".colLabel")
          .attr("y", function(d, i) {
              return i * cellSize;
          })
          .attr("transform", function(d, i) {
              return "translate(" + cellSize / 2 + ", -3) rotate(-90) rotate(45, 0, " + (i * cellSize) + ")";
          });
  } else if (newOrder == "sortinit_row") { // initial sort on rows (alphabetically if produced like this)
      t.selectAll(".cell")
          .attr("y", function(d) {
              var row = parseInt(d3.select(this).attr("row"));
              return row * cellSize;
          });
      t.selectAll(".rowLabel")
          .attr("y", function(d, i) {
              return i * cellSize;
          })
          .attr("transform", function(d, i) {
              return "translate(-3," + cellSize / 1.5 + ")";
          });
  } else if (newOrder == "sortinit_col_row") { // initial sort on rows and cols (alphabetically if produced like this)
      t.selectAll(".cell")
          .attr("x", function(d) {
              var col = parseInt(d3.select(this).attr("col"));
              return col * cellSize;
          })
          .attr("y", function(d) {
              var row = parseInt(d3.select(this).attr("row"));
              return row * cellSize;
          });
      t.selectAll(".colLabel")
          .attr("y", function(d, i) {
              return i * cellSize;
          })
          .attr("transform", function(d, i) {
              return "translate(" + cellSize / 2 + ", -3) rotate(-90) rotate(45, 0, " + (i * cellSize) + ")";
          });
      t.selectAll(".rowLabel")
          .attr("y", function(d, i) {
              return i * cellSize;
          })
          .attr("transform", function(d, i) {
              return "translate(-3," + cellSize / 1.5 + ")";
          });
        }
    },
    reset () {
      var svg = d3.select("#Heatmap");
      svg.selectAll("*").remove();
    },
    brush () {
      var columnLabels = document.getElementsByClassName('colLabels')[0];
      var modelIds = JSON.parse(this.GetResultsAll[13])

      var selectedIds = []
      for (let i = 0; i < this.highlighted.length; i++) {
          let looping = this.highlighted[i]
          selectedIds.push(looping)
      }
      for (let i = 0; i < modelIds.length; i++) {
          columnLabels.childNodes[i].style.fill = "#000";
      }
      for (let i = 0; i < selectedIds.length; i++) {
          let index = modelIds.indexOf(selectedIds[i])
          columnLabels.childNodes[index].style.fill = "#AF4427";
      }
    }
  },
  mounted () {

    EventBus.$on('limitPoints', data => {
      this.limitCompletelyPoints = data 
    })
    EventBus.$on('emittedEventCallingPerformanceProb', data => {
      this.dataFI = data 
    })
    EventBus.$on('emittedEventCallingAdditionalDataHeatmap', data => { this.ColorEachType = data })
    EventBus.$on('emittedEventCallingPerformanceProb', this.HeatmapView)
    EventBus.$on('emittedEventCallingPerformanceUpdate', this.HeatmapView)
    EventBus.$on('emittedEventCallingPerformanceUpdateHeat', this.HeatmapView)
    

    EventBus.$on('reset', this.reset)
  }
}
</script>

<style>
.heatmap {
  font-size: 9px;
  font-family: monospace;
}
rect.bordered {
  stroke: #000000;
  stroke-width:1px;   
}
text.mono {
  font-size: 9px;
  font-family: monospace;
}
text.legendElement {
  font-size: 10px;
}

text.hover {
  font-weight: bold;
  fill: #66F;
  font-background: #000;
}

.heatmap_tooltip {
  text-align: center;
  font-family: monospace;
  font-size: 14pt;
  color: #000;
  position: relative;
  background: rgba(255, 255, 255, 0.8);
  border: 4px solid #66F;
  padding: 5px;
  border-radius: 8px ;
  -webkit-border-top-left-radius: 8px;
  -webkit-border-top-right-radius: 8px;
  -webkit-border-bottom-right-radius: 8px;
  -webkit-border-bottom-left-radius: 8px;
  -khtml-border-top-left-radius: 8px;
  -khtml-border-top-right-radius: 8px;
  -khtml-border-bottom-right-radius: 8px;
  -khtml-border-bottom-left-radius: 8px;
  -moz-border-radius-topleft: 8px;
  -moz-border-radius-topright: 8px;
  -moz-border-radius-bottomright: 8px;
  -moz-border-radius-bottomleft: 8px;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  border-bottom-left-radius: 8px;
  width: 100px;
  z-index:10000;
  -webkit-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.8);
  -moz-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.8);
  box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.8);
}
.heatmap_tooltip:after, .heatmap_tooltip:before {
  top: 100%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}
.heatmap_tooltip:after {
  border-color: rgba(236, 240, 241, 0);
  border-top-color: #FFFFF;
  border-width: 10px;
  left: 50%;
  margin-left: -10px;
}
.heatmap_tooltip:before {
  border-color: rgba(44, 62, 80, 0);
  border-top-color: #66F;
  border-width: 16px;
  left: 50%;
  margin-left: -16px;
}

</style>