<template class='background'>
<div class="columns">
    <div class="popup" v-if="showPopup">
        Where do we keep an eye?
        <div class="option-button" @click="pushParkingData('entryexit')">Entry and Exit</div>
        <div class="option-button" @click="pushParkingData('overview')">Over the Parking Lot</div>
    </div>
  <div class="column">
      
      <div v-if="category==''">
        <div class="question">Who are you?</div>
        <div class="option-button" @click="adminSetup">I own a parking lot</div>
        <div class="option-button" @click="userSetup">I park my car everywhere</div>
      </div>
    <div class="adminSetup" v-if="category=='admin'">
        <div class="question">Where are the parking lots located?</div>
        <div id="map"></div>
        <div v-for="(parkingLot,index) in parkingLotCoordinates" v-bind:key="parkingLot">
            {{index+1}} <input v-model="parkingLotCoordinates[index]['numberOfSpots']">
        </div>
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
        parkingLotCoordinates: [],
        uid:''
      }
  },
  methods:{
    adminSetup(){
        this.uid = localStorage.getItem('uid')
        firebaseApp.db.doc("users/"+this.uid).update({
            type:"admin"
        })
        this.category = "admin";
        let self = this;
        mapboxgl.accessToken = 'pk.eyJ1IjoidmVlcjE5IiwiYSI6ImNrMnJqcjZhdTBxbHAzaXBoZHlhZjFwNnYifQ.1w8oqCFBa72f1vy3-v6z2w';
        this.$getLocation({
            enableHighAccuracy: true, //defaults to false
            timeout: Infinity, //defaults to Infinity
            maximumAge: 0 //defaults to 0
        })
        .then(coordinates => {
            console.log(coordinates)
            let yourLocation = {lat:coordinates.lat, lng:coordinates.lng }
            var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
            var map = new google.maps.Map(document.getElementById('map'), {zoom: 18, center:yourLocation });
            var marker = new google.maps.Marker({position: yourLocation, map: map,icon:iconBase+'info-i_maps.png'});
            let c=1
            google.maps.event.addListener(map, 'click', function(event) {
                self.parkingLotCoordinates.push({lat:event.latLng.lat(),lng:event.latLng.lng()})
                console.log(self.parkingLotCoordinates)
                var marker = new google.maps.Marker({
                    position: event.latLng,
                    label : ""+c,
                    map: map,
                    // icon: iconBase + 'parking_lot_maps.png',
                });
                c = c + 1
            });
        });
    },
    parkingLotsSelected(){
        this.showPopup = true;
        // this.pushParkingData()
    },
    pushParkingData(cameraPosition){

        this.uid = localStorage.getItem('uid')
        this.parkingLotCoordinates.forEach(x=>{
            console.log(x)
            x.numberOfSpots = parseInt(x.numberOfSpots)
            x.spotsFilled = 0
            x.cameraPosition = cameraPosition
            x.spots= []
            for(let i=0;i<x.numberOfSpots;i++){
                x.spots.push("")
            }
            firebaseApp.db.collection("parkingLots").add(x)
            .then(snapshot=>{
                console.log(snapshot.id)
                firebaseApp.db.doc("parkingLots/"+snapshot.id).update({
                    id:snapshot.id
                })
            })
        })
        let apikey = "AIzaSyB_vaGVTbrkNy4gcXoCRZ0FmbeWaGZE8ZA"
    },
    userSetup(){
        this.category = "user"
    },
    submitPlateNumber(){
        this.uid = localStorage.getItem('uid')
        firebaseApp.db.doc("users/"+this.uid).update({
            plateNumber:this.plateNumber
        }).then(x=>{
            localStorage.setItem('plateNumber',this.plateNumber)
            this.$router.push('home')
        })
    }
  },
  mounted(){
  }
}

</script>
<style scoped>
 #map {
        height: 400px;  /* The height is 400 pixels */
        width: 100%;  /* The width is the width of the web page */
       }
.columns {
  height: 100vh;
  width: 100vw;
  margin: 0;
  background-size: cover;
  background-position: center;
}
</style>
