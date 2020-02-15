<template class=''>
<div class="columns background">
  <div class="column">
    <h1 class="tagline">Wanna Park?</h1>
    <br><br><br><br><br><br><br><br><br><br><br><br><br>
    <div>
      <div class="modal popup1"> 
        <div class="modal-content" v-if="askPhone"> 
          <h1>Can I know your phone number?</h1>
          <input type="text" class="inp" v-model="phone" placeholder="Enter your Number">
          <div class="fancy-button bg-gradient2" @click="submitPhone()"><span>Submit</span></div> 
        </div> 
      </div>
      <div class="modal popup1"> 
        <div class="modal-content" v-if="askPlate">
          <h1>I'll have to identify your vehicle</h1>
          <input type="text" class="inp" v-model="plateNumber" placeholder="Enter your Car Plate Number">
          <div class="fancy-button bg-gradient2" @click="createUserAccount()"><span>Submit</span></div>
        </div> 
      </div>
      <div class="modal popup1" v-if="askQuestion"> 
        <div class="modal-content"> 
          <div>
            <div class="question" style="font-size: 40px;">Who are you?</div>
            <div class="sumbitButton fancy-button bg-gradient2" @click="submitAnswer('admin')"><span><i class="fa fa-envelope"></i>I own a parking lot</span></div>
            <div class="sumbitButton fancy-button bg-gradient2" @click="submitAnswer('user')"><span><i class="fa fa-envelope"></i>I park my car a lot</span></div>
          </div>
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
      phone:'',
      plateNumber:'',
      askPhone:true,
      askQuestion:false,
      askPlate:false,
      type:""
    }
  },
  methods:{
    submitAnswer(type){
      if(type == "user")
        this.type = type
      else {
        //Creating Admin Account
        localStorage.setItem('phone',this.phone)
        firebaseApp.db.doc("users/"+this.phone).get()
        .then(doc => {
          if(!doc.exists){
            firebaseApp.db.doc("users/"+this.phone).set({
              "phone":this.phone,
              "type":"admin",
            })
          }
          this.$router.push('setup')
        })
      }
      
      this.askPhone = false
      this.askPlate = true
      this.askQuestion = false

    },
    submitPhone(){
      this.askPhone = false
      this.askPlate = false
      this.askQuestion = true
    },
    createUserAccount(){
      localStorage.setItem('phone',this.phone)
      firebaseApp.db.doc("users/"+this.phone).get()
      .then(doc => {
        if(!doc.exists){
          firebaseApp.db.doc("users/"+this.phone).set({
            "phone":this.phone,
            "isParkedAt":"",
            "plate":this.plateNumber,
            "type":this.type
          })
          firebaseApp.db.doc("matchplates/"+this.plateNumber).set({
            "phone":this.phone
          })
          
        }
        this.$router.push('home')
      })
    }
  },
  beforeMount(){
    if(localStorage.getItem('uid') != null){
        this.$router.push('home')
      }
  }
}

</script>
<style scoped>
.tagline {
  font-size: 330%;
    color: white;
    font-family: 'Open sans';
    font-weight: 500;
    margin-top: 150px;
}
@import url('https://fonts.googleapis.com/css?family=Open+Sans&display=swap');
.columns {
  height: 100vh;
  width: 100vw;
  text-align:center;
  justify-content: center;
  margin: 0;
  background-size: cover;
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
</style>