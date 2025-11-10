import { Activity, Database, Zap, Shield, Globe } from 'lucide-react'

export default function AgentPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">TSI</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">TSI Agent Runtime</h1>
              <p className="text-gray-600">Transport Data Conversion Engine</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm font-medium text-gray-700">Online</span>
            </div>
            <div className="text-sm text-gray-500">
              Version 1.0.0 • Runtime: Node.js • Engine: TSI-AI
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Activity className="w-5 h-5 text-blue-600" />
              </div>
              <span className="text-sm text-gray-500">24h</span>
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-1">1,247</div>
            <div className="text-sm text-gray-600">Conversions</div>
            <div className="text-xs text-green-600 mt-1">↗ +12% vs yesterday</div>
          </div>

          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <Shield className="w-5 h-5 text-green-600" />
              </div>
              <span className="text-sm text-gray-500">Success Rate</span>
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-1">99.2%</div>
            <div className="text-sm text-gray-600">Validations</div>
            <div className="text-xs text-green-600 mt-1">↗ +0.3% this week</div>
          </div>

          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <Database className="w-5 h-5 text-purple-600" />
              </div>
              <span className="text-sm text-gray-500">Active Jobs</span>
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-1">23</div>
            <div className="text-sm text-gray-600">In Progress</div>
            <div className="text-xs text-blue-600 mt-1">Average: 2.3min</div>
          </div>

          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                <Globe className="w-5 h-5 text-orange-600" />
              </div>
              <span className="text-sm text-gray-500">Tenants</span>
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-1">156</div>
            <div className="text-sm text-gray-600">Active</div>
            <div className="text-xs text-green-600 mt-1">↗ +8 this month</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* API Status */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">API Endpoints</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">POST /api/v1/convert</div>
                  <div className="text-sm text-gray-600">Transport data conversion</div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Online</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">POST /api/v1/validate</div>
                  <div className="text-sm text-gray-600">Data validation engine</div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Online</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">GET /api/v1/status</div>
                  <div className="text-sm text-gray-600">Job status monitoring</div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Online</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">POST /api/provision</div>
                  <div className="text-sm text-gray-600">Tenant provisioning</div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Online</span>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mt-1">
                  <Zap className="w-4 h-4 text-green-600" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">EDIFACT conversion completed</div>
                  <div className="text-xs text-gray-600">Tenant: transport-agency-nl • 2 minutes ago</div>
                  <div className="text-xs text-gray-500">Job ID: tsi_1731234567_abc123</div>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mt-1">
                  <Shield className="w-4 h-4 text-blue-600" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">GTFS validation passed</div>
                  <div className="text-xs text-gray-600">Tenant: metro-transit-de • 5 minutes ago</div>
                  <div className="text-xs text-gray-500">Job ID: val_1731234456_def456</div>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mt-1">
                  <Database className="w-4 h-4 text-purple-600" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">New tenant provisioned</div>
                  <div className="text-xs text-gray-600">Organization: City Transport Prague • 12 minutes ago</div>
                  <div className="text-xs text-gray-500">Plan: Professional</div>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center mt-1">
                  <Globe className="w-4 h-4 text-orange-600" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">Real-time GTFS export</div>
                  <div className="text-xs text-gray-600">Tenant: regional-bus-sk • 18 minutes ago</div>
                  <div className="text-xs text-gray-500">Format: GTFS-Realtime protobuf</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* System Info */}
        <div className="mt-8 bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">System Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Engine Status</h3>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Conversion Engine:</span>
                  <span className="text-green-600 font-medium">Active</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Validation Engine:</span>
                  <span className="text-green-600 font-medium">Active</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Queue Processor:</span>
                  <span className="text-green-600 font-medium">Active</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Performance</h3>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Avg Response Time:</span>
                  <span className="text-gray-900">234ms</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Memory Usage:</span>
                  <span className="text-gray-900">67% (2.1GB)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">CPU Usage:</span>
                  <span className="text-gray-900">23%</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Supported Formats</h3>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">EDIFACT:</span>
                  <span className="text-gray-900">SKDUPD, TSDUPD</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">GTFS:</span>
                  <span className="text-gray-900">Static, Realtime</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Input:</span>
                  <span className="text-gray-900">JSON, XML, CSV</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}