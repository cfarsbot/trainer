<template>
    <v-app-bar prominent>
        <v-toolbar-title>Vokabeltrainer</v-toolbar-title>
                  
        
        <router-link to="/">
            <v-btn text> 
                Übersicht
            </v-btn>
        </router-link>

        <router-link to="/play">
            <v-btn text>
                Trainieren
            </v-btn>
        </router-link>

    </v-app-bar>
</template>

<script>
export default {
    name: "Navigation"

}
</script>
                          
                       
