<template>
  <v-card tile>
    <v-list dense>
      <v-subheader>Deine Wörterlisten</v-subheader>
      <v-list-item-group
        v-model="selectedItem"
        color="primary"
      >
        <v-list-item
          v-for="(entry, i) in entrys"
          :key="i"
        >
          <v-list-item-content>
            <v-list-item-title v-text="entry"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-card>
  
</template>
<script>
export default {
  props: ['entrys'],
  watch:{
    selectedItem:{
      handler(){
        this.$emit("selected-item", this.selectedItem)
      }
    }
  },
  data(){
    return{
      selectedItem: null,
      items: [],
    }   
  }
}
  
</script>