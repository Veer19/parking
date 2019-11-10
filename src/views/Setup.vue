<template class='background'>
<div class="columns">
  <div class="modal popup1" v-if="showPopup1"> 
    <div class="modal-content"> 
      <h1>Where do we keep an eye?</h1> 
      <div class="fancy-button bg-gradient2" @click="pushCameraData('entryexit')"><span><i class="fa fa-envelope"></i>Entry and Exit</span></div>
      <div class="fancy-button bg-gradient2" @click="pushCameraData('overview')"><span><i class="fa fa-envelope"></i>Over the Parking Lot</span></div> 
    </div> 
  </div>
  <div class="modal popup1" v-if="showPopup2"> 
    <div class="modal-content"> 
      <h1>How high will the camera be?</h1> 
      <div class="fancy-button bg-gradient2" @click="pushHeightData('high')"><span><i class="fa fa-envelope"></i>High</span></div>
      <div class="fancy-button bg-gradient2" @click="pushHeightData('low')"><span><i class="fa fa-envelope"></i>Low</span></div> 
    </div> 
  </div>
  <div class="modal popup1" v-if="showPopup3"> 
    <div class="modal-content"> 
      <h1>You're all set up!</h1> 
    </div> 
  </div>

  <div class="column">
      
      <div v-if="category==''">
        <div class="question" style="font-size: 40px;">Who are you?</div>
          <div class="sumbitButton fancy-button bg-gradient2" @click="adminSetup"><span><i class="fa fa-envelope"></i>I own a parking lot</span></div>
          <div class="sumbitButton fancy-button bg-gradient2" @click="userSetup"><span><i class="fa fa-envelope"></i>I park my car a lot</span></div>
      </div>
    <div class="adminSetup" v-if="category=='admin'">
        <div class="question">Where are the parking lots located?</div>
        <div id="map"></div>
        <br>
        <br>   
        <div v-for="(parkingLot,index) in parkingLotCoordinates" v-bind:key="parkingLot">
           
           <input type="text" class="inp" v-model="parkingLotCoordinates[index]['numberOfSpots']" id="inp" :placeholder="'Parking Lot '+ (index+1)">
           
           
          
        </div>
        <div class="sumbitButton fancy-button bg-gradient2" @click="parkingLotsSelected"><span><i class="fa fa-envelope"></i>I am all done!</span></div>
    </div>
    <div class="userSetup" v-if="category=='user'">
      <div class=""> 
        <div class="modal-content"> 
          <h1>Can we have your car's plate number?</h1>
           <input type="text plateNumber" class="inp" id="inp" placeholder="Enter Plate Number">
            <div class="sumbitButton fancy-button bg-gradient2" @click="submitPlateNumber"><span><i class="fa fa-envelope"></i>Submit</span></div>
        </div> 
      </div>
        
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
        uid:'',
        showPopup1:false,
        showPopup2:false,
        showPopup3:false,
        cameraPosition:"",
        cameraHeight:""
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
        this.showPopup1 = true;
        
    },
    pushCameraData(cameraPosition){
      this.cameraPosition = cameraPosition
      this.showPopup2 = true;
      this.showPopup1 = false;
    },
    pushHeightData(cameraHeight){
      this.cameraHeight = cameraHeight
      this.showPopup2 = false;
      this.showPopup3 = true
    },
    pushParkingData(cameraPosition){

        this.uid = localStorage.getItem('uid')
        this.parkingLotCoordinates.forEach(x=>{
            console.log(x)
            x.numberOfSpots = parseInt(x.numberOfSpots)
            x.cameraPosition = this.cameraPosition
            x.cameraHeight = this.cameraHeight
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
.popup1{
  position: absolute;
  z-index: 100000;
  height: 400px;
  border-radius: 15px;
  background: white;
  box-shadow: 0 24px 72px 0 rgba(0,0,0,.5);
}
    .modal {
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
    }
    .modal-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        padding: 1rem 1.5rem;
        width: 24rem;
        border-radius: 0.5rem;
    }
    .close-button {
        float: right;
        width: 1.5rem;
        line-height: 1.5rem;
        text-align: center;
        cursor: pointer;
        border-radius: 0.25rem;
        background-color: lightgray;
    }
    .close-button:hover {
        background-color: darkgray;
    }
    .show-modal {
        opacity: 1;
        visibility: visible;
        transform: scale(1.0);
        transition: visibility 0s linear 0s, opacity 0.25s 0s, transform 0.25s;
    }

@media screen and (max-width: 700px){
  .box{
    width: 70%;
  }
  .popup{
    width: 70%;
  }
}
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
@import url('https://fonts.googleapis.com/css?family=Open+Sans&display=swap');
.columns {
  height: 100vh;
  width: 100vw;
  text-align:center;
  justify-content: center;
  margin: 0;
  background-size: cover;
  align-items: center;
  background-position: center;
  display: flex;
}
.column
{    justify-content: center;

}

@media (max-width: 670px){
.play-button-container {
    margin: 0 auto -20%;
}
}
@media (max-width: 960px){
.play-button-container {
    -webkit-transform: scale(.8);
    transform: scale(.8);
}
}
.play-button-container {
    width: 250px;
    height: 250px;
    border-radius: 50%;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    display: -webkit-box;
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    background: -webkit-linear-gradient(330deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.2) 100%);
    background: linear-gradient(120deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.2) 100%);
    box-shadow: 0 24px 72px 0 rgba(0,0,0,.5);
    -webkit-transition: 300ms all cubic-bezier(.4,0,.2,1);
    transition: 300ms all cubic-bezier(.4,0,.2,1);
}
.play-button-container 
.play-button {
    z-index: 2;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: #fff;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,.3);
    display: -webkit-box;
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    -webkit-transition: 300ms all cubic-bezier(.4,0,.2,1);
    transition: 300ms all cubic-bezier(.4,0,.2,1);
}
.background{
  background-image: url("../assets/logiin.png");
  background-position: right;
}
.button{
    font-size: 40px;
   font-family: 'Open Sans', sans-serif;
}
* {
  box-sizing: border-box;
}


.inp {
  -webkit-appearance: none;
    width: 100%;
    border: 0;
    /* border: 1px black solid; */
    border-radius: 50px;
    margin: 10px 0;
    padding: 10px 50px;
    font-family: inherit;
    /* padding: 12px 0; */
    height: 48px;
    font-size: 16px;
    font-weight: 500;
    /* border-bottom: 2px solid #c8ccd4; */
    background: none;
    /* border-radius: 0; */
    color: #223254;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    -webkit-transition: all 0.15s ease;
    transition: all 0.15s ease;
    /* box-shadow: 0.8px 3px 5px black; */
}
.inp input:hover {
  background: rgba(34,50,84,0.03);
}
.inp input:not(:placeholder-shown) + span {
  color: #5a667f;
  transform: translateY(-26px) scale(0.75);
}
.inp input:focus {
  background: none;
  outline: none;
}
.inp input:focus + span {
  color: #07f;
  transform: translateY(-26px) scale(0.75);
}
.inp input:focus + span + .border {
  transform: scaleX(1);
}

</style>
