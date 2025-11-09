import { MetadataRoute } from 'next'
import { routing } from '../../i18n/routing'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://tsi.directory'
  
  const routes = [
    '',
    '/about',
    '/contact'
  ]
  
  const sitemapEntries: MetadataRoute.Sitemap = []
  
  // Add routes for each locale
  routing.locales.forEach(locale => {
    routes.forEach(route => {
      sitemapEntries.push({
        url: `${baseUrl}/${locale}${route}`,
        lastModified: new Date(),
        changeFrequency: 'weekly',
        priority: route === '' ? 1.0 : 0.8,
        alternates: {
          languages: routing.locales.reduce((acc, lang) => {
            acc[lang] = `${baseUrl}/${lang}${route}`
            return acc
          }, {} as Record<string, string>)
        }
      })
    })
  })
  
  // Add default redirects
  sitemapEntries.push({
    url: baseUrl,
    lastModified: new Date(),
    changeFrequency: 'weekly',
    priority: 1.0
  })
  
  return sitemapEntries
}