<template>
  <div>
    

    <div v-if="lang === 0">
      <div v-for="word in words" :key="word.id">
        <v-container>
          <v-row>
            <v-col md=1>
            
             {{ word.de }}       
            </v-col>
            <v-col md=4>
           
              <v-text-field
              value=""
              label="Englisch"
              outlined
              v-model="word.en"
              ></v-text-field>
            </v-col>


          <div v-if="showResults">
            <v-col md="2" v-if="word.result">
              Richtig!
            </v-col>
            <v-col md="2" v-else-if="!word.result">
              Falsch!
            </v-col>
          </div>

          </v-row>
        </v-container>
      </div>
    </div>
    <div v-else>
      <div v-for="word in words" :key="word.id">
        <v-container>
          <v-row>
            <v-col md=1>
            
             {{ word.en }}       
            </v-col>
            <v-col md=4>
           
              <v-text-field
              value=""
              label="Deutsch"
              outlined
              v-model="word.de"
              ></v-text-field>
            
            <div v-if="showResults">
              <v-col md="2" v-if="word.result">
                Richtig!
              </v-col>
              <v-col md="2" v-else-if="!word.result">
                Falsch!
              </v-col>
            </div>
          
            </v-col>
          </v-row>

        </v-container>
      </div>
    </div>
    <v-row>
      <v-col offset-md="1" md="1">
        <v-btn @click="save" color="green" dark>Fertig</v-btn>
      </v-col>
    </v-row>
    
  </div>
  
  
  
</template>

<script>
import axios from 'axios'
import config from '../../config'

import user_store from '../store/user'

export default {
  props: ['words', 'list_id', 'lang', 'showResults' ],
  name: 'Play-Words',

  methods:{
    save(){
      this.validate(this.lang)
    },
    validate(lang){
      var words = this.words
      var route = ""
      if(lang === 0){
        route = "validate_en"
      }
      if(lang === 1){
        route = "validate_de"
      }
      
      var user = user_store.getters.user
      var list_id = this.list_id
      axios.post(`${config.protocol}://${config.hostname}/${route}`, {// validate german solutions
        headers: {'Content-Type': 'application/json'},
          user, 
          words,
          list_id

          
        })
        .then( response => {
          
          console.log(response.data)
          this.words = [...response.data]
          this.showResults = true
        })
        .catch(function (error) {
          console.log(error)
        });

    }
  }
  }

</script>

<style>

</style>