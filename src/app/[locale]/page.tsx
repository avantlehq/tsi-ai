import { useTranslations } from 'next-intl'
import { ArrowRight, Zap, Shield, Globe } from 'lucide-react'
import { Link } from '../../../i18n/routing'

export default function HomePage() {
  const t = useTranslations()
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Navigation */}
      <nav className="px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">TSI</span>
            </div>
            <span className="font-bold text-xl">Directory</span>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-600 hover:text-gray-900">{t('navigation.home')}</Link>
            <Link href="/about" className="text-gray-600 hover:text-gray-900">{t('navigation.about')}</Link>
            <Link href="/contact" className="text-gray-600 hover:text-gray-900">{t('navigation.contact')}</Link>
            <a 
              href="https://tsi.avantle.ai/signup"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              {t('navigation.tryAgent')}
            </a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-6 py-20">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            {t('hero.title')}
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            {t('hero.description')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="https://tsi.avantle.ai/signup"
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
            >
              {t('hero.cta')}
              <ArrowRight className="w-5 h-5" />
            </a>
            <button className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
              {t('hero.secondaryCta')}
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              {t('features.title')}
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              {t('features.subtitle')}
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center p-6 rounded-xl bg-blue-50 border border-blue-100">
              <div className="w-12 h-12 bg-blue-600 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {t('features.edifact.title')}
              </h3>
              <p className="text-gray-600">
                {t('features.edifact.description')}
              </p>
            </div>
            
            <div className="text-center p-6 rounded-xl bg-green-50 border border-green-100">
              <div className="w-12 h-12 bg-green-600 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <Globe className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {t('features.gtfs.title')}
              </h3>
              <p className="text-gray-600">
                {t('features.gtfs.description')}
              </p>
            </div>
            
            <div className="text-center p-6 rounded-xl bg-purple-50 border border-purple-100">
              <div className="w-12 h-12 bg-purple-600 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {t('features.validation.title')}
              </h3>
              <p className="text-gray-600">
                {t('features.validation.description')}
              </p>
            </div>
            
            <div className="text-center p-6 rounded-xl bg-orange-50 border border-orange-100">
              <div className="w-12 h-12 bg-orange-600 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <ArrowRight className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {t('features.realtime.title')}
              </h3>
              <p className="text-gray-600">
                {t('features.realtime.description')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="px-6 py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              {t('useCases.title')}
            </h2>
            <p className="text-xl text-gray-600">
              {t('useCases.subtitle')}
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-xl shadow-sm border">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                {t('useCases.agencies.title')}
              </h3>
              <p className="text-gray-600">
                {t('useCases.agencies.description')}
              </p>
            </div>
            
            <div className="bg-white p-8 rounded-xl shadow-sm border">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                {t('useCases.consultants.title')}
              </h3>
              <p className="text-gray-600">
                {t('useCases.consultants.description')}
              </p>
            </div>
            
            <div className="bg-white p-8 rounded-xl shadow-sm border">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                {t('useCases.developers.title')}
              </h3>
              <p className="text-gray-600">
                {t('useCases.developers.description')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20 bg-blue-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            {t('cta.title')}
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            {t('cta.description')}
          </p>
          <a
            href="https://tsi.avantle.ai/signup"
            className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors inline-flex items-center gap-2"
          >
            {t('cta.button')}
            <ArrowRight className="w-5 h-5" />
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white px-6 py-12">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center space-x-2 mb-2">
                <div className="w-6 h-6 bg-blue-600 rounded flex items-center justify-center">
                  <span className="text-white font-bold text-xs">TSI</span>
                </div>
                <span className="font-bold">Directory</span>
              </div>
              <p className="text-gray-400">
                {t('footer.description')}
              </p>
            </div>
            <div className="text-gray-400">
              {t('footer.copyright')}
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
