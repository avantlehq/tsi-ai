import { NextRequest, NextResponse } from 'next/server';

// JWT verification function (mock implementation)
function verifyJWT(token: string): { valid: boolean; payload?: any } {
  try {
    // In production, use proper JWT verification with secret
    // For now, mock validation
    if (!token || token === 'invalid') {
      return { valid: false };
    }

    // Mock JWT payload
    const mockPayload = {
      tenantId: 'tenant_' + Math.random().toString(36).substr(2, 9),
      role: 'admin',
      exp: Math.floor(Date.now() / 1000) + (60 * 60), // 1 hour
      iat: Math.floor(Date.now() / 1000)
    };

    return { valid: true, payload: mockPayload };
  } catch {
    return { valid: false };
  }
}

// Rate limiting store (in production, use Redis or database)
const rateLimitStore = new Map();

function checkRateLimit(tenantId: string, maxRequests = 100, windowMs = 15 * 60 * 1000): boolean {
  const now = Date.now();
  const windowStart = now - windowMs;
  
  const requests = rateLimitStore.get(tenantId) || [];
  const recentRequests = requests.filter((timestamp: number) => timestamp > windowStart);
  
  if (recentRequests.length >= maxRequests) {
    return false; // Rate limit exceeded
  }
  
  recentRequests.push(now);
  rateLimitStore.set(tenantId, recentRequests);
  return true;
}

export default function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;
  
  // Handle API routes
  if (pathname.startsWith('/api/')) {
    return handleApiRequest(request);
  }
  
  // Continue with normal processing
  return NextResponse.next();
}

function handleApiRequest(request: NextRequest) {
  const pathname = request.nextUrl.pathname;
  
  // Public health check endpoint
  if (pathname === '/api/health') {
    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0'
    });
  }
  
  // Authentication required for all other API routes
  const authHeader = request.headers.get('authorization');
  const token = authHeader?.replace('Bearer ', '');
  
  if (!token) {
    return NextResponse.json(
      { error: 'Missing authorization header' },
      { status: 401 }
    );
  }
  
  const { valid, payload } = verifyJWT(token);
  if (!valid) {
    return NextResponse.json(
      { error: 'Invalid or expired token' },
      { status: 401 }
    );
  }
  
  // Rate limiting
  if (payload && !checkRateLimit(payload.tenantId)) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429 }
    );
  }
  
  // Add tenant info to headers for downstream processing
  if (payload) {
    const response = NextResponse.next();
    response.headers.set('x-tenant-id', payload.tenantId);
    response.headers.set('x-user-role', payload.role);
    return response;
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    // Always run for API routes
    '/api/(.*)',
  ],
};