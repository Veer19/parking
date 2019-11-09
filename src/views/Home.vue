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
      parkingLotDistances:{}
    }
  },
  methods: {
    initParking(){
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
      this.parkingDestination = this.parkingLotDistances.destinationAddresses[minIndex]
      console.log(this.parkingDestination)
      




    },
    getData(){
      this.$getLocation({
        enableHighAccuracy: false, //defaults to false
        timeout: Infinity, //defaults to Infinity
        maximumAge: 0 //defaults to 0
      })
      .then(coordinates => {
        console.log(coordinates);
      });
      // const Http = new XMLHttpRequest();
      // const url='https://sjce-hack.herokuapp.com/dwkahdkjawhdkjawnd';
      // Http.open("GET", url);
      // Http.send();
      // Http.onreadystatechange = () => {
      //   this.apiData = Http.responseText
      // }
    },
    login(){

    }
  },
  mounted(){
    var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
  var chicago = new google.maps.LatLng(41.850033, -87.6500523);
  var mapOptions = {
    zoom:7,
    center: chicago
  }
  var map = new google.maps.Map(document.getElementById('map'), mapOptions);
  directionsRenderer.setMap(map);
        
      // directionsService.route({
      //   origin: {lat: 37.77, lng: -122.447},  // Haight.
      //   destination: {lat: 37.768, lng: -122.511},  // Ocean Beach.
      //   // Note that Javascript allows us to access the constant
      //   // using square brackets and a string value as its
      //   // "property."
      //   travelMode: google.maps.TravelMode["DRIVING"]
      // }, function(response, status) {
      //   if (status == 'OK') {
      //     directionsRenderer.setDirections(response);
      //   } else {
      //     window.alert('Directions request failed due to ' + status);
      //   }
      // });















    let abc = this
    let docData = {}
    this.$getLocation({
            enableHighAccuracy: false, //defaults to false
            timeout: Infinity, //defaults to Infinity
            maximumAge: 0 //defaults to 0
    })
    .then(coordinates => {
      let origin = new google.maps.LatLng(coordinates.lat, coordinates.lng);
      let destinations = [] 
      firebaseApp.db.collection("parkingLots").onSnapshot(snapshot=>{
        snapshot.forEach(doc=>{
          docData = doc.data()
          destinations.push(new google.maps.LatLng(docData.lat, docData.lng))
          let service = new google.maps.DistanceMatrixService();
          service.getDistanceMatrix({
              origins: [origin],
              destinations: destinations,
              travelMode: 'DRIVING',
          }, (response,status)=>{
            console.log(response)
              abc.parkingLotDistances = response
          });
        })
      })
      
    })
  }
  
}
</script>
