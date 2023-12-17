// import i18n from '@/i18n'

import { loadView, scrollToTop } from '@/composables/utils'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: loadView('HomeView'),
    name: 'home_view'
  },
  {
    path: '/search',
    component: loadView('SearchView'),
    name: 'search_view'
  }
  // {
  //   path: '/',
  //   redirect: {
  //     name: 'videos_view',
  //     params: {
  //       lang: i18n.global.locale
  //     }
  //   }
  // },
  // {
  //   path: '/:lang',
  //   component: {
  //     template: '<router-view></router-view>'
  //   },
  //   children: [
  //     {
  //       path: 'browse',
  //       name: 'videos_view',
  //       component: loadView('VideosView')
  //     },
  //     {
  //       path: 'watch/:id(\\d+)',
  //       name: 'video_view',
  //       component: loadView('VideoView')
  //     }
  //   ]
  // }
]

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: scrollToTop,
  routes
})

// router.beforeEach((to, from, next) => {
//   const localeLanguage = to.params.lang
//   const supportedLanguages = ['en', 'es', 'fr']

//   if (!supportedLanguages.includes(localeLanguage)) {
//     next('en')
//   }
  
//   if (i18n.global.locale !== localeLanguage) {
//     i18n.global.locale = localeLanguage
//   }

//   next()
// })

export default router
