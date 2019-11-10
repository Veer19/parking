<template class=''>
<div class="columns background">
  <div class="column">
    
    <div class="button" @click="login" text="Login">Login</div>
    <div class="play-button-container">
<div class="play-button">
<svg>
<polygon points="10 33 10 1 34 17"></polygon>
</svg>
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
  methods:{
    login(){
      var provider = new firebase.auth.GoogleAuthProvider();
      firebaseApp.auth.signInWithPopup(provider)
      .then(snapshot=>{
        let user = snapshot.user
        localStorage.setItem('uid',user.uid)
        localStorage.setItem('name',user.displayName)
        
        return firebaseApp.db.doc("users/"+user.uid).get()
        .then(doc => {
          if(!doc.exists){
            firebaseApp.db.doc("users/"+ user.uid).set({
              name : user.displayName,
              phone: user.phoneNumber,
              uid:user.uid
            })
            this.$router.push('setup')
          }
          else {
              if (doc.data().type == "Admin"){
                  this.$router.push('admin')
              }
              else {
                  this.$router.push('home')
              }
          }
        })
        
      })
      .then(()=>{
          
      })
    }
  }
}

</script>
<style scoped>
.columns {
  height: 100vh;
  width: 100vw;
  margin: 0;
  background-size: cover;
  background-position: center;
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
.play-button-container
 {
    width: 164px;
    height: 164px;
    border-radius: 100px;
    -webkit-border-radius: 100px;
    -moz-border-radius: 100px;
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
.background{
  background-image: url("../assets/logiin.png");
  background-position: right;
}
</style>