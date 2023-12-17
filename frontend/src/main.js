import { createApp, markRaw } from 'vue'
// import { createApp, markRaw } from 'vue/dist/vue.esm-bundler'
import App from './App.vue'

import { createPinia } from 'pinia'
import { createVueSession } from './plugins/vue-storages/session-storage'
import { createVueLocalStorage } from './plugins/vue-storages/local-storage'
import { createAxios } from './plugins/axios'
import { createCompanyDetails } from './plugins/project'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createVuetify } from 'vuetify'

import router from './router'
import i18n from './i18n'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'


import 'vuetify/styles'
import '@/plugins/webfontloader'
import '@/plugins/fontawesome'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'mdb-ui-kit/css/mdb.min.css'
import '@mdi/font/css/materialdesignicons.css'
import '@/assets/style.css'

const pinia = createPinia()
const session = createVueSession()
const localstorage = createVueLocalStorage()

pinia.use(({ store }) => {
    store.$localStorage = markRaw(localstorage)
    store.$session = markRaw(session)
})

const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi
        }
    }
})

// pinia.use(({ store }) => {
//     store.router = toRaw(router)
//     store.localstorage = toRaw(localstorage)
//     store.session = toRaw(session)
// })

const app = createApp(App)

app.use(createCompanyDetails({
    legalName: 'Example',
    urls: [
        {
            name: 'default',
            url: 'http://example.com'
        }
    ],
    socials: [
        {
            name: 'YouTube',
            icon: 'fa-youtube',
            url: 'https://www.youtube.com/channel/UC5CF7mLQZhvx8O5GODZAhdA'
        },
        {
            name: 'Facebook',
            icon: 'fa-facebook',
            url: 'https://www.facebook.com/mdbootstrap'
        },
        {
            name: 'Twitter',
            icon: 'fa-twitter',
            url: 'https://twitter.com/MDBootstrap'
        }
    ]
}))
app.use(router)
app.use(createAxios())
app.use(session)
app.use(localstorage)
app.use(i18n)
app.use(pinia)
app.use(vuetify)

app.component('FontAwesomeIcon', FontAwesomeIcon)

app.mount('#app')
