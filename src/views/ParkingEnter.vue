<template>
  <div class="home">
    <br><br>
    <h1>{{parkingLotData.name}}</h1>
    <br><br>
    <h3>Follow the Green Light</h3>
    <div class="play-button-container">
      <div class="play-button">
        4 Spots Left
      </div>
    </div>
    <div class=""> 
      <br>
      <br>
      <br><br><br><br><br><br><br>
      <div class="modal-content">
          <h1 v-if="plateNumber!=''">Number Plate : {{plateNumber}}</h1>
      </div> 
    </div>
    <div class="">
      <div class="button" @click="openclose">
        <h4>Lock/Unlock VIP Spot</h4>
      </div>
    </div>
  </div>
  
</template>

<script>
// @ is an alias to /src
import firebaseApp from '../firebaseConfig'

export default {
  name: 'home',
  data(){
    return {
      spot:0,
      plateNumber:"",
      showSuccessIcon:false,
      parkingLotData:{}
    }
  },
  methods:{
    openclose(){
      firebaseApp.db.doc('vip/parkingspace').get().then(snap=>{
        firebaseApp.db.doc('vip/parkingspace').set({
          'unlocked': !snap.data().unlocked
        })
      })
    },
    lookForChangeInPaymentObject(){
      let phone = localStorage.getItem('phone')
      firebaseApp.db.doc("payments/"+phone).onSnapshot(snapshot=>{
        if(snapshot.exists){
          localStorage.setItem('amount',snapshot.data().cost)
          this.$router.push('parkingExit')
        }
      })
    }
  },
  beforeMount(){
    this.lookForChangeInPaymentObject()
    let self = this
    this.parkingLot = this.$route.params.parkingLot
    console.log(this.parkingLot)
    firebaseApp.db.collection('parkingLots').where('name','==',this.parkingLot).get()
    .then(snapshot=>{
      snapshot.forEach(function(doc) {
        self.parkingLotData = doc.data()      
      });
      console.log(this.parkingLotData)
    })
  }
  
}
</script>
<style>
.button{
  padding: 10px 50px;
  border-radius: 10px;
  color: white;
  background: #28282a;
  margin: 50px;
  font-size: 140%;
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
    background: green;
    color:white;
    font-size: 200%;
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

.bg-gradient2 span,
.bg-gradient2:before {
    background: linear-gradient(120deg,rgba(143,66,236,0) 0%,#812bea 100%);
    background-color: #b142ec;
}
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