/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import store from './store'
import App from './App.vue'


// Composables
import { createApp } from 'vue'

const app = createApp(App)

registerPlugins(app)

app.use(store)
app.mount('#app')
