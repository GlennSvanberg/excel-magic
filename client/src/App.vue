<template>
    <v-app>
        <v-layout class="rounded rounded-md">
            <v-app-bar app title="Excel AI Helper"></v-app-bar>
            <v-main>
                <v-row no-gutters>
                    <v-col cols="8" style="padding: 1vw 5vw;">
                        <SideBar />
                    </v-col>

                    <v-col cols="4">
                        <v-row style="padding: 50px">
                            <OutputLinks style="margin: auto;" v-for="file in outputLinks" :key="file" :file="file" />
                        </v-row>
                        <ChatBox />
                    </v-col>
                </v-row>
            </v-main>
        </v-layout>
    </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { mapState } from 'vuex';

export default defineComponent({
    computed: {
        ...mapState({
            outputLinks: (state: any) => state.outputLinks, // Assuming 'count' is a state property in the Vuex store
        }),
    },
});

</script>

