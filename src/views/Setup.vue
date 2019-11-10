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
        <div id="map"></div>
        <div v-for="(parkingLot,index) in parkingLotCoordinates" v-bind:key="parkingLot">
            {{index+1}} <input v-model="parkingLotCoordinates[index]['numberOfSpots']">
            {{parkingLotCoordinates[index]}}
        </div>
        <div class="sumbitButton fancy-button bg-gradient2" @click="parkingLotsSelected"><span><i class="fa fa-envelope"></i>All Selected</span></div>
    </div>
    <div class="userSetup" v-if="category=='user'">
        <div class="question">Can we know your lisence plate number?</div>
        <input class="plateNumber" v-model="plateNumber" placeholder="Lisence Plate Number" />
        <div class="sumbitButton fancy-button bg-gradient2" @click="submitPlateNumber"><span><i class="fa fa-envelope"></i>Submit</span></div>
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
        this.uid = localStorage.getItem('uid')
        firebaseApp.db.doc("users/"+this.uid).update({
            parkingLots:this.parkingLotCoordinates
        })
        this.parkingLotCoordinates.forEach(x=>{
            console.log(x)
            x.numberOfSpots = parseInt(x.numberOfSpots)
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

.bg-gradient2 span,
.bg-gradient2:before {
  background: linear-gradient(120deg,rgba(143,66,236,0) 0%,#812bea 100%);
    background-color: #b142ec;
}
a {
  text-decoration: none;
}
a:hover, a:focus, a:active {
  text-decoration: none;
}

/* fancy Button */
.fancy-button {
  display: inline-block;
  margin: 30px;
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-size: 17px;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  color: #ffffff;
  position: relative;
}
.fancy-button:before {
  content: '';
  display: inline-block;
  height: 40px;
  position: absolute;
  bottom: -5px;
  left: 30px;
  right: 30px;
  z-index: -1;
  border-radius: 30em;
  -webkit-filter: blur(20px) brightness(0.95);
          filter: blur(20px) brightness(0.95);
  -webkit-transform-style: preserve-3d;
          transform-style: preserve-3d;
  transition: all 0.3s ease-out;
}
.fancy-button i {
  margin-top: -1px;
  margin-right: 20px;
  font-size: 1.265em;
  vertical-align: middle;
}
.fancy-button span {
  display: inline-block;
  padding: 18px 60px;
  border-radius: 50em;
  position: relative;
  z-index: 2;
  will-change: transform, filter;
  -webkit-transform-style: preserve-3d;
          transform-style: preserve-3d;
  transition: all 0.3s ease-out;
}
.fancy-button:focus, .fancy-button:active {
  color: #ffffff;
}
.fancy-button:hover {
  color: #ffffff;
}
.fancy-button:hover span {
  -webkit-filter: brightness(1.05) contrast(1.05);
          filter: brightness(1.05) contrast(1.05);
  -webkit-transform: scale(0.95);
          transform: scale(0.95);
}
.fancy-button:hover:before {
  bottom: 0;
  -webkit-filter: blur(10px) brightness(0.95);
          filter: blur(10px) brightness(0.95);
}
.fancy-button.pop-onhover:before {
  opacity: 0;
  bottom: 10px;
}
.fancy-button.pop-onhover:hover:before {
  bottom: -7px;
  opacity: 1;
  -webkit-filter: blur(20px);
          filter: blur(20px);
}
.fancy-button.pop-onhover:hover span {
  -webkit-transform: scale(1.04);
          transform: scale(1.04);
}
.fancy-button.pop-onhover:hover:active span {
  -webkit-filter: brightness(1) contrast(1);
          filter: brightness(1) contrast(1);
  -webkit-transform: scale(1);
          transform: scale(1);
  transition: all 0.15s ease-out;
}
.fancy-button.pop-onhover:hover:active:before {
  bottom: 0;
  -webkit-filter: blur(10px) brightness(0.95);
          filter: blur(10px) brightness(0.95);
  transition: all 0.2s ease-out;
}
</style>
