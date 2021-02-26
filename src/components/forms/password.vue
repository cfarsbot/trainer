<template>
  <div>
    <v-text-field v-model="password" class=col-md-12 label="Password" hide-details="auto" @input="sendPassword"></v-text-field>         
  </div>
</template>

<script>

export default {
    name:"password",
    data(){
      return{
        password: "",    
        }
    },
    methods:{
      sendPassword(){
        this.$emit('get-password', this.password)
        console.log("trigger password ")
      }
    }
}
</script>
