<template class='background'>
<div class="columns">
  <div class="column">
    
    <div class="button" @click="login" text="Login">Login</div>
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
</style>
