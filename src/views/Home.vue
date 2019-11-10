<template >
  <div class="home">
    <div id="map"></div>
    <div class="submitButton  fancy-button bg-gradient2" @click="initParking">I need to park</div>
       
	<a href="#" class=" sumbitButton fancy-button bg-gradient2"><span><i class="fa fa-envelope"></i>I need to park</span></a>
    {{apiData}}
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
      destinationCoordinates:[]
    }
  },
  methods: {
    initParking(){
      let abc = this
      // console.log(this.parkingLotDistances)
      let parkingLots = this.parkingLotDistances.rows[0].elements
      let minDistance = 1000000000000000000000000;
      let minIndex = 0;
      for(let i=0;i<parkingLots.length;i++){
        if(minDistance>parkingLots[i].distance.value){
          minDistance = parkingLots[i].distance.value
          minIndex = i
        }
      }
      this.parkingDestination = this.destinationCoordinates[minIndex]
      let plateNumber = localStorage.getItem("plateNumber")
      console.log(this.parkingDestination.id)
      firebaseApp.db.doc("parkingLots/"+this.parkingDestination.id).onSnapshot(snapshot=>{
        let data = snapshot.data()
        for(let i=0;i<data.spots.length;i++){
          if(data.spots[i].plateNumber == plateNumber){
            this.$router.push({name:'parkingEnter', params: {spot: i+1 }})
          }
        }
      })
      console.log(this.parkingDestination)
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
            console.log(coordinates)
            console.log(abc.parkingDestination)
            directionsService.route({
              origin: {lat: coordinates.lat, lng: coordinates.lng},  // Haight.
              destination: {lat:abc.parkingDestination.lat, lng:abc.parkingDestination.lng},  // Ocean Beach.
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
    getData(){
      
      // const Http = new XMLHttpRequest();
      // const url='https://sjce-hack.herokuapp.com/dwkahdkjawhdkjawnd';
      // Http.open("GET", url);
      // Http.send();
      // Http.onreadystatechange = () => {
      //   this.apiData = Http.responseText
      // }
    }
  },
  mounted(){
    let abc = this
    let docData = {}
    this.$getLocation({
            enableHighAccuracy: true, //defaults to false
            timeout: Infinity, //defaults to Infinity
            maximumAge: 0 //defaults to 0
    })
    .then(coordinates => {
      let origin = new google.maps.LatLng(coordinates.lat, coordinates.lng);
      abc.destinations = [] 
      firebaseApp.db.collection("parkingLots").onSnapshot(snapshot=>{
        snapshot.forEach(doc=>{
          docData = doc.data()
          console.log(docData)
          abc.destinationCoordinates.push({
            lat:docData.lat, 
            lng:docData.lng,
            id:docData.id
          })
          abc.destinations.push(new google.maps.LatLng(docData.lat, docData.lng))
        })
        let service = new google.maps.DistanceMatrixService();
        console.log(abc.destinations)
        service.getDistanceMatrix({
              origins: [origin],
              destinations: abc.destinations,
              travelMode: 'DRIVING',
          }, (response,status)=>{
            console.log(status)
              console.log(response)
              abc.parkingLotDistances = response
          });
      })
      
    })
  }
  
}
</script>
<style scoped>
/* Mixins */
/* Mixins */
/* bg shortcodes */

.bg-gradient2 span,
.bg-gradient2:before {
  background: linear-gradient(120deg,rgba(143,66,236,0) 0%,#812bea 100%);
    background-color: #b142ec;
}

/* General */
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

#map {
        height: 500px;
      }
</style>