<template>
    <v-app>
        <v-layout class="rounded rounded-md">
            <v-app-bar app title="Excel AI Helper"></v-app-bar>
            <v-main>
                <v-row no-gutters style="height: 100vh;">
                    <v-col cols="4">
                        <SideBar />
                    </v-col>
                    <v-col cols="8">
                        <ChatBox />
                    </v-col>
                </v-row>
            </v-main>
        </v-layout>
    </v-app>
</template>

<script setup lang="ts">

</script>

