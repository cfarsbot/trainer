<template>
  <div>

         <v-text-field v-model="password"   
         class="col-md-12"          
            label="Passwort"
            hide-details="auto"
            @input="sendPassword"
            :append-icon="showInput ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showInput = !showInput"
            :type="showInput ? 'text' : 'password'">
            </v-text-field>       
  </div>
</template>

<script>

export default {
    name:"password",
    data(){
      return{
        password: "",
        showInput: false,    
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
