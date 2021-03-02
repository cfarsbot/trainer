<template>
    <div>
      <Navigation />
    <v-container fluid>
      <v-row no-gutters>
        <v-col md="2">
          Welche Sprache willst du dich Testen?
        
        
            <!-- Wordlists -->
            <Menu class="mt-4" :entrys="supported_lang" @selected-item="SelectionLangHandler"/>
            <List class="mt-4" :entrys="content" @selected-item="SelectionListHandler"/>
             
            
          <v-btn
          class="mt-4"
          @click="submit"
          color="primary"
          dark
          >Start</v-btn>
        </v-col>
        <v-col md="10">
          <Play :words="play_list" :list_id="list_id" :lang="selected_lang" :showResults="showResults"/>
        </v-col>
      </v-row>
    </v-container>
    </div>

</template>

<script>
import axios from 'axios'
import config from '../../config'
import user_store from '../store/user'

import Navigation from '../components/navigation'
import Menu from '../components/basic_menu'

import List from '../components/basic_list'
import Play from '../components/play_words'
//import user_store from '../store/user'
 export default {
  name: 'Login',
      
  data (){
    return{
      content: [],
      play_list: [],
      play_lang: "",
      list_name: "",
      list_id: "",
      supported_lang: ['Deutsch', 'Englisch'],
      selected_lang: "",
      showResults: false
      }
  },

  methods: {

    submit(){
      if(this.list_id != "" || this.selected_lang != ""){
        this.getPlaylist(this.list_id, this.selected_lang)
       
      }

      
    },
    SelectionLangHandler(selection){
      this.selected_lang = selection
      this.submit()
    },
    SelectionListHandler(selection){
      
      console.log(selection)
        this.list_name = this.content[selection].list_name
        this.list_id = this.content[selection].list_id
    },
    getList(){
      var user = user_store.getters.user
        axios.post(`${config.protocol}://${config.hostname}/wordlist`, {
          headers: {'Content-Type': 'application/json'},
            user
        })
        .then( response => {
          this.content = response.data
        })
        .catch(function (error) {
          console.log(error)
        });
    },
    getPlaylist(list_id, selected_lang){
      axios.post(`${config.protocol}://${config.hostname}/play_wordlist`, {
        headers: {'Content-Type': 'application/json'},
          user:{
            id: 7
          },
          data:{
            list_id,
            selected_lang
          }

          
        })
        .then( response => {
          console.log(response.data)
          this.play_list = response.data
        })
        .catch(function (error) {
          console.log(error)
        });
    }
        
  },
  mounted(){
    this.getList()
  },
  components:{
    List,
    Play,
    Navigation,
    Menu
  } 
 }

</script>
