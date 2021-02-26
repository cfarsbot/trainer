<template>
    <div>
        <h1>play</h1>
        <v-btn @click="getList">Get</v-btn>
    </div>

</template>

<script>
import axios from 'axios'
//import user_store from '../store/user'
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
     methods: {
         getList(){
             //var user = user_store.getters.user
              axios.post('http://127.0.0.1:5000/play_wordlist', {
                        headers: {'Content-Type': 'application/json'},
                        user:{
                            id: 2
                        }

                    })
                        .then( response => {
                           this.content = response.data
                            
                        })
                        .catch(function (error) {
                            console.log(error)
                        });
         }
        
        } 
 }

</script>
