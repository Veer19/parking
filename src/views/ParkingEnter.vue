<template>
  <div class="home">
    Move to Spot Number 
    {{spot}}
    <div class="invoice">
      <h1>Number Plate : {{plateNumber}}</h1>
      <br>
      <br>
      <p>Base Fare : Rs 50</p>
      <div @click="pay">Pay Now</div>
    </div>
    <div class="successIcon" v-if="showSuccessIcon">Sucess</div>
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
      showSuccessIcon:false
    }
  },
  methods: {
    pay(){
      let abc = this
      this.uid = localStorage.getItem('uid')
      let options = {
          "key": "rzp_test_xaUvxh6HGic4yG",
          "amount": 50000, //in paise
          "name": "Parking Fees",
          "prefill": {
              "name": "Veer Singh",
              "email": "veer.vs19@gmail.com",
              "contact": "7704080026"
          },
          "handler": function (response){
              abc.showSuccessIcon = true
          },
          "theme": {
            "color": "#F37254"
          }
      };
      
      //let rzp1 = new Razorpay(options);
      //rzp1.open();
      this.rzp1 = new Razorpay(options);
      this.rzp1.open();
      }
  },
  beforeMount(){
    this.spot = this.$route.params.spot
  }
  
}
</script>
<style>

</style>