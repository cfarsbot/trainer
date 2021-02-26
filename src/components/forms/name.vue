<template>
  <div>
    <v-text-field v-model="email" class=col-md-12 label="Name" hide-details="auto" @input="sendName"></v-text-field>
  </div>
</template>

<script>

export default {
  name:"email",
    data(){
      return{
        email: "",      
      }
    },
    methods: {
      sendName(){
        this.$emit('get-name', this.email)
        console.log("trigger email")
      }
    }
}
</script>
