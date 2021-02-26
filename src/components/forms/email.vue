<template>
  <div>
    <v-text-field v-model="email" class=col-md-12 label="Email" hide-details="auto" @input="sendEmail"></v-text-field>         
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
    sendEmail(){
      this.$emit('get-email', this.email)
        console.log("trigger email")
    }
  }
}
</script>
