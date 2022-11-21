<!-- Main Visualization View -->

<template>
<body>
    <b-container fluid class="bv-example-row">
      <b-row>
        <b-col cols="3">
          <div style="margin-right: -20px; margin-left: -10px">
          <mdb-card>
            <mdb-card-header color="dark-color" tag="h5" class="text-center">Data Sets and Sampling Techniques</mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-left" style="font-size: 18.5px; min-height: 302px">
                <DataSetSlider/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
          </div>
          <div style="margin-top: 10px; margin-right: -20px; margin-left: -10px">
          <mdb-card>
            <mdb-card-header color="dark-color" tag="h5" class="text-center">
            Data Details
            </mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-left" style="font-size: 18.5px; min-height: 600px">
                <Heatmap/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
          </div>
          <div style="margin-top: 10px; margin-right: -20px; margin-left: -10px">
          <mdb-card>
            <mdb-card-header color="dark-color" tag="h5" class="text-center">Sampling Execution Tracker</mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-left" style="font-size: 18.5px; min-height: 299px; max-height: 295px">
                <History/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
          </div>
        </b-col>
        <b-col cols="6">
          <mdb-card>
            <mdb-card-header color="dark-color" tag="h5" class="text-center">
              <small class="float-left" style ="margin-top: 4px">
              Global: [Sel: {{InstancesSel}} / All: {{InstancesAll}}]
              </small>
              Data Overview
              <small class="float-right" style ="margin-top: 4px">
              Suggestion: [Sel: {{InstancesSelSug}} / All: {{InstancesAllSug}}]
              </small>
              </mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-left" style="font-size: 18.5px; min-height: 255px">
                <Overview/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card> 
          <mdb-card style="margin-top: 10px;">
            <mdb-card-header color="dark-color" tag="h5" class="text-center">
              <small class="float-left">
                <button btn-dark style="visibility: visible"
                id="Remove"
                v-on:click="Remove">
                <font-awesome-icon icon="vial" />
                {{ underSamp }}
                </button>
              </small>
              Data Space
              <small class="float-right">
                <button
                id="Add" btn-dark style="visibility: visible"
                v-on:click="Add">
                <font-awesome-icon icon="vials" />
                {{ overSamp }}
                </button>
              </small>
              </mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-left" style="font-size: 18.5px; min-height: 1025px">
                <Space/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card> 
        </b-col>
        <b-col cols="3">
          <div style="margin-right: -10px; margin-left: -20px">
          <mdb-card>
            <mdb-card-header color="dark-color" tag="h5" class="text-center">Data Types Distribution</mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-left" style="font-size: 18.5px; min-height: 302px">
                <Types/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
          </div>
          <div style="margin-top: 10px; margin-right: -10px; margin-left: -20px">
          <mdb-card>
            <mdb-card-header  style=" z-index: 1" color="dark-color" tag="h5" class="text-center">
            <small class="float-left" style ="margin-top: 4px">
              Initial: [{{InitialValueBATrain}}%,{{InitialValueFMTrain}}%]
            </small>
              Predicted Probabilities
            <small class="float-right" style ="margin-top: 4px">
              Current: [{{CurrentValueBATrain}}%,{{CurrentValueFMTrain}}%]
            </small>
            </mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-left" style="font-size: 18.5px; min-height: 600px">
                <Predictions/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
          </div>
          <div style="margin-top: 10px; margin-right: -10px; margin-left: -20px">
          <mdb-card>
            <mdb-card-header color="dark-color" tag="h5" class="text-center" style="background-color: #C0C0C0;"><font-awesome-icon icon="star" style="margin-right: 5px"/>
              <small class="float-left" style ="margin-top: 4px">
              Initial: [{{InitialValueBA}}%,{{InitialValueFM}}%]
              </small>
            Test Set Confusion
            <small class="float-right" style ="margin-top: 4px">
              Current: [{{CurrentValueBA}}%,{{CurrentValueFM}}%]
            </small>
            </mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-left" style="font-size: 18.5px; min-height: 299px; max-height: 299px">
                <Confusion/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <div class="w3-container">
    <div id="myModal" class="w3-modal" style="position: fixed;">
      <div class="w3-modal-content w3-card-4 w3-animate-zoom">
        <header class="w3-container w3-light-grey"> 
        <h3 style="display:inline-block; font-size: 22px; margin-top: 15px; margin-bottom:15px; fill: black">Data Types Projections (SDC, Number of Neighbors, Minimum Distance)</h3>
        </header>
        <Export/>
        <div class="w3-container w3-light-grey w3-padding">
        <button style="float: right; margin-top: -3px; margin-bottom: -3px"
          id="closeModal" class="w3-button w3-right w3-white w3-border" 
          v-on:click="closeModalFun">
          <font-awesome-icon icon="window-close" />
          {{ valuePickled }}
          </button>
        </div>
        </div>
      </div>
    </div>
  </body>
</template>

<script>

import Vue from 'vue'
import DataSetSlider from './DataSetSlider.vue'
import Predictions from './Predictions.vue'
import Export from './Export.vue'
import Space from './Space.vue'
import Types from './Types.vue'
import History from './History.vue'
import Heatmap from './Heatmap.vue'
import Overview from './Overview.vue'
import Confusion from './Confusion.vue'
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import { mdbCard, mdbCardBody, mdbCardText, mdbCardHeader } from 'mdbvue'
import { EventBus } from '../main.js'
import $ from 'jquery'; // <-to import jquery
import 'bootstrap';
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default Vue.extend({
  name: 'Main',
  components: {
    DataSetSlider,
    Predictions,
    Export,
    Space,
    Types,
    History,
    Heatmap,
    Overview,
    Confusion,
    mdbCard,
    mdbCardBody,
    mdbCardHeader,
    mdbCardText
  },
  data () {
    return {
      valuePickled: 'Close',
      overSamp: 'Execute Oversample',
      underSamp: 'Execute Undersample',
      RetrieveValueFile: 'VehicleC', // this is for the default data set
      //RetrieveValueFile: 'VehicleC',
      InitialValueBA: 0,
      InitialValueFM: 0,
      CurrentValueBA: 0,
      CurrentValueFM: 0,
      InitialValueBATrain: 0,
      InitialValueFMTrain: 0,
      CurrentValueBATrain: 0,
      CurrentValueFMTrain: 0,
      reset: false,
      ModelSpaceUMAPSend: 0,
      PerformancePerModel: 0,
      XData: 0,
      XDataNorm: 0, 
      yData: 0,
      ClassifierIDsSamplingOv: [],
      ClassifierIDsSamplingUn: [],
      superVariable: [],
      InstancesAll: 0,
      InstancesSel: 0,
      InstancesAllSug: 0,
      InstancesSelSug: 0
    }
  },
  methods: {
    openModalFun () {
      $('#myModal').modal('show')
    },
    closeModalFun () {
      $('#myModal').modal('hide')
    },
    updateValuesFun () {
      const path = `http://127.0.0.1:5000/data/updateValues`
      const postData = {
        neigh: this.superVariable[0],
        underKey: this.superVariable[1],
        kOSS_NCR: this.superVariable[2],
        sOSS_SSNCR: this.superVariable[3],
        NS: this.superVariable[4],
        TS: this.superVariable[5],
        overKey: this.superVariable[6],
        kSMOTE_ADASYN: this.superVariable[7],
        sSMOTE_ADASYN: this.superVariable[8],
        typesData: this.superVariable[9],
        minDist: this.superVariable[10],
        typesDataUnder: this.superVariable[11],
      }

      const axiosConfig = {
      headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
      'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
      }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('Updated Backend!')
        this.getModelsPerformanceFromBackend()
      })
      .catch(error => {
      console.log(error)
      })
    },
    Remove () {
      EventBus.$emit('SendSelectedPointsUpdateIndicatorUnder')
    },
    Add () {
      EventBus.$emit('SendSelectedPointsUpdateIndicatorOver')
    },
    getCollectionFromBackend () {
      const path = `http://localhost:5000/data/ClientRequest`

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.Collection = response.data.Collection
          EventBus.$emit('emittedEventCallingDataPlot', this.Collection)
          console.log('Collection was overwritten with new data sent by the server!')
        })
        .catch(error => {
          console.log(error)
        })
    },
    getDatafromtheBackEnd () {
      const path = `http://localhost:5000/data/PlotClassifiers`
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.OverviewResults = response.data.OverviewResults
          console.log('Server successfully sent all the data related to visualizations!')
          EventBus.$emit('emittedEventCallingScatterPlot', this.OverviewResults)
          EventBus.$emit('emittedEventCallingGrid', this.OverviewResults)
          EventBus.$emit('emittedEventCallingGridSelection', this.OverviewResults)
          //this.getFinalResults()
        })
        .catch(error => {
          console.log(error)
        })
    },
    SendToServerData () {
      const path = `http://127.0.0.1:5000/data/SendtoSeverDataSet`

      const postData = {
        uploadedData: this.localFile
      }
      const axiosConfig = {
      headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
      'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
      }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('Sent the new uploaded data to the server!')
      })
      .catch(error => {
      console.log(error)
      })
    },
    getFinalResultsFromBackend () {
      const path = `http://localhost:5000/data/SendFinalResultsBacktoVisualize`

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.FinalResults = response.data.FinalResults
          EventBus.$emit('emittedEventCallingLinePlot', this.FinalResults)
        })
        .catch(error => {
          console.log(error)
        })
    },
    fileNameSend () {
      const path = `http://127.0.0.1:5000/data/ServerRequest`
      const postData = {
        fileName: this.RetrieveValueFile,
      }
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('File name was sent successfully!')
        this.getModelsPerformanceFromBackend()
      })
      .catch(error => {
        console.log(error)
      })
    },
    getModelsPerformanceFromBackend () {
      const path = `http://localhost:5000/data/PerformanceForEachModel`

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.PerformancePerModel = response.data.PerformancePerModel
          EventBus.$emit('limitPointsClear', [])
          EventBus.$emit('clearSelections', ['Outlier','Rare','Borderline','Safe'])
          EventBus.$emit('emittedEventCallingPerformanceProbPred', this.PerformancePerModel)
          EventBus.$emit('emittedEventCallingPerformanceProb', this.PerformancePerModel)
          console.log('Server successfully sent all computed information!')
        })
        .catch(error => {
          console.log(error)
        })
    },
    OverSampling () {
      if (this.ClassifierIDsSamplingOv.length == parseInt(this.InstancesAllSug)) {
        EventBus.$emit('firstTimeConfusion', 3)
      }
      var newIDsOver = []
      var start = this.InstancesAll - this.InstancesAllSug
      for (var i = 0; i < this.ClassifierIDsSamplingOv.length; i++) {
        newIDsOver.push(start)
        start = start + 1
      }
      const path = `http://127.0.0.1:5000/data/OverS`
      const postData = {
        actionUnder: [],
        neigh: this.superVariable[0],
        underKey: this.superVariable[1],
        kOSS_NCR: this.superVariable[2],
        sOSS_SSNCR: this.superVariable[3],
        NS: this.superVariable[4],
        TS: this.superVariable[5],
        actionOver: this.ClassifierIDsSamplingOv,
        overKey: this.superVariable[6],
        kSMOTE_ADASYN: this.superVariable[7],
        sSMOTE_ADASYN: this.superVariable[8],
        typesData: this.superVariable[9],
        minDist: this.superVariable[10],
        typesDataUnder: this.superVariable[11],
      }
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('Data for oversampling sent successfully!')
        EventBus.$emit('SendSelectedPointsUpdateIndicatorUn', [])
        EventBus.$emit('SendSelectedPointsUpdateIndicatorOv', newIDsOver)
        this.getModelsPerformanceFromBackend()
      })
      .catch(error => {
        console.log(error)
      })
    },
    UnderSampling () {
      EventBus.$emit('Continue', false)
      if (this.ClassifierIDsSamplingUn.length == parseInt(this.InstancesAllSug)) {
        EventBus.$emit('firstTimeConfusion', 3)
      }
      //EventBus.$emit('UpdateSankey', this.ClassifierIDsSampling)
      const path = `http://127.0.0.1:5000/data/UnderS`
      const postData = {
        actionUnder: this.ClassifierIDsSamplingUn,
        neigh: this.superVariable[0],
        underKey: this.superVariable[1],
        kOSS_NCR: this.superVariable[2],
        sOSS_SSNCR: this.superVariable[3],
        NS: this.superVariable[4],
        TS: this.superVariable[5],
        actionOver: [],
        overKey: this.superVariable[6],
        kSMOTE_ADASYN: this.superVariable[7],
        sSMOTE_ADASYN: this.superVariable[8],
        typesData: this.superVariable[9],
        minDist: this.superVariable[10],
        typesDataUnder: this.superVariable[11],
      }
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('Data for undersampling sent successfully!')
        EventBus.$emit('SendSelectedPointsUpdateIndicatorOv', [])
        this.getModelsPerformanceFromBackend()
      })
      .catch(error => {
        console.log(error)
      })
    },
    Reset () {
      const path = `http://127.0.0.1:5000/data/Reset`
      this.reset = true
      const postData = {
        ClassifiersList: this.reset
      }
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.post(path, postData, axiosConfig)
        .then(response => {
          console.log('The server side was reset! Done.')
          this.reset = false
          EventBus.$emit('resetViews')
          this.fileNameSend()
        })
        .catch(error => {
          console.log(error)
        })
    },
  },
  created () {

    // does the browser support the Navigation Timing API?
    if (window.performance) {
        console.info("window.performance is supported");
    }
    // do something based on the navigation type...
    if(performance.navigation.type === 1) {
        console.info("TYPE_RELOAD");
        this.Reset();
    }
  },
  mounted() {

    var modal = document.getElementById('myModal')
    window.onclick = function(event) {
      //alert(event.target)
        if (event.target == modal) {
            modal.style.display = "none";
        } 
    }

    loadProgressBar()
    window.onbeforeunload = function(e) {
      return 'Dialog text here.'
    }
    $(window).on("unload", function(e) {
      alert('Handler for .unload() called.');
    })

    //Prevent double click to search for a word. 
    document.addEventListener('mousedown', function (event) {
      if (event.detail > 1) {
      event.preventDefault();
      }
    }, false);

    EventBus.$on('OpenModal', this.openModalFun)

    EventBus.$on('SendSelectedPointsUpdateIndicatorOv', data => { this.ClassifierIDsSamplingOv = data})
    EventBus.$on('SendSelectedPointsUpdateIndicatorUn', data => { this.ClassifierIDsSamplingUn = data})
    EventBus.$on('SendSelectedPointsUpdateIndicatorOver', this.OverSampling)
    EventBus.$on('SendSelectedPointsUpdateIndicatorUnder', this.UnderSampling)
    
    EventBus.$on('updateNeighborsGlobal', data => { this.superVariable = data })
    EventBus.$on('updateNeighborsGlobal', this.updateValuesFun)

    EventBus.$on('updateBA', data => { this.InitialValueBA = data })
    EventBus.$on('updateFM', data => { this.InitialValueFM = data })

    EventBus.$on('updateBACur', data => { this.CurrentValueBA = data })
    EventBus.$on('updateFMCur', data => { this.CurrentValueFM = data })

    EventBus.$on('updateBATrain', data => { this.InitialValueBATrain = data })
    EventBus.$on('updateFMTrain', data => { this.InitialValueFMTrain = data })

    EventBus.$on('updateBACurTrain', data => { this.CurrentValueBATrain = data })
    EventBus.$on('updateFMCurTrain', data => { this.CurrentValueFMTrain = data })

    EventBus.$on('updateSelGlobal', data => { this.InstancesSel = data })
    EventBus.$on('updateAllGlobal', data => { this.InstancesAll = data })
    EventBus.$on('updateSelSuggestion', data => { this.InstancesSelSug = data })
    EventBus.$on('updateAllSuggestion', data => { this.InstancesAllSug = data })
  },
})
</script>

<style lang="scss">

#nprogress .bar {
background: red !important;
}

#nprogress .peg {
box-shadow: 0 0 10px red, 0 0 5px red !important;
}

#nprogress .spinner-icon {
border-top-color: red !important;
border-left-color: red !important;
}

body {
  font-family: 'Helvetica', 'Arial', sans-serif !important;
  left: 0px;
  right: 0px;
  top: 0px;
  bottom: 0px;
  margin-top: -10px !important;
  //overflow: hidden !important; // remove scrolling
}

.modal-backdrop {
  z-index: -1 !important;
}

.card-body {
   padding: 0.60rem !important;
}

hr {
  margin-top: 1rem;
  margin-bottom: 1rem;
  border: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

@import './../assets/w3.css';
</style>