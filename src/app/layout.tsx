import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'TSI Agent Runtime - Transform Transport Data with AI',
  description: 'Professional-grade conversion platform for public transport data. Generate SKDUPD, TSDUPD, and GTFS formats with one click.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}