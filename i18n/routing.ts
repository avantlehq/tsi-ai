import { defineRouting } from 'next-intl/routing'
import { createNavigation } from 'next-intl/navigation'

export const routing = defineRouting({
  locales: ['en', 'sk', 'de'],
  defaultLocale: 'en',
  pathnames: {
    '/': '/',
    '/about': {
      en: '/about',
      sk: '/o-projekte', 
      de: '/uber-uns'
    },
    '/contact': {
      en: '/contact',
      sk: '/kontakt',
      de: '/kontakt'
    }
  }
})

export const { Link, redirect, usePathname, useRouter } = createNavigation(routing)