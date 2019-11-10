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
      
    }
  },
  methods: {
    
  },
  mounted(){
    this.spot = this.$route.params.spot
  }
  
}
</script>
<style>

</style>