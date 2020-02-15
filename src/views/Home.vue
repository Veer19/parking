<template >
  <div class="home background">
    <div id="map"></div>
    <div class="play-button-container">
      <div class="play-button">
        <div class="button" style="color:black !important;" @click="initParking">Park Now</div>
      </div>
    </div>
    <!-- <div class=" bottom" @click="parked" v-if="showParkedButton"><span><i class="fa fa-envelope"></i>I'm There</span></div> -->
  </div>
</template>


<script>
// @ is an alias to /src
import firebaseApp from '../firebaseConfig'

export default {
  name: 'home',
  data(){
    return {
      apiData:"",
      distanceRequestUrl:"",
      apiKey:"AIzaSyB_vaGVTbrkNy4gcXoCRZ0FmbeWaGZE8ZA",
      parkingLotDistances:{},
      destinations:[],
      destinationCoordinates:[],
      showParkedButton:false,
      parkingMarkers:[]
    }
  },
  methods: {
    parked(){
      this.$router.push({name:'parkingEnter', params: {spot: i+1 }})
    },
    initParking(selectedParking){
      // document.getElementById('map').style.height = 80+"vh"
      // this.showParkedButton = true
      let abc = this
      // let plateNumber = localStorage.getItem("plateNumber")
      // firebaseApp.db.doc("parkingLots/"+this.parkingDestination.id).onSnapshot(snapshot=>{
      //   let data = snapshot.data()
      //   for(let i=0;i<data.spots.length;i++){
      //     if(plateNumber!="" && data.spots[i].plateNumber == plateNumber){
      //       //CHECK IF PARKING LOT IS EMPTY
      //     }
      //   }
      // })
      // console.log(this.parkingDestination)
      if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            let coordinates = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            }
            var directionsService = new google.maps.DirectionsService();
            var directionsRenderer = new google.maps.DirectionsRenderer();
            var myLocation = new google.maps.LatLng(coordinates.lat,coordinates.lng);
            var mapOptions = {
              zoom:25,
              center: myLocation
            }
            var map = new google.maps.Map(document.getElementById('map'), mapOptions);
            directionsRenderer.setMap(map);
            console.log("From ")
            console.log(coordinates)
            console.log("To ")
            console.log(selectedParking)
            directionsService.route({
              origin: {lat: coordinates.lat, lng: coordinates.lng},  // Haight.
              destination: {lat:selectedParking.lat, lng:selectedParking.lng},  // Ocean Beach.
              // Note that Javascript allows us to access the constant
              // using square brackets and a string value as its
              // "property."
              travelMode: ["WALKING"]
            }, function(response, status) {
              if (status == 'OK') {
                directionsRenderer.setDirections(response);
              } else {
                window.alert('Directions request failed due to ' + status);
              }
            });

          }, function() {
            console.log("error")
          });
        } else {
          // Browser doesn't support Geolocation
          console.log("error")
        }

    },
    lookForChangeInUserObject(){
      let phone = localStorage.getItem('phone')
      firebaseApp.db.doc("users/"+phone).onSnapshot(snapshot=>{
        let userData = snapshot.data()
        console.log(userData)
        if(userData.isParkedAt != ""){
          this.$router.push('parkingEnter/'+userData.isParkedAt)
        }
      })
    }
  },
  mounted(){
    this.lookForChangeInUserObject();
    let abc = this
    document.getElementById('map').style.height = 100+"vh"
    let docData = {}
    this.$getLocation({
            enableHighAccuracy: true, //defaults to false
            timeout: Infinity, //defaults to Infinity
            maximumAge: 0 //defaults to 0
    })
    .then(coordinates => {
      let yourLocation = {lat:coordinates.lat, lng:coordinates.lng }
      let origin = new google.maps.LatLng(coordinates.lat, coordinates.lng);

      var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
      var map = new google.maps.Map(document.getElementById('map'), {zoom: 14, center:yourLocation });
      let userPositionMarker = new google.maps.Marker({position: yourLocation, map: map,icon:iconBase+'man.png'});
      
      abc.destinations = [] 
      abc.parkingMarkers = []
      firebaseApp.db.collection("parkingLots").onSnapshot(snapshot=>{
        abc.parkingLots = []
        snapshot.forEach(doc=>{
          docData = doc.data()
          abc.parkingLots.push(doc.data())
          console.log(docData)
          abc.parkingMarkers.push(new google.maps.Marker({position: {lat:docData.lat,lng:docData.lng}, map: map,icon:iconBase+'parking_lot.png'}))

          
          //abc.destinations.push(new google.maps.LatLng(docData.lat, docData.lng))
        })
        let service = new google.maps.DistanceMatrixService();
        abc.parkingMarkers.forEach(marker => {
          google.maps.event.addListener(marker, 'click', function() {
            console.log(marker)
            abc.initParking({"lat":marker.getPosition().lat(),"lng":marker.getPosition().lng()})
          });
        })

        
        

        // var marker = new google.maps.Marker({
        //         position: event.latLng,
        //         label : ""+c,
        //         map: map,
        //         // icon: iconBase + 'parking_lot_maps.png',
        // });

        
          
      })
      
    })
    
  }
  
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css?family=Open+Sans&display=swap');
.bottom{
  position: absolute;
    bottom: 0;
    /* bottom: 50px; */
    height: 20vh;
    background: linear-gradient(120deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.2) 100%);
    width: 100%;
    /* margin: 100px; */
    padding: 50px;
    font-size: 30px;
    box-sizing: border-box;
    color: white;
}
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
      margin-top: 100px;

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
  background-image: url("../assets/parknow.png");
  background-position: right;
  height: 100vh;
    display: flex;
    align-items: center;
}
.button{
    font-size: 40px;
   font-family: 'Open Sans', sans-serif;
}
#map {
  width: 100vw;
        height:0px;
        position: absolute;
        z-index: 1000000000000000;
        top: 0;
        left: 0;
      }
</style>