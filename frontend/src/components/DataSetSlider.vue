<template>
<div>
  <label id="data" for="param-dataset" data-toggle="tooltip" data-placement="right" title="Tip: use one of the data sets already provided or upload a new file.">{{ dataset }}</label>
  <select id="selectFile" @change="selectDataSet()">
      <option value="VehicleC.csv" >Vehicle Silhouette</option>
      <option value="breastC.csv" >Breast Cancer</option>
      <option value="IrisC.csv" selected>Iris Flower</option>
  </select>
  <button style="float: right;" class="btn-outline-dark"
  id="know"
  v-on:click="knowClass">
  <font-awesome-icon icon="th" />
  {{ valueKnowE }}
  </button>
  &nbsp;&nbsp;&nbsp;
  <ul class="nav nav-tabs" id="myTab" role="tablist">
  <li class="nav-item">
    <a class="nav-link active" id="cluster-tab" @click="clickedClusterTab()" data-toggle="tab" href="#cluster" role="tab" aria-controls="cluster" aria-selected="false"><font-awesome-icon icon="dot-circle"/> UMAP</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" id="profile-tab" @click="clickedUnder()" data-toggle="tab" href="#profile" role="tab" aria-controls="profile" aria-selected="false"><font-awesome-icon icon="times-circle"/> Undersampling (US)</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" id="contact-tab" @click="clickedOver()" data-toggle="tab" href="#contact" role="tab" aria-controls="contact" aria-selected="false"><font-awesome-icon icon="plus-circle"/> Oversampling (OS)</a>
  </li>
  </ul>
    <div class="tab-content" id="myTabContent">
      <div class="tab-pane fade show active" id="cluster" role="tabpanel" aria-labelledby="cluster-tab">
        <div id="BarChartUMAP" style="display: none"></div>
        <div id="LineChartUMAP" style="display: none"></div>
      </div>
        <div class="tab-pane fade show" id="profile" role="tabpanel" aria-labelledby="profile-tab">
                  <div id="checkbox_div" class="switch-toggle switch-3 switch-candy" style="margin-top: 10px; margin-bottom: 5px">

                    <input id="disun" name="un" type="radio" checked="checked"/>
                    <label for="disun" @click="underNothing()">Disabled</label>

                    <input id="oss" name="un" type="radio"/>
                    <label for="oss" @click="clickedOSS()">OSS</label>

                    <input id="ncr" name="un" type="radio"/>
                    <label for="ncr" @click="clickedNCR()">NCR</label>

                    <a></a>
                  </div>
              <table id="tableUnder" class="table table-borderless table-sm" style="display: none">
                <tbody>
                  <tr>
                  <td>Types:</td>
                  <div class="switch-toggle checkID" style="margin-top: 3px">

                    <input id="safeUnder" @change="WhatHappenedUnder()" name="type" type="checkbox" checked="checked"/>
                    <label for="safeUnder">Safe</label>

                    <input id="bordUnder" @change="WhatHappenedUnder()" name="type" type="checkbox" checked="checked"/>
                    <label for="bordUnder">Borderline</label>

                    <input id="rareUnder" @change="WhatHappenedUnder()" name="type" type="checkbox" checked="checked" />
                    <label for="rareUnder">Rare</label>

                    <input id="outUnder" @change="WhatHappenedUnder()" name="type" type="checkbox" checked="checked"/>
                    <label for="outUnder">Outlier</label>

                    <a></a>
                  </div>
                  </tr>
                  <tr>
                    <td>K-value NN:</td>
                    <td><b-form-slider ref="basic1" v-model="basicValue1" :min="1" :max="50" trigger-change-event @slide-stop="kNNUnderSlider" style="padding-right: 15px;"></b-form-slider>{{ basicValue1 }}</td>
                  </tr>
                  <tr id="thresh" style="display: none">
                    <td>Threshold:</td>
                    <td><b-form-slider ref="basic2" v-model="basicValue2" :min="0" :max="100" trigger-change-event @slide-stop="thrsUnderSlider" style="padding-right: 15px;"></b-form-slider>{{ basicValue2 }}%</td>
                  </tr>
                  <tr id="seed" >
                    <td>Seeds:</td>
                    <td><b-form-slider ref="basic3" v-model="basicValue3" :min="1" :max="250" :step="1" trigger-change-event @slide-stop="seedUnderSlider" style="padding-right: 15px;"></b-form-slider>{{ basicValue3 }}</td>
                  </tr>
                  <tr>
                  <td>Sampling:</td>
                  <div class="switch-toggle switch-3 switch-candy" style="margin-top: 3px">

                    <input id="majun" name="samun" type="radio" />
                    <label for="majun" @click="clickedMajUnder()">Majority</label>

                    <input id="nminun" name="samun" type="radio" />
                    <label for="nminun" @click="clickedNotMinUnder()">≠ Minority</label>

                    <input id="nmajun" name="samun" type="radio" />
                    <label for="nmajun" @click="clickedNotMajUnder()">≠ Majority</label>

                    <input id="customun" name="samun" type="radio" checked="checked" />
                    <label for="customun" @click="clickedCusUnder()">All</label>

                    <a></a>
                  </div>
                  </tr>
                </tbody>
              </table>
        </div>
        <div class="tab-pane fade" id="contact" role="tabpanel" aria-labelledby="contact-tab">
              <div class="switch-toggle switch-3 switch-candy" style="margin-top: 10px; margin-bottom: 5px">

                          <input id="disov" name="ov" type="radio" checked="checked"/>
                          <label for="disov" @click="overNothing()">Disabled</label>

                          <input id="smote" name="ov" type="radio"/>
                          <label for="smote" @click="clickedSMOTE()">SMOTE</label>

                          <input id="adasyn" name="ov" type="radio"/>
                          <label for="adasyn" @click="clickedADASYN()">ADASYN</label>

                          <a></a>
                        </div>
                    <table id="tableOver" class="table table-borderless table-sm" style="display: none">
                      <tbody>
                        <tr>
                        <td>Types:</td>
                        <div class="switch-toggle checkID" style="margin-top: 3px">

                          <input id="safe" @change="WhatHappened()" name="type" type="checkbox" checked="checked"/>
                          <label for="safe">Safe</label>

                          <input id="bord" @change="WhatHappened()" name="type" type="checkbox" checked="checked"/>
                          <label for="bord">Borderline</label>

                          <input id="rare" @change="WhatHappened()" name="type" type="checkbox" checked="checked" />
                          <label for="rare">Rare</label>

                          <input id="out" @change="WhatHappened()" name="type" type="checkbox" checked="checked"/>
                          <label for="out">Outlier</label>

                          <a></a>
                        </div>
                        </tr>
                        <tr>
                          <td>K-value NN:</td>
                          <td><b-form-slider ref="basic4" v-model="basicValue4" :min="1" :max="50" trigger-change-event @slide-stop="kNNOverSlider" style="padding-right: 15px;"></b-form-slider>{{ basicValue4 }}</td>
                        </tr>
                        <tr>
                        <td>Sampling:</td>
                        <div class="switch-toggle switch-3 switch-candy" style="margin-top: 3px">

                          <input id="majov" name="samov" type="radio"  />
                          <label for="majov" @click="clickedMajOver()">Minority</label>

                          <input id="nminov" name="samov" type="radio"/>
                          <label for="nminov" @click="clickedNotMinOver()">≠ Minority</label>

                          <input id="nmajov" name="samov" type="radio" />
                          <label for="nmajov" @click="clickedNotMajOver()">≠ Majority</label>

                          <input id="customov" name="samov" type="radio" checked="checked" />
                          <label for="customov" @click="clickedCusOver()">All</label>

                          <a></a>
                        </div>
                        </tr>
                      </tbody>
                    </table>
          </div>
        </div>
        </div>
</template>

<script>
import { EventBus } from '../main.js'
import * as d3Base from 'd3'
import * as Plotly from 'plotly.js'
import { sliderBottom } from 'd3-simple-slider'
import 'bootstrap-toggle/css/bootstrap-toggle.css'
import 'bootstrap-slider/dist/css/bootstrap-slider.css'
import $ from 'jquery'; // <-to import jquery
// attach all d3 plugins to the d3 library
const d3v5 = Object.assign(d3Base, { sliderBottom })

export default {
  name: 'DataSetSlider',
  data () {
    return {
      valueKnowE: 'Data Types Projections',
      defaultDataSet: 'VehicleC', // default value for the first data set
      //defaultDataSet: 'VehicleC',
      activeUnder: 0,
      activeOver: 0,
      basicValueGlob: 0,
      minDist: 0,
      maxValue: 9,
      basicValue1: 5,
      basicValue2: 50,
      basicValue3: 1,
      sampleUnder: 'all',
      textClass0Under: '',
      textClass1Under: '',
      textClass2Under: '',
      basicValue4: 5,
      sampleOver: 'all',
      types: ['safe','borderline','rare','outlier'],
      typesUnder: ['safe','borderline','rare','outlier'],
      textClass0Over: '',
      textClass1Over: '',
      textClass2Over: '',
      superVariable: [],
      dataset: 'Data Set:',
      onceOnly: true,
      AllData: [],
      kValues: [5,6,7,8,9,10,11,12,13],
      mDistValues: [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    }
  },
  methods: {
    knowClass () {
      EventBus.$emit('OpenModal')
    },
    clickedOver () {
      document.getElementById("disun").checked = true;
    },
    clickedUnder () {
    },
    clickedClusterTab () {
      document.getElementById("BarChartUMAP").style.display = "";
      document.getElementById("LineChartUMAP").style.display = "";
    },
    globalFunction () {
      this.superVariable[0] = this.basicValueGlob
      this.superVariable[1] = this.activeUnder
      this.superVariable[2] = this.basicValue1
      this.superVariable[3] = this.sampleUnder
      this.superVariable[4] = this.basicValue3
      this.superVariable[5] = (this.basicValue2 / 100)
      this.superVariable[6] = this.activeOver
      this.superVariable[7] = this.basicValue4
      this.superVariable[8] = this.sampleOver
      this.superVariable[9] = this.types
      this.superVariable[10] = this.minDist
      this.superVariable[11] = this.typesUnder
      console.log(this.superVariable)
      EventBus.$emit('updateNeighborsGlobal', this.superVariable)
    },
    kNNUnderSlider () {
      this.globalFunction()
    },
    thrsUnderSlider () {
      this.globalFunction()
    }, 
    seedUnderSlider () {
      this.globalFunction()
    },
    clickedMajUnder () {
      this.sampleUnder = 'majority'
      this.globalFunction()
    },
    clickedNotMinUnder () {
      this.sampleUnder = 'not minority'
      this.globalFunction()
    },
    clickedNotMajUnder () {
      this.sampleUnder = 'not majority'
      this.globalFunction()
    },
    WhatHappenedUnder () {
      var safe = document.getElementById('safeUnder');
      var bord = document.getElementById('bordUnder');
      var rare = document.getElementById('rareUnder');
      var out = document.getElementById('outUnder');

      if (safe.checked)
        this.typesUnder[0] = 'safe'
      else
        this.typesUnder[0] = ''
      if (bord.checked)
        this.typesUnder[1] = 'borderline'
      else
        this.typesUnder[1] = ''
      if (rare.checked)
        this.typesUnder[2] = 'rare'
      else
        this.typesUnder[2] = ''
      if (out.checked)
        this.typesUnder[3] = 'outlier'
      else
        this.typesUnder[3] = ''
      this.globalFunction()
    },
    clickedCusUnder () {
      this.sampleUnder = 'all'
      this.globalFunction()
    },
    kNNOverSlider () {
      this.globalFunction()
    },
    underNothing () {
      EventBus.$emit('firstTimeConfusion', 4)
      document.getElementById("tableUnder").style.display = "none";
      document.getElementById("BarChartUMAP").style.display = "none";
      document.getElementById("LineChartUMAP").style.display = "none";
      EventBus.$emit('updateMode', 0)
      this.activeUnder = 0
      this.globalFunction()
    },
    clickedOSS () {
      document.getElementById("tableUnder").style.display = "";
      document.getElementById("thresh").style.display = "none";
      document.getElementById("seed").style.display = "";
      EventBus.$emit('updateMode', 1)
      this.activeUnder = 1
      this.globalFunction()
    },
    clickedNCR () {
      document.getElementById("tableUnder").style.display = "";
      document.getElementById("seed").style.display = "none";
      document.getElementById("thresh").style.display = "";
      EventBus.$emit('updateMode', 1)
      this.activeUnder = 2
      this.globalFunction()
    },
    overNothing () {
      EventBus.$emit('firstTimeConfusion', 4)
      document.getElementById("tableOver").style.display = "none";
      document.getElementById("BarChartUMAP").style.display = "none";
      document.getElementById("LineChartUMAP").style.display = "none";
      EventBus.$emit('updateMode', 0)
      this.activeOver = 0
      this.globalFunction()
    },
    clickedSMOTE () {
      document.getElementById("tableOver").style.display = "";
      EventBus.$emit('updateMode', 2)
      this.activeOver = 1
      this.globalFunction()
    },
    clickedADASYN () {
      document.getElementById("tableOver").style.display = "";
      EventBus.$emit('updateMode', 2)
      this.activeOver = 2
      this.globalFunction()
    },
    clickedMajOver () {
      this.sampleOver = 'minority'
      this.globalFunction()
    },
    clickedNotMinOver () {
      this.sampleOver = 'not minority'
      this.globalFunction()
    },
    clickedNotMajOver () {
      this.sampleOver = 'not majority'
      this.globalFunction()
    },
    clickedCusOver () {
      this.sampleOver = 'all'
      this.globalFunction()
    },
    WhatHappened () {
      var safe = document.getElementById('safe');
      var bord = document.getElementById('bord');
      var rare = document.getElementById('rare');
      var out = document.getElementById('out');

      if (safe.checked)
        this.types[0] = 'safe'
      else
        this.types[0] = ''
      if (bord.checked)
        this.types[1] = 'borderline'
      else
        this.types[1] = ''
      if (rare.checked)
        this.types[2] = 'rare'
      else
        this.types[2] = ''
      if (out.checked)
        this.types[3] = 'outlier'
      else
        this.types[3] = ''
      this.globalFunction()
    },
    selectDataSet () {   
      const fileName = document.getElementById('selectFile')
      this.defaultDataSet = fileName.options[fileName.selectedIndex].value
      this.defaultDataSet = this.defaultDataSet.split('.')[0]

      this.dataset = "Data set"
      d3v5.select("#data").select("input").remove(); // Remove the selection field.
      EventBus.$emit('SendToServerDataSetConfirmation', this.defaultDataSet)
    },
      BarChartViewUMAP() {

        document.getElementById("BarChartUMAP").style.display = "";
        Plotly.purge('BarChartUMAP')

        var distribution = JSON.parse(this.AllData[14])
        var whichToPickAuto = JSON.parse(this.AllData[16])
        var currentValues = this.kValues
        var colorOutlines = ['rgba(217,217,217,1)','rgba(150,150,150,1)','rgba(82,82,82,1)','rgba(0,0,0,1)']
        var types = ['Safe','Borderline','Rare','Outlier']

        var traverseArray = []
        var resultingArray = []

        for (let k = 0; k < types.length; k++) {
          traverseArray = []
          for (let m = 0; m < distribution.length; m++) {
            traverseArray.push(distribution[m][k].toFixed(2))
          }
          resultingArray.push(traverseArray)
        }

        var data = []

        for (var i = (types.length-1); i >= 0; i--) {
          data.push({
            type: 'bar',
            name: types[i],
            x: currentValues,
            y: resultingArray[i],
            marker: {
              color: colorOutlines[i]
            },
          })  
        }
        var tickTextCompute = [];
        for (let i = 0; i < currentValues.length; i++) {
          if (i == this.basicValueGlob)
            tickTextCompute.push('<b>* ' + currentValues[i].toString() + ' *</b>      ')
          else
            tickTextCompute.push(currentValues[i].toString() + '      ')
        }

          var width = 615
          var height = 120

          var layout = {
            yaxis: {
              title: 'Types (%)'
            },
            x: 1,
            xanchor: 'right',
            xaxis: {
              tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
              tickvals: this.kValues,
              ticktext: tickTextCompute,
              title: 'Number of Neighbors',
            },
            barmode: 'stack',
            font: { family: 'Helvetica', size: 14, color: '#000000' },
            autosize: false,
            width: width,
            height: height,
            showlegend: false,
            margin: {
              l: 50,
              r: 0,
              b: 35,
              t: 5,
              pad: 0
            },
          }
      
          var myPlot = document.getElementById('BarChartUMAP')

          var config = {scrollZoom: false, displaylogo: false, displayModeBar: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: true}

          Plotly.newPlot(myPlot, data, layout, config)
          
          myPlot.on('plotly_click', function(data){
            var pt
            var ind
              for(var i=0; i < data.points.length; i++){
                  pt = data.points[i].x
              }
              for (var j=0; j < currentValues.length; j++) {
                if (currentValues[j] == pt) 
                  ind = j
              }
              EventBus.$emit('firstTimeConfusion', 2)
              EventBus.$emit('sendNewK', ind)
              EventBus.$emit('sendNewDist', whichToPickAuto[ind])
          });
      },
    LineChartView () {
        document.getElementById("LineChartUMAP").style.display = "";
        Plotly.purge('LineChartUMAP')

        var distances = JSON.parse(this.AllData[15])
        var currentValues = this.mDistValues

        var yAxis = []
        for (let i=0; i<distances[this.basicValueGlob].length; i++) {
          yAxis.push(distances[this.basicValueGlob][i].toFixed(2))
        }

        var trace1 = {
          x: this.mDistValues,
          y: yAxis,
          type: 'scatter',
          line: {
            color: 'rgb(0, 0, 0)',
          },
          marker: {
            symbol: 'diamond'
          }
        }

        var data = [trace1]

        var tickTextCompute = [];
        for (let i = 0; i < currentValues.length; i++) {
          if (i == this.minDist)
            tickTextCompute.push('<b>* ' + currentValues[i].toString() + ' *</b>    ')
          else
            tickTextCompute.push(currentValues[i].toString() + '     ')
        }

        var width = 615
        var height = 100

        var layout = {
          yaxis: {
            title: 'SDC (%)'
          },
          x: 1,
          xanchor: 'right',
          xaxis: {
            tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
            tickvals: this.mDistValues,
            ticktext: tickTextCompute,
            title: 'Minimum Distance',
          },
          font: { family: 'Helvetica', size: 14, color: '#000000' },
          autosize: false,
          width: width,
          height: height,
          showlegend: false,
          margin: {
            l: 50,
            r: 0,
            b: 35,
            t: 5,
            pad: 0
          },
        }
    
        var myPlot = document.getElementById('LineChartUMAP')

        var config = {scrollZoom: false, displaylogo: false, displayModeBar: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: true}

        Plotly.newPlot(myPlot, data, layout, config)
        
        myPlot.on('plotly_click', function(data){
          var ind
          ind = data.points[0].pointIndex
          EventBus.$emit('firstTimeConfusion', 2)
          EventBus.$emit('sendNewDist', ind)
        });

    }
  },
  mounted () {
    EventBus.$on('SendSelectedPointsUpdateIndicatorOver', data => { 
      document.getElementById("tableOver").style.display = "none";
      document.getElementById("BarChartUMAP").style.display = "none";
      document.getElementById("LineChartUMAP").style.display = "none";
      //EventBus.$emit('updateMode', 0) missing that!
      this.activeOver = 0
      document.getElementById("disov").checked = true; 
    })
    EventBus.$on('SendSelectedPointsUpdateIndicatorUnder', data => { 
      document.getElementById("tableUnder").style.display = "none";
      document.getElementById("BarChartUMAP").style.display = "none";
      document.getElementById("LineChartUMAP").style.display = "none";
      EventBus.$emit('updateMode', 0)
      this.activeUnder = 0
      document.getElementById("disun").checked = true; 
    })
    EventBus.$on('emittedEventUpdateSlider', data => { this.AllData = data })
    EventBus.$on('emittedEventUpdateSlider', this.BarChartViewUMAP)
    EventBus.$on('emittedEventUpdateSlider', this.LineChartView)
    EventBus.$on('sendNewK',  data => {
        this.basicValue1 = this.kValues[data]
        this.basicValue4 = this.kValues[data]
        this.basicValueGlob = data 
       })
    EventBus.$on('sendNewDist',  data => { this.minDist = data })
    EventBus.$on('sendNewDist',  this.globalFunction)
  },
}
</script>

<style>

.nav-link {
  color: black !important;
}

.nav-link.active {
  color: #000000 !important;
}

.slider-handle {
  background: #000000 !important;
}

.checkID input[type=checkbox] {
    display: none;
}

.checkID input:checked + label {
    color: #000000;
}

.checkID input:checked + label:before {
    content: "\2713 ";
}

.checkID {
  border: solid 1px black;
}

/* new stuff */
.check {
    visibility: hidden;
}

input:checked + label .check {
    visibility: visible;
}

input.checkbox:checked + label:before {
  
    content: "";
}



.switch-toggle {
  font-size: 16px;
}

.switch-toggle label:not(.disabled) {
  cursor: pointer;
}

.switch-toggle a, .switch-light span span {
  display: none; }

/* We can't test for a specific feature,
 * so we only target browsers with support for media queries.
 */
@media only screen {
  /* Checkbox
 */
  .switch-light {
    position: relative;
    display: block;
    /* simulate default browser focus outlines on the switch,
   * when the inputs are focused.
   */ }
    .switch-light::after {
      clear: both;
      content: "";
      display: table; }
    .switch-light *, .switch-light *:before, .switch-light *:after {
      box-sizing: border-box; }
    .switch-light a {
      display: block;
      -webkit-transition: all 0.2s ease-out;
      -moz-transition: all 0.2s ease-out;
      transition: all 0.2s ease-out; }
    .switch-light label, .switch-light > span {
      /* breathing room for bootstrap/foundation classes.
     */
      line-height: 2em;
      vertical-align: middle; }
    .switch-light input:focus ~ span a, .switch-light input:focus + label {
      outline-width: 2px;
      outline-style: solid;
      outline-color: Highlight;
      /* Chrome/Opera gets its native focus styles.
     */ }
      @media (-webkit-min-device-pixel-ratio: 0) {
        .switch-light input:focus ~ span a, .switch-light input:focus + label {
          outline-color: -webkit-focus-ring-color;
          outline-style: auto; } }
  /* don't hide the input from screen-readers and keyboard access
 */
  .switch-light input {
    position: absolute;
    opacity: 0;
    z-index: 3; }
  .switch-light input:checked ~ span a {
    right: 0%; }
  /* inherit from label
 */
  .switch-light strong {
    font-weight: inherit; }
  .switch-light > span {
    position: relative;
    overflow: hidden;
    display: block;
    min-height: 2em;
    /* overwrite 3rd party classes padding
   * eg. bootstrap .well
   */
    padding: 0;
    text-align: left; }
  .switch-light span span {
    position: relative;
    z-index: 2;
    display: block;
    float: left;
    width: 50%;
    text-align: center;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none; }
  .switch-light a {
    position: absolute;
    right: 50%;
    top: 0;
    z-index: 1;
    display: block;
    width: 50%;
    height: 100%;
    padding: 0; }
  /* Radio Switch
 */
  .switch-toggle {
    position: relative;
    display: block;
    /* simulate default browser focus outlines on the switch,
   * when the inputs are focused.
   */
    /* For callout panels in foundation
  */
    padding: 0 !important;
    /* 2 items
   */
    /* 3 items
   */
    /* 4 items
   */
    /* 5 items
   */
    /* 6 items
   */ }
    .switch-toggle::after {
      clear: both;
      content: "";
      display: table; }
    .switch-toggle *, .switch-toggle *:before, .switch-toggle *:after {
      box-sizing: border-box; }
    .switch-toggle a {
      display: block;
      -webkit-transition: all 0.2s ease-out;
      -moz-transition: all 0.2s ease-out;
      transition: all 0.2s ease-out; }
    .switch-toggle label, .switch-toggle > span {
      /* breathing room for bootstrap/foundation classes.
     */
      line-height: 2em;
      vertical-align: middle; }
    .switch-toggle input:focus ~ span a, .switch-toggle input:focus + label {
      outline-width: 2px;
      outline-style: solid;
      outline-color: Highlight;
      /* Chrome/Opera gets its native focus styles.
     */ }
      @media (-webkit-min-device-pixel-ratio: 0) {
        .switch-toggle input:focus ~ span a, .switch-toggle input:focus + label {
          outline-color: -webkit-focus-ring-color;
          outline-style: auto; } }
    .switch-toggle input {
      position: absolute;
      left: 0;
      opacity: 0; }
    .switch-toggle input + label {
      position: relative;
      z-index: 2;
      display: block;
      float: left;
      padding: 0 0.5em;
      margin: 0;
      text-align: center; }
    .switch-toggle a {
      position: absolute;
      top: 0;
      left: 0;
      padding: 0;
      z-index: 1;
      width: 10px;
      height: 100%; }
    .switch-toggle label:nth-child(2):nth-last-child(4), .switch-toggle label:nth-child(2):nth-last-child(4) ~ label, .switch-toggle label:nth-child(2):nth-last-child(4) ~ a {
      width: 50%; }
    .switch-toggle label:nth-child(2):nth-last-child(4) ~ input:checked:nth-child(3) + label ~ a {
      left: 50%; }
    .switch-toggle label:nth-child(2):nth-last-child(6), .switch-toggle label:nth-child(2):nth-last-child(6) ~ label, .switch-toggle label:nth-child(2):nth-last-child(6) ~ a {
      width: 33.33%; }
    .switch-toggle label:nth-child(2):nth-last-child(6) ~ input:checked:nth-child(3) + label ~ a {
      left: 33.33%; }
    .switch-toggle label:nth-child(2):nth-last-child(6) ~ input:checked:nth-child(5) + label ~ a {
      left: 66.66%; }
    .switch-toggle label:nth-child(2):nth-last-child(8), .switch-toggle label:nth-child(2):nth-last-child(8) ~ label, .switch-toggle label:nth-child(2):nth-last-child(8) ~ a {
      width: 25%; }
    .switch-toggle label:nth-child(2):nth-last-child(8) ~ input:checked:nth-child(3) + label ~ a {
      left: 25%; }
    .switch-toggle label:nth-child(2):nth-last-child(8) ~ input:checked:nth-child(5) + label ~ a {
      left: 50%; }
    .switch-toggle label:nth-child(2):nth-last-child(8) ~ input:checked:nth-child(7) + label ~ a {
      left: 75%; }
    .switch-toggle label:nth-child(2):nth-last-child(10), .switch-toggle label:nth-child(2):nth-last-child(10) ~ label, .switch-toggle label:nth-child(2):nth-last-child(10) ~ a {
      width: 20%; }
    .switch-toggle label:nth-child(2):nth-last-child(10) ~ input:checked:nth-child(3) + label ~ a {
      left: 20%; }
    .switch-toggle label:nth-child(2):nth-last-child(10) ~ input:checked:nth-child(5) + label ~ a {
      left: 40%; }
    .switch-toggle label:nth-child(2):nth-last-child(10) ~ input:checked:nth-child(7) + label ~ a {
      left: 60%; }
    .switch-toggle label:nth-child(2):nth-last-child(10) ~ input:checked:nth-child(9) + label ~ a {
      left: 80%; }
    .switch-toggle label:nth-child(2):nth-last-child(12), .switch-toggle label:nth-child(2):nth-last-child(12) ~ label, .switch-toggle label:nth-child(2):nth-last-child(12) ~ a {
      width: 16.6%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(3) + label ~ a {
      left: 16.6%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(5) + label ~ a {
      left: 33.2%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(7) + label ~ a {
      left: 49.8%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(9) + label ~ a {
      left: 66.4%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(11) + label ~ a {
      left: 83%; }
  /* Candy Theme
 * Based on the "Sort Switches / Toggles (PSD)" by Ormal Clarck
 * http://www.premiumpixels.com/freebies/sort-switches-toggles-psd/
 */
  .switch-toggle.switch-candy, .switch-light.switch-candy > span {
    background-color: #efefef;
    border-radius: 3px;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.3), 0 1px 0 rgba(255, 255, 255, 0.2); }
  .switch-light.switch-candy span span, .switch-light.switch-candy input:checked ~ span span:first-child, .switch-toggle.switch-candy label {
    color: #000;
    font-weight: bold;
    text-align: center;
    text-shadow: 0 0 0 #191b1e; }
  .switch-light.switch-candy input ~ span span:first-child, .switch-light.switch-candy input:checked ~ span span:nth-child(2), .switch-candy input:checked + label {
    color: #fff;
    text-shadow: 0 0 0 rgba(255, 255, 255, 0.5); }
  .switch-candy a {
    border: 1px solid #333;
    border-radius: 3px;
    box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.45);
    background-color: #000000;
    background-image: -webkit-linear-gradient(top, rgba(255, 255, 255, 0.2), transparent);
    background-image: linear-gradient(to bottom, rgba(255, 255, 255, 0.2), transparent); }
  .switch-candy-blue a {
    background-color: #0090ff; }
  .switch-candy-yellow a {
    background-color: #f5e560; }
  /* iOS Theme
*/
  .switch-ios.switch-light span span {
    color: #888b92; }
  .switch-ios.switch-light a {
    left: 0;
    top: 0;
    width: 2em;
    height: 2em;
    background-color: #fff;
    border-radius: 100%;
    border: 0.25em solid #D8D9DB;
    -webkit-transition: all .2s ease-out;
    -moz-transition: all .2s ease-out;
    transition: all .2s ease-out; }
  .switch-ios.switch-light > span {
    display: block;
    width: 100%;
    height: 2em;
    background-color: #D8D9DB;
    border-radius: 1.75em;
    -webkit-transition: all .4s ease-out;
    -moz-transition: all .4s ease-out;
    transition: all .4s ease-out; }
  .switch-ios.switch-light > span span {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    opacity: 0;
    line-height: 1.875em;
    vertical-align: middle;
    -webkit-transition: all .2s ease-out;
    -moz-transition: all .2s ease-out;
    transition: all .2s ease-out; }
    .switch-ios.switch-light > span span:first-of-type {
      opacity: 1;
      padding-left: 1.875em; }
    .switch-ios.switch-light > span span:last-of-type {
      padding-right: 1.875em; }
  .switch-ios.switch-light input:checked ~ span a {
    left: 100%;
    border-color: #4BD865;
    margin-left: -2em; }
  .switch-ios.switch-light input:checked ~ span {
    border-color: #4BD865;
    box-shadow: inset 0 0 0 30px #4BD865; }
  .switch-ios.switch-light input:checked ~ span span:first-of-type {
    opacity: 0; }
  .switch-ios.switch-light input:checked ~ span span:last-of-type {
    opacity: 1;
    color: #fff; }
  .switch-ios.switch-toggle {
    background-color: #D8D9DB;
    border-radius: 30px;
    box-shadow: inset rgba(0, 0, 0, 0.1) 0 1px 0; }
    .switch-ios.switch-toggle a {
      background-color: #4BD865;
      border: 0.125em solid #D8D9DB;
      border-radius: 1.75em;
      -webkit-transition: all 0.12s ease-out;
      -moz-transition: all 0.12s ease-out;
      transition: all 0.12s ease-out; }
    .switch-ios.switch-toggle label {
      height: 2.4em;
      color: #888b92;
      line-height: 2.4em;
      vertical-align: middle; }
  .switch-ios input:checked + label {
    color: #3e4043; }
  /* Holo Theme
 */
  .switch-toggle.switch-holo, .switch-light.switch-holo > span {
    background-color: #464747;
    border-radius: 1px;
    box-shadow: inset rgba(0, 0, 0, 0.1) 0 1px 0;
    color: #fff;
    text-transform: uppercase; }
  .switch-holo label {
    color: #fff; }
  .switch-holo > span span {
    opacity: 0;
    -webkit-transition: all 0.1s;
    -moz-transition: all 0.1s;
    transition: all 0.1s; }
    .switch-holo > span span:first-of-type {
      opacity: 1; }
  .switch-holo > span span, .switch-holo label {
    font-size: 85%;
    line-height: 2.15625em; }
  .switch-holo a {
    background-color: #666;
    border-radius: 1px;
    box-shadow: inset rgba(255, 255, 255, 0.2) 0 1px 0, inset rgba(0, 0, 0, 0.3) 0 -1px 0; }
  /* Selected ON switch-light
*/
  .switch-holo.switch-light input:checked ~ span a {
    background-color: #000000; }
  .switch-holo.switch-light input:checked ~ span span:first-of-type {
    opacity: 0; }
  .switch-holo.switch-light input:checked ~ span span:last-of-type {
    opacity: 1; }
  /* Material Theme
 */
  /* switch-light
 */
  .switch-light.switch-material a {
    top: -0.1875em;
    width: 1.75em;
    height: 1.75em;
    border-radius: 50%;
    background: #fafafa;
    box-shadow: 0 0.125em 0.125em 0 rgba(0, 0, 0, 0.14), 0 0.1875em 0.125em -0.125em rgba(0, 0, 0, 0.2), 0 0.125em 0.25em 0 rgba(0, 0, 0, 0.12);
    -webkit-transition: right .28s cubic-bezier(.4, 0, .2, 1);
    -moz-transition: right .28s cubic-bezier(.4, 0, .2, 1);
    transition: right .28s cubic-bezier(.4, 0, .2, 1); }
  .switch-material.switch-light {
    overflow: visible; }
    .switch-material.switch-light::after {
      clear: both;
      content: "";
      display: table; }
  .switch-material.switch-light > span {
    overflow: visible;
    position: relative;
    top: 0.1875em;
    width: 3.25em;
    height: 1.5em;
    min-height: auto;
    border-radius: 1em;
    background: rgba(0, 0, 0, 0.26); }
  .switch-material.switch-light span span {
    position: absolute;
    clip: rect(0 0 0 0); }
  .switch-material.switch-light input:checked ~ span a {
    right: 0;
    background: #000000;
    box-shadow: 0 0.1875em 0.25em 0 rgba(0, 0, 0, 0.14), 0 0.1875em 0.1875em -0.125em rgba(0, 0, 0, 0.2), 0 0.0625em 0.375em 0 rgba(0, 0, 0, 0.12); }
  .switch-material.switch-light input:checked ~ span {
    background: rgba(63, 81, 181, 0.5); }
  /* switch-toggle
 */
  .switch-toggle.switch-material {
    overflow: visible; }
    .switch-toggle.switch-material::after {
      clear: both;
      content: "";
      display: table; }
  .switch-toggle.switch-material a {
    top: 48%;
    width: 0.375em !important;
    height: 0.375em;
    margin-left: 0.25em;
    background: #3f51b5;
    border-radius: 100%;
    -webkit-transform: translateY(-50%);
    -moz-transform: translateY(-50%);
    -ms-transform: translateY(-50%);
    -o-transform: translateY(-50%);
    transform: translateY(-50%);
    -webkit-transition: -webkit-transform 0.4s ease-in;
    -moz-transition: -moz-transform 0.4s ease-in;
    transition: transform 0.4s ease-in; }
  .switch-toggle.switch-material label {
    color: rgba(0, 0, 0, 0.54);
    font-size: 1em; }
  .switch-toggle.switch-material label:before {
    content: '';
    position: absolute;
    top: 48%;
    left: 0;
    display: block;
    width: 0.875em;
    height: 0.875em;
    border-radius: 100%;
    border: 0.125em solid rgba(0, 0, 0, 0.54);
    -webkit-transform: translateY(-50%);
    -moz-transform: translateY(-50%);
    -ms-transform: translateY(-50%);
    -o-transform: translateY(-50%);
    transform: translateY(-50%); }
  .switch-toggle.switch-material input:checked + label:before {
    border-color: #000000; }
  /* ripple
 */
  .switch-light.switch-material > span:before, .switch-light.switch-material > span:after, .switch-toggle.switch-material label:after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    z-index: 3;
    display: block;
    width: 4em;
    height: 4em;
    border-radius: 100%;
    background: #3f51b5;
    opacity: .4;
    margin-left: -1.25em;
    margin-top: -1.25em;
    -webkit-transform: scale(0);
    -moz-transform: scale(0);
    -ms-transform: scale(0);
    -o-transform: scale(0);
    transform: scale(0);
    -webkit-transition: opacity .4s ease-in;
    -moz-transition: opacity .4s ease-in;
    transition: opacity .4s ease-in; }
  .switch-light.switch-material > span:after {
    left: auto;
    right: 0;
    margin-left: 0;
    margin-right: -1.25em; }
  .switch-toggle.switch-material label:after {
    width: 3.25em;
    height: 3.25em;
    margin-top: -0.75em; }
  @-webkit-keyframes materialRipple {
    0% {
      -webkit-transform: scale(0); }

    20% {
      -webkit-transform: scale(1); }

    100% {
      opacity: 0;
      -webkit-transform: scale(1); } }

  @-moz-keyframes materialRipple {
    0% {
      -moz-transform: scale(0); }

    20% {
      -moz-transform: scale(1); }

    100% {
      opacity: 0;
      -moz-transform: scale(1); } }

  @keyframes materialRipple {
    0% {
      -webkit-transform: scale(0);
      -moz-transform: scale(0);
      -ms-transform: scale(0);
      -o-transform: scale(0);
      transform: scale(0); }

    20% {
      -webkit-transform: scale(1);
      -moz-transform: scale(1);
      -ms-transform: scale(1);
      -o-transform: scale(1);
      transform: scale(1); }

    100% {
      opacity: 0;
      -webkit-transform: scale(1);
      -moz-transform: scale(1);
      -ms-transform: scale(1);
      -o-transform: scale(1);
      transform: scale(1); } }

  .switch-material.switch-light input:not(:checked) ~ span:after, .switch-material.switch-light input:checked ~ span:before, .switch-toggle.switch-material input:checked + label:after {
    -webkit-animation: materialRipple .4s ease-in;
    -moz-animation: materialRipple .4s ease-in;
    animation: materialRipple .4s ease-in; }
  /* trick to prevent the default checked ripple animation from showing
 * when the page loads.
 * the ripples are hidden by default, and shown only when the input is focused.
 */
  .switch-light.switch-material.switch-light input ~ span:before, .switch-light.switch-material.switch-light input ~ span:after, .switch-material.switch-toggle input + label:after {
    visibility: hidden; }
  .switch-light.switch-material.switch-light input:focus:checked ~ span:before, .switch-light.switch-material.switch-light input:focus:not(:checked) ~ span:after, .switch-material.switch-toggle input:focus:checked + label:after {
    visibility: visible; } }

/* Bugfix for older Webkit, including mobile Webkit. Adapted from
 * http://css-tricks.com/webkit-sibling-bug/
 */
@media only screen and (-webkit-max-device-pixel-ratio: 2) and (max-device-width: 80em) {
  .switch-light, .switch-toggle {
    -webkit-animation: webkitSiblingBugfix infinite 1s; } }

@-webkit-keyframes webkitSiblingBugfix {
  from {
    -webkit-transform: translate3d(0, 0, 0); }

  to {
    -webkit-transform: translate3d(0, 0, 0); } }

/*# sourceMappingURL=toggle-switch.css.map */
</style>