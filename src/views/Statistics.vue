<template>
  <div>
      <Navigation />

      <v-container fluid>
        <v-row>
          <v-col md=4>
            <v-card>
              <v-card-title>
              {{user.name}}
              </v-card-title>
                Total korrekte Antworten {{user.Count_Correct}} <br>
                Total falsche Antworten {{user.Count_Correct}}
          
            </v-card>

                    </v-col>
                </v-row>
            </v-container>
    <div v-for="stat in stats_list" :key="stat.list_id">
      <v-container fluid>
        <v-row>
          <v-col md=4>
            <v-card>
              <v-card-title>
                {{ stat.list_name}}
              </v-card-title>
                
              Korrekte Vokabeln beim letzten versuch
              <p>{{stat.count_correct}}</p>
              Falsche Vokabeln beim letzten versuch
              <p>{{stat.count_false}}</p>
            </v-card>

                    </v-col>
                </v-row>
            </v-container>
          




        </div>

      <v-btn @click="getStats">GET</v-btn>
  </div>
</template>

<script>
import axios from 'axios'
import config from '../../config'

import user_store from '../store/user'
import Navigation from '../components/navigation'

export default {
name: 'Statistics',
  data(){
    return{
        count_correct: "",
        count_false: "",
        stats_list: [],
        user: ""
    }
},
mounted(){
    this.buildStats()
},
methods: {
    buildStats(){
      this.getStats()
      this.user = user_store.getters.user
        

    },
    getStats(){
        var user = user_store.getters.user
        
            axios.post(`${config.protocol}://${config.hostname}/stats`, {
            headers: {'Content-Type': 'application/json'},
            user,
            })
            .then( response => {
                console.log(response.data)
                this.stats_list = response.data
            })
            .catch(function (error) {
              console.log(error)
            });

            console.log(user)
            axios.post(`${config.protocol}://${config.hostname}/get_user`, {
            headers: {'Content-Type': 'application/json'},
            user,
            })
            .then( response => {
                console.log(response.data)
                user_store.commit('saveUser', response.data)
            })
            .catch(function (error) {
              console.log(error)
            });
    }
},
components:{
    Navigation
}
}
</script>

<style>

</style>