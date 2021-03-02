<template>

  <v-row class="col-md-6 offsett-md-3" style="margin-top: 30px">
    <v-col>
      <v-card>
        <Email @get-email="emailHandler" />
        <Password @get-password="passwordHandler"/>
        <Name @get-name="nameHandler"/>
      </v-card>
      <v-row style="margin-top:30px;">          
        <v-col class="col-md-10 ">
          <router-link to="/login">
            <v-btn @click="save">Registrieren</v-btn>
            {{ user }}
          </router-link>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import axios from 'axios';
import config from '../../config'

import Email from '../components/forms/email.vue';
import Password from '../components/forms/password.vue';
import Name from '../components/forms/name.vue';





export default {
  name: 'Register',    
  data (){
    return{
      user:{
        password: "",
        email: "",
        name: "",
      },   
    }         
  },
  methods: {
    emailHandler(email){
      this.user.email = email;
    },

    passwordHandler(password){
      //console.log(`passwordHander ${password}`)
      this.user.password = password;
    },

    nameHandler(name){
      this.user.name = name;
    },

    save(){
      this.post_register(this.user);
    },
    
    post_register(user){
      if( !(user.password == "" || user.email == "" || user.name == "")){
        console.log(user)
        axios.post(`${config.protocol}://${config.hostname}/register`, {
          headers: {'Content-Type': 'application/json'},
          user
        })
        .then( response => {
          console.log(response.data);
          
          this.$router.push('/')
          })
          .catch(function (error) {
            if(error.response.status == 406){
              console.log("Password oder Email falsch")
            }else{
              console.log(error)
            }
          });
        }  
    },   
  },
  components:{
    Email,
    Password,
    Name
  }
  
}

</script>
