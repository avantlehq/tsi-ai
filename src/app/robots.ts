import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
    },
    sitemap: 'https://tsi.directory/sitemap.xml',
    host: 'https://tsi.directory'
  }
}