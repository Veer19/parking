<template class='background'>
<div class="columns">
  <div class="column">
      
      <div v-if="category==''">
        <div class="question">Who are you?</div>
        <div class="option-button" @click="adminSetup">I own a parking lot</div>
        <div class="option-button" @click="userSetup">I park my car everywhere</div>
      </div>
    <div class="adminSetup" v-if="category=='admin'">
        <div class="question">Where are the parking lots located?</div>
        <div id='map' style='width: 100%; height: 500px;'></div>
        <div class="sumbitButton" @click="parkingLotsSelected">All Selected</div>
    </div>
    <div class="userSetup" v-if="category=='user'">
        <div class="question">Can we know your lisence plate number?</div>
        <input class="plateNumber" v-model="plateNumber" placeholder="Lisence Plate Number" />
        <div class="sumbitButton" @click="submitPlateNumber">Submit</div>
    </div>
  </div>
  
</div>

</template>
<script>
import firebase from 'firebase'
import firebaseApp from '../firebaseConfig'
export default {
  name: 'login',
  data(){
      return {
        uid:"",
        category:"",
        center: { lat: 45.508, lng: -73.587 },
        markers: [],
        places: [],
        currentPlace: null,
        plateNumber:"",
        parkingLotCoordinates: []
      }
  },
  methods:{
    adminSetup(){
        this.category = "admin";
        let self = this;
        mapboxgl.accessToken = 'pk.eyJ1IjoidmVlcjE5IiwiYSI6ImNrMnJqcjZhdTBxbHAzaXBoZHlhZjFwNnYifQ.1w8oqCFBa72f1vy3-v6z2w';
        this.$getLocation({
            enableHighAccuracy: false, //defaults to false
            timeout: Infinity, //defaults to Infinity
            maximumAge: 0 //defaults to 0
        })
        .then(coordinates => {
            console.log(coordinates);
            
            var map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/streets-v11',
                center: [coordinates.lng, coordinates.lat],
                zoom: 15
            });
            map.on('load', function () {
                var marker = new mapboxgl.Marker()
                    .setLngLat([coordinates.lng, coordinates.lat],)
                    .addTo(map);
            });

            map.on('click', function (e) {
                let clickedCoordinates = {
                    lng: e.lngLat.wrap().lng,
                    lat: e.lngLat.wrap().lat
                }
                console.log(clickedCoordinates)
                self.parkingLotCoordinates.push(clickedCoordinates)
                console.log(self.parkingLotCoordinates)
                var marker = new mapboxgl.Marker()
                    .setLngLat([clickedCoordinates.lng, clickedCoordinates.lat])
                    .addTo(map);
            });
        });
    },
    parkingLotsSelected(){
        this.uid = localStorage.getItem('uid')
        console.log(this.parkingLotCoordinates)
        firebaseApp.db.doc("users/"+this.uid).update({
            parkingLots:this.parkingLotCoordinates
        })
        this.parkingLotCoordinates.forEach(x=>{
            firebaseApp.db.collection("parkingLots").add(x)
        })
        let apikey = "AIzaSyB_vaGVTbrkNy4gcXoCRZ0FmbeWaGZE8ZA"
    },
    userSetup(){

    },
    submitPlateNumber(){
        this.uid = localStorage.getItem('uid')
        firebaseApp.db.doc("users/"+this.uid).update({
            plateNumber:this.plateNumber
        }).then(x=>{
            this.$router.push('home')
        })
    }
  },
  mounted(){
  }
}

</script>
<style scoped>
.columns {
  height: 100vh;
  width: 100vw;
  margin: 0;
  background-size: cover;
  background-position: center;
}
</style>
