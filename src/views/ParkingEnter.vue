<template>
  <div class="home">
    Move to Spot Number 
    
    {{spot}}


  </div>
  
</template>

<script>
// @ is an alias to /src
import firebaseApp from '../firebaseConfig'

export default {
  name: 'home',
  data(){
    return {
      spot:0
    }
  },
  methods: {
    
  },
  beforeMount(){
    this.spot = this.$route.params.spot
  }
  
}
</script>
<style>

</style>