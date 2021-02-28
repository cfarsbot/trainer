<template>
    <v-data-table
      :headers="headers"
      :items="words"
      sort-by="calories"
      class="elevation-2"
      >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-toolbar-title>{{list_name }}</v-toolbar-title>
          
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="500px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
              color="red"
              dark
              class="mb-2 ml-4"
              @click="deleteList"
              >
              Liste löschen
              </v-btn>

              <v-btn
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                Hinzufügen
              </v-btn>
            </template>
            
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.de"
                        label="Deutsches Wort"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.en"
                        label="Englisches Wort"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                                <v-btn
                  color="blue darken-1"
                  text
                  @click="save"
                >
                  Speichern
                </v-btn>                
                <v-btn
                  color="blue darken-1"
                  text
                  @click="close"
                >
                  Abbrechen
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="headline">Willst du wirklich {{ editedItem.en}} / {{ editedItem.de }} löschen?</v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="deleteItemConfirm">Ja</v-btn>
                <v-btn color="blue darken-1" text @click="closeDelete">Abbrechen</v-btn>

                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDeleteList" max-width="500px">
            <v-card>
              <v-card-title class="headline">Willst du wirklich {{ list_name }} löschen? </v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="deleteListConfirm">Ja</v-btn>
                <v-btn color="blue darken-1" text @click="closeDelete">Abbrechen</v-btn>                
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          class="mr-2"
          @click="editItem(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          small
          @click="deleteItem(item)"
        >
          mdi-delete
        </v-icon>
      </template>

    </v-data-table>
</template>
<script>
import axios from 'axios'
import config from '../../config'
import user_store from '../store/user'
    export default {
      props: ['words', 'list_name', 'list_id'],
      data: () => ({
      condition: false,
      dialog: false,
      dialogDelete: false,
      dialogDeleteList: false,
      headers: [
        {
          text: 'Deutsch',
          align: 'start',
          sortable: true,
          value: 'de',
        },
        { text: 'Englisch', value: 'en' },
        { text: 'Actions', value: 'actions', sortable: true },
      ],
      editedIndex: -1,
      editedItem: {
        de: '',
        en: '',
        id: '',
      },
      defaultItem: {
        de: '',
        en: '',
      },
    }),

    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'Wörter Hinzufügen' : 'Bearbeiten'
      },
    },

    watch: {
      dialog (val) {
        val || this.close()
      },
      dialogDelete (val) {
        val || this.closeDelete()
      },
    },

    methods: {

      

      updateWord(word){
        var user = user_store.getters.user
          axios.patch(`https://${config.hostname}/update_wordlist`, {
                        headers: {'Content-Type': 'application/json'},
                        word,
                        user

                    })
                        .then( response => {
                            console.log(response.data);  
                        })
                        .catch(function (error) {
                          console.log(error)
                        });
      },

      // takes the word, list_id of the word and reads user from store
      // creates event to update the component
      addWord(word, list_id){
        var user = user_store.getters.user
        axios.put(`https://${config.hostname}/update_wordlist`, {
          
                        headers: {'Content-Type': 'application/json'},
                        word,
                        user,
                        list_id
                        

                    })
                        .then( response => {
                            console.log(response.data)  
                            // need to update the cached list, because a new ui for the created word needs to be generated
                            this.$emit("update", response.data)
                        })
                        .catch(function (error) {
                          console.log(error)
                        });
      },

      deleteWord(word){
        // read user from store
        var user = user_store.getters.user
                // axios wants the data to be deleted inside the data Object... https://stackoverflow.com/a/53263784
                console.log(word)
                axios.delete(`https://${config.hostname}/update_wordlist`, {                        
                        data:{
                          user,
                          word
                        }


                    })
                        .then( response => {
                            console.log(response.data);  
                        })
                        .catch(function (error) {
                          console.log(error)
                        });
      },
      
    
   
      // edit word pair in Object words
      // item = selected element
      editItem (item) {
        this.editedIndex = this.words.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
      
      // delete word pair in Object words
      // item = selected element
      deleteItem (item) {
        this.editedIndex = this.words.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },
      // show "do you wanna realy delete" panel
      deleteList(){
        this.dialogDeleteList = true
  
      },

      // create event to delete words[]
      // component gets refreshed by parrent 
      deleteListConfirm(){
        // this.words = ""
        this.$emit("delete-list", this.list_id)
        this.dialogDeleteList = false
      },

      // remove element from words[]
      deleteItemConfirm () {
        this.words.splice(this.editedIndex, 1)
        console.log("Delete")
        this.deleteWord(this.editedItem)
        this.closeDelete()
      },

      // closes edit words panel
      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      // close delete words panel
      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1

        })
      },

      save () {
        if (this.editedIndex > -1) {
          // called when words get edited
          // existing words are in the editedIndex range from 0 to n+1
          Object.assign(this.words[this.editedIndex], this.editedItem)
          this.updateWord(this.editedItem)
          console.log("wort bearbeitet")
          console.log(this.editedItem)
        } else {
          // editedIndex seems to be empty
         // called when words get added
          this.words.push(this.editedItem)
          this.addWord(this.editedItem, this.list_id)
        }
        // close dialoge
        this.close()
      },
    },
  }
</script>