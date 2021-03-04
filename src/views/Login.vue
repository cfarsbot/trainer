<template>

    <v-row class="col-md-6 offsett-md-3" style="margin-top: 30px">
        <v-col>
            <v-card>
                <Email @get-email="emailHandler" />
                <Password @get-password="passwordHandler"/>
        
            </v-card>
            <v-row style="margin-top:30px;">
                <v-col class="col-md-2">
                    <v-btn @click="save" color="primary" >Login</v-btn>
                </v-col>
                <v-col class="col-md-10 ">
                    <router-link to="/register">
                        <v-btn>Registrieren</v-btn>
                    </router-link>
                  <v-list-item href="https://netcup.de" target="_blank">Netcup Reflink</v-list-item>


                </v-col>


            </v-row>
        </v-col>
    </v-row>
</template>

<script>
import axios from 'axios';

import Email from '../components/forms/email.vue';
import Password from '../components/forms/password.vue';
import user_store from '../store/user'
import config from '../../config';

 export default {
  name: 'Login',
      
  data (){ 
    return{
      user:{
        password: "",
        email: "",
        },   
    }
  },
  components:{
    Email,
    Password
  },
  methods: {

    emailHandler(email){
      this.user.email = email;
    },

    passwordHandler(password){
      //console.log(`passwordHander ${password}`)
      this.user.password = password;
    },

    save(){
      this.post_login(this.user);
    },
    post_login: function(user){
    
      if( !(user.password == "" || user.email == "")){
        axios.post(`${config.protocol}://${config.hostname}/login`, {
          headers: {'Content-Type': 'application/json'},
            user
          })
          .then( response => {
            console.log(response.data);
            user_store.commit('saveUser', response.data)
            
            if(response.data.email != ""){
              this.$router.push('/')
            }else{
              console.log("Email oder Passwort ist falsch!")
            }
          })
          .catch(function (error) {
            if(error.response.status == 403){
              console.log("Password oder Email falsch")
            }else{
              console.log(error)
            }
          });
        }  
      },
  }
}
</script>
