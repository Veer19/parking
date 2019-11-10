<template>
  <div class="home">
    <div id="map"></div>
    <div class="sumbitButton" @click="initParking">I need to park</div>
        

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
        abc.destinationCoordinates = []
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
<style>

#map {
        height: 500px;
      }
</style>