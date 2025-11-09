import createNextIntlPlugin from 'next-intl/plugin'
import type { NextConfig } from "next";

const withNextIntl = createNextIntlPlugin()

const nextConfig: NextConfig = {
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb'
    }
  }
};

export default withNextIntl(nextConfig);
