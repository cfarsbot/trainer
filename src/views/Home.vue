<!--  Childs: Navigation  /components/navigation.vue
              Table       /components/basic_list.vue
              List        /components/curd_table.vue
               
      Displays all Wordlists of the (logged in) user
      Create new Wordlists, edit existing ones
      -->

<template>
  <div>
    <Navigation />
    <v-container fluid>
      <v-row no-gutters>
        <v-col md="2">
          <!--
            Show all (word)lists
            entrys:"all lists to be shown"
               -->
          <List class="mt-4" :entrys="content" @selected-item="SelectionHandler"/>
          <v-btn color="primary" class="mt-2" @click="newListDialoge">Liste erstellen</v-btn>
        </v-col>
        <v-col md="10">
          <!-- 
            description: Show all words of selected list

            scope=:       refers to @selected-item (List component)
                          holds index value of the list that the user selects
            
            words=:       holds the words to be diplayed in an arraylist

            list_id=:     id of selected list
            list_name:    name of selected list

            @delete-list: called, when button "Delete list" clicked
            
            @update:      called, when user creates new word

            class:        margin left: 3, margin top: 4 (vuetify values, not px)
             -->

          <Table v-if="show_table"
          :scope="selectedItem" 
          :words="words" 
          :list_id="list_id" 
          :list_name="list_name" 
          @delete-list="deleteListHandler"
          @update="init"
          class="ml-3 mt-4"/>
          <div v-else>
            Keine Wörterliste gefunden, erstelle doch eine!
          </div>
          </v-col>
      </v-row>

       <v-dialog v-model="dialogCreateList" max-width="500px">
            <v-card>
              <v-card-title class="headline">Wie soll die neue Liste heißen?</v-card-title>

           <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="12"
                      md="12"
                    >
                      <v-text-field
                        v-model="newListName"
                        label="Name"
                      ></v-text-field>
                    </v-col>
            
                  </v-row>
                </v-container>
              </v-card-text>


              
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="newList">Speichern</v-btn>
                <v-btn color="blue darken-1" text @click="closeDialoge">Abbrechen</v-btn>                
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
  
    </v-container>
    
    
    
  

  </div>
</template>

<script>
import axios from 'axios'

import Navigation from '../components/navigation.vue'
import List from '../components/basic_list.vue'
import Table from '../components/curd_table.vue'

import user_store from '../store/user'

export default {
  name: 'Home',

  data(){
        return{
            selectedItem: "",
            content:[],
            words: [],
            list_id: "",
            list_name: "",
            show_table: false,
            dialogCreateList: false,
            newListName: ""
        }
    },

    components: {
      List,
      Table,
      Navigation
    }, 
    mounted(){
      // get content
      this.getList()
    },
  
    methods: {
      init(data){
        this.content = data
        if (typeof (data[0]).list_name != undefined){
          console.log("there is data")
          console.log(data)
          this.show_table = true
          this.words = this.content[0].array
          this.list_name = this.content[0].list_name
          this.list_id = this.content[0].list_id
          
        }
    
      },

      newListDialoge(){
        this.dialogCreateList = true  
      },

      closeDialoge(){
        this.dialogCreateList = false
      },

      newList(){
        
        this.closeDialoge()
        this.createList(this.newListName)
      },

      deleteListHandler(list_id){
        console.log(list_id)
        console.log(this.content)

        if(list_id == this.list_id){ // should be allways the case, but you never know
          this.content.splice(this.selectedItem, 1)
          this.selectedItem = ""
          this.words = ""
          this.list_id = ""
          this.list_name = ""
          this.show_table = false
          this.deleteList(list_id)
        }
      },

      SelectionHandler(selection){
        console.log(selection)

        this.words = this.content[selection].array
        this.list_name = this.content[selection].list_name
        this.list_id = this.content[selection].list_id
        },

      // Create new list
      // data: Name of new list
      createList(data){
        var user = user_store.getters.user
        console.log(data)
        if(data != ""){
          axios.put('http://127.0.0.1:5000/create_wordlist', {
            headers: {'Content-Type': 'application/json'},
            data,
            user,
            })
            .then( response => {
              this.init(response.data)
            })
            .catch(function (error) {
              console.log(error)
            });
          }     
      },
      // deletes list
      // list_id: id of the list about to be deleted
      deleteList(list_id){
        var user = user_store.getters.user
          axios.delete('http://127.0.0.1:5000/wordlist', {                        
            data:{ list_id, user}
            })
            .then( response => {
              this.init(response.data)                            
            })
            .catch(function (error) {
              console.log(error)
            });
      },

      getList(){
        var user = user_store.getters.user
        axios.post('http://127.0.0.1:5000/wordlist', {
          headers: {'Content-Type': 'application/json'},
          user
          })
          .then( response => {
            this.init(response.data)                            
          })
          .catch(function (error) {
            console.log(error)
          });
      },
    }
  }


</script>
